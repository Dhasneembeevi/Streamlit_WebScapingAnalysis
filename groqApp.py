# from bs4 import BeautifulSoup
# # from groqApp import Groq
# from groq import Groq
# import streamlit as st
# import requests
# # from groq import Groq

# # Set up Groq API Key
# GROQ_API_KEY = "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"  # Replace with your API key
# client = Groq(api_key=GROQ_API_KEY)

# # Streamlit App Title
# st.title("Amazon & Flipkart Price Fetcher with Groq Insights")
# st.write("Enter a product name to fetch its price details and analyze using Groq models.")

# # Input field for product name
# product_name = st.text_input("Product Name", placeholder="e.g., iPhone 14")

# # Search Button
# if st.button("Fetch Prices"):
#     if product_name:
#         # Function to scrape Amazon prices
#         def scrape_amazon(product):
#             url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
#             headers = {"User-Agent": "Mozilla/5.0"}
#             response = requests.get(url, headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             try:
#                 price = soup.find('span', {'class': 'a-price-whole'}).text.strip()
#                 return price
#             except AttributeError:
#                 return "Price not found"

#         # Function to scrape Flipkart prices
#         def scrape_flipkart(product):
#             url = f"https://www.flipkart.com/search?q={product.replace(' ', '+')}"
#             headers = {"User-Agent": "Mozilla/5.0"}
#             response = requests.get(url, headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             try:
#                 price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()
#                 return price
#             except AttributeError:
#                 return "Price not found"

#         # Fetch Prices
#         amazon_price = scrape_amazon(product_name)
#         flipkart_price = scrape_flipkart(product_name)

#         # Display Results
#         st.write(f"**Amazon Price:** {amazon_price}")
#         st.write(f"**Flipkart Price:** {flipkart_price}")

#         # Use Groq Model for Additional Insights
#         def groq_analyze(text):
#             # from groq import Groq
#             client = Groq()
#             completion = client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": "Explain why fast inference is critical for reasoning models"
#                     }
#                 ]
#             )
#             print(completion.choices[0].message.content)
            
        
        

#         insights = groq_analyze(f"Amazon Price: {amazon_price}, Flipkart Price: {flipkart_price}")
#         st.write("**Groq Analysis:**")
#         st.write(insights)
#     else:
#         st.error("Please enter a product name.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq, NotFoundError

# Set up Groq API Key
GROQ_API_KEY = "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"  # Replace this in production
client = Groq(api_key=GROQ_API_KEY)

# Streamlit App Title
st.title("Amazon & Flipkart Price Fetcher with Groq Insights")
st.write("Enter a product name to fetch its price details and analyze using Groq models.")

# Input field for product name
product_name = st.text_input("Product Name", placeholder="e.g., iPhone 14")

# Function to scrape Amazon price
# def scrape_amazon(product):
#     url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     try:
#         price_whole = soup.find('span', {'class': 'a-price-whole'}).text.strip().replace(',', '')
#         price_decimal = soup.find('span', {'class': 'a-price-decimal'})
#         price_fraction = price_decimal.find_next_sibling('span') if price_decimal else None
#         if price_fraction:
#             price = f"{price_whole}.{price_fraction.text.strip()}"
#         else:
#             price = price_whole
#         return f"₹{price}"
#     except AttributeError:
#         return "Price not found"

import requests
from bs4 import BeautifulSoup

def scrape_amazon(product_name):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    query = product_name.replace(' ', '+')
    url = f"https://www.amazon.in/s?k={query}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Failed to fetch page"

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Amazon price spans often have this class
    results = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')
    for item in results:
        title = item.select_one("h2 span")
        price_whole = item.select_one("span.a-price-whole")
        price_fraction = item.select_one("span.a-price-fraction")
        
        if title and price_whole:
            price = f"₹{price_whole.text.strip()}"
            if price_fraction:
                price += f".{price_fraction.text.strip()}"
            return price

    return "Price not found"

# Example
product = "iPhone 16"
price = scrape_amazon(product)
print(f"Amazon Price for {product}: {price}")



# Function to scrape Flipkart price
def scrape_flipkart(product):
    url = f"https://www.flipkart.com/search?q={product.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price = soup.find('div', {'class': 'Nx9bqj CxhGGd'}).text.strip()
        return price
    except AttributeError:
        return "Price not found"

def groq_analyze(text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an assistant analyzing product data."},
                {"role": "user", "content": f"Analyze the following product details: {text}"}
            ],
            temperature=0.7,
            max_tokens=512,
            stream=False,
        )
        return completion.choices[0].message.content
    except NotFoundError as e:
        return f"Model not found: {e.response['error']['message']}"
# Search Button
if st.button("Fetch Prices"):
    if product_name:
        amazon_price = scrape_amazon(product_name)
        flipkart_price = scrape_flipkart(product_name)

        st.write(f"**Amazon Price:** {amazon_price}")
        st.write(f"**Flipkart Price:** {flipkart_price}")

        # Get insights from Groq
        insights = groq_analyze(
            f"Compare these two prices for {product_name} and suggest which platform is better and why.\n"
            f"Amazon Price: {amazon_price}, Flipkart Price: {flipkart_price}"
        )
        st.write("**Groq Analysis:**")
        st.write(insights)
    else:
        st.error("Please enter a product name.")


# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# # import os

# # Set up Groq API Key
# api_key = "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"
# # api_key = os.environ.get("GROQ_API_KEY")
# # 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
# # Streamlit App Title
# st.title("Amazon & Flipkart Price Fetcher")
# st.write("Enter a product name to fetch its price details from Amazon and Flipkart.")

# # Input field for product name
# product_name = st.text_input("Product Name", placeholder="e.g., iPhone 14")

# # Search Button
# if st.button("Fetch Prices"):
#     if product_name:
#         # Function to scrape Amazon prices
#         def scrape_amazon(product):
#             url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
#             headers = {"User-Agent": "Mozilla/5.0"}
#             response = requests.get(url, headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             try:
#                 price = soup.find('span', {'class': 'a-price-whole'}).text.strip()
#                 return price
#             except AttributeError:
#                 return "Price not found"

#         # Function to scrape Flipkart prices using Selenium
#         def scrape_flipkart(product):
#             # options = Options()
#             # options.add_argument("--headless")
#             # service = Service("/path/to/chromedriver")  # Update with your ChromeDriver path
#             # driver = webdriver.Chrome(service=service, options=options)
#             options = webdriver.ChromeOptions()
#             options.add_argument("--headless")  # Optional: Run in background
#             driver = webdriver.Chrome(options=options) 
#             driver.get(f"https://www.flipkart.com/search?q={product.replace(' ', '+')}")
#             try:
#                 price_element = driver.find_element(By.CLASS_NAME, "_30jeq3._16Jk6d")
#                 price = price_element.text.strip()
#                 driver.quit()
#                 return price
#             except Exception as e:
#                 driver.quit()
#                 return "Price not found"

#         # Fetch Prices
#         amazon_price = scrape_amazon(product_name)
#         flipkart_price = scrape_flipkart(product_name)
        
        
        
        

#         # Display Results
#         st.write(f"**Amazon Price:** {amazon_price}")
#         st.write(f"**Flipkart Price:** {flipkart_price}")
#     else:
#         st.error("Please enter a product name.")

# # Optional: Use Groq model for advanced reasoning (example placeholder)
# if api_key:
#     st.write("Using Groq model for additional insights...")
#     url = "https://api.groq.com/openai/v1/models"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     response = requests.get(url, headers=headers)
#     model = response.json()
#     st.json(model)
# else:
#     st.warning("Groq API Key not found.")
