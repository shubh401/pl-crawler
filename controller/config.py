from playwright.sync_api import sync_playwright, Playwright, BrowserContext
from collections import defaultdict
from expose import *

import traceback
import aiohttp
import logging
import time
import json
import sys
import os

# BASE LOGGER
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename=f"/home/logs/runtime_logs/{os.getenv('TEST_ID', '1')}.log",
    filemode="a+"
)
logging.getLogger("urllib3").setLevel(logging.ERROR)

# CRAWL CONFIG
ALLOWED_RETRIALS = 5
TMP_PATH = "/tmp/chromiumDataDir/"

DATASET = os.getenv('DATASET')
TEST_ID = os.getenv('TEST_ID')
TARGET_URL = os.getenv('URL')
BROWSER = os.getenv('BROWSER', 'chrome')

# PAGE CONFIG
CRAWL_TIMEOUT = 10000
NAVIGATION_TIMEOUT = 30000
WAIT_TIMEOUT = 10

# PAGE MODULES
CAPTURE_MODULES = ["api_hooks", "prop_hooks"]
EXPOSED_MODULES = ["logger"]

# AUXILIARY
NEWLINE = '\n'
HAR_PATH = f"/home/logs/har_logs"
TRACE_PATH = f"/home/logs/traces"

# CONTEXT CONFIG
CHROMIUM_LAUNCH_ARGS = {
    "headless": False,
    "timeout": 30000,
    "ignore_https_errors": True,
    "viewport": { 'width': 1920, 'height': 1080 },
    "locale": "en-US",
    "record_har_content": "embed",
    "record_har_mode": "minimal",
    "accept_downloads": False,
    "ignore_default_args": ["--enable-automation"],
    "record_har_path": f"{HAR_PATH}/{os.getenv('TEST_ID', '1')}.har",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.176 Safari/537.36",
    "args": [
        '--no-first-run',
        '--disable-infobars',
        '--disable-setuid-sandbox',
        '--ignore-certificate-errors',
        '--disable-software-rasterizer',
        '--start-maximized',
        '--shm-size=2G',
        '--allow-running-insecure-content',
        '--ignore-certificate-errors-spki-list',
    ]
}

FIREFOX_LAUNCH_ARGS = {
    "headless": False,
    "timeout": 30000,
    "ignore_https_errors": True,
    "viewport": { 'width': 1920, 'height': 1080 },
    "locale": "en-US",
    "record_har_content": "embed",
    "record_har_mode": "minimal",
    "accept_downloads": False,
    "ignore_default_args": ["--enable-automation"],
    "record_har_path": f"{HAR_PATH}/{os.getenv('TEST_ID', '1')}.har",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.176 Safari/537.36",
    "args": [
        '--no-first-run',
        '--disable-infobars',
        '--disable-setuid-sandbox',
        '--ignore-certificate-errors',
        '--disable-software-rasterizer',
        '--start-maximized',
        '--allow-running-insecure-content',
        '--ignore-certificate-errors-spki-list',
    ],
    "firefox_user_prefs": {
        'devtools.debugger.remote-enabled': True,
        'devtools.debugger.prompt-connection': False,
    },

}
