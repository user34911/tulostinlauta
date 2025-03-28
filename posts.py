import db
def add_post(title, model_year, grade, review, user_id):
    sql = """INSERT INTO posts (title, model_year, grade, review, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, model_year, grade, review, user_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT posts.title,
                    posts.id,
                    posts.model_year,
                    posts.grade,
                    posts.review,
                    users.username,
                    users.id user_id
            FROM posts, users WHERE posts.user_id = users.id AND posts.id = ?"""
    return db.query(sql, [post_id])[0]

def update_post(post_id, title, model_year, grade, review):
    sql = """UPDATE posts SET title = ?,
                              model_year = ?,
                              grade = ?,
                              review = ?
            WHERE id = ?"""
    db.execute(sql, [title, model_year, grade, review, post_id])

def delete_post(post_id):
    sql = "DELETE FROM posts WHERE id = ?"
    db.execute(sql, [post_id])

def find_posts(query):
    sql = """SELECT id, title
             FROM posts
             WHERE review LIKE ?
             OR title LIKE ?
             OR model_year LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])