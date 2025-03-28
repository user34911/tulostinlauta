import db
def add_post(title, model_year, grade, review, user_id):
    sql = """INSERT INTO posts (title, model_year, grade, review, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, model_year, grade, review, user_id])