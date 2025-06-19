from flask import Flask, render_template, flash, request, redirect

from Source.APIs.registrationAPI import register_new_user
from Source.Constants.Constants import SECRET_KEY

# Flask app setup and config
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Flask app page routing
@app.route("/")
def get_root_page():
    return redirect("/login")


@app.route("/login")
def get_login_page():
    return render_template("loginPage.html")


@app.route("/register", methods = ["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repeated_password = request.form["repeated-password"]
        result = register_new_user(username, password, repeated_password, False)

        match result:
            case "success":
                flash("New user successfully registered")
                return redirect("/login")
            case "userInDatabase":
                flash("Username already exists")
            case "passwordsDoNotMatch":
                flash("Passwords do not match")
            case _:
                flash("Unknown error has occurred")

    return render_template("registerPage.html")


# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)
