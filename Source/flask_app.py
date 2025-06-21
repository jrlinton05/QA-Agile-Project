from crypt import methods

from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from Source.APIs.ReviewAPIs.create_review_api import create_review
from Source.APIs.ReviewAPIs.delete_review_api import delete_review
from Source.APIs.UserAPIs.login_api import validate_user_login
from Source.APIs.UserAPIs.registration_api import register_new_user
from Source.Constants.constants import SECRET_KEY
from Source.Enums.delete_api_return_codes import DeleteReturnCodes
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.registration_return_codes import RegistrationReturnCodes
from Source.Enums.login_return_codes import LoginReturnCodes
from Source.Helpers.build_list_of_products_helper import build_list_of_products
from Source.Helpers.build_list_of_reviews_helper import build_list_of_reviews
from Source.Helpers.build_user_class_from_database_helper import build_user
from Source.Helpers.is_user_admin_helper import is_user_admin
from Source.Models.user import User

# Flask app setup and config
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Flask login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(username):
    return build_user(username)

# Flask app page routing
@app.route("/")
def root_page():
    if current_user.is_authenticated:
        return redirect("/products")
    else:
        return redirect("/login")


@app.route("/login", methods = ["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = validate_user_login(username, password)

        match result:
            case LoginReturnCodes.USER_NOT_EXIST:
                flash("This user does not exist", "info")
            case LoginReturnCodes.INCORRECT_PASSWORD:
                flash("Password is incorrect", "info")
            case GenericReturnCodes.SUCCESS:
                is_admin = is_user_admin(username)
                if is_admin == GenericReturnCodes.ERROR:
                    flash("Unknown error when checking admin status", "error")
                else:
                    user = User(username, is_admin)
                    login_user(user)
                    next_page = request.args.get('next')
                    if next_page is None:
                        return redirect("/products")
                    else:
                        return redirect(next_page)
            case _:
                flash("Unknown error has occurred", "error")

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
                flash("New user successfully registered", "success")
                return redirect("/login")
            case RegistrationReturnCodes.USER_IN_DATABASE:
                flash("Username already exists", "info")
            case RegistrationReturnCodes.PASSWORD_INVALID:
                flash("Password does not match requirements", "info")
            case RegistrationReturnCodes.PASSWORDS_DO_NOT_MATCH:
                flash("Passwords do not match", "info")
            case _:
                flash(f"Unknown error has occurred: {result}", "error")

    return render_template("register-page.html")

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("root_page"))

@app.route("/products")
@login_required
def products_page():
    products = build_list_of_products()
    return render_template("product-page.html", products=products)


@app.route("/products/<product_id>", methods=["GET", "POST"])
@login_required
def review_page(product_id):
    if request.method == "POST":
        username = current_user.get_id()
        review_title = request.form["review_title"]
        review_body = request.form["review_body"]
        review_score = request.form["review_score"]
        result = create_review(review_title, review_body, review_score, product_id, username)
        if result == GenericReturnCodes.ERROR:
            flash("Unknown error occurred", "error")
        if result == GenericReturnCodes.SUCCESS:
            flash("Review created", "success")
    reviews = build_list_of_reviews(product_id)
    return render_template("review-page.html", reviews=reviews)


@app.route("/delete-review/<review_id>", methods=["POST"])
@login_required
def delete_review_form(review_id):
    product_id = request.form["product_id"]
    result = delete_review(review_id, current_user.get_id())
    if result == DeleteReturnCodes.USERNAME_DOES_NOT_MATCH:
        flash("You are not authorised to delete this review", "error")
    if result == DeleteReturnCodes.ITEM_DOES_NOT_EXIST:
        flash(f"Error: review_id {review_id} does not exist", "error")
    if result == GenericReturnCodes.ERROR:
        flash("Unknown error", "error")
    if result == GenericReturnCodes.SUCCESS:
        flash("Successfully deleted review", "success")

    return redirect(url_for("review_page", product_id=product_id))

# If this file is ran from the IDE, deploy the website locally in debug mode
if __name__ == "__main__":
    app.run(debug=True)
