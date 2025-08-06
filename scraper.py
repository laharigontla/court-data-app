import os

def scrape_case_by_cnr(cnr_number):
    # ✅ Show mock data only on Render
    if os.environ.get("RENDER", "").lower() == "true":
        return {
            "result": f"""
CNR Number: {cnr_number}
Case Type: Civil Suit
Filing Date: 01-Jan-2022
Status: Pending
Petitioner: John Doe
Respondent: State of Andhra Pradesh
Court: Guntur District Court
Next Hearing: 25-Aug-2025
            """.strip()
        }

    # ✅ Otherwise (locally), use real Selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import time

    options = Options()
    # options.add_argument("--headless")  # Uncomment only after testing locally
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

        wait = WebDriverWait(driver, 20)

        cnr_input = wait.until(EC.presence_of_element_located((By.ID, "cino")))
        cnr_input.clear()
        cnr_input.send_keys(cnr_number)

        print("🧠 Please solve CAPTCHA in the browser manually.")
        input("✅ Press ENTER after solving CAPTCHA and clicking the 'Search' button...")

        wait.until(EC.presence_of_element_located((By.ID, "history_cnr")))

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
