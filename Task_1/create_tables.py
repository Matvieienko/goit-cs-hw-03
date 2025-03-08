import psycopg2

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

# Основна логіка скрипта
def main():
    # Підключення до бази даних
    conn = connect_to_db()
    if not conn:
        return  # Виходимо, якщо підключення не вдалося

    cursor = conn.cursor()

    try:
        # Створення таблиці users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """)

        # Створення таблиці status
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """)

        # Створення таблиці tasks
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # Додавання статусів, якщо вони ще не існують
        cursor.execute("""
        INSERT INTO status (name) 
        VALUES ('new'), ('in progress'), ('completed')
        ON CONFLICT (name) DO NOTHING;
        """)

        # Збереження змін
        conn.commit()
        print("Таблиці створені успішно!")
    except psycopg2.Error as e:
        print(f"Помилка під час створення таблиць: {e}")
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