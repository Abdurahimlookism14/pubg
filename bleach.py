import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    area REAL DEFAULT 0,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries (id)
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities (id)
);

INSERT INTO countries (title) VALUES ('Кыргызстан'), ('Германия'), ('Китай');
INSERT INTO cities (title, area, country_id) VALUES
    ('Бишкек', 127.0, 1), ('Ош', 182.0, 1),
    ('Берлин', 891.8, 2), ('Мюнхен', 310.7, 2),
    ('Пекин', 16808.0, 3), ('Шанхай', 6340.5, 3), ('Гуанчжоу', 3843.4, 3);
INSERT INTO students (first_name, last_name, city_id) VALUES
    ('Алексей', 'Иванов', 1), ('Мария', 'Петрова', 1),
    ('Иван', 'Сидоров', 2), ('Ольга', 'Кузнецова', 2),
    ('Фридрих', 'Шульц', 3), ('Анна', 'Мюллер', 3),
    ('Дун', 'Ли', 5), ('Сяо', 'Чжан', 5),
    ('Мэй', 'Чжоу', 6), ('Цзян', 'Хуан', 6),
    ('Лю', 'Чен', 7), ('Мин', 'Ли', 7),
    ('Катарина', 'Шмит', 4), ('Ганс', 'Фишер', 4),
    ('Айгерим', 'Султанова', 2);
''')


def show_cities_and_students():
    cursor.execute("SELECT id, title FROM cities")
    cities = cursor.fetchall()
    print("Вы можете отобразить список учеников по ID города, для выхода введите 0:")
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    city_id = int(input("Введите ID города: "))
    if city_id == 0:
        return False
    cursor.execute('''
        SELECT students.first_name, students.last_name, countries.title,
        cities.title, cities.area
        FROM students
        JOIN cities ON students.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE cities.id = ?
    ''', (city_id,))
    students = cursor.fetchall()
    for student in students:
        print(
            f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: "
            f"{student[2]}, Город: {student[3]}, Площадь: {student[4]}")
    return True


while show_cities_and_students():
    pass

conn.commit()
conn.close()