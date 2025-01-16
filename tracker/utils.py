from bs4 import BeautifulSoup
import requests
import json
import os

STATE_FILE = "website_state.json"

def fetch_website_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract car listings
    cars = []
    products = soup.select("li.product")
    for product in products:
        title = product.select_one(".woocommerce-loop-product__title").text.strip()
        price = product.select_one(".price").text.strip() if product.select_one(".price") else "N/A"
        image = product.select_one("img").get("src", "").strip() if product.select_one("img") else "No Image"
        details = {
            "title": title,
            "price": price,
            "image": image
        }
        cars.append(details)

    return cars

def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
