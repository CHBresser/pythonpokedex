import sqlite3
from prettytable import PrettyTable, from_db_cursor

# Force user to provide table name
while True:
    qTable = input("What table would you like?")
    if(qTable):
        break
    else:
        print("You must enter a table!!")
qColumn = input("Which column are we querying?")
qid = input("What are we looking for?")


def queryDB(table, column, id):

    # Declare Function Variables
    sqlite_file = 'veekun-pokedex.sqlite'
    queried_table = table
    id_column = column
    some_id = id
    listHeaders = []
    pokemonID = []
    headerList = ['pokemon.identifier', 'pokemon.height', 'pokemon.weight', 'pokemon.base_experience', 'abilities.identifier']
    # Connect to SQLite3 Database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Grab Table Headers
    c.execute("PRAGMA table_info({tn})".\
        format(tn=queried_table))
    columns = c.fetchall()
    columns = list(columns)
    
    # Previous command has a lot of useless information, filter out just the header info we need
    for column in columns:
        listHeaders.append(column[1])

    # If all earlier prompts were answered.
    if(qTable and qColumn and qid):
        c.execute("SELECT * FROM {tn} WHERE {cn} LIKE '{id}'".\
           format(tn=queried_table, cn=id_column, id=some_id))
        all_rows = c.fetchall()
    # If only table was provided. (Table is required, and forced ;)
    else:
        c.execute("SELECT * FROM {tn}".\
            format(tn=queried_table))
        all_rows = c.fetchall()
        
    # Create Table object with appropriate headers
    x = PrettyTable(listHeaders)
    # Add all rows to table iteratively 
    for row in all_rows:
        x.add_row(row)
        if(table == "pokemon"):
            # IF table is pokemon, while iterating through rows, append the pokemon id number to the pokemon id list (used for abilities)
            pokemonID.append(row[0])
    # "Display" table if not pokemon, if pokemon carry on and gather more information
    if (table != 'pokemon'):
        print(x)
    # Display abilities
    needAbil = ''
    if(table == 'pokemon'):
        needAbil = input("Would you like to see their abilities? ")
        formatHeader = [] 
        for item in headerList:
            # Split the string of headers into a list of (pokemon, identifier, abilities, identifier, etc)
            tempList = item.split('.')
            # PrettyTable won't take more than one Field name of the same name, so I must iterate through the fields and make sure that pokemon.identifier and abilities.identifier don't both split to identifier
            if(item == 'abilities.identifier'):
                formatHeader.append('Ability ID')
            else:
            # If not abilities.identifier then append the second half of each split (--pokemon--, identifier)
                formatHeader.append(tempList[1])
    if(needAbil == 'y' or needAbil == 'Y' or needAbil == 'yes' or needAbil == 'Yes' or needAbil == 'YES'):
        pokeTable = PrettyTable(formatHeader)
        for id in pokemonID:
            # Grab the pokemon name and ability name using the id #'s from pokemon_abilities
            c.execute('''SELECT pokemon.identifier, pokemon.height, pokemon.weight, pokemon.base_experience, abilities.identifier
                FROM pokemon_abilities
                INNER JOIN abilities ON abilities.id = pokemon_abilities.ability_id 
                INNER JOIN pokemon ON pokemon.id = pokemon_abilities.pokemon_id
                WHERE pokemon_abilities.pokemon_id="{aID}"'''.\
                format(aID=id))
            abilities = c.fetchall()
            for row in abilities:
                pokeTable.add_row(row)
        print(pokeTable.get_string(sortby="identifier"))
        

    #Close SQL connection
    conn.close()
    
# Call queryDB function providing all variables (even if not used) function validates input.
queryDB(qTable, qColumn, qid)