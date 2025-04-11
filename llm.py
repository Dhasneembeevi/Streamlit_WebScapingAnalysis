import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

GEMINI_API_KEY = "AIzaSyCM87KDRP2Kdv6cDlXlkm-c8HJGh8VSlWo"
genai.configure(api_key=GEMINI_API_KEY)
try:
    models = genai.list_models()
    for model in models:
        print(model)
        # st.write(model)
except Exception as e:
    print(f"Error listing models: {e}")
def query_gemini(prompt):
    """Sends a prompt to the Gemini Pro model and returns the response."""
    try:
        # model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
        # model = genai.GenerativeModel('gemini-1.5-flash-8b-latest')
        # model = genai.GenerativeModel('gemini-1.5-flash-8b')
        # model = genai.GenerativeModel('gemini-1.5-flash-8b-001')
        # model = genai.GenerativeModel('gemini-1.5-flash-002')
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error querying Gemini API: {e}"

def fetch_amazon_price(product_name):
    """Searches Amazon for the product and tries to extract the price."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        price_element = soup.find('span', class_='a-price-whole')
        fraction_element = soup.find('span', class_='a-price-fraction')

        if price_element and fraction_element:
            return f"₹{price_element.text}{fraction_element.text}"
        elif price_element:
            return f"₹{price_element.text}"
        else:
            return "Price not found on Amazon."
    except Exception as e:
        return f"Error fetching price from Amazon: {e}"

# def fetch_flipkart_price(product_name):
#     """Searches Flipkart for the product and tries to extract the price."""
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
#         search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
#         response = requests.get(search_url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'lxml')

#         price_element = soup.find('div', class_='_30jeq3 _16Jk6d')
#         if price_element:
#             return price_element.text.strip()
#         else:
#             return "Price not found on Flipkart."
#     except Exception as e:
#         return f"Error fetching price from Flipkart: {e}"

import requests
from bs4 import BeautifulSoup
import time
import requests
from bs4 import BeautifulSoup
import time

def fetch_flipkart_price(product_name, max_retries=3, retry_delay=2):
    try:
        headers = {'User-Agent': 'Your User Agent String'}
        search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        for attempt in range(max_retries):
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            price_element = soup.find('div', class_='_30jeq3 _16Jk6d')  # Ensure this is the correct class
            if price_element:
                return price_element.text.strip()
            else:
                if attempt < max_retries - 1:
                    print(f"Flipkart: Price element not found. Retrying in {retry_delay} seconds (Attempt {attempt + 1})...")
                    time.sleep(retry_delay)
                else:
                    return "Price not found on Flipkart after multiple retries."
        return "Price not found on Flipkart."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price from Flipkart (Attempt {attempt + 1}): {e}")
        if attempt < max_retries - 1 and response is not None and response.status_code == 500:
            print(f"Flipkart: Internal Server Error. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        elif response is not None and response.status_code == 403:
            return f"Error fetching price from Flipkart: Forbidden (403). Flipkart might be blocking scraping."
        elif response is not None:
            return f"Error fetching price from Flipkart: {response.status_code} {response.reason}"
        elif attempt < max_retries - 1:
            print(f"Flipkart: Connection error. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            return f"Error fetching price from Flipkart after multiple retries: {e}"
    except Exception as e:
        return f"Error processing Flipkart response: {e}"
# def fetch_flipkart_price(product_name, max_retries=3, retry_delay=2):
#     try:
#         headers = {'User-Agent': 'Your User Agent String'}
#         search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
#         for attempt in range(max_retries):
#             response = requests.get(search_url, headers=headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, 'lxml')
#             price_element = soup.find('div', class_='_30jeq3 _16Jk6d')
#             if price_element:
#                 return price_element.text.strip()
#             else:
#                 if attempt < max_retries - 1:
#                     print(f"Flipkart: Price element not found. Retrying in {retry_delay} seconds (Attempt {attempt + 1})...")
#                     time.sleep(retry_delay)
#                 else:
#                     return "Price not found on Flipkart after multiple retries."
#         return "Price not found on Flipkart."
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching price from Flipkart (Attempt {attempt + 1}): {e}")
#         if attempt < max_retries - 1 and response is not None and response.status_code == 500:
#             print(f"Flipkart: Internal Server Error. Retrying in {retry_delay} seconds...")
#             time.sleep(retry_delay)
#         elif response is not None and response.status_code == 403:
#             return f"Error fetching price from Flipkart: Forbidden (403). Flipkart might be blocking scraping."
#         elif response is not None:
#             return f"Error fetching price from Flipkart: {response.status_code} {response.reason}"
#         elif attempt < max_retries - 1:
#             print(f"Flipkart: Connection error. Retrying in {retry_delay} seconds...")
#             time.sleep(retry_delay)
#         else:
#             return f"Error fetching price from Flipkart after multiple retries: {e}"
#     except Exception as e:
#         return f"Error processing Flipkart response: {e}"

# In your Streamlit app, call the modified function:
# flipkart_price = fetch_flipkart_price(product_name)
def fetch_croma_price(product_name):
    """Searches Croma for the product and tries to extract the price."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        search_url = f"https://www.croma.com/search?text={product_name.replace(' ', '%20')}"
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        price_element = soup.find('span', class_='selling-price')
        if price_element:
            return price_element.text.strip()
        else:
            return "Price not found on Croma."
    except Exception as e:
        return f"Error fetching price from Croma: {e}"

st.title("Product Price Checker with Gemini AI Summary")

product_name = st.text_input("Enter the product name to search:")

if st.button("Get Prices and Summary"):
    if product_name:
        with st.spinner("Fetching prices..."):
            amazon_price = fetch_amazon_price(product_name)
            # flipkart_price = fetch_flipkart_price(product_name)
            # croma_price = fetch_croma_price(product_name)

        st.subheader(f"Current Prices for '{product_name}':")
        st.write(f"Amazon: {amazon_price}")
        # st.write(f"Flipkart: {flipkart_price}")
        # st.write(f"Croma: {croma_price}")

        # with st.spinner("Getting summary from Gemini AI..."):
        #     prompt = f"Summarize the current prices for '{product_name}' found on Amazon ({amazon_price}), Flipkart ({flipkart_price}), and Croma ({croma_price})."
        #     gemini_summary = query_gemini(prompt)

        # st.subheader("Price Summary from Gemini AI:")
        # st.markdown(gemini_summary)

    else:
        st.warning("Please enter a product name.")
# streamlit as st
# import google.generativeai as genai
# import requests
# from bs4 import BeautifulSoup

# # Replace with your actual Gemini API key
# genai.configure(api_key="AIzaSyCM87KDRP2Kdv6cDlXlkm-c8HJGh8VSlWo")

# def query_gemini(prompt):
#     """Sends a prompt to the Gemini Pro model and returns the response."""
#     try:
#         modelTest = genai.list_models()
#         print(modelTest)

#         model = genai.GenerativeModel('gemini-1.5-flash')
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error querying Gemini API: {e}"

# st.title("Interact with Gemini AI")

# user_prompt = st.text_area("Enter your prompt for Gemini AI:", height=150)

# if st.button("Get Response"):
#     if user_prompt:
#         with st.spinner("Fetching response from Gemini AI..."):
#             gemini_response = query_gemini(user_prompt)
#         st.subheader("Gemini AI's Response:")
#         st.markdown(gemini_response)
#     else:
#         st.warning("Please enter a prompt.")   

# def fetch_amazon_price(product_url):
#     try:
#         headers = {'User-Agent': 'Your User Agent String'} # Important to avoid blocking
#         response = requests.get(product_url, headers=headers)
#         response.raise_for_status() # Raise an exception for bad status codes
#         soup = BeautifulSoup(response.content, 'lxml')
#         price_element = soup.find('span', class_='a-offscreen') # Example class, inspect Amazon's page
#         if price_element:
#             return price_element.text.strip()
#         else:
#             return "Price not found on Amazon."
#     except Exception as e:
#         return f"Error fetching price from Amazon: {e}"

# # ... (similar functions for Flipkart and Croma) ...

# st.title("Product Price Checker")

# product_query = st.text_input("Enter the product name (or URL):")

# if st.button("Get Prices"):
#     if product_query:
#         st.subheader(f"Prices for '{product_query}':")

#         # You would need to determine if the user provided a name or a URL
#         # and adapt your fetching logic accordingly. For simplicity, let's assume URLs for now.

#         amazon_price = fetch_amazon_price("AMAZON_PRODUCT_URL_HERE") # Replace with actual URL
#         st.write(f"Amazon: {amazon_price}")

#         flipkart_price = fetch_flipkart_price("FLIPKART_PRODUCT_URL_HERE") # Replace with actual URL
#         st.write(f"Flipkart: {flipkart_price}")

#         croma_price = fetch_croma_price("CROMA_PRODUCT_URL_HERE") # Replace with actual URL
#         st.write(f"Croma: {croma_price}")

#         gemini_prompt = f"Summarize the prices found for '{product_query}' on Amazon, Flipkart, and Croma."
#         gemini_summary = query_gemini(gemini_prompt)
#         st.subheader("Price Summary from Gemini AI:")
#         st.markdown(gemini_summary)

#     else:
#         st.warning("Please enter a product name or URL.")