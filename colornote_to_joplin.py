import requests
import sqlite3
import json

DATABASE_LOCATION = 'colornote.db'

class InvalidJoplinConnectionError(Exception):
    pass


class Database:
    """The connection to the database"""
    def __init__(self, db_location):
        self.conn = sqlite3.connect(db_location)
        self.cur = None
    def execute(self, query):
        if not self.cur:
            self.cur = self.conn.cursor()
        self.cur.execute(query)
        return self.cur.fetchall()
    def __del__(self):
        self.conn.close()

class JoplinApi:
    """Rudementary and very limited Joplin API abstraction"""
    def __init__(self, port, token ):
        #TODO Check you can connect to the API
        self.token_string = "?token=" + token
        self.url = "http://127.0.0.1:{}/".format(port)
        r = requests.get(self.url + "folders" + self.token_string)
        if r.status_code != 200:
            raise InvalidJoplinConnectionError("Joplin API call returned with code {} (should be 200).".format(r.status_code))

    def create_folder(self, name):
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "ping" + self.token_string, json={'title':name})
        return r.json()["id"]
def setup():
    # Get token, port, and establish connection to database
    print ("Hi. ")
    print ("Before we start, make sure you've backed up your database, then modified it according to the instructions in the README. ")
    print ("What's your authorization token?  ")
    auth_token = input()
    print("Great! What port is the webclipper listening on?  ")
    port_number = input()
    print("Awesome! I'll get right to it. Please hold...")



#    /// Connecting to a database went here
    return (cur, url, token_string)

def get_categories(cur):
# Get the names of the colornote "categories"/colors and their corresponding id
    cur.execute('SELECT note FROM notes WHERE title = "name_label_0";')
    record = json.loads( cur.fetchone()[0] )['D']
    categories = { key[-1] : record[key]['V'] for key in record }
    return categories

def create_top_level_folder():
# Create a notebook in Joplin that will contain all the imported notes. Return its id
    r = requests.post(url+ "folders" + token_string, json={'title':"From colornote"})
    return r.json()["id"]

def import_notes(cur, label_id, label_name, url, token_string, top_level_folder_id):
# Move all the notes within a given category/color to a seperate folder in joplin
    # Create new folder and save id
    r = requests.post(url+ "folders" + token_string, json={'title':label_name, 'parent_id' : top_level_folder_id,})
    folder_id = r.json()["id"]
    # Get all the notes corresponding to the label
    cur.execute('SELECT title, note, created_date, modified_date FROM notes WHERE color_index = "{}" AND NOT folder_id = "256";'.format(label_id))
    record = cur.fetchall()
    # For each of the notes, import it into the folder we just created
    # Note - those two replacements in the body transform the checklists so they still work
    for r in record:
        r = requests.post(url+ "notes" + token_string, json={
            'title':r[0],
            'parent_id' : folder_id,
            "body" : r[1].replace("[ ]", "- [ ]").replace("[V]", "- [x]"),
            "user_created_time": int(r[2]),
            "user_updated_time" : int(r[3]),
            })

# Main function
port = "41184"
token = "61d1be526ff931d9da99c57d322f1ca314dd0fd09f56d3b56475d42eebba982d2e5823b6d54a9aaaf4ee22223881cd343ab5b2eb37795142027a466b73243f46"
api = JoplinApi(port, token)



# cur, url, token_string = setup()
# top_level_folder_id = create_top_level_folder()
# categories = get_categories(cur)
#
# for key in categories:
#     import_notes(cur, key, categories[key], url, token_string, top_level_folder_id)
#
# print ("Looks like we're all done! Thanks.")
