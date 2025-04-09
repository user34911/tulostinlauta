import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_posts(user_id):
    sql = "SELECT id, title FROM posts WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])
