import os
import json
from utils import fetch_website_content, load_previous_state, save_current_state, generate_plain_text_email
from dotenv import load_dotenv
from pathlib import Path

data_folder = Path(__file__).resolve().parent.parent / "data"
data_folder.mkdir(exist_ok=True)
state_file = data_folder / "website_state.json"
email_file_path = data_folder / "email_content.txt"

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
            content = fetch_website_content(url)

            previous_content = previous_state.get(url, [])
            new_items = [item for item in content if item not in previous_content]

            if new_items:
                new_listings.append({"url": url, "new_items": new_items})

            for item in content:
                item["price"] = item["price"].replace("\u00a3", "£")

            current_state[url] = content

        if new_listings:
            email_content = generate_plain_text_email(new_listings)

            # Save email content to a file for GitHub Actions
            with open(email_file_path, "w") as email_file:
                email_file.write(email_content)

        save_current_state(current_state, state_file)
    except Exception as e:
        error_content = f"Error in Website Tracker\nAn error occurred:\n{e}\n"
        with open(email_file_path, "w") as email_file:
            email_file.write(error_content)

if __name__ == "__main__":
    main()