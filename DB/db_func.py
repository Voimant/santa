

from DB.DB import conn
import psycopg2.extras



def check_out_pass(password):
    with conn.cursor() as cur:
        select_query = "select pass_room from room where pass_room = %s"
        cur.execute(select_query, (password, ))
        ret = cur.fetchone()
        return ret

def db_checkout_gifts(chat_id):
    with conn.cursor() as cur:
        my_room = db_kakashka(chat_id)
        select_query = "select status_game from room where id = %s"
        cur.execute(select_query, (my_room[0], ))
        ret = cur.fetchone()
        return ret



def db_true_result(chat_id):
    with conn.cursor() as cur:
        my_room = db_kakashka(chat_id)
        update_query = "UPDATE room set status_game = true where id = %s"
        cur.execute(update_query, (my_room[0], ))
        conn.commit()


def my_gift_friend(chat_id):
    with conn.cursor() as cur:
        select_query = "SELECT my_room from users where chat_id = %s"
        cur.execute(select_query, (chat_id,))
        ret = cur.fetchone()
        select_query_2 = "SELECT chat_id_gifts from couple where chat_id_santa = %s and room_id = %s"
        cur.execute(select_query_2, (chat_id, ret[0]))
        chat_id_friend = cur.fetchone()
        select_query_3 = "SELECT gift from room_members where room_id = %s and user_id = %s"
        cur.execute(select_query_3, (ret[0], chat_id_friend[0]))
        gift = cur.fetchone()
        select_query_4 = "Select name from users where chat_id = %s"
        cur.execute(select_query_4, (chat_id_friend[0], ))
        name_friend = cur.fetchone()
        select_query_5 = "select name_room from room where id = %s"
        cur.execute(select_query_5,(ret[0], ))
        name_room = cur.fetchone()
        return [name_friend[0], gift[0], name_room[0]]




def reslut_game(chat_id_santa, chat_id_gifts, room_id):
    with conn.cursor() as cur:
        insert_query = "insert into couple (chat_id_santa, chat_id_gifts, room_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
        cur.execute(insert_query, (chat_id_santa, chat_id_gifts, room_id))
        conn.commit()


def my_role(chat_id):
    with conn.cursor() as cur:
        select_query = "select my_room from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        select_query_2 = "select role from room_members where user_id = %s AND room_id = %s"
        cur.execute(select_query_2, (chat_id, ret[0]))
        ret = cur.fetchone()
        return ret

def my_name(chat_id):
    with conn.cursor() as cur:
        select_query = "SELECT name from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        return ret

def db_kakashka(chat_id):
    with conn.cursor() as cur:
        select_query = "SELECT my_room from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        return ret

def db_kaka(com_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        select_query = "select gift, user_id from room_members where room_id = %s"
        cur.execute(select_query, (com_id,))
        res = cur.fetchall()
        res_list = [dict(row) for row in res]
        return res_list

# print(db_kaka(db_kakashka(423947942)[0]))

def db_gifts(chat_id, text):
    with conn.cursor() as cur:
        select_query = "SELECT my_room from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        print(text , chat_id, ret[0])
        update_query = "UPDATE room_members set gift = %s where user_id = %s AND room_id = %s"
        cur.execute(update_query, (text, chat_id, ret[0]))
        conn.commit()



def db_gifts_check(chat_id):
    with conn.cursor() as cur:
        select_query = "SELECT my_room from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        select_query_2 = "SELECT gift from room_members where user_id = %s AND room_id = %s"
        cur.execute(select_query_2, (chat_id, ret[0]))
        ret_1 = cur.fetchone()
        return ret_1

def db_start(chat_id):
    with conn.cursor() as cur:
        select_query = 'select my_room from users where chat_id = %s'
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        print(ret)
        if ret is not None:
            return True
        else:
            return False




def db_in_group(chat_id):
    with conn.cursor() as cur:
        select_query = 'select my_room from users where chat_id = %s'
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        if ret is not None:
             select_query_2 = "select name_room from room where id = %s"
             cur.execute(select_query_2, (ret[0],))
             ret_1 = cur.fetchone()
             return f'Сейчас вы в комнате {ret_1[0]}'
        else:
            return f'Вы еще не вошли в комнату с тайным сантой'

def db_in_group_id(chat_id):
    with conn.cursor() as cur:
        select_query = 'select my_room from users where chat_id = %s'
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        return ret






def db_join_call_room(chat_id, name_room):
    with conn.cursor() as cur:
        select_query = "select id from room where name_room = %s"
        cur.execute(select_query, (name_room,))
        ret = cur.fetchone()
        if ret is not None or ret != ['']:
            update_query = "UPDATE users set my_room = %s where chat_id = %s"
            cur.execute(update_query, (ret[0], chat_id))
            conn.commit()
            select_users = "select user_id from room_members where user_id = %s"
            cur.execute(select_users, (chat_id, ))
            ret_users = cur.fetchone()
            if ret_users is None:
                insert_query = "INSERT INTO room_members (room_id, user_id, role) VALUES (%s, %s, 'member') ON CONFLICT DO NOTHING"
                cur.execute(insert_query, (ret[0], chat_id))
                select_query_2 = "select name_room from room where id = %s"
                print(ret)
                cur.execute(select_query_2, (ret[0], ))
                ret_name = cur.fetchone()
                conn.commit()









def my_party_list(chat_id):
    with conn.cursor() as cur:
        select_query = "select room_id from room_members where user_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchall()
        if ret is not None:
            list_group = []
            res_list = []
            for one in ret:
                for ind in one:
                    res_list.append(ind)

            for group in res_list:
                select_query = "SELECT name_room from room where id = %s"
                cur.execute(select_query, (group, ))
                ret_name = cur.fetchone()
                list_group.append(ret_name[0])
            return list_group
        else:
            return False

#print(my_party_list(423947942))

def db_join_room(chat_id, pass_room):
    with conn.cursor() as cur:
        select_query = "select id from room where pass_room = %s"
        cur.execute(select_query, (pass_room,))
        ret = cur.fetchone()
        print(ret)
        if ret is not None:
            update_query = "UPDATE users set my_room = %s where chat_id = %s"
            cur.execute(update_query, (ret[0], chat_id))
            conn.commit()
            select_users = "select user_id from room_members where user_id = %s and room_id = %s"
            cur.execute(select_users, (chat_id, ret[0]))
            ret_users = cur.fetchone()
            print(ret_users, 'ретузер')
            if ret_users is None:
                insert_query = "INSERT INTO room_members (room_id, user_id, role) VALUES (%s, %s, 'member') ON CONFLICT DO NOTHING"
                cur.execute(insert_query, (ret[0], chat_id))
                select_query_2 = "select name_room from room where id = %s"
                print(ret, 'последний принт')
                cur.execute(select_query_2, (ret[0], ))
                ret_name = cur.fetchone()
                conn.commit()
                return ret_name
            else:
                print(False)
                return False


def db_add_new_user(chat_id):
    with conn.cursor() as cur:
        insert_query = "INSERT INTO users (chat_id) VALUES (%s) ON CONFLICT DO NOTHING"
        cur.execute(insert_query, (chat_id, ))
        conn.commit()


def db_new_room(chat_id, name, password):
    with conn.cursor() as cur:
        select_query = "SELECT name_room from room where name_room = %s"
        cur.execute(select_query, (name, ))
        rett = cur.fetchone()
        print(rett)
        if rett is None or rett == [""]:
            insert_query = "INSERT into room (name_room, pass_room) VALUES (%s, %s) RETURNING id"
            cur.execute(insert_query, (name, password))
            ret = cur.fetchone()

            insert_query_2 = "INSERT INTO room_members (room_id, user_id, role) VALUES (%s, %s, 'admin') ON CONFLICT DO NOTHING"
            cur.execute(insert_query_2, (ret[0], chat_id))
            update_query = "UPDATE users set my_room = %s where chat_id = %s"
            cur.execute(update_query, (ret[0], chat_id))
            conn.commit()
            return True
        else:
            return False

#print(db_new_room(423947942, 'имя_тест', 'Пароль_тест'))



def db_add_name(chat_id, name):
    with conn.cursor() as cur:
        update_query = "UPDATE users set name = %s where chat_id = %s"
        cur.execute(update_query, (name, chat_id))
        conn.commit()

def db_check_name_second_name(chat_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        select_query = "SELECT name, second_name from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        res = cur.fetchall()
        res_list = [dict(row) for row in res]
        return res_list

# print(db_check_name_second_name(423947942))






"""Удаление сообщений"""
def db_message_id(chat_id):
    with conn.cursor() as cur:
        select_query = "SELECT message_id from messages where user_id = (SELECT chat_id from users where chat_id = %s)"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchall()
        ret_list = []
        for x in ret:
            for one in x:
                ret_list.append(one)

        return ret_list

def db_clear_message_id(chat_id):
    with conn.cursor() as cur:
        delete_query = "DELETE from messages where user_id = (SELECT chat_id from users where chat_id = %s)"
        cur.execute(delete_query, (chat_id, ))
        conn.commit()

def db_add_message_id(chat_id, message_id):
    with conn.cursor() as cur:
        select_query = "select chat_id from users where chat_id = %s"
        cur.execute(select_query, (chat_id, ))
        ret = cur.fetchone()
        insert_query = "INSERT INTO messages (user_id, message_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        cur.execute(insert_query,(ret[0], message_id))
        conn.commit()