import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image, join_date, about_me
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_posts(user_id):
    sql = "SELECT id, title, model_year, grade FROM posts WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    time = date.today()
    sql = "INSERT INTO users (username, password_hash, join_date) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, time])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    return db.query(sql, [user_id])[0][0]

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def update_aboutme(user_id, content):
    sql = "UPDATE users SET about_me = ? WHERE id = ?"
    db.execute(sql, [content, user_id])

def get_aboutme(user_id):
    sql = "SELECT about_me FROM users WHERE id = ?"
    return db.query(sql, [user_id])[0][0]