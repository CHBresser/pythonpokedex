import sqlite3
from prettytable import PrettyTable

while True:
    qTable = input("What table would you like?")
    if(qTable):
        break
    else:
        print("You must enter a table!!")
qColumn = input("Which column are we querying?")
qid = input("What are we looking for?")


def queryDB(table, column, id):

    # Declare Variables
    sqlite_file = 'veekun-pokedex.sqlite'
    queried_table = table
    id_column = column
    some_id = id
    listHeaders = []
    pokemonID = []
    abilityList = []

    # Connect to SQLite3 Database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("PRAGMA table_info({tn})".\
        format(tn=queried_table))
    columns = c.fetchall()
    columns = list(columns)
    
    # Query and format output
    for column in columns:
        listHeaders.append(column[1])

    if(qTable and qColumn and qid):
        c.execute("SELECT * FROM {tn} WHERE {cn} LIKE '{id}'".\
            format(tn=queried_table, cn=id_column, id=some_id))
        all_rows = c.fetchall()
    else:
        c.execute("SELECT * FROM {tn}".\
            format(tn=queried_table))
        all_rows = c.fetchall()
    x = PrettyTable(listHeaders)
    # Add all rows to table
    for row in all_rows:
        x.add_row(row)
        if(table == "pokemon"):
            pokemonID.append(row[0])
    
    print(x)
    
    print("Abilities: ")
    for id in pokemonID:
        c.execute('''SELECT pokemon.identifier, abilities.identifier  
            FROM pokemon_abilities
            INNER JOIN abilities ON abilities.id = pokemon_abilities.ability_id 
            INNER JOIN pokemon ON pokemon.id = pokemon_abilities.pokemon_id
            WHERE pokemon_abilities.pokemon_id="{aID}"'''.\
            format(aID=id))
        abilities = c.fetchall()
        print(abilities)
        
    tabstring = x.get_string
    
    #Close SQL connection
    conn.close()
queryDB(qTable, qColumn, qid)