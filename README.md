# Sina Finance News 24 Scraper

## Overview
This Python-based scraper is designed to automatically gather key financial news items highlighted in red font (important news) from Sina Finance's 24-hour news feed. It integrates Telegram for real-time updates and leverages OpenAI's GPT-4 API to generate daily news summaries.

## Key Features
- **Targeted Scraping**: Extracts key financial news from Sina Finance's 24-hour news section.
- **Real-time Telegram Updates**: Sends news items to a specified Telegram chat as they are scraped.
- **Daily News Summary**: Utilizes OpenAI's GPT-4 API to create and send a concise summary of the day's most critical news via Telegram.
- **CSV Data Storage**: Logs all scraped news items in a CSV file for archival and further analysis.

## Prerequisites
- Python 3.x
- Selenium WebDriver
- Requests library
- CSV library
- OpenAI API key
- Telegram Bot token and Chat ID

## Installation

### Step 1: Clone the Repository
```
git clone [Your Repository URL]
cd [Your Repository Name]
```

### Step 2: Install Required Python Packages
```
pip install selenium requests webdriver_manager openai
```

## Configuration
Before running the scraper, you need to set up the following configurations:
- **Telegram Bot Token and Chat ID**: Replace the placeholders in the script with your actual Telegram bot token and chat ID.
- **OpenAI API Key**: Insert your OpenAI API key in the script.

## Usage
Execute the scraper script with the following command:
```
python main.py
```

The script will continuously scrape the Sina Finance news feed and send real-time updates as well as a daily summary to the specified Telegram chat.

## Contributing
Contributions, bug reports, and feature requests are welcome. Please fork the repository, make your changes, and submit a pull request.


---

**Disclaimer**: This scraper is for educational and research purposes only. Ensure compliance with Sina Finance's terms of use and respect any copyright or data usage regulations.

