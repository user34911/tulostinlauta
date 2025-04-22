import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, make_response, g, flash
import math, time
import config
import posts, users
import markupsafe
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    post_count = posts.post_count()
    page_count = math.ceil(post_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_posts = posts.get_posts(page, page_size)
    return render_template("index.html", posts=all_posts, page=page, page_count=page_count)

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

@app.route("/find_class/<value>")
def find_class(value):
    results = posts.find_posts(value)
    return render_template("find_post.html", query=value, results=results)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    classes = posts.get_classes(post_id)
    comments = posts.get_comments(post_id)
    image = posts.get_image(post_id)
    return render_template("show_post.html", post=post, classes=classes, comments=comments, image=image)

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
    return render_template("new_post.html", classes=classes, filled={})

@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    model_year = request.form["model_year"]
    if not model_year or int(model_year) < 0 or len(model_year) > 4:
        abort(403)
    grade = request.form["grade"]
    if not grade:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)

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

    file = request.files["image"]
    if not file.filename.endswith(".jpg") and file:
        flash("VIRHE: Väärä tiedostomuoto")
        filled = {"title": title, "model_year": model_year, "grade": grade, "review": review}
        for entry in classes:
            filled[entry[0]] = entry[1]
        return render_template("new_post.html", classes=all_classes, filled=filled)
    image = file.read()
    if len(image) > 1000 * 1024:
        flash("VIRHE: Liian suuri kuva")
        filled = {"title": title, "model_year": model_year, "grade": grade, "review": review}
        for entry in classes:
            filled[entry[0]] = entry[1]
        return render_template("new_post.html", classes=all_classes, filled=filled)


    post_id = posts.add_post(title, model_year, grade, review, user_id, classes, image)

    return redirect("/post/" + str(post_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

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

    image = posts.get_image(post_id)

    return render_template("edit_post.html", post=post, classes=classes, all_classes=all_classes, image=image)

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()
    check_csrf()
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

    file = request.files["image"]
    if not file.filename.endswith(".jpg") and file:
        flash("VIRHE: Väärä tiedostomuoto")
        image = posts.get_image(post_id)
        return render_template("edit_post.html", post=post, classes=classes, all_classes=all_classes, image=image)
    image = file.read()
    if len(image) > 1000 * 1024:
        flash("VIRHE: Liian suuri kuva")
        image = posts.get_image(post_id)
        return render_template("edit_post.html", post=post, classes=classes, all_classes=all_classes, image=image)
    if not image:
        image = posts.get_image(post_id)

    posts.update_post(post_id, title, model_year, grade, review, classes, image)

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
        check_csrf()
        if "delete" in request.form:
            posts.delete_post(post_id)
            return redirect("/")
        else:
            return redirect("/post/" + str(post_id))

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if len(username) > 16:
        abort(403)

    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: Salasanat eivät täsmää")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    try:
        users.create_user(username, password1)
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("VIRHE: Käyttäjänimi varattu")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

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
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: Väärä tiedostomuoto")
            return redirect("/add_image")

        image = file.read()
        if len(image) > 1000 * 1024:
            flash("VIRHE: Liian suuri kuva")
            return redirect("/add_image")

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

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response