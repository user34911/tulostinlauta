import db
def add_post(title, model_year, grade, review, user_id):
    sql = """INSERT INTO posts (title, model_year, grade, review, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, model_year, grade, review, user_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT posts.title, posts.model_year, posts.grade, posts.review, users.username
            FROM posts, users WHERE posts.user_id = users.id AND posts.id = ?"""
    return db.query(sql, [post_id])[0]