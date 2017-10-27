from flask import Flask, flash, redirect, render_template, request, session, abort
import sqlite3
from pokemon import Pokemon

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
    curPokemon = Pokemon(name)
    return render_template(
        'pokemon.html', **locals())

# Any page from /id/# will look up the id and go to the appropriate page
@app.route('/id/<string:id>/')
def idPokemon(id):
    # Connect to SQLite3 Database
    sqlite_file = 'veekun-pokedex.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
       
    # Currently gets all information from the pokemon table using the id from the URL
    c.execute("SELECT * FROM pokemon WHERE id='{pid}'".\
            format(pid=id))
    all_rows = c.fetchall()
    
    curPokemon = Pokemon(all_rows[0][1])
    return render_template(
        'pokemon.html', **locals())

# List of Pokemon
@app.route('/pokemon/')
def pokemonList():
    # Connect to SQLite3 Database
    sqlite_file = 'veekun-pokedex.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    c.execute('''SELECT id, identifier, height, weight FROM pokemon''')
    list = c.fetchall()
    return render_template(
        'pokemonlist.html', **locals())

# Autorun the app on 0.0.0.0 when this python script is called. 
if __name__ == "__main__":
        app.run(host='0.0.0.0')
