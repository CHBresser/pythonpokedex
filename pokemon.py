import sqlite3

class Pokemon:
    id = 0
    name = ""
    height = ""
    weight = "" 
    type = ""
    stats = []
    
    def __init__(self, pokename):
        self.name = pokename
        if self.name:
            self.queryDB()
        
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
        temptype = c.fetchall()
        self.type = temptype[0][0]
        
        # Grab base stats before converting pokemon_id to long notation
        c.execute('''SELECT stats.identifier, pokemon_stats.base_stat
                 FROM pokemon_stats
                 INNER JOIN stats ON pokemon_stats.stat_id = stats.id
                 WHERE pokemon_stats.pokemon_id="{sID}"'''.\
          format(sID=self.id)) 
        self.stats = c.fetchall()
        
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
        
        