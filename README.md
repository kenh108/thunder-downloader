# NBA Downloader

A Python application that automatically downloads the most recent NBA game replays for a specified team. The application runs in a Docker container and can send notifications via Telegram when new games are downloaded.

## Features

- Automatically detects and downloads the most recent NBA game replays for your favorite team
- Runs on a configurable schedule (default: every 15 minutes)
- Downloads high-quality video from ok.ru hosting service
- Telegram notifications for successful downloads
- Comprehensive logging
- Docker containerization for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone or download the application files to a directory on your system.

2. Create the necessary directories:
```bash
mkdir -p downloads logs
```

3. Update the `docker-compose.yml` file with your preferred team configuration (see Configuration section below).

4. Run the application:
```bash
docker-compose up -d
```

The application will start and begin checking for new games according to the configured schedule.

## Configuration

Configure the application by modifying the environment variables in the `docker-compose.yml` file:

### Team Configuration
- `NBA_TEAM_NAME`: Full name of the NBA team (e.g., "Oklahoma City Thunder")
- `NBA_TEAM_SLUG`: URL-friendly team name (e.g., "oklahoma-city-thunder")
- `NBA_TEAM_KEYWORDS`: Comma-separated keywords for team identification

### Scheduling
- `NBA_CHECK_INTERVAL`: How often to check for new games (in minutes, default: 15)

### Telegram Notifications (Optional)
- `TELEGRAM_ENABLED`: Set to "true" to enable Telegram notifications
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (create via BotFather)
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

## File Structure

```
nba-downloader/
├── nba_downloader/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── config.py            # Configuration settings
│   ├── downloader.py        # Core downloading logic
│   └── telegram_notifier.py # Telegram notification handler
├── scripts/
│   └── entrypoint.sh        # Container entrypoint script
├── downloads/               # Downloaded game videos
├── logs/                   # Application logs
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .dockerignore
```

## How It Works

1. The application starts and sets up a scheduled job based on the configured interval
2. On each run, it navigates to basketball-video.com and finds your team's page
3. It identifies the most recent game that matches your team
4. The application finds the ok.ru hosted version of the game
5. It extracts the video URL and downloads the game using yt-dlp
6. If Telegram is enabled, it sends a notification when a new game is downloaded
7. The process repeats according to the schedule

## Logs

Application logs are stored in the `logs/` directory with daily rotation. Log files are named in the format `nba_downloader_YYYYMMDD.log`.

## Monitoring

To check the application status:

```bash
# View logs
docker-compose logs nba-downloader

# Follow logs in real-time
docker-compose logs -f nba-downloader
```

## Stopping the Application

```bash
docker-compose down
```

## Customization

### Changing Teams

To monitor a different NBA team, update the team configuration in `docker-compose.yml`:

```yaml
environment:
  - NBA_TEAM_NAME=Los Angeles Lakers
  - NBA_TEAM_SLUG=los-angeles-lakers
  - NBA_TEAM_KEYWORDS=lakers,los angeles lakers,los-angeles-lakers
```

### Adjusting Check Frequency

Change the check interval by modifying the `NBA_CHECK_INTERVAL` environment variable (in minutes):

```yaml
environment:
  - NBA_CHECK_INTERVAL=30  # Check every 30 minutes
```

## Troubleshooting

- Check the logs in the `logs/` directory for detailed error information
- Ensure the Docker container has sufficient disk space for video downloads
- Verify network connectivity from within the container
- Check that the team configuration matches the naming conventions used on basketball-video.com

## Notes

- Downloaded games are stored in the `downloads/` directory as MP4 files
- The application checks if a game has already been downloaded to avoid duplicates
- Games are typically available several hours after the live broadcast ends
- The application requires internet access to function properly
