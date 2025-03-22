import sqlite3


class Database():
    try:
            
        def __init__(self, database_file):
            self.connection = sqlite3.connect(database_file, check_same_thread=False)
            self.cursor = self.connection.cursor()
                    
        def add_user_id_to_db(self, user_id):
            with self.connection:
                self.cursor.execute('SELECT * FROM user_list') # This will return a cursor object
                all_users = self.cursor.fetchall()  # Fetch all rows from the query result
                # I used user_ids = [row[0] for row in all_users] to extract the user IDs from the result set because self.cursor.fetchall() returns a list of tuples
                user_ids = [row[0] for row in all_users]  # Extract the user IDs from the fetched rows; 
        

                if int(user_id) in user_ids:
                    print('User is already in db')
                    return
                else:
                    self.cursor.execute('INSERT INTO user_list VALUES (?)', (user_id,))
                
        def get_all_user_ids(self):
            all_users = self.cursor.execute('SELECT * FROM user_list')
            user_ids = [row[0] for row in all_users] 
            return user_ids
        
        def count_users(self):
            return self.cursor.execute('SELECT COUNT(*) FROM user_list')
        
        def add_queue(self, chat_id):
            with self.connection:
                return self.cursor.execute('INSERT INTO queue (chat_id) VALUES (?)', (chat_id,))
        
        def delete_queue(self, chat_id):
            with self.connection:
                return self.cursor.execute('DELETE FROM queue WHERE chat_id = ?', (chat_id,))
        
        def get_chat(self, bot_id):
            with self.connection:
                # This will return the whole row
                # chat = self.cursor.execute('SELECT * FROM queue', ()).fetchmany(1)
                chat = self.cursor.execute('SELECT * FROM queue WHERE chat_id != ?', (bot_id,)).fetchmany(1)
                
                # If chat is found then it's gonna be and will be evaluated to True
                if (bool(len(chat))):
                    for row in chat:
                        return row[1]  # taking chat_id from db
                else:
                    return False
        
        def delete_chat(self, id_chat):
            with self.connection:
                return self.cursor.execute('DELETE FROM chats WHERE id = (?)', (id_chat,))
        
        def create_chat(self, chat_one, chat_two):
            with self.connection:
                if chat_two != 0:
                    # Creating chat
                    self.cursor.execute('DELETE FROM queue WHERE chat_id = ?', (chat_two,))
                    self.cursor.execute('INSERT INTO chats (chat_one, chat_two) VALUES (?, ?)', (chat_one, chat_two))
                    return True

                else:
                    # Adding user to queue if user is not found
                    return False
                
        def get_active_chat(self, chat_id):
            with self.connection:
                # search for use in chat_one row
                chat = self.cursor.execute('SELECT * FROM chats WHERE chat_one = (?)', (chat_id, ))
                id_chat = 0
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[2]]
                
                # if chat was not found search for us in chat_two
                if id_chat == 0:
                    chat = self.cursor.execute('SELECT * FROM chats WHERE chat_two = (?)', (chat_id, ))
                    for row in chat:
                        id_chat = row[0]
                        chat_info = [row[0], row[1]]
                        
                        if id_chat == 0:
                            return False
                        else:
                            return chat_info
                else:
                    return chat_info
    except Exception:
        print('Error ocurred')
