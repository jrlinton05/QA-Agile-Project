import os
from flask import Flask, render_template

template_dir = os.path.abspath('../Templates')
app = Flask(__name__, template_folder=template_dir)

# Routes the main page of the site to the relevant HTML template
@app.route("/")
def run_test_page():
    return render_template("testPage.html")

# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)