from flask import Flask, render_template

app = Flask(__name__)


# Flask app page routing
@app.route("/")
def get_root_page():
    return render_template('loginPage.html')


@app.route("/login")
def get_login_page():
    return render_template('loginPage.html')


@app.route("/register")
def get_register_page():
    return render_template('registerPage.html')


# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)
