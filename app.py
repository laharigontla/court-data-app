from flask import Flask, render_template, request
from scraper import scrape_case_by_cnr  # 🟢 Make sure this matches your function name

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        cnr = request.form["cnr"]
        data = scrape_case_by_cnr(cnr)  # 🟢 Calls your Selenium function
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
