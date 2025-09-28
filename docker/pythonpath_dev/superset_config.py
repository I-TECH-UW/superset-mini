# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.alerts",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    task_annotations = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "reports.scheduler": {"rate_limit": "10/m"},
        "alerts.scheduler": {"rate_limit": "10/m"},
    }
    beat_schedule = {
        # Reports scheduling - runs every minute to check for scheduled reports
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        # Clean up old report logs daily at midnight
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
        # Alerts scheduling - runs every minute to check for triggered alerts
        "alerts.scheduler": {
            "task": "alerts.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        # Clean up old alert logs daily at 1 AM
        "alerts.prune_log": {
            "task": "alerts.prune_log",
            "schedule": crontab(minute=0, hour=1),
        },
    }


CELERY_CONFIG = CeleryConfig

# =============================================================================
# ALERTS AND REPORTS CONFIGURATION
# =============================================================================

# Enable alerts and reports feature
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True,  # Enable dashboard-based access control for reports
}

# Alert and Reports Notification Settings
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True  # Set to False to enable actual notifications
ALERT_REPORTS_ATTACH_REPORTS = True  # Attach report files to email notifications
ALERT_REPORTS_MIN_INTERVAL = 60  # Minimum interval between alerts in seconds

# Email Configuration for Alerts and Reports
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", "True").lower() == "true"
SMTP_SSL_SERVER_AUTH = os.getenv("SMTP_SSL_SERVER_AUTH", "False").lower() == "true"
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_MAIL_FROM = os.getenv("SMTP_MAIL_FROM", "superset@localhost")

# Slack Configuration for Alerts and Reports (disabled)
# SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN", "")
# SLACK_PROXY = os.getenv("SLACK_PROXY", "")

# WebDriver Configuration for Report Screenshots
WEBDRIVER_TYPE = os.getenv("WEBDRIVER_TYPE", "chrome")
WEBDRIVER_BASEURL = "http://superset:8088/"  # When using docker compose baseurl should be http://superset_app:8088/
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
    "--disable-web-security",
    "--allow-running-insecure-content",
]

# Report Configuration
REPORTS_CHART_HEIGHT = 600  # Height of charts in reports (pixels)
REPORTS_CHART_WIDTH = 800   # Width of charts in reports (pixels)
REPORTS_WEBDRIVER_WINDOW = {
    "dashboard": (1600, 2000),
    "slice": (3000, 1200),
}

# Alert Configuration
ALERT_SQL_BASED_ALERT_QUERY_TIMEOUT = 300  # Timeout for alert queries in seconds
ALERT_MAX_RETRIES = 3  # Maximum retry attempts for failed alerts

SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
