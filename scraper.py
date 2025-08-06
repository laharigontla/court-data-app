from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_case_by_cnr(cnr_number):
    options = Options()
    options.add_argument("--headless")  # Enable headless mode for deployment
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

        wait = WebDriverWait(driver, 20)

        # Locate and fill in the CNR input field
        cnr_input = wait.until(EC.presence_of_element_located((By.ID, "cino")))
        cnr_input.clear()
        cnr_input.send_keys(cnr_number)

        # CAPTCHA present – cannot proceed in headless/Render
        return {
            "error": "This service uses a CAPTCHA that cannot be bypassed automatically. Please run the app locally to search CNR numbers."
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
