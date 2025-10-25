import logging
import os
import time
import threading
from datetime import datetime
from .downloader import NBADownloader
from .config import Config

def setup_logging():
    """Setup application-wide logging"""
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(Config.LOG_DIR, f"nba_downloader_{date_str}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
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
        logger.info(f"Most recent {Config.TEAM_NAME} game is not downloaded or download failed")

    logger.info("=== NBA game check completed ===\n")

def schedule_next_job():
    """Schedule the next job to run after CHECK_INTERVAL_MINUTES"""
    timer = threading.Timer(Config.CHECK_INTERVAL_MINUTES * 60, run_job_sequence)
    timer.daemon = True
    timer.start()

def run_job_sequence():
    """Run job and schedule the next one"""
    job()
    schedule_next_job()

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("NBA Downloader started")
    logger.info(f"Checking for the most recent {Config.TEAM_NAME} game every {Config.CHECK_INTERVAL_MINUTES} minutes")

    # Run immediately on startup
    run_job_sequence()

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("NBA Downloader stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("NBA Downloader shutdown complete")

if __name__ == "__main__":
    main()
