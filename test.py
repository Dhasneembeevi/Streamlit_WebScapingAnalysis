import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def fetch_amazon_price(product_name):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    search_query = product_name.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={search_query}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]'))
        )
        results = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]')

        for item in results:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 span").text
                price_whole = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                try:
                    price_fraction = item.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                except:
                    price_fraction = "00"
                price = f"₹{price_whole}.{price_fraction}"
                driver.quit()
                return price
            except:
                continue

        driver.quit()
        return "Price not found"
    except Exception as e:
        driver.quit()
        return "Failed to fetch page"

def fetch_flipkart_price(product_name):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    search_query = product_name.replace(" ", "+")
    url = f"https://www.flipkart.com/search?q={search_query}"
    driver.get(url)

    try:
        try:
            close_login = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
            )
            close_login.click()
        except:
            pass

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nx9bqj"))
        )

        products = driver.find_elements(By.CSS_SELECTOR, "div.tUxRFH")

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, "div.KzDlHZ").text
                price = product.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text
                driver.quit()
                return price
            except:
                continue

        driver.quit()
        return "Price not found"
    except Exception as e:
        driver.quit()
        return "Failed to fetch page"

st.set_page_config(page_title="Product Price Checker", layout="centered")
st.title("🛍️ Live Price Checker - Amazon & Flipkart")

product_input = st.text_input("Enter product name:", "")

if st.button("Search Price"):
    if product_input.strip() == "":
        st.warning("Please enter a product name.")
    else:
        with st.spinner("Fetching price... Please wait."):
            amazon_price = fetch_amazon_price(product_input)
            flipkart_price = fetch_flipkart_price(product_input)

        st.subheader(f"🔍 Results for: `{product_input}`")
        st.write(f"**Amazon Price:** {amazon_price}")
        st.write(f"**Flipkart Price:** {flipkart_price}")