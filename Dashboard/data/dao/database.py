import sqlite3
from datetime import datetime

import pandas as pd
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Create a file path for "example.txt" in the script's directory
file_path = os.path.join(script_dir, 'deepcase.db')


class Database(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Check if the instance is already initialized
            self.conn = sqlite3.connect(file_path, check_same_thread=False)
            self.cur = self.conn.cursor()
            self.filename = 'defaultfilename'
            self.initialized = True  # Mark the instance as initialized
            # self.drop_database()
            # self.create_tables()
        return

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files
                                (filename TEXT PRIMARY KEY)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS events
                                (id_event INTEGER, filename TEXT, timestamp REAL, machine TEXT, event TEXT, label INT, 
                                PRIMARY KEY(id_event, filename),
                                FOREIGN KEY (filename) REFERENCES files(filename)
                                )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS mapping
                               (id INTEGER, name TEXT, filename TEXT,
                               PRIMARY KEY(id, filename),
                               FOREIGN KEY (filename) REFERENCES files(filename)
                               )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS clusters
                               (id_cluster INTEGER, filename TEXT, name_cluster TEXT, score INT,
                               PRIMARY KEY(id_cluster, filename),
                               FOREIGN KEY (filename) REFERENCES files(filename)
                               )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS sequences
                               (id_sequence INTEGER, filename TEXT, id_cluster INTEGER, mapping_value INT, risk_label TEXT,
                               PRIMARY KEY(id_sequence, filename),
                               FOREIGN KEY (filename) REFERENCES files(filename)
                               FOREIGN KEY (id_cluster) REFERENCES clusters(id_cluster),
                               FOREIGN KEY (id_sequence) REFERENCES events(id_event),
                               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
                               )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS context_events
                               (id_sequence INTEGER, filename TEXT, event_position INTEGER, attention REAL, mapping_value INT, 
                               PRIMARY KEY(event_position, id_sequence, filename),
                               FOREIGN KEY (filename) REFERENCES files(filename), 
                               FOREIGN KEY (id_sequence) REFERENCES sequences(id_sequence),
                               FOREIGN KEY (mapping_value) REFERENCES mapping(id)
                               )''')
        self.conn.commit()
        return

    def switch_current_file(self, filename):
        # Checl if the filename exists in the database
        if filename in self.get_filenames()['filename'].values:
            self.filename = filename
            return True
        return False

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
    def store_input_file(self, input_file_df: pd.DataFrame, filename):
        now = datetime.now()
        # Append current datetime to the filename
        self.filename = filename + '_' + now.strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute("INSERT  INTO files (filename) VALUES (?)", (self.filename,))
        self.conn.commit()

        input_file_df['filename'] = self.filename
        input_file_df.to_sql('events', self.conn, if_exists='append', index=False, dtype={
            'id_event': 'INTEGER',
            'filename': 'TEXT',
            'timestamp': 'REAL',
            'machine': 'TEXT',
            'event': 'TEXT',
            'label': 'INT'
        })
        self.conn.commit()
        return True

    def store_sequences(self, sequence_df: pd.DataFrame):
        # Upload to sequence table
        sequence_df['filename'] = self.filename
        sequence_df.reset_index(inplace=True)
        sequence_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        sequence_df.to_sql('sequences', con=self.conn, if_exists='append', index=False)
        self.conn.commit()
        return

    def store_mapping(self, mapping):
        # sequences_old_df = pd.read_sql_query('''SELECT * FROM sequences WHERE filename = ?''', self.conn, params=[self.filename])
        # context_events_old_df = pd.read_sql_query('''SELECT * FROM context_events WHERE filename = ?''', self.conn, params=[self.filename])
        # Iterate through dict and upload to mapping table
        for key, value in mapping.items():
            self.cur.execute("INSERT OR REPLACE INTO mapping (id, name, filename) VALUES (?, ?, ?)",
                             (key, value, self.filename))
            self.conn.commit()
        return

    def store_context(self, context_df: pd.DataFrame):
        # Upload to context events table
        context_df['filename'] = self.filename

        context_df.to_sql('context_events', con=self.conn, if_exists='append', index=False)
        self.conn.commit()
        return

    def store_clusters(self, clusters_df: pd.DataFrame):

        clusters_old_df = pd.read_sql_query('''SELECT * FROM sequences WHERE filename = ?''', self.conn,
                                            params=[self.filename])
        other_clusters_df = pd.read_sql_query('''SELECT * FROM sequences WHERE NOT filename = ?''', self.conn,
                                            params=[self.filename])
        clusters_df['id_sequence'] = clusters_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        clusters_old_df['id_sequence'] = clusters_old_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        # Append updated attention column to the old attention dataframe
        merged_df = clusters_old_df.merge(clusters_df, on='id_sequence', how='left', suffixes=('', '_updated'))
        # Ensure 'attention' and 'attention_updated' columns are of a numeric type
        cols_to_convert = ['id_cluster', 'id_cluster_updated']
        merged_df[cols_to_convert] = merged_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
        # Filling null values in 'attention' column with values from 'attention_updated'
        merged_df['id_cluster'] = merged_df['id_cluster'].fillna(merged_df['id_cluster_updated'])
        merged_df.drop(columns=['id_cluster_updated'], inplace=True)
        merged_df['filename'] = self.filename
        result_df = pd.concat([merged_df, other_clusters_df], ignore_index=True)
        result_df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)

        self.conn.commit()
        return

    def store_attention(self, attention_df: pd.DataFrame):
        attention_old_df = pd.read_sql_query('''SELECT * FROM context_events WHERE filename = ?''', self.conn,
                                             params=[self.filename])
        other_attention_df = pd.read_sql_query('''SELECT * FROM context_events WHERE NOT filename = ?''', self.conn,
                                              params=[self.filename])

        attention_df['id_sequence'] = attention_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        attention_old_df['id_sequence'] = attention_old_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        # Append updated attention column to the old attention dataframe
        merged_df = attention_old_df.merge(attention_df, on=['id_sequence', 'event_position'], how='left',
                                           suffixes=('', '_updated'))
        # Ensure 'attention' and 'attention_updated' columns are of a numeric type
        cols_to_convert = ['attention', 'attention_updated']
        merged_df[cols_to_convert] = merged_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
        # Filling null values in 'attention' column with values from 'attention_updated'
        merged_df['attention'] = merged_df['attention'].fillna(merged_df['attention_updated'])
        merged_df.drop(columns=['attention_updated'], inplace=True)
        merged_df['filename'] = self.filename
        # Remove old records
        result_df = pd.concat([merged_df , other_attention_df], ignore_index=True)

        result_df.to_sql('context_events', con=self.conn, if_exists='replace', index=False)
        self.conn.commit()
        return

    def update_sequence_score(self, score_df: pd.DataFrame):
        score_old_df = pd.read_sql_query('''SELECT * FROM sequences WHERE filename = ?''', self.conn,
                                         params=[self.filename])
        others_score_df = pd.read_sql_query('''SELECT * FROM sequences WHERE NOT filename = ?''', self.conn,
                                         params=[self.filename])

        score_df['id_sequence'] = score_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        score_old_df['id_sequence'] = score_old_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
        # Append updated score column to the old score dataframe
        merged_df = score_old_df.merge(score_df, on=['id_sequence'], how='left',
                                       suffixes=('', '_updated'))
        # Ensure 'score' and 'score_updated' columns are of a numeric type

        merged_df.drop(columns='risk_label', inplace=True)
        merged_df.rename(columns={'risk_label_updated': 'risk_label'}, inplace=True)
        merged_df['filename'] = self.filename
        result_df = pd.concat([merged_df, others_score_df], ignore_index=True)
        result_df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)
        self.conn.commit()
        return

    def fill_cluster_table(self):
        query = """SELECT id_cluster, id_cluster AS name_cluster, MAX(risk_label) AS score  
        FROM sequences 
        WHERE filename = ?
        GROUP BY id_cluster;
        """
        clusters_df = pd.read_sql_query(query, self.conn, params=[self.filename])
        clusters_df['filename'] = self.filename
        other_clusters_df = pd.read_sql_query("SELECT * FROM clusters WHERE NOT filename = ?", self.conn, params=[self.filename])
        result_df = pd.concat([clusters_df, other_clusters_df], ignore_index=True)
        result_df.to_sql("clusters", con=self.conn, if_exists='replace', index=False)
        return

    ########################################################################
    #                         Data aggregation                             #
    ########################################################################
    def get_input_table(self) -> pd.DataFrame:
        # columns: timestamp,machine,event,label
        return pd.read_sql_query('''SELECT * FROM events WHERE filename = ?''', self.conn, params=[self.filename])

    def get_sequences(self) -> pd.DataFrame:
        # columns: main_event_name, timestamp, machine,  id_cluster, risk_label
        result = pd.read_sql_query('''SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label 
                                        FROM mapping, sequences, events 
                                        WHERE sequences.mapping_value = mapping.id 
                                        AND events.id_event = sequences.id_sequence
                                        AND sequences.filename = ?''', self.conn, params=[self.filename])
        return result

    def get_sequence_by_id(self, sequence_id: int) -> pd.DataFrame:
        query = "SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label " \
                "FROM mapping, sequences, events " \
                "WHERE sequences.mapping_value = mapping.id " \
                "AND events.id_event = ?" \
                "AND sequences.filename = ?"
        result = pd.read_sql_query(query, self.conn, params=[sequence_id, self.filename])
        return result

    def get_context_by_sequence_id(self, sequence_id: int) -> pd.DataFrame:
        # columns:  event_position, event_name, attention
        query = """SELECT context_events.event_position, mapping.name, context_events.attention 
                FROM mapping, context_events 
                WHERE context_events.mapping_value = mapping.id 
                AND context_events.id_sequence = ? 
                AND context_events.filename = ?"""
        # parameterized query to avoid sql injection
        result = pd.read_sql_query(query, self.conn, params=[sequence_id, self.filename])
        return result

    def get_clusters(self) -> pd.DataFrame:
        result = pd.read_sql_query('''SELECT * FROM clusters WHERE filename = ?''', self.conn, params=[self.filename])
        return result

    def get_sequences_per_cluster(self, cluster_id: int) -> pd.DataFrame:
        query = """SELECT events.id_event, sequences.id_sequence, mapping.name, events.timestamp, events.machine, 
                sequences.id_cluster, sequences.risk_label
                FROM mapping, sequences, events 
                WHERE sequences.mapping_value = mapping.id 
                AND events.id_event = sequences.id_sequence 
                AND sequences.id_cluster = ? 
                AND sequences.filename = ?"""
        result = pd.read_sql_query(query, self.conn, params=[float(cluster_id), self.filename])
        return result

    def get_mapping(self) -> pd.DataFrame:
        query = "SELECT  mapping.name, mapping.id " \
                "FROM mapping " \
                "WHERE filename = ?"
        result = pd.read_sql_query(query, self.conn, params=[self.filename])
        return result

    #

    def set_cluster_name(self, id_cluster: int, name_cluster: str):
        query = "UPDATE clusters SET name_cluster = ? WHERE id_cluster = ? AND filename = ?"
        self.cur.execute(query, (name_cluster, id_cluster, self.filename))
        self.conn.commit()
        return

    def set_risk_value(self, event_id, risk_value):
        query = "UPDATE sequences SET risk_label = ? WHERE id_sequence = ? AND filename = ?"
        self.cur.execute(query, (risk_value, event_id, self.filename))
        self.conn.commit()
        return True

    def get_filenames(self):
        return pd.read_sql_query('''SELECT * FROM files''', self.conn)


