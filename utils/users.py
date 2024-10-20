class User:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, public_key TEXT)")
        self.connection.commit()

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()
    
    def create_user(self, username, first_name, last_name, public_key):
        self.cursor.execute("INSERT INTO users (username, first_name, last_name, public_key) VALUES (?, ?, ?, ?)", (username, first_name, last_name, public_key))
        self.connection.commit()
