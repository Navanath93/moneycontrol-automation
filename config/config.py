import os

# Base URL (can be overridden for staging/QA)
BASE_URL = os.getenv("MC_BASE_URL", "https://www.moneycontrol.com/")

# Wait times
SHORT_WAIT = int(os.getenv("SHORT_WAIT", 5))
LONG_WAIT = int(os.getenv("LONG_WAIT", 30))

# Credentials (must be set in environment)
USERNAME = os.getenv("MC_USERNAME", "")
PASSWORD = os.getenv("MC_PASSWORD", "")
if not USERNAME or not PASSWORD:
    raise RuntimeError("MC_USERNAME and MC_PASSWORD must be set in environment variables")

# Browser defaults
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# User-Agent (centralized for consistency)
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36"
)
