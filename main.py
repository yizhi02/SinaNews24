import threading
import time
import os
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import openai

# 设置你的Telegram机器人的token和chat_id
telegram_bot_token = 'Input_your_bot_token_here'
telegram_chat_id = 'Input_your_chat_id_here(optional)'
# 初始化 OpenAI 客户端
openai.api_key = "input_your_api_key_here"

# 设置每日总结新闻的时间
summary_hour = 23
summary_minute = 30

def send_telegram_message(text):
    """发送消息到Telegram"""
    try:
        send_text = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&parse_mode=Markdown&text={text}'
        response = requests.get(send_text)
        return response.json()
    except Exception as e:
        print(f"\033[91m发送Telegram消息时出错: {e}\033[0m")  # 红色输出错误信息
        return None

def fetch_news(existing_news):
    print("\033[94m启动浏览器，开始爬取新闻...\033[0m")
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://finance.sina.com.cn/7x24/")
    print("\033[94m页面加载中...\033[0m")

    max_scroll_attempts = 3
    attempts = 0
    new_news = {}
    last_index = -1

    while attempts < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        attempts += 1

        focus_news_elements = driver.find_elements(By.CLASS_NAME, 'bd_i_focus')
        print("\033[94m检查新闻中...\033[0m")

        for index, element in enumerate(focus_news_elements):
            if index <= last_index:
                continue

            news_date = datetime.now().strftime("%Y-%m-%d")
            news_text = element.text.strip()
            news_entry = f"{news_date},{news_text}"

            if news_text not in existing_news:
                if news_date not in new_news:
                    new_news[news_date] = set()
                new_news[news_date].add(news_text)
                print(f"\033[95m发现新新闻: {news_text}\033[0m")
                send_telegram_message(news_text)

            last_index = len(focus_news_elements) - 1

    driver.quit()
    print("\033[92m爬取完成。\033[0m")
    return new_news

file_path = 'sina_news.csv'
if not os.path.exists(file_path):
    print("\033[93m新闻文件不存在，创建新文件...\033[0m")
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Date", "News"])  # 写入表头

existing_news = set()
with open(file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)  # 跳过表头
    for row in csv_reader:
        existing_news.add(f"{row[1]}")

def summarize_and_send_news():
    """读取当天的新闻，使用ChatGPT 4 API生成总结，并通过Telegram发送"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        todays_news = []
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # 跳过表头
            for row in csv_reader:
                if row[0] == today:
                    todays_news.append(row[1])

        if todays_news:
            news_text = ' '.join(todays_news)
            summary = generate_summary_with_gpt4(news_text)
            send_telegram_message(summary)
        else:
            send_telegram_message("今日无新闻要闻。")
    except Exception as e:
        print(f"\033[91m生成新闻总结时出错: {e}\033[0m")



def generate_summary_with_gpt4(text):
    """使用ChatGPT 4 API生成新闻总结"""
    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # 或其他适合您账户的模型
            messages=[
                {"role": "system", "content": "put_prompt_here"},
                {"role": "user", "content": f"接下来，请你总结以下新闻:\n{text}"}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"\033[91m请求ChatGPT 4 API时发生异常: {e}\033[0m")
        return "生成新闻总结时出现问题。"

def run_scheduled_tasks():
    """运行定时任务的线程函数"""
    while True:
        now = datetime.now()
        if now.hour == summary_hour and now.minute == summary_minute:
            summarize_and_send_news()
            # 休眠足够长的时间以确保任务不会在同一分钟内重复执行
            time.sleep(120)
        else:
            # 每分钟检查一次时间
            time.sleep(30)

# 创建并启动后台线程来处理定时任务
threading.Thread(target=run_scheduled_tasks, daemon=True).start()

while True:
    print(f"\033[94m[{datetime.now()}] 开始新的爬取周期...\033[0m")
    new_news = fetch_news(existing_news)
    if new_news:
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            for date, news_set in sorted(new_news.items()):
                for news in sorted(news_set):
                    news_entry = f"{date},{news}"
                    csv_writer.writerow([date, news])
                    existing_news.add(news)
            print(f"\033[92m[{datetime.now()}] 新闻文件已更新。\033[0m")
    else:
        print(f"\033[93m[{datetime.now()}] 没有发现新的新闻。\033[0m")
    time.sleep(10)   # 或根据需要调整这个等待时间
