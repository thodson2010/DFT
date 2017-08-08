#Sequal DB information
'''
This is the file that configures the sqlite DB to store high scores.
This file is only run once to construct the SQL DB
'''
import sqlite3

database_file = "score_db.db"

#You can write raw SQL as a string
sql_create_scores_table = ("""CREATE TABLE IF NOT EXISTS high_scores (
                                    id integer PRIMARY KEY,
                                    user text NOT NULL,
                                    score integer NOT NULL
                                );""")

fakeNames = [("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0),("TPH", 0)]

#Create a connection with database
conn = sqlite3.connect(database_file)
c = conn.cursor()

#Execute that raw SQL
c.execute(sql_create_scores_table)
print "Sucessfully created new database."

#Adding Fake data
c.executemany("INSERT INTO high_scores(user, score) VALUES (?,?)",fakeNames)
print "Fake users added successfully. "

conn.commit()
conn.close()
