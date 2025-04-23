import re
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    options = Options()
    options.add_argument("--headless")  # use old headless mode for stability
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--enable-unsafe-swiftshader")  # to suppress WebGL fallback warning

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)

def fetch_amazon_price(product_name):
    driver = init_driver()
    try:
        search_query = product_name.replace(" ", "+")
        url = f"https://www.amazon.in/s?k={search_query}"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]'))
        )

        results = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]')

        for item in results:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 span").text
                price_text = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                price_numeric = float(price_text.replace(",", "").strip())

                try:
                    discount_element = item.find_element(By.XPATH, './/span[contains(text(), "% off")]')
                    discount_text = discount_element.text
                    discount_percent = float(re.search(r"(\d+)%", discount_text).group(1))
                    mrp_calculated = price_numeric / (1 - (discount_percent / 100))
                    mrp_final = f"₹{round(mrp_calculated):,}"
                except Exception as e:
                    mrp_final = "Not available"

                return {
                    "title": title,
                    "price": f"₹{price_numeric:,.2f}",
                    "mrp": mrp_final
                }
            except Exception as e:
                continue

        return {"title": "N/A", "price": "Price not found", "mrp": "N/A"}
    except Exception as e:
        print(f"[Amazon Error] {e}")
        return {"title": "Error", "price": "Failed to fetch page", "mrp": "N/A"}
    finally:
        driver.quit()

def fetch_flipkart_price(product_name):
    driver = init_driver()
    try:
        search_query = product_name.replace(" ", "+")
        url = f"https://www.flipkart.com/search?q={search_query}"
        driver.get(url)

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
                try:
                    mrp = product.find_element(By.CSS_SELECTOR, "div.yRaY8j").text
                except:
                    mrp = "Not available"
                return {
                    "title": title,
                    "price": price,
                    "mrp": mrp
                }
            except Exception as e:
                continue

        return {"title": "N/A", "price": "Price not found", "mrp": "N/A"}
    except Exception as e:
        print(f"[Flipkart Error] {e}")
        return {"title": "Error", "price": "Failed to fetch page", "mrp": "N/A"}
    finally:
        driver.quit()



st.set_page_config(page_title="Product Price Checker", layout="centered")
st.title("🛍️ Live Price Checker - Amazon & Flipkart")

product_input = st.text_input("Enter product name:")

if st.button("Search Price"):
    if product_input.strip() == "":
        st.warning("Please enter a product name.")
    else:
        with st.spinner("Fetching prices from Amazon & Flipkart..."):
            amazon_data = fetch_amazon_price(product_input)
            flipkart_data = fetch_flipkart_price(product_input)

        st.subheader(f"🔍 Results for: `{product_input}`")

        st.markdown("### 🛒 Amazon")
        st.write(f"**Variant Name:** {amazon_data['title']}")
        st.write(f"**Price:** {amazon_data['price']}")
        st.write(f"**MRP:** {amazon_data['mrp']}")

        st.markdown("### 🛍️ Flipkart")
        st.write(f"**Variant Name:** {flipkart_data['title']}")
        st.write(f"**Price:** {flipkart_data['price']}")
        st.write(f"**MRP:** {flipkart_data['mrp']}")
