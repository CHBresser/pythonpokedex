import sqlite3

class Pokemon:
    # Declare Class Variables
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
    evolvesFrom =""
    evolvesTo = ""
    evolutions = []
    
    
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
        c.execute('''SELECT DISTINCT moves.identifier, types.identifier, moves.power, moves.pp, moves.accuracy
                     FROM moves
                     INNER JOIN pokemon_moves ON pokemon_moves.move_id = moves.id
                     INNER JOIN types ON moves.type_id = types.id
                     WHERE pokemon_moves.pokemon_id="{pID}"'''.\
                format(pID=self.id))
        self.moves = c.fetchall()
        
        self.evolutions = []
        self.evolutionChain()
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
        lastID = 721
        if option == "previous":
            if self.id == '1' or self.id == 1:
                return str(lastID)
            else:
                strID = str(self.id-1)
                if(len(strID) == 1):
                    return ("00" + strID)
                elif(len(strID) == 2):
                    return ("0" + strID)
                else:
                    return strID
        elif option == "next":
            if self.id == '721' or self.id == 721:
                return "001"
            else:
                strID = str(self.id+1)
                if(len(strID) == 1):
                    return ("00" + strID)
                elif(len(strID) == 2):
                    return ("0" + strID)
                else:
                    return strID
        else:
            strID = str(option)
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
       
        lastID = 721
        
        if option == "previous":
            if self.id == '1' or self.id == 1:
                # Currently gets identifier from the pokemon table using the previous id
                c.execute("SELECT identifier FROM pokemon WHERE id='{pid}'".\
                    format(pid=(str(lastID))))
                results = c.fetchall()
                return results[0][0]
            else:
                prevID = self.id - 1
                # Currently gets identifier from the pokemon table using the previous id
                c.execute("SELECT identifier FROM pokemon WHERE id='{pid}'".\
                    format(pid=(prevID)))
                results = c.fetchall()
                return results[0][0]
        elif option == "next":
            if self.id == lastID:
                # Currently gets identifier from the pokemon table using the previous id
                c.execute("SELECT identifier FROM pokemon WHERE id='1'")
                results = c.fetchall()
                return results[0][0]
            else:
                nextID = self.id + 1
                # Currently gets * from the pokemon table using the next id
                c.execute("SELECT identifier FROM pokemon WHERE id='{pid}'".\
                    format(pid=(nextID)))
                results = c.fetchall()
                return results[0][0]
            
        # Close the connection
        conn.close()
            
        
    def evolutionChain(self):
        # Connect to SQLite3 Database
        sqlite_file = 'veekun-pokedex.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        c.execute('''SELECT evolves_from_species_id FROM pokemon_species WHERE id="{pID}"'''.\
                format(pID=self.id))
            
        evolveID = c.fetchall()
        if evolveID:
            evolveID = evolveID[0][0]
        
            # Currently gets identifier from the pokemon table using the evolvesFromID
            c.execute("SELECT identifier FROM pokemon_species WHERE id='{pid}'".\
             format(pid=evolveID))
            results = c.fetchall()
            if results:
                self.evolutions.insert(0,results[0][0])
                self.evolutions.insert(1, self.name)
                
            # Check to see if there was another previous evolutionChain
            c.execute('''SELECT evolves_from_species_id FROM pokemon_species WHERE id="{pID}"'''.\
                format(pID=evolveID))
            
            evolveID = c.fetchall()
            if evolveID:
                evolveID = evolveID[0][0]
        
                # Currently gets identifier from the pokemon table using the evolvesFromID
                c.execute("SELECT identifier FROM pokemon_species WHERE id='{pid}'".\
                    format(pid=evolveID))
                results = c.fetchall()
                if results:
                    self.evolutions.insert(0,results[0][0])
        if not self.evolutions:
            self.evolutions.insert(0, self.name)
        c.execute('''SELECT id FROM pokemon_species WHERE evolves_from_species_id="{pID}"'''.\
                format(pID=self.id))
            
        evolveID = c.fetchall()
        if evolveID:
            evolveID = evolveID[0][0];
        
            # Currently gets * from the pokemon table using the next id
            c.execute("SELECT identifier FROM pokemon_species WHERE id='{pid}'".\
             format(pid=evolveID))
            results = c.fetchall()
            if results:
                self.evolutions.append(results[0][0])
                
            # Check to see if there is another evolution after
            c.execute('''SELECT id FROM pokemon_species WHERE evolves_from_species_id="{pID}"'''.\
                format(pID=evolveID))
            
            evolveID = c.fetchall()
            if evolveID:
                evolveID = evolveID[0][0]
        
                # Currently gets identifier from the pokemon table using the evolvesFromID
                c.execute("SELECT identifier FROM pokemon_species WHERE id='{pid}'".\
                    format(pid=evolveID))
                results = c.fetchall()
                if results:
                    self.evolutions.append(results[0][0])
    def queryIDFromName(self, qname):
        # Connect to SQLite3 Database
        sqlite_file = 'veekun-pokedex.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        c.execute("SELECT id FROM pokemon WHERE identifier='{pname}'".\
            format(pname=qname))
        tempName = c.fetchall()
        if tempName:
            return tempName[0][0]