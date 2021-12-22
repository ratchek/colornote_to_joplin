import requests
import sqlite3
import json

DATABASE_LOCATION = 'colornote.db'

class JoplinConnectionError(Exception):
    def __init__(self, api_call, response_code, response_body):
        """ Takes the method you were calling, the response code and the response body """
        self.response_code = response_code
        self.response_body = response_body
        self.message = "Joplin API '{}' call returned with code {} (should be 200). Here's the content of the response: \n _____ \n {} \n _____ \n ".format(api_call, response_code, response_body)
        super().__init__(self.message)

class Database:
    """Database connection manager"""
    def __init__(self, db_location):
        self.conn = sqlite3.connect(db_location)
        self.cur = self.conn.cursor()
    def execute(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    def __del__(self):
        self.conn.close()

class JoplinApi:
    """Rudementary and very limited Joplin API abstraction"""
    def __init__(self, port, token ):
        """Sets the connection variables and checks if connection can be established"""
        self.token_string = "?token=" + token
        self.url = "http://127.0.0.1:{}/".format(port)
        r = requests.get(self.url + "folders" + self.token_string)
        if r.status_code != 200:
            raise JoplinConnectionError("test", r.status_code, r.text)

    def create_top_level_folder(self):
        """ Create a notebook in Joplin that will contain all the imported notes."""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "folders" + self.token_string, json={'title':"Imported from colornote"})
        if r.status_code != 200:
            raise JoplinConnectionError("Create Folder", r.status_code, r.text)
        self.top_level_folder_id = r.json()["id"]

    def create_subcategory_folder(self, name):
        """Creates folder in the top level folder and returns it's id"""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "folders" + self.token_string, json={'title':name, 'parent_id' : self.top_level_folder_id})
        if r.status_code != 200:
            raise JoplinConnectionError("Create Subfolder", r.status_code, r.text)
        return r.json()["id"]

    def create_note(self, title, folder_id, note_body, user_created_time, user_updated_time):
        """Creates folder in the top level folder and returns it's id"""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "notes" + self.token_string, json={
            'title':title,
            'parent_id' : folder_id,
            # Note - these two replacements in the body transform the checklists so they still work
            "body" : note_body.replace("[ ]", "- [ ]").replace("[V]", "- [x]"),
            "user_created_time": user_created_time,
            "user_updated_time" : user_updated_time,
            })
        if r.status_code != 200:
            raise JoplinConnectionError("Create Note", r.status_code, r.text)

def setup():
    """ Get token, port, initialize database and joplin api classes """
    print ("Hi. ")
    print ("Before we start, make sure you've backed up your database, then modified it according to the instructions in the README. ")
    print ("\nWhat's your authorization token?  ")
    auth_token = input()
    print("\nGreat! What port is the webclipper listening on?  ")
    port_number = input()
    print("Awesome! I'll get right to it. Please hold...")

    database = Database(DATABASE_LOCATION)
    joplin = JoplinApi(port_number, auth_token)

    return (database, joplin)

def get_categories(database):
    """ Get the names of the colornote "categories"/colors and their corresponding id """
    db_results = database.execute('SELECT note FROM notes WHERE title = "name_label_0";')
    record = json.loads( db_results[0][0] )['D']
    categories = { key[-1] : record[key]['V'] for key in record }
    return categories



def import_notes(database, joplin, label_id, label_name):
    """ Move all the notes within a given category/color to a seperate folder in joplin """
    # Create new folder and save id
    folder_id = joplin.create_subcategory_folder(label_name)
    print ("--- Creating notes in " + label_name + "---")
    # Get all the notes corresponding to the label
    records = database.execute('SELECT title, note, created_date, modified_date FROM notes WHERE color_index = "{}" AND NOT folder_id = "256";'.format(label_id))
    # For each of the notes, import it into the folder we just created
    for record in records:
        joplin.create_note(title=record[0], folder_id=folder_id, note_body=record[1], user_created_time=int(record[2]), user_updated_time=int(record[3]),)
    print("Done!")

# Main function
database, joplin = setup()

joplin.create_top_level_folder()
categories = get_categories(database)

for key in categories:
    import_notes(database, joplin, key, categories[key])

print ("Looks like we're all done! Thanks.")
