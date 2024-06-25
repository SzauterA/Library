import re
import bcrypt
import patterns
from sql_connect import connect
from datetime import datetime
import textwrap


#felhasználónév bekérése és validálása
def get_username():
    print("Username can contain letters/numbers/underscores/hyphens, must start with a letter.")
    while True:
        try:
            username = input("Username: ")
            if re.fullmatch(patterns.username_pattern, username):
                print("Valid username.")
                return username
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid username!")

#felhasználó teljes nevének bekérése és validálása
def get_fullname():
    print("Full name must contain firstname and lastname separated with withe space, both start with capital.")
    while True:
        try:
            name = input("Full name: ")
            if re.fullmatch(patterns.name_pattern, name):
                print("Valid name.")
                return name
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid name!")

#felhasználó e-mail címének bekérése és validálása
def get_email():
    print("The email address must be in a valid email format.")
    while True:
        try:
            email = input("Email address: ")
            if re.fullmatch(patterns.email_pattern, email):
                print("Valid email address.")
                return email
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid email address!")

#felhasználó telefonszámának bekérése és validálása
def get_phonenumber():
    print("Your phone number can be maximum 20 characters long, can have only numbers in it and should start with a '+'.")
    while True:
        try:
            phone = input("Phone number: ")
            if re.fullmatch(patterns.phone_pattern, phone):
                print("Valid phone number.")
                return phone
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid phone number!")

#felhasználó születési dátumának bekérése és validálása
def get_birthdate():
    print("Your birthdate must be in the following format: YYYY-mm-dd.")
    while True:
        try:
            date_str = input("Birthdate: ")
            birthdate = datetime.strptime(date_str, '%Y-%m-%d').date()
            if re.fullmatch(patterns.date_pattern, date_str):
                print("Valid birthdate.")
                return birthdate
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid birthdate!")

#felhasználó jelszavának bekérése és validálása
def get_password():
    print("The password must be minimum 8 characters long and should contain at least one of the following characters: lowercase, uppercase and number.")
    while True:
        try:
            password = input("Password: ")
            if re.fullmatch(patterns.password_pattern, password):
                print("Valid password.")
                return password
            else:
                raise ValueError
        except ValueError:
            print("Please provide a valid password!")

#felhasználó jelszavának megerősítése
def confirm_password(password):
    print("Provide the same password as previously.")
    while True:
        confirmed_password = input("Password again: ")
        if confirmed_password == password:
            print("Passwords match.")
            return confirmed_password
        else:
            print("The two given passwords should match!")

#felhasználó jelszavának elrejtése etikus tárolás céljából
def hash_password(confirmed_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(confirmed_password.encode(), salt)
    return hashed_password.decode('utf-8')

#felhasználó jogosultságának bekérése és validálása (nem túl életszerű de így kipróbálható az összes)
def get_permission():
    print(textwrap.dedent("""\
        Choose the level of permisson you want to have!
        Level 1: listing
        Level 2: listing, modification
        Level 3: listing, modification, deletion
        Level 4: listing, modification, deletion, addition
    """))
    while True:
        try:
            permission_num = int(input("Your permission level: "))
        except ValueError:
            print("Please provide a valid number!")
            continue

        if permission_num == 1:
            return 1
        elif permission_num == 2:
            return 2
        elif permission_num == 3:
            return 3
        elif permission_num == 4:
            return 4
        else:
            ("Please choose only from the given numbers!")

#dictionarybe gyűjti a megszerzett és validált adatokat majd visszaadja azt
def make_dict():
    username = get_username()
    name = get_fullname()
    email = get_email()
    phone = get_phonenumber()
    birthdate = get_birthdate()
    password = get_password()
    confirmed_password = confirm_password(password)
    hashed_password = hash_password(confirmed_password)
    permission = get_permission()
    
    if username and name and email and phone and birthdate and password and confirmed_password and hashed_password and permission:
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'phone': phone,
            'birthdate': birthdate,
            'password': hashed_password,
            'permission': permission
        }
    return user_data    

                   
#adatok beillesztése az adatbázisba
def signup():
    conn, cur = connect()
    if conn and cur:
        user_data = make_dict()
        if user_data:
            try: 
                query = """
                    INSERT INTO library.customers (username, name, email, phone, birth, password, permission)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(query,(
                    user_data['username'],
                    user_data['name'],
                    user_data['email'],
                    user_data['phone'],
                    user_data['birthdate'],
                    user_data['password'],
                    user_data['permission'],
                ))
                conn.commit()
                print("Succesful registration.")
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
            finally:
                cur.close()
                conn.close()
    else:
        print("Unable to connect to database.")