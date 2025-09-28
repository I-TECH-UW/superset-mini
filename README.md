## Welcome to Superset for CHT Repository

This repository is for running Superset with the Community Health Toolkit (CHT).

The goal is to configure it to run smoothly with [CHT-Sync](https://github.com/medic/cht-sync) and includes comprehensive alerts and reports functionality.

## Quick Start

```bash
cp docker/.env.example docker/.env
docker-compose up -d
```

## NGINX

If you're installing this superset on the same server that is running CHT application, the NGINX service will not start because of the port conflict. You'll need to proxy superset using CHT Nginx.

---

# Alerts and Reports Configuration

This Superset instance is pre-configured with comprehensive alerts and reports functionality for monitoring CHT data and sending automated notifications.

## Overview

The following features are configured and ready to use:

### ✅ What's Already Configured

1. **Feature Flags**: Alerts and reports are enabled
2. **Celery Configuration**: Enhanced with proper task scheduling for both alerts and reports
3. **WebDriver Setup**: Configured for report screenshot generation
4. **Email & Slack Integration**: Ready for notification setup
5. **Report Settings**: Optimized dimensions and browser options

## Configuration Details

### 1. Core Settings

```python
# Alerts and reports are enabled
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True,  # Dashboard-based access control
}

# Currently in dry-run mode for safety
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
```

### 2. Celery Task Scheduling

The system includes comprehensive task scheduling:

- **Reports Scheduler**: Runs every minute to check for scheduled reports
- **Alerts Scheduler**: Runs every minute to check for triggered alerts
- **Log Cleanup**: Daily cleanup of old logs at midnight and 1 AM
- **Rate Limiting**: Configured to prevent system overload

## Setting Up Notifications

### Email Configuration

Add these environment variables to your `docker/.env` file:

```bash
# For Gmail (example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_STARTTLS=True
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_MAIL_FROM=your-email@gmail.com

# For Outlook
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_STARTTLS=True
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_MAIL_FROM=your-email@outlook.com
```

### Slack Configuration (Optional)

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Create a new app or select existing
3. Add these OAuth scopes:
   - `incoming-webhook`
   - `files:write`
   - `chat:write`
   - `channels:read`
   - `groups:read`
4. Install app to workspace
5. Copy the Bot User OAuth Access Token
6. Add to your `docker/.env` file:
   ```bash
   SLACK_API_TOKEN=xoxb-your-slack-bot-token
   ```

### Enable Notifications

Once you've configured your notification channels, add this to your `docker/.env` file:

```bash
ALERT_REPORTS_NOTIFICATION_DRY_RUN=False
```

**⚠️ Important**: Only set this to `False` after testing your email/Slack configuration!

## Using Alerts and Reports

### Creating Alerts

1. Go to **Alerts & Reports** → **Alerts**
2. Click **+ Alert**
3. Configure:
   - **Chart**: Select the chart to monitor
   - **Condition**: Set threshold conditions
   - **Recipients**: Add email addresses or Slack channels
   - **Schedule**: Set how often to check

### Creating Reports

1. Go to **Alerts & Reports** → **Reports**
2. Click **+ Report**
3. Configure:
   - **Dashboard/Chart**: Select what to report on
   - **Recipients**: Add email addresses or Slack channels
   - **Schedule**: Set delivery frequency (daily, weekly, etc.)

### Common Use Cases for CHT

1. **Health Metrics**: Daily reports on key health indicators
2. **Data Quality**: Alerts when CHT data sync issues occur
3. **Performance Monitoring**: Reports on dashboard performance metrics
4. **Compliance**: Automated reports for health authorities

## Troubleshooting

### Email Not Working
1. Check SMTP credentials in `docker/.env`
2. Verify firewall/network access to SMTP server
3. For Gmail, ensure you're using an App Password, not your regular password
4. Check Superset logs: `docker-compose logs superset`

### Reports Not Generating
1. Ensure Chrome is installed in the container (included in base image)
2. Check that the base URL is accessible from within the container
3. Verify dashboard/chart permissions for the report user

### Celery Tasks Not Running
1. Ensure Redis is running: `docker-compose ps redis`
2. Check Celery worker: `docker-compose logs superset-worker`
3. Check beat scheduler: `docker-compose logs superset-worker-beat`

## Security Considerations

1. **Credentials**: Store sensitive credentials in `docker/.env`, not in config files
2. **Permissions**: Use dashboard RBAC to control who can create alerts/reports
3. **Dry Run**: Always test in dry-run mode first
4. **Rate Limiting**: The configuration includes rate limiting to prevent abuse

## Monitoring

Monitor your alerts and reports system:

1. **Logs**: Check Superset logs for task execution status
2. **Celery Monitoring**: Use Flower or similar tools to monitor Celery tasks
3. **Redis**: Monitor Redis for task queue health
4. **Database**: Check the `alerts` and `reports` tables for execution history

## Support

For issues or questions:
1. Check Superset documentation: https://superset.apache.org/docs/
2. Review logs: `docker-compose logs [service-name]`
3. Verify environment variable configuration in `docker/.env`
4. Test with simple alert/report first before complex setups
