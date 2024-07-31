import psycopg2
from faker import Faker


def fill_up_db(cur, conn):
    fake = Faker()

    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email)
        )

    statuses = ["new", "in progress", "completed"]
    for status in statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s)", (status,))

    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    for _ in range(20):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = fake.random_element(status_ids)
        user_id = fake.random_element(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id),
        )

    conn.commit()


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="neoversity",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
    )

    cur = conn.cursor()

    fill_up_db(cur, conn)
    cur.close()
    conn.close()
