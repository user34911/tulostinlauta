import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, make_response
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
    classes = posts.get_classes(post_id)
    comments = posts.get_comments(post_id)
    return render_template("show_post.html", post=post, classes=classes, comments=comments)

@app.route("/post_image/<int:post_id>")
def show_post_image(post_id):
    image = posts.get_image(post_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/new_post")
def new_post():
    require_login()
    classes = posts.get_all_classes()
    return render_template("new_post.html", classes=classes)

@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    model_year = request.form["model_year"]
    if not model_year or int(model_year) < 0:
        abort(403)
    grade = request.form["grade"]
    if not grade:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".jpg") and file:
        return "VIRHE: väärä tiedostomuoto"
    image = file.read()
    if len(image) > 1000 * 1024:
        return "VIRHE: liian suuri kuva"
    
    user_id = session["user_id"]

    all_classes = posts.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes:
                abort(403)
            if entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    post_id = posts.add_post(title, model_year, grade, review, user_id, classes, image)

    return redirect("/post/" + str(post_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()

    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        abort(403)
    post_id = request.form["post_id"]
    post = posts.get_post(post_id)
    if not post:
        abort(403)
    user_id = session["user_id"]

    posts.add_comment(post_id, user_id, comment)

    return redirect("/post/" + str(post_id))

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    all_classes = posts.get_all_classes()
    classes = {}
    for class_entry in all_classes:
        classes[class_entry] = ""
    for entry in posts.get_classes(post_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_post.html", post=post, classes=classes, all_classes=all_classes)

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
    if not title or len(title) > 50:
        abort(403)
    model_year = request.form["model_year"]
    if not model_year or int(model_year) < 0:
        abort(403)
    grade = request.form["grade"]
    if not grade:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)

    all_classes = posts.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes:
                abort(403)
            if entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    posts.update_post(post_id, title, model_year, grade, review, classes)

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

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")

    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 1000 * 1024:
            return "VIRHE: liian suuri kuva"

        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response
