import db
def add_post(title, model_year, grade, review, user_id, classes, image):
    sql = """INSERT INTO posts (title, model_year, grade, review, user_id, image)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, model_year, grade, review, user_id, image])

    post_id = db.last_insert_id()

    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [post_id, title, value])

    return post_id

def add_comment(post_id, user_id, comment):
    sql = "INSERT INTO comments (user_id, post_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, post_id, comment])

def get_comments(post_id):
    sql = """SELECT c.comment, u.id user_id, u.username
             FROM comments c, users u
             WHERE c.post_id = ? AND c.user_id = u.id
             ORDER BY c.id ASC"""
    return db.query(sql, [post_id])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def get_classes(post_id):
    sql = "SELECT title, value FROM post_classes WHERE post_id = ?"
    return db.query(sql, [post_id])

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
    result = db.query(sql, [post_id])
    return result[0] if result else None

def get_image(post_id):
    sql = "SELECT image FROM posts WHERE id = ?"
    result = db.query(sql, [post_id])
    if not result:
        return None

    image = result[0][0]
    if not image:
        return None
    return image

def update_post(post_id, title, model_year, grade, review, classes):
    sql = """UPDATE posts SET title = ?,
                              model_year = ?,
                              grade = ?,
                              review = ?
             WHERE id = ?"""
    db.execute(sql, [title, model_year, grade, review, post_id])

    sql = "DELETE FROM post_classes WHERE post_id = ?"
    db.execute(sql, [post_id])

    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [post_id, title, value])

def update_image(post_id, image):
    sql = "UPDATE posts SET image = ? WHERE id = ?"
    db.execute(sql, [image, post_id])

def delete_post(post_id):
    sql = "DELETE FROM post_classes WHERE post_id = ?"
    db.execute(sql, [post_id])
    sql = "DELETE FROM posts WHERE id = ?"
    db.execute(sql, [post_id])

def find_posts(query):
    sql = """SELECT id, title
             FROM posts
             WHERE review LIKE ?
             OR title LIKE ?
             OR model_year LIKE ?
             ORDER BY id DESC"""
    haku = "%" + query + "%"
    return db.query(sql, [haku, haku, haku])