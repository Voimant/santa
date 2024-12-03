import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

with psycopg2.connect(user=os.getenv('DB_USER'),
                      password=os.getenv('DB_PASSWORD'),
                      port="5432",
                      database=os.getenv('DB_NAME')) as conn:
    def create_db():
        """
        Функция, создающая структуру БД (таблицы)
        :return: База данных создана
        """
        with conn.cursor() as cur:
            create_table = ("CREATE TABLE IF NOT EXISTS users ("
                            "role VARCHAR (255), "
                            "chat_id BIGINT PRIMARY KEY, "
                            "name VARCHAR (255), "
                            "second_name VARCHAR (255), "
                            "my_room int); "
                            "CREATE TABLE IF NOT EXISTS room ("
                            "id SERIAL PRIMARY KEY, "
                            "name_room VARCHAR (255), "
                            "pass_room VARCHAR (255),"
                            "status_game BOOLEAN);"
                            "CREATE TABLE IF NOT EXISTS room_members ("
                            "id SERIAL PRIMARY KEY, "
                            "room_id int REFERENCES room (id) ON DELETE CASCADE,"
                            "user_id int REFERENCES users (chat_id) ON DELETE CASCADE, "
                            "role VARCHAR (255), "
                             "gift TEXT);"
                            "CREATE TABLE IF NOT EXISTS couple ("
                            "id SERIAL PRIMARY KEY,"
                            "chat_id_santa BIGINT,"
                            "chat_id_gifts BIGINT,"
                            "room_id int REFERENCES room (id) ON DELETE CASCADE);"
                            "CREATE TABLE IF NOT EXISTS messages ("
                            "id SERIAL PRIMARY KEY, "
                            "message_id VARCHAR (255), "
                            "user_id int REFERENCES users (chat_id) ON DELETE CASCADE);")
            cur.execute(create_table)
            conn.commit()

create_db()