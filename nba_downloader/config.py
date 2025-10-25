import os
from datetime import datetime

class Config:
    # URLs
    BASKETBALL_VIDEO_URL = "http://basketball-video.com"
    OKRU_URL= "https://ok.ru"

    # Team configuration
    TEAM_NAME = "Oklahoma City Thunder"
    TEAM_SLUG = "oklahoma-city-thunder"
    TEAM_KEYWORDS = [
        "thunder",
        "oklahoma city thunder",
        "oklahoma-city-thunder",
        "okc",
        "oklahoma"
    ]

    # Scheduling
    CHECK_INTERVAL_MINUTES = 15

    # Download paths
    DOWNLOAD_DIR = "/app/downloads"
    LOG_DIR = "/app/logs"

    # Browser settings
    WEBDRIVER_TIMEOUT = 30
    HEADLESS_BROWSER = True
