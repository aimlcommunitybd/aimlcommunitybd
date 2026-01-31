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
from sqlmodel import select, update

from app.db import get_session, init_db
from app.supabasedb import get_online_db_table
from app.models import Activity, User, ActivityCategory
from app.utils import save_uploaded_file, format_event_date, delete_file
from app import settings


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config["DEBUG"] = settings.DEBUG
# app.config['ACTIVITY_IMG_FOLDER'] = settings.ACTIVITY_IMG_FOLDER
app.config['MAX_IMG_SIZE'] = settings.MAX_IMG_SIZE
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# os.makedirs(app.config['ACTIVITY_IMG_FOLDER'], exist_ok=True)
logger = structlog.get_logger(__name__)


@app.route("/")
def home():
    """Serve the home page.
    Fetch activities from db and social links.
    Returns:
        _renders index.html
    """
    now = datetime.now()
    activities = get_online_db_table(table_name="activities", order_by="event_date")

    leaders, volunteers = get_team_data()
    return render_template(
        "index.html", 
        social_links=get_social_links(), 
        activities=activities,
        leaders=leaders,
        volunteers=volunteers
    )


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("assets", filename)


@app.route("/healthz")
def health():
    return "OK", 200


@app.route("/coc/")
def coc():
    return redirect("https://github.com/aimlcommunitybd/public-docs/blob/main/legal/code-of-conduct.md")
    # return render_template("legal/code-of-conduct.html")


@app.route("/blog/")
def blog():
    blog_url = "https://aimlcommunitybd.hashnode.dev/"
    return redirect(blog_url)


def get_social_links():
    return {
        "linkedin": "https://www.linkedin.com/company/python-bangladesh/",
        "discord": "https://discord.gg/sR52eYRFba",
        "whatsapp": "https://whatsapp.com/channel/0029VbAf0s70rGiMzJfG4u2B", 
        "github": "https://github.com/pythonbangladesh",
    }



def get_team_data():
    leaders_data = [
        {
            "name": "Md. Taufiqul Haque Khan Tusar",
            "role": "NLP & Backend Engineer at LaLoka Labs, Tokyo, Japan | Community Admin",
            "image": "taufiq.jpg",
            "linkedin": ""
        },
        {
            "name": "Sajib Hossain",
            "role": "Lead Artificial Intelligence Engineer at TulipTech, Dhaka, Bangladesh",
            "image": "sajib.jpg",
            "linkedin": "https://www.linkedin.com/in/sajib-hossain-b189ba189/"
        },
        {
            "name": "Md Sultanul Islam Ovi",
            "role": "PhD Scholar at Dept. of CS, George Mason University, Virginia, USA",
            "image": "ovi.jpg",
            "linkedin": "https://www.linkedin.com/in/md-sultanul-islam-ovi/"
        },
        {
            "name": "Kazi Junaid Mahmud",
            "role": "Marketing Data Analyst, Talent Care Education Ltd, London, UK",
            "image": "junaid.jpg",
            "linkedin": "https://www.linkedin.com/in/junaid-mahmud/"
        },
        {
            "name": "Md. Abdur Rakib Mollah",
            "role": "Machine Learning Engineer, Euclido, Ontario, Canada",
            "image": "rakib.jpg",
            "linkedin": "https://www.linkedin.com/in/abdurrakibmollah/"
        },
        {
            "name": "Majidul Islam",
            "role": "AI Programmer at Sysnova Information Systems Ltd, Dhaka, Bangladesh",
            "image": "majid.jpg",
            "linkedin": "https://www.linkedin.com/in/majidulislammurad/"
        },
        {
            "name": "Mansura Naznine",
            "role": "Research Assistant, Qatar University, Doha, Qatar",
            "image": "mansura.jpg",
            "linkedin": "https://www.linkedin.com/in/mansura-naznine/"
        },
        {
            "name": "Md Abdullah Al Hasib",
            "role": "Artificial Intelligence Developer, Creative AI, Amman, Jordan",
            "image": "hasib.jpg",
            "linkedin": "https://www.linkedin.com/in/md-abdullah-al-hasib-874174194/"
        },
        {
            "name": "Md Hasnain Ali",
            "role": "Associate Software Engineer at Vivasoft Ltd, Dhaka, Bangladesh",
            "image": "hasnain.jpg",
            "linkedin": "https://www.linkedin.com/in/mdhasnainali/"
        }
    ]

    volunteers_data = [
        {
            "name": "Mehedi Hasan Shihab",
            "role": "ML Engineer (Intern) at Bondstain Technology Ltd., Bangladesh",
            "image": "shihab.jpg",
            "linkedin": "https://www.linkedin.com/in/shihab24/"
        },
        {
            "name": "An Naser Nabil",
            "role": "Freelance Content Writer at Prothom Alo and Earki",
            "image": "nabil.jpg",
            "linkedin": "https://www.linkedin.com/in/ann-naser-nabil/"
        },
        {
            "name": "Towfiqur Rashid",
            "role": "Undergradute Student at Dept. of Urban & Regional Planning, RUET, Bangladesh",
            "image": "towfik.jpg",
            "linkedin": "https://www.linkedin.com/in/towfiqur-rashid/"
        },
        {
            "name": "Sushomoy Nandi",
            "role": "Undergradute Student at Dept. of CSE, NITER, Bangladesh",
            "image": "sushmoy.jpg",
            "linkedin": "https://www.linkedin.com/in/sushmoy-nandi-737b41307/"
        }
    ]
    
    return leaders_data, volunteers_data



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


# ---------------------
# Admin Dashboard 
# ---------------------

@app.route("/admin")
@login_required
def admin_dashboard():
    with get_session() as session:
        activities = session.exec(
            select(Activity).order_by(Activity.event_date.desc())
        ).all()
    return render_template(
        "admin/dashboard.html", 
        user=current_user, 
        activities=activities,
    )

@app.route("/admin/activities/create", methods=["POST"])
@login_required
def create_activity():
    logger.info("[CREATE] New Activity")
    title=request.form.get('title', '').strip()
    category=ActivityCategory(request.form.get('category'))
    description=request.form.get('description', '').strip()
    image=request.files['image']
    youtube_link=request.form.get('youtube_link', '').strip()
    event_date=request.form.get('event_date')
    logger.info(
        "[Creating] Activity",
        title=title,
        category=category,
        description=description,
        image=image,
        youtube_link=youtube_link,
        event_date=event_date,
    )
    try:
        image_url = save_uploaded_file(
            file=image,
            filename=title,
        )
        event_date = format_event_date(
            event_date=event_date
        )
        new_activity = Activity(
            title=title,
            category=category,
            description=description,
            image_url=image_url,
            youtube_link=youtube_link,
            event_date=event_date,
        )
        with get_session() as session:
            session.add(new_activity)
            session.commit()
            flash(f"Activity poster uploaded into '{new_activity.image_url}'!", "success")
            flash(f"Activity '{new_activity.title}' added successfully!", "success")
            logger.info(
                "[CREATED] New activity", 
                id=new_activity.id,
                title=new_activity.title,
                category=new_activity.category,
                description=new_activity.description,
                image_url=new_activity.image_url,
                youtube_link=new_activity.youtube_link,
                event_date=new_activity.event_date,
            )

    except Exception as e:
        flash(f"Error adding activity: {str(e)}", "error")
        logger.error("Error creating activity", error=str(e))

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/activities/<int:activity_id>/update", methods=["POST"])
@login_required
def update_activity(activity_id):
    """Update existing activity"""
    title = request.form.get('title', '').strip()
    category = ActivityCategory(request.form.get('category'))
    description = request.form.get('description', '').strip()
    youtube_link = request.form.get('youtube_link', '').strip()
    event_date = request.form.get('event_date')
    image = request.files.get('image')
    image_filename = image.filename if image else None
    logger.info(
        "[Update] Activity", 
        activity_id=activity_id,
        title=title,
        category=category,
        description=description,
        youtube_link=youtube_link,
        event_date=event_date,
        image_filename=image_filename, 
    )
    try:
        with get_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                flash("Activity not found", "error")
                return redirect(url_for("admin_dashboard"))
            img_file = image
            if img_file:
                new_image_url = save_uploaded_file(img_file)
                delete_file(activity.image_url)
                activity.image_url = new_image_url
            
            if event_date:
                event_date = format_event_date(
                    event_date=event_date
                )
                activity.event_date = event_date
            activity.title = title
            activity.category = category
            activity.description =  description
            activity.youtube_link = youtube_link
            session.commit()
            flash(f"Activity '{activity.title}' updated successfully!", "success")
            logger.info(
                "[Updated] Activity", 
                activity_id=activity.id,
                title=activity.title,
                category=activity.category,
                description=activity.description,
                youtube_link=activity.youtube_link,
                event_date=activity.event_date,
                image_url=activity.image_url, 
            )
    except Exception as e:
        flash(f"Error updating activity: {str(e)}", "error")
        logger.error("Error updating activity", error=str(e))
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/activities/<int:activity_id>/delete", methods=["POST"])
@login_required
def delete_activity(activity_id):
    logger.info("[Delete] Activity", activity_id=activity_id)
    try:
        with get_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                flash("Activity not found", "error")
                return redirect(url_for("admin_dashboard"))
            activity_title = activity.title
            if activity.image_url:
                file_path = activity.image_url[1:]  # Remove leading slash
                if os.path.exists(file_path):
                    os.remove(file_path)
            session.delete(activity)
            session.commit()
            flash(f"Activity '{activity_title}' deleted successfully!", "success")
            logger.warning("[DELETED] Activity", activity_id=activity_id, title=activity_title)
    except Exception as e:
        flash(f"Error deleting activity: {str(e)}", "error")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    init_db()  # Initialize the database
    port = int(os.getenv("PORT", 10000))
    print(f"---------Starting app on port {port}-------------")
    app.run(debug=True, host="0.0.0.0", port=port)
