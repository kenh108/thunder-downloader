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

    def find_thunder_games(self):
        """Find and click the page for Thunder games"""
        try:
            self.logger.info(f"Navigating to {Config.BASE_URL}")
            self.driver.get(Config.BASE_URL)

            WebDriverWait(self.driver, Config.WEBDRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            # Find link for Thunder page
            games_link = self.driver.find_elements(By.TAG_NAME, "a")

            for link in games_link:
                href = link.get_attribute('href') or ""
                text = link.text.lower()

                # Check if this is related to Thunder
                if any(keyword in href.lower() or keyword in text
                    for keyword in Config.TEAM_KEYWORDS):
                    # Correct link is always first on page
                    self.logger.info(f"Found Thunder page, navigating to: {href}")
                    self.driver.get(href)
                    return True

            self.logger.error("Thunder page not found")
            return False

        except Exception as e:
            self.logger.error(f"Error finding Thunder page: {e}")
            return False

    def find_most_recent_game(self):
        """Find and click the most recent game"""
        try:
            WebDriverWait(self.driver, Config.WEBDRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            # Find all game links
            game_links = self.driver.find_elements(By.TAG_NAME, "a")

            for link in game_links:
                href = link.get_attribute('href') or ""
                text = link.text.strip()

                # Ensure this is valid game and Thunder game
                if (self.is_actual_game(href, text) and
                    self.is_thunder_game(href, text)):
                    self.logger.info(f"Found most recent game: {text}, navigating to: {href}")
                    self.driver.get(href)
                    return True

            self.logger.error("No game links found")
            return False

        except Exception as e:
            self.logger.error(f"Error finding game links: {e}")
            return False

    def is_actual_game(self, href, text):
        """Check if this is an actual game link (not navigation page)"""
        if not href or not text:
            return False

        href_lower = href.lower()
        text_lower = text.lower()

        # Should be a game paeg with the format: team1-vs-team2-full-game-replay-date-nba
        is_game_page = (
            "-vs-" in href_lower and
            "full-game-replay" in href_lower and
            "nba" in href_lower
        )

        return is_game_page

    def is_thunder_game(self, href, text):
        """Check if link is for a Thunder game"""
        if not href or not text:
            return False

        href_lower = href.lower()
        text_lower = text.lower()

        # Check for Thunder keywords in the game link
        return any(keyword in href_lower or keyword in text_lower
                    for keyword in Config.TEAM_KEYWORDS)

    def find_okru_hosted_recording(self):
        """Find and click the Watch button for the ok.ru hosted game recording"""
        try:
            WebDriverWait(self.driver, Config.WEBDRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            # Find the paragraph that contains "(OK)" (meaning hosted by ok.ru)
            ok_servers = self.driver.find_elements(By.XPATH, "//p[contains(., '(OK)')]")

            for server in ok_servers:
                # Watch button is in the next <p> sibling element
                next_p = server.find_element(By.XPATH, "./following-sibling::p[1]")

                # Find the Watch link within this next paragraph
                watch_links = next_p.find_elements(By.XPATH, ".//a[contains(., 'Watch')]")

                if watch_links:
                    watch_link = watch_links[0]
                    href = watch_link.get_attribute('href')
                    self.logger.info(f"Found OK.ru Watch button, navigating to: {href}")
                    self.driver.get(href)
                    return True

            self.logger.error("No ok.ru Watch button found")
            return False

        except Exception as e:
            self.logger.error(f"Error finding ok.ru Watch button: {e}")
            return False

    def extract_okru_link(self):
        """Extract ok.ru video URL from iframe"""
        try:
            WebDriverWait(self.driver, Config.WEBDRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            # Find all iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

            for iframe in iframes:
                src = iframe.get_attribute('src') or ""

                # Check if this is an ok.ru video embed
                if 'ok.ru/videoembed' in src:
                    # Convert embed URL to direct video URL
                    video_id = src.split('/')[-1]
                    video_url = f"https://ok.ru/video/{video_id}"
                    self.logger.info(f"Found ok.ru video: {video_url}")
                    return video_url

            self.logger.error("No ok.ru video link found")
            return False

        except Exception as e:
            self.logger.error(f"Error finding ok.ru video link: {e}")
            return False

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

            if not self.find_thunder_games():
                return False
            
            if not self.find_most_recent_game():
                return False

            if not self.find_okru_hosted_recording():
                return False

            video_url = self.extract_okru_link()
            if not video_url:
                return False

            return False

        except Exception as e:
            self.logger.error(f"Unexpected error in run method: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
