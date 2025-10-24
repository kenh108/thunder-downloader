import os
from datetime import datetime

class Config:
    # URLs
    BASE_URL = "http://basketball-video.com"
    VIDEO_HOST_URL = "https://ok.ru"

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

    # Download paths
    DOWNLOAD_DIR = "/app/downloads"
    LOG_DIR = "/app/logs"

    # Scheduling
    CHECK_INTERVAL_MINUTES = 15

    # Browser settings
    WEBDRIVER_TIMEOUT = 30
    HEADLESS_BROWSER = True


    @staticmethod
    def get_log_file():
        """Generate log file path with timestamp"""
        date_str = datetime.now().strftime("%Y%m%d")
        return os.path.join(Config.LOG_DIR, f"thunder_downloader_{date_str}.log")
