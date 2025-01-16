import os
import json
from utils import fetch_website_content, load_previous_state, save_current_state
from dotenv import load_dotenv
from pathlib import Path

# Load .env for local testing
data_folder = Path(__file__).resolve().parent.parent / "data"
data_folder.mkdir(exist_ok=True)
state_file = data_folder / "website_state.json"
email_file_path = data_folder / "email_content.html"

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    try:
        # Load URLs from configuration file
        with open(".config", "r") as config_file:
            urls = [line.strip() for line in config_file if line.strip()]

        previous_state = load_previous_state(state_file)
        current_state = {}
        new_listings = []

        for url in urls:
            content = fetch_website_content(url)  # Extract only the car listings with pictures

            previous_content = previous_state.get(url, [])
            new_items = [item for item in content if item not in previous_content]

            if new_items:
                new_listings.append({"url": url, "new_items": new_items})

            # Clean up price formatting in content
            for item in content:
                item["price"] = item["price"].replace("\u00a3", "£")

            current_state[url] = content

        if new_listings:
            email_body = "<html><body>"
            for listing in new_listings:
                email_body += f"<h2>New Listings from {listing['url']}:</h2>\n<ul>"
                for item in listing['new_items']:
                    email_body += f"<li><strong>{item['title']}</strong> - {item['price']}<br><img src='{item['image']}' alt='{item['title']}' width='200'/></li>\n"
                email_body += "</ul><br>"
            email_body += "</body></html>"

            # Save email content to a file for GitHub Actions
            with open(email_file_path, "w") as email_file:
                email_file.write(email_body)

        save_current_state(current_state, state_file)
    except Exception as e:
        # Save error message to a file for GitHub Actions
        with open(email_file_path, "w") as email_file:
            email_file.write(f"<html><body><h2>Error in Website Tracker</h2><p>An error occurred:<br>{e}</p></body></html>")

if __name__ == "__main__":
    main()