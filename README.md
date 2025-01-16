## Website Tracker with Email Notifications

### Overview

This project tracks specified websites for changes and sends email notifications when new content is detected. It is designed to run as a GitHub Actions workflow and supports comparing the current state of websites against previously saved states to detect changes.

### Features

- Tracks specified websites for changes.
- Detects and reports new content.
- Sends email notifications

### How It Works

1. The script loads URLs from the .config file.
2. Fetches the content of each URL and compares it against the saved state in website_state.json.
3. If new content is detected, it generates an email report and saves it to email_content.txt.
4. GitHub Actions sends the email using the saved report.
5. Updates website_state.json to reflect the current state.


### License

This project is licensed under the MIT License.
