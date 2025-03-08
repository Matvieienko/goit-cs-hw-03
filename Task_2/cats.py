from pymongo import MongoClient

# Підключення до MongoDB Atlas
MONGO_URI = "mongodb+srv://matvieienko:qwerty12345@cluster0.ydd3j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_to_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client["cats_database"]  # Назва бази даних
        collection = db["cats"]       # Назва колекції
        print("Підключено до MongoDB Atlas!")
        return collection
    except Exception as e:
        print(f"Помилка підключення до MongoDB Atlas: {e}")
        return None

# Функція для створення нового документа (кота)
def create_cat(collection, name, age, features):
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Кіт {name} доданий з ID: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні кота: {e}")

# Функція для виведення всіх записів
def read_all_cats(collection):
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка при читанні даних: {e}")

# Функція для пошуку кота за ім'ям
def find_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Помилка при пошуку кота: {e}")

# Функція для оновлення віку кота за ім'ям
def update_cat_age(collection, name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота {name} оновлено до {new_age}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")

# Функція для додавання нової характеристики до кота за ім'ям
def add_cat_feature(collection, name, new_feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.modified_count > 0:
            print(f"Додано нову характеристику для кота {name}: {new_feature}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")

# Функція для видалення кота за ім'ям
def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Прощавай {name}. Запис про кота {name} видалений.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Помилка при видаленні запису: {e}")

# Функція для видалення всіх записів
def delete_all_cats(collection):
    try:
        result = collection.delete_many({})
        print(f"Прощавайте всі. Видалено {result.deleted_count} записи.")
    except Exception as e:
        print(f"Помилка при видаленні всіх записів: {e}")

# Основна логіка скрипта
def main():
    collection = connect_to_mongodb()
    if collection is None:  # Виправлено: порівнюємо з None
        return

    # Приклад використання функцій
    create_cat(collection, "barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat(collection, "murzik", 5, ["любить спати", "сірий"])
    create_cat(collection, "ryzhik", 2, ["грається з м'ячем", "любить гуляти"])
    create_cat(collection, "pushok", 4, ["пухнастий", "дружелюбний"])

    print("\n Читання (Read)")
    print("\n Виведення всіх записів із колекції")
    read_all_cats(collection)

    print("\n Пошук кота barsik")
    find_cat_by_name(collection, "barsik")

    print("\n Оновлення (Update)")
    print("\n Оновлення віку кота barsik:")
    update_cat_age(collection, "barsik", 4)

    print("\n Додавання нової характеристики коту barsik:")
    add_cat_feature(collection, "barsik", "любить молоко")
    
    print("\n Оновлення віку кота ryzhik:")
    update_cat_age(collection, "ryzhik", 3)
    
    print("\n Додавання нової характеристики коту ryzhik:")
    add_cat_feature(collection, "ryzhik", "любить гратися з дітьми")

    print("\n Після оновлення:")
    find_cat_by_name(collection, "barsik")
    find_cat_by_name(collection, "ryzhik")

    print("\n Видалення (Delete)")
    print("\n Видалення кота murzik:")
    delete_cat_by_name(collection, "murzik")

    print("\n Виведення всіх записів із колекції:")
    read_all_cats(collection)

    print("\n Видалення всіх записів із колекції:")
    delete_all_cats(collection)

    print("\n Виведення всіх записів із колекції:")
    read_all_cats(collection)

if __name__ == "__main__":
    main()