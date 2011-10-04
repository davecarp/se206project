import sqlite3 

def sql(query, params=()):
    """ Run a sql query and return the result. """
    
    c = db.cursor()
    c.execute(query, params)

    return list(c)

def create_tables():
    """ Sets up the database for the first run. """  

    # Create users table
    sql("""create table users ( "id" integer primary key,
                                "name" varchar(30),
                                "age" integer,
                                "username" varchar(30),
                                "password" varchar(96)
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

def create_user(name, age, username, hashedpw):
    """ Inserts a user into the users table. """

    sql("""insert into users("name", "age", "username", "password") values
           (?, ?, ?, ?)""", (name, age, username, hashedpw))
    db.commit()
      




    
db = sqlite3.connect("spelloramadatabase.db")

