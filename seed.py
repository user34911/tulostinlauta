import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM posts")
db.execute("DELETE FROM comments")

user_count = 1000
post_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

classes1 = ["USA", "Japani", "Kiina", "Muu"]
classes2 = ["Laser", "LED", "Mustesuihku", "3D", "Matriisi", "Lämpö", "Kiinteä muste", "Piirturi", "Tarra", "Muu"]

for i in range(1, post_count + 1):
    sql = """INSERT INTO posts (title, model_year, grade, review, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, ["tulostin" + str(i), random.randint(1, 2030), random.randint(1, 5), "kuvaus" + str(i), random.randint(1, user_count)])

    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    db.execute(sql, [str(i), "Valmistusmaa", random.choice(classes1)])
    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    db.execute(sql, [str(i), "Valmistusmaa", random.choice(classes2)])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    post_id = random.randint(1, post_count)
    db.execute("""INSERT INTO comments (comment, user_id, post_id)
                  VALUES (?, ?, ?)""",
               ["message" + str(i), user_id, post_id])

db.commit()
db.close()
