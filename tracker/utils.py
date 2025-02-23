import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def fetch_website_content(url):
    """
    Fetches the car listings from the given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        list: A list of dictionaries containing car details.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract car listings
        cars = []
        products = soup.select("li.product")
        for product in products:
            title = product.select_one(".woocommerce-loop-product__title").text.strip()
            price = product.select_one(".price").text.strip().replace("\u00a3", "£") if product.select_one(".price") else "N/A"
            image = product.select_one("img").get("src", "").strip() if product.select_one("img") else "No Image"
            details = {
                "title": title,
                "price": price,
                "image": image
            }
            cars.append(details)

        return cars
    except Exception as e:
        raise Exception(f"Error fetching content from {url}: {e}")


def load_previous_state(state_file):
    """
    Loads the previous state of the website content from the state file.

    Args:
        state_file (Path): The path to the state file.

    Returns:
        dict: The previously stored state of the websites.
    """
    if state_file.exists():
        with open(state_file, "r") as f:
            return json.load(f)
    return {}


def save_current_state(state, state_file):
    """
    Saves the current state of the website content to the state file.

    Args:
        state (dict): The current state of the websites.
        state_file (Path): The path to the state file.
    """
    with open(state_file, "w") as f:
        json.dump(state, f, indent=4)


def generate_plain_text_email(new_listings):
    """
    Generates a plain text email content for new listings.

    Args:
        new_listings (list): A list of dictionaries containing new listings.

    Returns:
        str: The plain text email content.
    """
    email_content = "New Listings Found:\n\n"
    for listing in new_listings:
        email_content += f"From: {listing['url']}\n"
        for item in listing['new_items']:
            email_content += f"- Title: {item['title']}\n  Price: {item['price']}\n"
            if item['image']:
                email_content += f"  Image: {item['image']}\n"
        email_content += "\n"
    return email_content