import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from jinja2 import Template

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

def generate_email_content(new_listings):
    """
    Generates an HTML email content for new listings using Jinja2 templates.

    Args:
        new_listings (list): A list of dictionaries containing new listings.

    Returns:
        str: The rendered HTML email content.
    """
    html_template = """
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #333;">New Listings Found</h2>
        {% for site in listings %}
          <h3 style="color: #555;">From: {{ site.url }}</h3>
          <ul style="list-style-type: none; padding: 0;">
          {% for item in site.new_items %}
            <li style="margin-bottom: 20px;">
              <p><strong style="font-size: 16px;">{{ item.title }}</strong></p>
              <p style="color: #555;">Price: {{ item.price }}</p>
              {% if item.image %}
              <img src="{{ item.image }}" style="max-width: 200px; height: auto; margin-top: 10px;">
              {% endif %}
            </li>
          {% endfor %}
          </ul>
        {% endfor %}
      </body>
    </html>
    """
    template = Template(html_template)
    return template.render(listings=new_listings)