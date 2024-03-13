import sqlite3
import pandas as pd


#TODO: make it run with server start
conn = sqlite3.connect('deepcase.db')
cur = conn.cursor()

# create events table and copy alerts.csv there

cur.execute('''CREATE TABLE IF NOT EXISTS events
               (id_event INTEGER PRIMARY KEY, timestamp REAL, machine TEXT, event TEXT, label INT)''')

#TODO: change into input file instead of system upload
df = pd.read_csv('alerts.csv')
df.reset_index(inplace=True)
df.rename(columns={'index': 'id_event'}, inplace=True)
df.to_sql('events', conn,if_exists='replace', index=False, dtype={
    'id_event': 'INTEGER',
    'timestamp': 'REAL',
    'machine': 'TEXT',
    'event': 'TEXT',
    'label': 'INT'
})
# create all other tables
cur.execute('''CREATE TABLE IF NOT EXISTS mapping
               (id INTEGER PRIMARY KEY, name TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS clusters
               (id_cluster INTEGER PRIMARY KEY, score INT, risk label TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS sequences
               (id_sequence INTEGER PRIMARY KEY, id_cluster INTEGER, mapping_value INT, risk_label TEXT,
               FOREIGN KEY (id_cluster) REFERENCES clusters(id_cluster),
               FOREIGN KEY (id_sequence) REFERENCES events(id_event),
               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
               )''')

cur.execute('''CREATE TABLE IF NOT EXISTS context_events
               (id_sequence INTEGER, event_position INTEGER, attention REAL, mapping_value INT, 
               PRIMARY KEY(event_position, id_sequence),
               FOREIGN KEY (id_sequence) REFERENCES sequences(id_sequence),
               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
               )''')

conn.commit()

