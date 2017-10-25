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
        
# Autorun the app on 0.0.0.0 when this python script is called. 
if __name__ == "__main__":
        app.run(host='0.0.0.0')
