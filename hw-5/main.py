import psycopg2

def create_db(conn):
    with conn.cursor() as cur:

        cur.execute("""
        DROP TABLE phone;
        DROP TABLE users
        ;
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id serial primary key,
        first_name varchar(50) not null,
        last_name varchar(50),
        email varchar(100) not null unique
        )
        ;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        id serial primary key,
        phone_number varchar(30) not null unique,
        user_id integer not null references users(id) on delete cascade
        )
        ;
        """)
        conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    request_str = """
        INSERT INTO users (first_name, last_name, email)
        VALUES ('{first_name}', '{last_name}', '{email}') returning id
        ;
        """.format(first_name = first_name, last_name = last_name, email = email)
    with conn.cursor() as cur:        
        cur.execute(request_str)
        id = cur.fetchone()
        print('Добавлен пользователь: ', id[0])
    if phones:
        add_phone(conn, id[0], phones)

def check_client_id(conn, client_id):
    """Функция проверяет, существует ли пользователь с таким id"""
    requers_str = """
    SELECT id FROM users
    WHERE id = {client_id}
    ;
    """.format(client_id = client_id)

    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchone()
        return rezult[0] if rezult else None

def add_phone(conn, client_id, phone):
    """Функция добавляет телефон для указанного пользователя"""
    client = check_client_id(conn, client_id)
    if client:
        requers_str = """
        INSERT INTO phone (phone_number, user_id)
        VALUES ('{num}', '{id}') RETURNING phone_number, user_id
        ;
        """.format(num = phone, id = client_id)
        
        with conn.cursor() as cur:
            cur.execute(requers_str)
            rezult = cur.fetchone()
            print('Добавлен телефон : ', rezult[0], ', пользователю id: ', client_id)

def find_phone_id(conn, client_id, phone):
    """Функция ищет id телефона и его возвращает"""
    requers_str = """
    SELECT id FROM phone
    WHERE phone_number = {phone} and user_id = {id}
    ;
    """.format(phone = f"'{phone}'", id = client_id)
    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchone()
        return rezult[0] if rezult else None

def update_phone(conn, client_id, phone_id, phone):
    """Функция обновляет телефон у указанного пользователя"""
    requers_str = """
    UPDATE phone SET phone_number = {phone}
    WHERE id = {phone_id} and user_id = {client_id} RETURNING id, phone_number, user_id
    ;
    """.format(phone = f"'{phone}'", phone_id = phone_id, client_id = client_id)

    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchone()
        print('Обновлен телефон: ', rezult)

def update_client(conn, client_id, str_args):
    """Функция обновляет данные в БД у указанного пользователя
    str_args - готовая строка для установки в SET
    """
    requers_str = """
    UPDATE users SET {args}
    WHERE id = {client_id} RETURNING *
    ;
    """.format(args = str_args, client_id = client_id)
    
    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchone()
        print('Обновлены данные пользователя: ', rezult)

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    '''В параметр phones передается кортеж со старым и новым телефонами'''
    if phones:
        phone_id = find_phone_id(conn, client_id, phones[0])
        if phone_id:
            update_phone(conn, client_id, phone_id, phones[1])
        else:
            print('Указанный телефон не принадлежит клиенту')
    
    list_args = []
    if first_name:
        list_args.append(f"first_name = '{first_name}'")
    if last_name:
        list_args.append(f"last_name = '{last_name}'")
    if email:
        list_args.append(f"email = '{email}'")
    if len(list_args):
        str_args = ', '.join(list_args)
        update_client(conn, client_id, str_args)


def delete_phone(conn, client_id, phone):
    requers_str = """
    DELETE FROM phone 
    WHERE phone_number = {phone} and user_id = {client_id} RETURNING *
    ;
    """.format(phone = f"'{phone}'", client_id = client_id)
    
    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchone()
        if rezult:
            print('Удален телефон пользователя: ', rezult)
        else:
            print('Телефон не найден')

def delete_client(conn, client_id):
    requers_str = """
    DELETE FROM users 
    WHERE id = {client_id} RETURNING *
    ;
    """.format(client_id = client_id)
    
    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchall()
        if rezult:
            print('Удален пользователь: ', rezult)
        else:
            print('Пользователь не найден')

def select_db(conn, str):
    '''Функция делает запрос в БД с указанной строкой,
    возвращает результат запроса
    '''
    rez = []
    with conn.cursor() as cur:
        cur.execute(str)
        rezult = cur.fetchall()
        for item in rezult:
            rez.append(item[0])
        return rez[0] if len(rez) == 1 else rez

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    dist_args = locals()
    if phone:
        requers_str = """
        SELECT user_id FROM phone
        WHERE phone_number = {phone}
        ;
        """.format(phone = f"'{phone}'")
        return select_db(conn, requers_str)
    
    if email:
        requers_str = """
        SELECT id FROM users
        WHERE email = {email}
        ;
        """.format(email = f"'{email}'")
        return select_db(conn, requers_str)
    
    items = []
    for key, val in dist_args.items():
        if key == 'first_name' or key == 'last_name':
            if val:
                items.append(f"{key} = '{val}'")
    str_item = ' and '.join(items)
    requers_str = """
    SELECT id FROM users
    WHERE {str_item}
    ;
    """.format(str_item = str_item)
    return select_db(conn, requers_str)

def get_all_users(conn):
    requers_str = """
    SELECT * FROM users u
    LEFT JOIN phone p on u.id = p.user_id
    ORDER BY u.id asc
    ;
    """
    with conn.cursor() as cur:
        cur.execute(requers_str)
        rezult = cur.fetchall()
        return rezult if rezult else None


with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
    create_db(conn)

    add_client(conn, "Иван", "Иванов", "ivan@email.ru")
    add_client(conn, 'Сергей', 'Петров', 'sergey@email.ru', '+74951111111')
    add_client(conn, 'Сергей', 'Сидоров', 'sergeyS@email.ru', '+749533333333')
    add_phone(conn, 1, '+74552222222')
    add_phone(conn, 3, '+74552222555')
    print('Все пользователи: ', get_all_users(conn))
    
    print('Найден id пользователя по email: ', find_client(conn, email='ivan@email.ru'))
    print('Найден id пользователя по имени и фамилии: ', find_client(conn, first_name='Сергей', last_name='Петров'))
    print('Найден id пользователя по телефону: ', find_client(conn, phone='+74951111111'))
    print('Найдены id пользователей по имени: ', find_client(conn, first_name='Сергей'))
    print('Найден id телефона по номеру: ', find_phone_id(conn, 3, '+749533333335'))

    change_client(conn, 1, phones=('+74552222222', '+74552222223'))
    change_client(conn, 1, first_name='Олег')
    change_client(conn, 2, first_name='Иван', email='sergey-new@email.ru')

    delete_phone(conn, 1, '+74552222222')
    delete_phone(conn, 1, '+74552222223')
    delete_client(conn, 5)
    print('Все пользователи: ', get_all_users(conn))
    delete_client(conn, 3)
    print('Все пользователи: ', get_all_users(conn))

conn.close()