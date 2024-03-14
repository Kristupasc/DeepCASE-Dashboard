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
        # create all tables
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

    def store_file(self, file_df: pd.DataFrame):
        # Old method
        file_df.reset_index(inplace=True)
        file_df.rename(columns={'index': 'id_event'}, inplace=True)
        # TODO: Remove switch to append after testing is done
        file_df.to_sql('events', self.conn, if_exists='replace', index=False)
        return

    def store_sequences(self, sequence_df: pd.DataFrame):
        # Upload to sequence table
        sequence_df.to_sql('sequences', con=self.conn, if_exists='append', index=False)
        return

    def store_mapping(self, mapping):
        # Iterate through dict and upload to mapping table
        for key, value in mapping.items():
            self.cur.execute("INSERT OR REPLACE INTO mapping (id, name) VALUES (?, ?)", (key, value))
            self.conn.commit()
        return

    def store_context(self, context_df: pd.DataFrame):
        # Upload to context events table
        context_df.to_sql('context_events', con=self.conn, if_exists='append', index=False)
        return

    def store_clusters(self, clusters_df: pd.DataFrame):
        self.cur.execute('''DROP TABLE IF EXISTS temporary''')
        self.cur.execute('''CREATE TABLE temporary (id_sequence INTEGER PRIMARY KEY, id_cluster TEXT)''')
        clusters_df.to_sql('temporary', con=self.conn, if_exists='replace', index=False)
        # no such column: temporary.id_sequence

        cluster_valued_df = pd.read_sql_query('''SELECT sequences.id_sequence, temporary.id_cluster, sequences.mapping_value, sequences.risk_label
                            FROM sequences, temporary
                             WHERE sequences.id_sequence = temporary.id_sequence''', self.conn)
        cluster_null_df = pd.read_sql_query('''SELECT sequences.id_sequence, sequences.mapping_value, sequences.risk_label
                                                        FROM sequences
                                                        LEFT JOIN temporary ON sequences.id_sequence = temporary.id_sequence
                                                        WHERE temporary.id_sequence IS NULL;
                                                        ''', self.conn)
        # print(cluster_null_df)
        # TODO: join df and null_df
        cluster_valued_df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)

        # self.cur.execute('''UPDATE sequences
        #                     SET id_cluster = (SELECT tm.id_cluster
        #                                       FROM temporary tm
        #                                       WHERE  tm.id_sequence = id_sequence)
        #                     WHERE id_sequence IN (SELECT id_sequence
        #                                           FROM temporary tm
        #                                           WHERE tm.id_sequence= id_sequence
        #                                           )
        #                     AND id_cluster IS NULL''')
        # TODO: Drop temp table
        return

    def store_attention(self, attention_df: pd.DataFrame):
        self.cur.execute('''DROP TABLE IF EXISTS temp_attention''')
        self.cur.execute('''CREATE TABLE temp_attention (id_sequence INTEGER PRIMARY KEY, attention NUM)''')

        attention_df.to_sql('temp_attention', con=self.conn, if_exists='replace', index=False)

        # attention_combined_df = pd.read_sql_query('''SELECT context_events.id_sequence,context_events.event_position, temp_attention.attention, context_events.mapping_value
        #                     FROM context_events, temp_attention
        #                      WHERE context_events.id_sequence = temp_attention.id_sequence
        #                      AND context_events.event_position = temp_attention.event_position''', self.conn)
        attention_null_df = pd.read_sql_query('''SELECT context_events.id_sequence, context_events.event_position, 
                                                               temp_attention.attention, context_events.mapping_value
                                                        FROM context_events
                                                        LEFT JOIN temp_attention 
                                                        ON context_events.id_sequence = temp_attention.id_sequence
                                                        AND context_events.event_position = temp_attention.event_position
                                                        WHERE context_events.attention IS NULL
                                                        ''', self.conn)

        # print(attention_null_df)
        attention_null_df.to_sql('context_events', con=self.conn, if_exists='replace', index=False)
        # TODO: Drop temp table
        return

    def store_risk_labels(self, risk_label_df: pd.DataFrame):
        print(risk_label_df)
        return

