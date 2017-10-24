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
    # Convert name to lower
    name = name.lower()
    # Connect to SQLite3 Database
    sqlite_file = 'veekun-pokedex.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    # PRAGMA retrieves the table schema, I then in the template pokemon.html iterate through
    # and grab just the headers from the query.
    c.execute("PRAGMA table_info(pokemon)")
    columns = c.fetchall()
    
    # Currently gets all information from the pokemon table using the name retreived from the 
    c.execute("SELECT * FROM pokemon WHERE identifier='{pid}'".\
        format(pid=name))
    
    all_rows = c.fetchall()
    
    # Grab pokemon_id from query and convert to string
    pokemon_id = all_rows[0][0]
    pokemon_id = str(pokemon_id)
    
    # Grab base stats before converting pokemon_id to long notation
    c.execute('''SELECT stats.identifier, pokemon_stats.base_stat
                 FROM pokemon_stats
                 INNER JOIN stats ON pokemon_stats.stat_id = stats.id
                 WHERE pokemon_stats.pokemon_id="{sID}"'''.\
          format(sID=pokemon_id)) 
    base_stats = c.fetchall()
    
    # Determine Length of pokemon_id, if 1 digit add two 0's at beginning, or 2 add 1 0, etc
    # This is used in the template to hotlink from Nintendo's site, is not a viable solution. Will need to host profiles later on
    if(len(pokemon_id) == 1):
        pokemon_id = "00" + pokemon_id
    elif(len(pokemon_id) == 2):
        pokemon_id = "0" + pokemon_id
        
    # Close SQL connection when done    
    conn.close()
    return render_template(
        'pokemon.html', **locals())
        
# Autorun the app on 0.0.0.0 when this python script is called. 
if __name__ == "__main__":
        app.run(host='0.0.0.0')
