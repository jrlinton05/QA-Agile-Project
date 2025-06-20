from flask import Flask, render_template, flash, request, redirect
from flask_login import LoginManager, login_user, current_user

from Source.APIs.UserAPIs.login_api import validate_user_login
from Source.APIs.UserAPIs.registration_api import register_new_user
from Source.Constants.constants import SECRET_KEY
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.registration_result import RegistrationResult
from Source.Enums.login_result import LoginResult
from Source.Helpers.build_user_class_from_database_helper import build_user
from Source.Helpers.is_user_admin_helper import is_user_admin
from Source.Models.user import User

# Flask app setup and config
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Flask login setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return build_user(username)

# Flask app page routing
@app.route("/")
def get_root_page():
    if current_user.is_authenticated:
        return f"You have successfully logged in as {current_user.get_id()}"
    else:
        return redirect("/login")


@app.route("/login", methods = ["GET", "POST"])
def get_login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = validate_user_login(username, password)

        match result:
            case LoginResult.USER_NOT_EXIST:
                flash("This user does not exist")
            case LoginResult.INCORRECT_PASSWORD:
                flash("Password is incorrect")
            case GenericReturnCodes.SUCCESS:
                is_admin = is_user_admin(username)
                if is_admin == GenericReturnCodes.ERROR:
                    flash("Unknown error when checking admin status")
                else:
                    user = User(username, is_admin)
                    login_user(user)
                    next_page = request.args.get('next')
                    if next_page is None:
                        return f"You have successfully logged in as {username}"
                    else:
                        return redirect(next_page)
            case _:
                flash("Unknown error has occurred")

    return render_template("login-page.html")


@app.route("/register", methods = ["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repeated_password = request.form["repeated-password"]
        result = register_new_user(username, password, repeated_password, False)

        match result:
            case GenericReturnCodes.SUCCESS:
                flash("New user successfully registered")
                return redirect("/login")
            case RegistrationResult.USER_IN_DATABASE:
                flash("Username already exists")
            case RegistrationResult.PASSWORD_INVALID:
                flash("Password does not match requirements")
            case RegistrationResult.PASSWORDS_DO_NOT_MATCH:
                flash("Passwords do not match")
            case _:
                flash(f"Unknown error has occurred: {result}")

    return render_template("register-page.html")


# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)
