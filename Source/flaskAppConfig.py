from flask import Flask, render_template

app = Flask(__name__)

# Routes the main page of the site to the relevant HTML template
@app.route("/")
def run_test_page():
    return render_template('loginPage.html')

# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)