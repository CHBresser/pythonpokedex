import sqlite3

class Pokemon:
    id = 0
    name = ""
    height = ""
    weight = "" 
    type = []
    stats = []
    abilities = []
    moves = []
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 
        'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark',
        'steel', 'fairy']
    
    def __init__(self, pokename="", pokeid=""):
        if pokename:
            self.name = pokename
            self.queryDB()
        elif pokeid:
            self.id = pokeid
            self.queryDBbyID()
        
    def queryDB(self):
        # Convert name to lower
        self.name = self.name.lower()
        # Connect to SQLite3 Database
        sqlite_file = 'veekun-pokedex.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        # Currently gets all information from the pokemon table using the name retreived from the 
        c.execute("SELECT * FROM pokemon WHERE identifier='{pid}'".\
            format(pid=self.name))
    
        all_rows = c.fetchall()
        
        self.id = all_rows[0][0]
        self.height = all_rows[0][3]
        self.weight = all_rows[0][4]
        
        c.execute('''SELECT types.identifier FROM types
                    INNER JOIN pokemon_types ON pokemon_types.type_id = types.id
                    WHERE pokemon_types.pokemon_id="{pid}"'''.\
             format(pid=self.id))
        self.type = c.fetchall()
        
        # Grab base stats before converting pokemon_id to long notation
        c.execute('''SELECT stats.identifier, pokemon_stats.base_stat
                 FROM pokemon_stats
                 INNER JOIN stats ON pokemon_stats.stat_id = stats.id
                 WHERE pokemon_stats.pokemon_id="{sID}"'''.\
          format(sID=self.id)) 
        self.stats = c.fetchall()
        
        #Grab pokemon abilities
        c.execute('''SELECT abilities.identifier
                    FROM abilities
                    INNER JOIN pokemon_abilities ON pokemon_abilities.ability_id = abilities.id
                    WHERE pokemon_abilities.pokemon_id="{pID}"'''.\
                format(pID=self.id))
        self.abilities = c.fetchall()
        
        # Get Available Moves
        c.execute('''SELECT moves.identifier, types.identifier, moves.power, moves.pp, moves.accuracy
                     FROM moves
                     INNER JOIN pokemon_moves ON pokemon_moves.move_id = moves.id
                     INNER JOIN types ON moves.type_id = types.id
                     WHERE pokemon_moves.pokemon_id="{pID}"'''.\
                format(pID=self.id))
        self.moves = c.fetchall()
        
        # Close connection to DB
        conn.close()
    def idLong(self):
        #########################################################
        ## This function converts the variable length id into  ##
        ## a fixed length of 3 id (1, 10, 100)->(001, 010, 100)##
        ## This is used to hotlink from Nintendo's site and is ##
        ## not a viable long term solution, will need to turn  ##
        ## and host the pokemon profile photos inside the      ##
        ## application.                                        ##
        #########################################################
        strID = str(self.id)
        if(len(strID) == 1):
            return ("00" + strID)
        elif(len(strID) == 2):
            return ("0" + strID)
        else:
            return strID
    def idLongOther(self, option):
        #########################################################
        ## This function converts the variable length id into  ##
        ## a fixed length of 3 id (1, 10, 100)->(001, 010, 100)##
        ## This is used to hotlink from Nintendo's site and is ##
        ## not a viable long term solution, will need to turn  ##
        ## and host the pokemon profile photos inside the      ##
        ## application.                                        ##
        ##                                                     ##
        ## This is similar to idLong but then subtracts or adds## 
        #########################################################
        
        if option == "previous":
            strID = str(self.id-1)
            if(len(strID) == 1):
                return ("00" + strID)
            elif(len(strID) == 2):
                return ("0" + strID)
            else:
                return strID
        elif option == "next":
            strID = str(self.id+1)
            if(len(strID) == 1):
                return ("00" + strID)
            elif(len(strID) == 2):
                return ("0" + strID)
            else:
                return strID
    def queryDBbyID(self):
        # Connect to SQLite3 Database
        sqlite_file = 'veekun-pokedex.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        # Currently gets all information from the pokemon table using the name retreived from the 
        c.execute("SELECT * FROM pokemon WHERE identifier='{pid}'".\
            format(pid=self.id))
    
        all_rows = c.fetchall()
        
        self.name = all_rows[0][1]
        self.height = all_rows[0][3]
        self.weight = all_rows[0][4]
        
        c.execute('''SELECT types.identifier FROM types
                    INNER JOIN pokemon_types ON pokemon_types.type_id = types.id
                    WHERE pokemon_types.pokemon_id="{pid}"'''.\
             format(pid=self.id))
        self.type = c.fetchall()
        
        # Grab base stats before converting pokemon_id to long notation
        c.execute('''SELECT stats.identifier, pokemon_stats.base_stat
                 FROM pokemon_stats
                 INNER JOIN stats ON pokemon_stats.stat_id = stats.id
                 WHERE pokemon_stats.pokemon_id="{sID}"'''.\
          format(sID=self.id)) 
        self.stats = c.fetchall()
        
        #Grab pokemon abilities
        c.execute('''SELECT abilities.identifier
                    FROM abilities
                    INNER JOIN pokemon_abilities ON pokemon_abilities.ability_id = abilities.id
                    WHERE pokemon_abilities.pokemon_id="{pID}"'''.\
                format(pID=self.id))
        self.abilities = c.fetchall()
        
        # Close connection to DB
        conn.close()    
        
    def nameOther(self, option):
        # Connect to SQLite3 Database
        sqlite_file = 'veekun-pokedex.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        if option == "previous":
            prevID = self.id - 1
            # Currently gets identifier from the pokemon table using the previous id
            c.execute("SELECT identifier FROM pokemon WHERE id='{pid}'".\
                format(pid=(prevID)))
            results = c.fetchall()
            return results[0][0]
        elif option == "next":
            nextID = self.id + 1
            # Currently gets * from the pokemon table using the next id
            c.execute("SELECT identifier FROM pokemon WHERE id='{pid}'".\
                format(pid=(nextID)))
            results = c.fetchall()
            return results[0][0]
            
        # Close the connection
        conn.close()
            
        
        