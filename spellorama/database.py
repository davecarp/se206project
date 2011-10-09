import sqlite3 

def sql(query, params=()):
    """ Run a sql query and return the result. """
    
    c = db.cursor()
    c.execute(query, params)

    return c

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
                                    "example" varchar(100),
                                    "difficulty" varchar(3)
                                    );""")

    # Create available lists table
    sql("""create table availableLists ( "list_ID" integer references "listIdent"("list_ID"),
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


    # Create a new list in the lists table that created words can be added to.
    with db:
        sql("""insert into listIdent ("list_name") values (?)""", ("Created Words",))
    
def username_exists(username):
    """Tests to see if a given string exists as a username. """

    if sql("""select * from users where "username"=?""", (username,)).fetchone():  
        return True
    else: 
        return False

def get_hashedpw(username):
    """Returns the hashed password for a given username. """
    return list(sql("""select "password" from users where "username"=?;""", (username,)))

def create_user(name, username, account_type, hashedpw):
    """ Inserts a user into the users table. """

    with db:
        sql("""insert into users("name", "username", "password", "account_type") values
               (?, ?, ?, ?)""", (name, username, hashedpw, account_type))



def get_account_type(username):
    """ Gets account type for a given username. """
    
    return sql("""select account_type from users where "username"=?""", (username,)).fetchone()[0]

def get_student_list():
    """Gets list of users with account type as student"""

    return list(sql("""select * from users where account_type="student";"""))

def change_password(ID, password):
    """ Resets the password of a user given their userID. """

    with db:
        sql("""update users set "password"=? where "user_ID"=?""", (password,ID))
    

def add_word(word, defin, context, diff):
    """ Adds a word to the database. """
    
    with db:   
        return sql("""insert into wordIdent ("word", "meaning", "example", "difficulty") 
                      values (?, ?, ?, ?);""", (word, defin, context, diff)).lastrowid
    

def add_list(filename):
    """ Adds a list to the database. """
        
    with db:
        return sql("""insert into listIdent ("list_name") values (?)""", (filename,)).lastrowid

def add_wordlist_mappings(list_ID, word_ID):

    with db:
        sql("""insert into listToWord ("list_ID", "word_ID") values (?,?)""", 
            (list_ID, word_ID))

def get_filenames():
    """ Gets list of .tldr files. """

    return sql("""select * from listIdent;""")

def get_words_from_file(list_ID):
    """ Gets list of words from a given file ID. """

    
    word_IDs= sql("""select word_ID from listToWord where list_ID=?""", (list_ID,))
    
    result = []

    for (i,) in word_IDs:
        result.append(sql("""select * from wordIdent where word_ID = ?;""", (i,)).fetchone())

    return result
        
def get_word_id(word, defin, ex, diff):
        
    return sql("""select * from wordIdent where "word"=? and "meaning"=? and "example"=?
               and "difficulty"=?;""", (word, defin, ex, diff))

def get_lists():
	
    return list(sql("""select * from listIdent;"""))

def get_available_lists(userID):

    list_IDs = sql("""select list_ID from availableLists where user_ID=?;""",
                   (userID,))

    result = []
    
    for (i,) in list_IDs:
        result.append(sql("""select * from listIdent where list_ID=?;""", (i,)).fetchone())

    return list(result)

def add_available_list(list_ID, user_ID):
    
    with db:
        sql("""insert into availableLists (list_ID, user_ID) values (?, ?);""",
            (list_ID, user_ID))

def remove_available_list(list_ID, user_ID):

    with db:
        sql("""delete from availableLists where list_ID=? and user_ID=?;""", 
            (list_ID, user_ID))

def get_student(username):

    return sql("""select * from users where username=?;""", (username,)).fetchone()

def add_incorrect_word(user_ID, word_ID):
        
    if not sql("""select * from incorrectWords where user_ID=? and word_ID=?;""",
               (user_ID, word_ID)):    
        with db:
            sql("""insert into incorrectWords (user_ID, word_ID) values (?,?);""",
                (user_ID, word_ID))

def get_incorrect_words(user_ID):

    word_IDs = sql("""select word_ID from incorrectWords where user_ID=?;""",
                   (user_ID,))

    result = []

    for (i,) in word_IDs:
        result.append(sql("""select * from wordIdent where word_ID = ?;""", (i,)).fetchone())

    return list(result)

def remove_incorrect_word(user_ID, word_ID):

    with db:
        sql("""delete from incorrectWords where user_ID=? and word_ID=?;""",
            (user_ID, word_ID))

def update_users_scores(words_t, words_c, words_i, per_c, per_i, userID):

    with db:
        sql("""update users set words_spelt=?, words_correct=?,
            words_incorrect=?, percent_correct=?, percent_incorrect=? where
            user_ID=?;""", (words_t, words_c, words_i, per_c, per_i, userID))
        
    
        


   
      




    
db = sqlite3.connect("spelloramadatabase.db")

