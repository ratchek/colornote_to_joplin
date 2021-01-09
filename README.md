##### This is a script that will import notes from your Colornotes database to Joplin

## The "Why?"
Colornotes unfortunately doesn't allow you to export your data in any way (aside from exporting each note one by one). So if you aren't using it, **don't start now**. If you were and want to switch to a different app, this tool might be for you.
##### Why Joplin? Why not csv or markdown or another format?
Mainly because it's the app I intend on using. Also because it has an API that will enable me to keep the creation and modification dates intact in each note.
After you import this into Joplin, feel free to use its export options and get whatever format you'd like.
So, what will this tool preserve?
 * Title
 * Body
 * Color category
 * Creation date
 * Modification date

**Note**: this tool will *not* preserve the creation date for folders, any geolocation data, tags, or anything besides what's listed above. So MAKE SURE YOU HAVE A BACKUP OF YOUR DATABASE.
### **I AM NOT RESPONSIBLE FOR ANY LOST DATA**


## The "How?"
##### Prerequisites:
 * You need python or python3 installed on your system.
 * You need to have the  *requests*, *sqlite3*, and *json* modules installed (but they come pre-installed with python 3, so try not to worry about it)

##### Prepping the database
 * First of all, you will need to *get* the database used by colornote. You will need a rooted android phone or emulator. Here's an excellent guide: (You will just need to do till step 7)

 	https://android.stackexchange.com/questions/35207/import-data-from-colornote-app

#### ** --- Warning. In order to make this work, you will need to delete geolocation data from your notes, so MAKE SURE YOU HAVE A BACKUP --- **
* Once you've opened your database in the sqlite browser, in the "database structure" tab, click on the "notes" table to highlight it. Then click "Modify Table" at the top. You should get a popup window titled "edit table definition"
* Scroll down to lattitude and longitude and delete both. Close the popup, close the sqlite browser and make sure you save the changes.
* Copy the database into the folder containing *colornote_to_joplin.py* and make sure it's named "colornote.db"

##### Prepping Joplin
 * Open Joplin
 * Go to Tools -> Options -> Webclipper
 * Enable the webclipper service
 * Copy the API key (it's near the bottome of that page) and port number (it's near the top of the page. Above the "disable web clipper service" button. Default is 41184)

## Zhu Li, Do The Thing!
 * Open a terminal and navigate to the folder where the program and database are stored.
 * Run the app by typing "python colornote_to_joplin.py" or "python3 colornote_to_joplin.py"
 * Input API key and port number when prompted.
 * This may take a bit, depending on the ammount of notes you have. Don't freak out.
 * You're done! Congrats.
