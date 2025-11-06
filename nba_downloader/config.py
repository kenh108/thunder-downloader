import os
from datetime import datetime

class Config:
    # URLs
    BASKETBALL_VIDEO_URL = "https://basketball-video.com"
    OKRU_URL= "https://ok.ru"

    # Team configuration with env variable fallbacks
    TEAM_NAME = os.getenv('NBA_TEAM_NAME', "Oklahoma City Thunder")
    TEAM_SLUG = os.getenv('NBA_TEAM_SLUG', "oklahoma-city-thunder")
    TEAM_KEYWORDS = os.getenv('NBA_TEAM_KEYWORDS', "thunder,oklahoma city thunder,oklahoma-city-thunder,okc,oklahoma").split(",")

    # Scheduling
    CHECK_INTERVAL_MINUTES = int(os.getenv('NBA_CHECK_INTERVAL', 15))

    # Download paths
    DOWNLOAD_DIR = "/app/downloads"
    LOG_DIR = "/app/logs"

    # Browser settings
    WEBDRIVER_TIMEOUT = 30
    HEADLESS_BROWSER = True

    # Telegram Bot configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
