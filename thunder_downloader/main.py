import logging
import time
import schedule
from datetime import datetime
from .downloader import ThunderDownloader
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
    """Scheduled job to check for and download Thunder games"""
    logger = logging.getLogger(__name__)
    logger.info("=== Starting Thunder game check ===")

    downloader = ThunderDownloader()
    success = downloader.run()

    if success:
        logger.info("Thunder game download completed successfully")
    else:
        logger.info("No game downloaded or download failed")

    logger.info("=== Thunder game check completed ===\n")

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Thunder Downloader started")
    logger.info(f"Checking for new games every {Config.CHECK_INTERVAL_MINUTES} minutes")

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
        logger.info("Thunder Downloader stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Thunder Downloader shutdown complete")

if __name__ == "__main__":
    main()
