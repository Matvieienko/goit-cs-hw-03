import psycopg2
from faker import Faker
import random

# Функція для підключення до бази даних
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="qwerty",
            host="localhost"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None

# Функція для додавання випадкових користувачів
def add_random_users(cursor, fake, num_users=20):
    users = []
    try:
        for _ in range(num_users):
            fullname = fake.name()
            email = fake.unique.email()
            cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
            users.append(cursor.fetchone()[0])
        return users
    except psycopg2.Error as e:
        print(f"Помилка при додаванні користувачів: {e}")
        return []

# Функція для отримання ID статусів
def get_status_ids(cursor):
    try:
        cursor.execute("SELECT id FROM status;")
        return [row[0] for row in cursor.fetchall()]
    except psycopg2.Error as e:
        print(f"Помилка при отриманні статусів: {e}")
        return []

# Функція для додавання випадкових завдань
def add_random_tasks(cursor, fake, users, status_ids, num_tasks=50):
    try:
        for _ in range(num_tasks):
            title = fake.sentence(nb_words=6)
            description = fake.text()
            status_id = random.choice(status_ids)
            user_id = random.choice(users)
            cursor.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
                (title, description, status_id, user_id)
            )
    except psycopg2.Error as e:
        print(f"Помилка при додаванні завдань: {e}")

# Основна логіка скрипта
def main():
    fake = Faker()

    # Підключення до бази даних
    conn = connect_to_db()
    if not conn:
        return  # Виходимо, якщо підключення не вдалося

    cursor = conn.cursor()

    try:
        # Додавання випадкових користувачів
        users = add_random_users(cursor, fake)
        if not users:
            raise Exception("Не вдалося додати користувачів")

        # Отримання ID статусів
        status_ids = get_status_ids(cursor)
        if not status_ids:
            raise Exception("Не вдалося отримати статуси")

        # Додавання випадкових завдань
        add_random_tasks(cursor, fake, users, status_ids)

        # Збереження змін
        conn.commit()
        print("Таблиці успішно заповнені випадковими даними!")
    except Exception as e:
        print(f"Помилка під час виконання скрипта: {e}")
        conn.rollback()  # Відкат змін у разі помилки
    finally:
        # Закриття курсора та з'єднання
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Запуск основної функції
if __name__ == "__main__":
    main()