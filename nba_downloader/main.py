import logging
import time
import schedule
from datetime import datetime
from .downloader import NBADownloader
from .config import Config

def setup_logging():
    """Setup application-wide logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.get_log_file()),
            logging.StreamHandler()
        ]
    )

def job():
    """Scheduled job to download new NBA games"""
    logger = logging.getLogger(__name__)
    logger.info(f"=== Starting NBA game check ===")

    downloader = NBADownloader()
    success = downloader.run()

    if success:
        logger.info(f"Most recent {Config.TEAM_NAME} game is downloaded")
    else:
        logger.info("Most recent {Config.TEAM_NAME} game is not downloaded or download failed")

    logger.info("=== NBA game check completed ===\n")

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("NBA Downloader started")
    logger.info(f"Checking for the most recent {Config.TEAM_NAME} game every {Config.CHECK_INTERVAL_MINUTES} minutes")

    # Schedule the job
    schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(job)

    # Run immediately on startup
    job()

    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("NBA Downloader stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("NBA Downloader shutdown complete")

if __name__ == "__main__":
    main()
