import sqlite3 

def sql(query, params=()):
    """ Run a sql query and return the result. """
    
    c = db.cursor()
    c.execute(query, params)

    return list(c)

def create_tables():
    """ Sets up the database for the first run. """  

    # Create users table
    sql("""create table users ( "name" varchar(30),
                                "username" varchar(30),
                                "password" varchar(96)
                                );""")
    
    # Create account type tables
    sql("""create table accounttypes ( "username" varchar(30),
                                       "type" varchar(30)
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

    sql("""insert into users("name", "username", "password") values
           (?, ?, ?)""", (name, username, hashedpw))

    sql("""insert into accounttypes("username", "type") values (?, ?)""", (username, account_type))

    db.commit()

def get_account_type(username):
    """ Gets account type for a given username. """
    
    ls = sql("""select type from accounttypes where "username"=?""", (username,))
    return ls[0][0]
      




    
db = sqlite3.connect("spelloramadatabase.db")

