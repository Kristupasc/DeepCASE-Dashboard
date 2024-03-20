import sqlite3
import pandas as pd
import os
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Create a file path for "example.txt" in the script's directory
file_path = os.path.join(script_dir, 'deepcase.db')
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect(file_path)
        self.cur = self.conn.cursor()
        #self.create_tables()
        return

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS events
                                (id_event INTEGER PRIMARY KEY, timestamp REAL, machine TEXT, event TEXT, label INT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS mapping
                               (id INTEGER PRIMARY KEY, name TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS clusters
                               (id_cluster INTEGER PRIMARY KEY, score INT, risk label TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS sequences
                               (id_sequence INTEGER PRIMARY KEY, id_cluster INTEGER, mapping_value INT, risk_label TEXT,
                               FOREIGN KEY (id_cluster) REFERENCES clusters(id_cluster),
                               FOREIGN KEY (id_sequence) REFERENCES events(id_event),
                               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
                               )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS context_events
                               (id_sequence INTEGER, event_position INTEGER, attention REAL, mapping_value INT, 
                               PRIMARY KEY(event_position, id_sequence),
                               FOREIGN KEY (id_sequence) REFERENCES sequences(id_sequence),
                               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
                               )''')
        self.conn.commit()
        return
    def store_input_file(self, input_file_df):
        input_file_df.to_sql('events', self.conn, if_exists='replace', index=False, dtype={
            'id_event': 'INTEGER',
            'timestamp': 'REAL',
            'machine': 'TEXT',
            'event': 'TEXT',
            'label': 'INT'
        })
        self.conn.commit()
        return

    def drop_database(self):
        # Fetch the list of all tables in the database
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        # Iterate over the list of tables and drop each table
        for table_name in tables:
            # Each table_name is a tuple, so get the first element
            self.cur.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
        self.conn.commit()
        return
    ########################################################################
    #                         Data insertion                               #
    ########################################################################
    def store_file(self, file_df: pd.DataFrame):
        # Old method
        file_df.reset_index(inplace=True)
        file_df.rename(columns={'index': 'id_event'}, inplace=True)
        # TODO: Remove switch to append after testing is done
        file_df.to_sql('events', self.conn, if_exists='replace', index=False)
        self.conn.commit()
        return

    def store_sequences(self, sequence_df: pd.DataFrame):
        # Upload to sequence table
        sequence_df.to_sql('sequences', con=self.conn, if_exists='append', index=False)
        self.conn.commit()
        return

    def store_mapping(self, mapping):
        sequences_old_df = pd.read_sql_query('''SELECT * FROM sequences''', self.conn)
        context_events_old_df = pd.read_sql_query('''SELECT * FROM context_events''', self.conn)
        # Iterate through dict and upload to mapping table
        for key, value in mapping.items():
            self.cur.execute("INSERT OR REPLACE INTO mapping (id, name) VALUES (?, ?)", (key, value))
            self.conn.commit()
        return
    def store_context(self, context_df: pd.DataFrame):
        # Upload to context events table
        context_df.to_sql('context_events', con=self.conn, if_exists='append', index=False)
        self.conn.commit()
        return

    def store_clusters(self, clusters_df: pd.DataFrame):
        clusters_old_df = pd.read_sql_query('''SELECT * FROM sequences''', self.conn)
        # Append updated attention column to the old attention dataframe
        merged_df = clusters_old_df.merge(clusters_df, on='id_sequence', how='left', suffixes=('', '_updated'))
        # Ensure 'attention' and 'attention_updated' columns are of a numeric type
        cols_to_convert = ['id_cluster', 'id_cluster_updated']
        merged_df[cols_to_convert] = merged_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
        # Filling null values in 'attention' column with values from 'attention_updated'
        merged_df['id_cluster'] = merged_df['id_cluster'].fillna(merged_df['id_cluster_updated'])
        merged_df.drop(columns=['id_cluster_updated'], inplace=True)
        merged_df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)

        self.conn.commit()
        return

    def store_attention(self, attention_df: pd.DataFrame):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS temp_att
                                      (id_sequence INTEGER, event_position INTEGER, attention REAL, 
                                      PRIMARY KEY(event_position, id_sequence),
                                      FOREIGN KEY (id_sequence) REFERENCES sequences(id_sequence)
                                      )''')
        attention_df.to_sql('temp_att', con=self.conn, if_exists='replace', index=False)
        attention_old_df = pd.read_sql_query('''SELECT * FROM context_events''', self.conn)
        # Append updated attention column to the old attention dataframe
        merged_df = attention_old_df.merge(attention_df, on=['id_sequence', 'event_position'], how='left',
                                           suffixes=('', '_updated'))
        # Ensure 'attention' and 'attention_updated' columns are of a numeric type
        cols_to_convert = ['attention', 'attention_updated']
        merged_df[cols_to_convert] = merged_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
        # Filling null values in 'attention' column with values from 'attention_updated'
        merged_df['attention'] = merged_df['attention'].fillna(merged_df['attention_updated'])
        merged_df.drop(columns=['attention_updated'], inplace=True)
        merged_df.to_sql('context_events', con=self.conn, if_exists='replace', index=False)
        self.conn.commit()
        return

    def store_risk_labels(self, risk_label_df: pd.DataFrame):
        print(risk_label_df)
        return
    ########################################################################
    #                         Data aggregation                             #
    ########################################################################
    def get_input_table(self):
        # columns: timestamp,machine,event,label
        return pd.read_sql_query('''SELECT * FROM events''', self.conn)


    def get_sequences(self):
        # columns: id_sequence, id_cluster,  name,machine,timestamp, risk_label
        #
        result = pd.read_sql_query('''''', self.conn)
        # columns: main_event_name, timestamp, machine,  id_cluster, risk_label
        result = pd.read_sql_query('''SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label 
                                        FROM mapping, sequences, events 
                                        WHERE sequences.mapping_value = mapping.id 
                                        AND events.id_event = sequences.id_sequence''', self.conn)
        return result

    #TODO: create method to get only one sequence by id + same for context (?)

    def get_context_by_sequence_id(self, sequence_id):
        # columns:  event_position, event_name, attention
        query = "SELECT context_events.event_position, mapping.name, context_events.attention " \
                "FROM mapping, context_events " \
                "WHERE context_events.mapping_value = mapping.id " \
                "AND context_events.id_sequence = " + str(sequence_id)
        result = pd.read_sql_query(query, self.conn)
        return result

    def get_clusters(self):
        # columns:
        result = pd.read_sql_query('''''', self.conn)
        result = pd.read_sql_query('''SELECT * FROM clusters''', self.conn)
        return result

    def get_context(self):
        # columns:
        result = pd.read_sql_query('''''', self.conn)
    def get_sequences_per_cluster(self, cluster_id):

        query = "SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label " \
                "FROM mapping, sequences, events " \
                "WHERE sequences.mapping_value = mapping.id " \
                "AND events.id_event = sequences.id_sequence " \
                "AND sequences.id_cluster = " + str(cluster_id)
        result = pd.read_sql_query(query, self.conn)
        return result