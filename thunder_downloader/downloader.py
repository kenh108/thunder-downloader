import logging
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import urljoin
import re

from .config import Config

class ThunderDownloader:
    def __init__(self):
        self.driver = None
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.get_log_file()),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_browser(self):
        """Setup Chrome browser with options"""
        chrome_options = Options()
        if Config.HEADLESS_BROWSER:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(Config.WEBDRIVER_TIMEOUT)
        self.logger.info("Browser setup complete")

    #def find_thunder_game(self):
    #    """Find and click the latest Thunder game"""
    #    try:
    #        self.logger.info(f"Navigating to {Config.BASE_URL}")
    #        self.driver.get(Config.BASE_URL)

    #        # Find all game links
    #        game_links = self.driver.find_elements(By.TAG_NAME, "a")

    #        for link in game_links:
    #            href = link.get_attribute('href') or ""
    #            text = link.text.lower()

    #            # Check if this is a Thunder game
    #            if any(keyword in href.lower() or keyword in text
    #                for keyword in Config.TEAM_KEYWORDS):
    #                self.logger.info(f"Found Thunder game: {text} - {href}")
    #                link.click()
    #                return True

    #        self.logger.error("No Thunder games found on the page")
    #        return False

    #    except Exception as e:
    #        self.logger.error(f"Error finding Thunder game: {e}")
    #        return False

    def find_thunder_page(self):
        """Find and click the page for Thunder games"""
        try:
            self.logger.info(f"Navigating to {Config.BASE_URL}")
            self.driver.get(Config.BASE_URL)

            # Find link for Thunder page
            games_link = self.driver.find_elements(By.TAG_NAME, "a")

            for link in games_link:
                href = link.get_attribute('href') or ""
                text = link.text.lower()

                # Check if this is related to Thunder
                if any(keyword in href.lower() or keyword in text
                    for keyword in Config.TEAM_KEYWORDS):
                    # Correct link is always first on page
                    self.logger.info(f"Found Thunder page: {text} - {href}")
                    link.click()
                    return True

            self.logger.error("Thunder page not found")
            return False

        except Exception as e:
            self.logger.error(f"Error finding Thunder page: {e}")
            return False

    def get_stream_links(self):
        """Get all stream links from the game page"""
        try:
            # Wait for page to load and find stream links
            stream_links = WebDriverWait(self.driver, Config.WEBDRIVER_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )

            # Filter for stream links (adjust selector as needed)
            stream_urls = []
            for link in stream_links:
                href = link.get_attribute('href')
                if href and ('stream' in href.lower() or 'video' in href.lower()):
                    stream_urls.append(href)

            self.logger.info(f"Found {len(stream_urls)} stream links")
            return stream_urls

        except TimeoutException:
            self.logger.error("Timeout waiting for stream links")
            return []

    def extract_okru_video_url(self, stream_url):
        """Navigate to stream and extract ok.ru video URL"""
        try:
            self.logger.info(f"Navigating to stream: {stream_url}")
            self.driver.get(stream_url)

            # Wait for video element or iframe
            time.sleep(5) # Allow page to load

            # Look for ok.ru video URLs in the page source or iframes
            page_source = self.driver.page_source
            okru_pattern = r'https?://(?:www\.)?ok\.ru/video/\d+'
            matches = re.findall(okru_pattern, page_source)

            if matches:
                video_url = matches[0]
                self.logger.info(f"Found ok.ru video URL: {video_url}")
                return video_url

            self.logger.error("No ok.ru video URL found in stream page")
            return None

        except Exception as e:
            self.logger.error(f"Error extreacting ok.ru URL: {e}")
            return None

    def download_video(self, video_url):
        """Download video using yt-dlp"""
        try:
            output_template = Config.get_output_template()
            cmd = [
                'yt-dlp',
                video_url,
                '-o', output_template,
                '--no_overwrites'
            ]

            self.logger.info(f"Starting download: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            self.logger.info("Download completed successfully")
            self.logger.debug(f"yt-dlp output: {result.stdout}")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Download failed: {e}")
            self.logger.error(f"yt-dlp stderr: {e.stderr}")
            return False

    def run(self):
        """Main execution method"""
        self.logger.info("Starting Thunder game download process")

        try:
            self.setup_browser()

            if not self.find_thunder_page():
                return False

            stream_urls = self.get_stream_links()
            if not stream_urls:
                return False

            # Try first stream link
            video_url = self.extract_okru_video_url(stream_urls[0])
            if not video_url:
                return False

            return self.download_video(video_url)

        except Exception as e:
            self.logger.error(f"Unexpected error in run method: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
