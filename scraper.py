from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_case_by_cnr(cnr_number):
    options = Options()
    # options.add_argument("--headless")  # Runs without opening Chrome visibly
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

        wait = WebDriverWait(driver, 20)

        # Step 1: Fill the CNR number
        cnr_input = wait.until(EC.presence_of_element_located((By.ID, "cino")))
        cnr_input.clear()
        cnr_input.send_keys(cnr_number)

        # Step 2: Ask user to solve CAPTCHA manually
        print("🧠 Please solve CAPTCHA in browser manually (headless mode is ON, so this won't work here).")
        print("⚠️ Temporarily DISABLE headless mode to solve CAPTCHA. Then re-enable it once solved.")
        input("📌 Press ENTER after solving CAPTCHA and clicking the 'Search' button...")

        # Step 3: Wait for the results to load
        wait.until(EC.presence_of_element_located((By.ID, "history_cnr")))

        # Step 4: Parse with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        result_div = soup.find("div", id="history_cnr")
        if result_div:
            case_details = result_div.get_text(separator="\n").strip()
            return {"result": case_details}
        else:
            return {"error": "Result not found or incorrect CNR number."}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
