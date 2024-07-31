import psycopg2
from psycopg2 import sql
from faker import Faker


# Функція для підключення до бази даних
def connect_to_db():
    return psycopg2.connect(
        dbname="neoversity",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
    )


# Функція для перевірки існування користувача
def user_exists(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists


# Додати нового користувача, якщо він не існує
def add_user_if_not_exists(user_id):
    if not user_exists(user_id):
        conn = connect_to_db()
        cur = conn.cursor()
        fake = Faker()
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (id, fullname, email) VALUES (%s, %s, %s)",
            (user_id, fullname, email),
        )
        conn.commit()
        cur.close()
        conn.close()


# Отримати всі завдання певного користувача
def get_tasks_by_user(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


# Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM tasks 
        WHERE status_id = (SELECT id FROM status WHERE name = %s)
    """,
        (status_name,),
    )
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


# Оновити статус конкретного завдання
def update_task_status(task_id, new_status_name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE tasks 
        SET status_id = (SELECT id FROM status WHERE name = %s) 
        WHERE id = %s
    """,
        (new_status_name, task_id),
    )
    conn.commit()
    cur.close()
    conn.close()


# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM users 
        WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
    """
    )
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# Додати нове завдання для конкретного користувача
def add_task(title, description, status_name, user_id):
    add_user_if_not_exists(user_id)
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tasks (title, description, status_id, user_id) 
        VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
    """,
        (title, description, status_name, user_id),
    )
    conn.commit()
    cur.close()
    conn.close()


# Отримати всі завдання, які ще не завершено
def get_uncompleted_tasks():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM tasks 
        WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """
    )
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


# Видалити конкретне завдання
def delete_task(task_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()


# Знайти користувачів з певною електронною поштою
def find_users_by_email(email_pattern):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))
    conn.commit()
    cur.close()
    conn.close()


# Отримати кількість завдань для кожного статусу
def get_task_counts_by_status():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT status.name, COUNT(tasks.id) 
        FROM tasks 
        JOIN status ON tasks.status_id = status.id 
        GROUP BY status.name
    """
    )
    counts = cur.fetchall()
    cur.close()
    conn.close()
    return counts


# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_user_email_domain(email_domain):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT tasks.* 
        FROM tasks 
        JOIN users ON tasks.user_id = users.id 
        WHERE users.email LIKE %s
    """,
        (email_domain,),
    )
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE description IS NULL")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks_in_progress():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT users.fullname, tasks.title 
        FROM tasks 
        JOIN users ON tasks.user_id = users.id 
        JOIN status ON tasks.status_id = status.id 
        WHERE status.name = 'in progress'
    """
    )
    user_tasks = cur.fetchall()
    cur.close()
    conn.close()
    return user_tasks


# Отримати користувачів та кількість їхніх завдань
def get_users_and_task_counts():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT users.fullname, COUNT(tasks.id) 
        FROM users 
        LEFT JOIN tasks ON users.id = tasks.user_id 
        GROUP BY users.fullname
    """
    )
    user_task_counts = cur.fetchall()
    cur.close()
    conn.close()
    return user_task_counts


if __name__ == "__main__":
    print(get_tasks_by_user(1))
    print(get_tasks_by_status("new"))
    update_task_status(1, "completed")
    print(get_users_without_tasks())
    add_task("new task", "new task description", "new", 1)
    print(get_uncompleted_tasks())
    delete_task(1)
    print(find_users_by_email("%@gmail.com"))
    update_user_name(1, "new name")
    print(get_task_counts_by_status())
    print(get_tasks_by_user_email_domain("%@gmail.com"))
    print(get_tasks_without_description())
    print(get_users_and_tasks_in_progress())
    print(get_users_and_task_counts())
