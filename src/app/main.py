from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)

import os
import structlog
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlmodel import select

from app.db import get_session, init_db
from app.models import Activity, User

load_dotenv()
logger = structlog.get_logger(__name__)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/")
def home():
    now = datetime.now()
    SOCIAL_LINKS = {
        "linkedin": "https://www.linkedin.com/company/python-bangladesh/",
        "discord": "https://discord.gg/sR52eYRFba",
        "whatsapp": "https://whatsapp.com/channel/0029VbAf0s70rGiMzJfG4u2B",
        "github": "https://github.com/pythonbangladesh",
    }
    with get_session() as session:
        activities = session.exec(
            select(Activity).order_by(Activity.event_date.desc())
        ).all()

        # Update is_upcoming=False for past events
        for activity in activities:
            if not activity.is_upcoming:
                continue
            with get_session() as session:
                activity.is_upcoming = (
                    activity.event_date and 
                    activity.event_date > now
                )
                session.commit()
    
    return render_template(
        "index.html", social_links=SOCIAL_LINKS, activities=activities
    )


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("assets", filename)


@app.route("/healthz")
def health():
    return "OK", 200


@app.route("/coc")
def coc():
    return render_template("legal/code-of-conduct.html")

# --------------------------
# Admin and Authentication
# --------------------------

@login_manager.user_loader
def load_user(user_id):
    with get_session() as session:
        user = session.get(User, int(user_id))
        if user:
            session.expunge(user)
        return user


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with get_session() as session:
            user = session.exec(select(User).where(User.email == email)).one_or_none()

            if user and user.check_password(password):
                logger.info("User logged in", user=user, admin=user.is_admin)
                login_user(user)
                return redirect(url_for("admin_dashboard"))
            else:
                logger.warning("Invalid login attempt", email=email)
                flash("Invalid email or password")
                return redirect(url_for("login"))

    return render_template("admin/login.html")


@app.route("/logout/")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/admin/")
@login_required
def admin():
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    return render_template("admin/dash.html", user=current_user)


if __name__ == "__main__":
    init_db()  # Initialize the database
    port = int(os.getenv("PORT", 10000))
    print(f"---------Starting app on port {port}-------------")
    app.run(debug=True, host="0.0.0.0", port=port)
