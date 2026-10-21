
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

URL = "https://quotes.toscrape.com/js/"

driver = None

try:
    print("Starting Selenium scraper...")

    driver = webdriver.Chrome()
    driver.get(URL)

    wait = WebDriverWait(driver, 15)

    # Wait until the dynamically loaded quotes appear
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".quote")
        )
    )

    print("Website title:", driver.title)
    print("Website URL:", driver.current_url)

    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote")
    print("Total quotes found:", len(quotes))
    print("-" * 50)

    for number, quote in enumerate(quotes, start=1):
        text = quote.find_element(
            By.CSS_SELECTOR, ".text"
        ).text

        author = quote.find_element(
            By.CSS_SELECTOR, ".author"
        ).text

        print(f"{number}. Quote: {text}")
        print(f"   Author: {author}")

except TimeoutException:
    print("Timed out waiting for the quotes to load.")

except WebDriverException as error:
    print("Browser or Selenium error:", error)

finally:
    if driver is not None:
        driver.quit()
        print("Browser closed.")
