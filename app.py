from flask import Flask, render_template, request
import os

# Import the function only when running locally
from scraper import scrape_case_by_cnr

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        cnr = request.form["cnr"]

        # ✅ If running on Render, skip scraping and show a warning
        if os.environ.get("RENDER", "").lower() == "true":
            data = {
                "error": "❌ Due to CAPTCHA on the eCourts site, live case search is not available on the deployed version. Please run locally to use this feature."
            }
        else:
            # ✅ Local mode — run full scraper
            data = scrape_case_by_cnr(cnr)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
