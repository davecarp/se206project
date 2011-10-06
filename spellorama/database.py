import sqlite3 

def sql(query, params=()):
    """ Run a sql query and return the result. """
    
    c = db.cursor()
    c.execute(query, params)

    return list(c)

def create_tables():
    """ Sets up the database for the first run. """  

    # Create users table
    sql("""create table users ( "user_ID" integer primary key,
                                "name" varchar(30),
                                "username" varchar(30),
                                "password" varchar(96),
                                "account_type" varchar(10),
                                "words_spelt" integer,
                                "words_correct" integer,
                                "words_incorrect" integer,
                                "percent_correct" double,
                                "percent_incorrect" double
                                );""")
    
    # Create list ID table
    sql("""create table listIdent ( "list_ID" integer primary key,
                                    "list_name" varchar(30)
                                    );""")
    
    # Create word ID table
    sql("""create table wordIdent ( "word_ID" integer primary key,
                                    "word" varchar(30),
                                    "meaning" varchar(100),
                                    "example" varchar(100)
                                    );""")

    # Create available lists table
    sql("""create table avaliableLists ( "list_ID" integer references "listIdent"("list_ID"),
                                         "user_ID" integer references "users"("user_ID"),
                                         primary key ("list_ID","user_ID")
                                         );""")
    # Create new word to list table
    sql("""create table listToWord ( "list_ID" integer references "listIdent"("list_ID"),
                                     "word_ID" integer references "wordIdent"("word_ID"),
                                     primary key ("list_ID", "word_ID")
                                     );""")

    # Create new incorrect word table
    sql("""create table incorrectWords ( "user_ID" integer references "users"("user_ID"),
                                         "word_ID" integer references "wordIdent"("word_ID"),
                                         primary key ("user_ID", "word_ID")
                                         );""")

    # Create new listResults table
    sql(""" create table listResults ( "user_ID" integer references "users"("user_ID"),
                                       "list_ID" integer references "listIdent"("list_ID"),
                                       "percent_correct" double,
                                       "percent_incorrect" double,
                                       "words_correct" integer,
                                       "words_incorrect" integer,
                                       "words_total",
                                       primary key ("user_ID", "list_ID")
                                       );""")
    
def username_exists(username):
    """Tests to see if a given string exists as a username. """

    if sql("""select * from users where "username"=?""", (username,)):  
        return True
    else: 
        return False

def get_hashedpw(username):
    """Returns the hashed password for a given username. """
    ls = sql("""select "password" from users where "username"=?""", (username,));
    return ls

def create_user(name, username, account_type, hashedpw):
    """ Inserts a user into the users table. """

    sql("""insert into users("name", "username", "password", "account_type") values
           (?, ?, ?, ?)""", (name, username, hashedpw, account_type))

    db.commit()

def get_account_type(username):
    """ Gets account type for a given username. """
    
    ls = sql("""select account_type from users where "username"=?""", (username,))
    return ls[0][0]

def get_student_list():
    """Gets list of users with account type as student"""

    return sql("""select * from users where account_type="student";""")

def change_password(ID, password):
    """ Resets the password of a user given their userID. """

    sql("""update users set "password"=? where "user_ID"=?""", (password,ID))
    db.commit()
      




    
db = sqlite3.connect("spelloramadatabase.db")

