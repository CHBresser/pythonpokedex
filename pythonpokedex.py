from flask import Flask, flash, redirect, render_template, request, session, abort
import sqlite3

# Create an instance of the Flask class
app = Flask(__name__)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Any page from /pokemon/____, eventually will have input checking to make sure
# that it is a pokemon name.     
@app.route('/pokemon/<string:name>/')
def pokemon(name):
    # Connect to SQLite3 Database
    sqlite_file = '../veekun-pokedex.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    c.execute("PRAGMA table_info(pokemon)")
    columns = c.fetchall()
    
    c.execute("SELECT * FROM pokemon WHERE identifier='{pid}'".\
        format(pid=name))
    
    all_rows = c.fetchall()
    pokemon_id = all_rows[0][0]
    pokemon_id = str(pokemon_id)
    if(len(pokemon_id) == 1):
        pokemon_id = "00" + pokemon_id
    elif(len(pokemon_id) == 2):
        pokemon_id = "0" + pokemon_id
        
    return render_template(
        'name.html', **locals())
        
# Autorun the app when this python script is called. 
if __name__ == "__main__":
        app.run()
