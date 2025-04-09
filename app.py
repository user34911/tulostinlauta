import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
import db
import config
import posts, users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts=all_posts)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    posts = users.get_posts(user_id)
    return render_template("show_user.html", user=user, posts=posts)

@app.route("/find_post")
def find_post():
    query = request.args.get("query")
    if query:
        results = posts.find_posts(query)
    else:
        query = ""
        results = []
    return render_template("find_post.html", query=query, results=results)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    return render_template("show_post.html", post=post)

@app.route("/new_post")
def new_post():
    require_login()
    return render_template("new_post.html")

@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    model_year = request.form["model_year"]
    if not model_year or model_year < 0:
        abort(403)
    grade = request.form["grade"]
    if not grade:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)
    user_id = session["user_id"]

    posts.add_post(title, model_year, grade, review, user_id)

    return redirect("/")

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_post.html", post=post)

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()
    post_id = request.form["post_id"]

    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    model_year = request.form["model_year"]
    grade = request.form["grade"]
    review = request.form["review"]

    posts.update_post(post_id, title, model_year, grade, review)

    return redirect("/post/" + str(post_id))

@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_post.html", post=post)

    if request.method == "POST":
        if "delete" in request.form:
            posts.delete_post(post_id)
            return redirect("/")
        else:
            return redirect("/post/" + str(post_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")