import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import os

import torch

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
        if not hasattr(self, 'initialized'):
        # Check if the instance is already initialized
            self.conn = sqlite3.connect(file_path, check_same_thread=False)

            self.cur = self.conn.cursor()
            self.filename = 'emptyfile'
            self.initialized = True  # Mark the instance as initialized
            # self.drop_database()
            self.create_tables()
        return

    @classmethod
    def reset(cls):
        if cls._instance:
            cls._instance.conn.close()
        cls._instance = None


    ########################################################################
    #                         Database manipulation                        #
    ########################################################################

    def create_tables(self):
        """
        Creates tables files, events, mapping, clusters, sequences, context_events via SQLite

        Returns
        -------
            None
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS files
                                (filename TEXT PRIMARY KEY, custom_name TEXT, run BOOLEAN NOT NULL)''')
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
                               (id_sequence INTEGER, filename TEXT, id_cluster INTEGER, mapping_value INT, risk_label INT,
                               PRIMARY KEY(id_sequence, filename),
                               FOREIGN KEY (filename) REFERENCES files(filename), 
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
        return True

    def drop_database(self):
        """
        Deletes all the tables in the database

        Returns
        -------
            None
        """
        # Fetch the list of all tables in the database
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        # Iterate over the list of tables and drop each table
        for table_name in tables:
            # Each table_name is a tuple, so get the first element
            self.cur.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
        self.conn.commit()
        return

    def switch_current_file(self, filename):
        """
        Switches currently used file if indicated filename exists in the database
        Parameters
        ----------
            filename (str) : name of file to become a currently used file
        Returns
        -------
            True : if new filename was found in the database and then successfully set as a current file
            False : if new filename does not exist in the database
        """
        # Check if the filename exists in the database
        if filename in self.get_filenames().values.flatten().tolist():
            self.filename = filename
            return True
        return False

    ########################################################################
    #                         Data insertion                               #
    ########################################################################
    def store_input_file(self, input_file_df: pd.DataFrame, filename) -> bool:
        """
        Saves input_file_df dataframe generated from input csv file into events table under corresponding filename.
        Also saves name of the input file into files table.

        Parameters
        ----------
            input_file_df (pd.DataFrame) : contains initial information about all events
            filename (str) : name of the file DeepCase should perform analysis onto
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            now = datetime.now()
            # Append current datetime to the filename
            self.filename = filename + '_' + now.strftime("%Y-%m-%d %H:%M:%S")
            self.cur.execute("INSERT  INTO files (filename, custom_name, run) VALUES (?, ?, ?)",
                             (self.filename, self.filename, 0))
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def store_sequences(self, sequence_df: pd.DataFrame) -> bool:
        """
        Saves sequence_df dataframe produced by DeepCase sequencing function into sequence table under corresponding filename.

        Parameters
        ----------
            sequence_df (pd.DataFrame) : contains data about main events of the sequences
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            # Upload to sequence table
            sequence_df['filename'] = self.filename
            sequence_df.reset_index(inplace=True)
            sequence_df.rename(columns={'index': 'id_sequence'}, inplace=True)
            sequence_df.to_sql('sequences', con=self.conn, if_exists='append', index=False)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def store_mapping(self, mapping) -> bool:
        """
        Saves mapping of events codes to events names produced by DeepCase sequencing function into mapping table under corresponding filename.

        Parameters
        ----------
            mapping (dict) : dictionary where key is the unique id of event, and value is the name of the corresponding events
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            for key, value in mapping.items():
                self.cur.execute("INSERT OR REPLACE INTO mapping (id, name, filename) VALUES (?, ?, ?)",
                                 (key, value, self.filename))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        # Iterate through dict and upload to mapping table

    def store_context(self, context_df: pd.DataFrame) -> bool:
        """
        Saves dataframe with context events of the sequence produced by DeepCase sequencing function
        into context_events table under corresponding filename. The dataframe rows correspond to the sequence already
        stored in the database, and columns are the context events to the sequence in the order of their occurrence
        from 0 to 9.

        Parameters
        ----------
            context_df (pd.DataFrame) : contains data about ten context events of the sequence
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            context_df['filename'] = self.filename
            context_df.to_sql('context_events', con=self.conn, if_exists='append', index=False)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def store_clusters(self, clusters_df: pd.DataFrame) -> bool:
        """
        Saves clusters_df dataframe produced by DeepCase clustering function into sequence table under corresponding filename.
        Each of the clusters id aligns to a unique per-file sequence id.

        Parameters
        ----------
            clusters_df (pd.DataFrame) : contains the ids of clusters for each sequence
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """

        try:
            clusters_old_df = pd.read_sql_query('''SELECT * FROM sequences WHERE filename = ?''', self.conn,
                                                params=[self.filename])
            other_clusters_df = pd.read_sql_query('''SELECT * FROM sequences WHERE NOT filename = ?''', self.conn,
                                                  params=[self.filename])
            clusters_df['id_sequence'] = clusters_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
            clusters_old_df['id_sequence'] = clusters_old_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
            # Append updated attention column to the old attention dataframe
            merged_df = clusters_old_df.merge(clusters_df, on='id_sequence', how='left', suffixes=('', '_updated'))

            merged_df.drop(columns='id_cluster', inplace=True)
            merged_df.rename(columns={'id_cluster_updated': 'id_cluster'}, inplace=True)

            merged_df['filename'] = self.filename
            result_df = pd.concat([merged_df, other_clusters_df], ignore_index=True)
            result_df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)

            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def store_attention(self, attention_df: pd.DataFrame) -> bool:
        """
        Stores attention vector produced by DeepCase into context_events table under corresponding filename.
        Input dataframe contains attention to all the context events already stored in the databasae. The function
        performs mapping between context event and its attention

        Parameters
        ----------
            attention_df (pd.DataFrame) : attention vector of context events
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """

        try:
            attention_old_df = pd.read_sql_query('''SELECT * FROM context_events WHERE filename = ?''', self.conn,
                                                 params=[self.filename])
            other_attention_df = pd.read_sql_query('''SELECT * FROM context_events WHERE NOT filename = ?''', self.conn,
                                                   params=[self.filename])

            attention_df['id_sequence'] = attention_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
            attention_old_df['id_sequence'] = attention_old_df['id_sequence'].apply(pd.to_numeric, errors='coerce')
            # Append updated attention column to the old attention dataframe
            merged_df = attention_old_df.merge(attention_df, on=['id_sequence', 'event_position'], how='left',
                                               suffixes=('', '_updated'))

            merged_df.drop(columns='attention', inplace=True)
            merged_df.rename(columns={'attention_updated': 'attention'}, inplace=True)

            merged_df['filename'] = self.filename
            # Remove old records
            result_df = pd.concat([merged_df, other_attention_df], ignore_index=True)

            result_df.to_sql('context_events', con=self.conn, if_exists='replace', index=False)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def fill_cluster_table(self) -> bool:
        """
        Fills in clusters table by extracting unique cluster_ids form sequencing table and assigning them
        risk label that is max risk label among all sequences in the cluster.

        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        query = """SELECT id_cluster, id_cluster AS name_cluster, MAX(risk_label) AS score  
        FROM sequences 
        WHERE filename = ?
        GROUP BY id_cluster;
        """
        try:
            clusters_df = pd.read_sql_query(query, self.conn, params=[self.filename])
            clusters_df['filename'] = self.filename
            other_clusters_df = pd.read_sql_query("SELECT * FROM clusters WHERE NOT filename = ?", self.conn,
                                                  params=[self.filename])
            result_df = pd.concat([clusters_df, other_clusters_df], ignore_index=True)
            result_df.to_sql("clusters", con=self.conn, if_exists='replace', index=False)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def set_cluster_name(self, id_cluster: int, name_cluster: str) -> bool:
        """
        Updates the name of the existing cluster into the custom one.

        Parameters
        ----------
            id_cluster (int) : id of cluster which name is to be changed
            name_cluster (str) : new name to be assigned to a selected cluster
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            query = "UPDATE clusters SET name_cluster = ? WHERE id_cluster = ? AND filename = ?"
            self.cur.execute(query, (name_cluster, id_cluster, self.filename))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def set_risk_value(self, event_id, risk_value) -> bool:
        """
        Updates the risk label of the selected sequence.

        Parameters
        ----------
            event_id (int) : unique id of the event which score is to be changed
            risk_value (int) : new risk value to set to selected event
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            query = "UPDATE sequences SET risk_label = ? WHERE id_sequence = ? AND filename = ?"
            self.cur.execute(query, (risk_value, event_id, self.filename))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def set_file_name(self, filename: str, new_name: str) -> bool:
        """
        Updates the file name of the selected file.

        Parameters
        ----------
            filename (str) : unique name of the file to be changed
            new_name (str) : custom filename to set to selected file
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            query = "UPDATE files SET custom_name = ? WHERE filename = ?"
            self.cur.execute(query, (new_name, filename))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def set_run_flag(self) -> bool:
        """
        Changes run status to True when DeepCase finishes its analysis on the selected file.

        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            query = "UPDATE files SET run = 1 WHERE filename = ?"
            self.cur.execute(query, [self.filename])
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    ########################################################################
    #                         Data update                                  #
    ########################################################################
    def update_cluster_table(self, ):  # why comma
        """
        Updates the risk label of all the clusters.

        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
            query = """SELECT sequences.id_cluster, clusters.name_cluster, MAX(risk_label) AS score  
                            FROM sequences, clusters
                            WHERE sequences.filename = ?
                            AND sequences.filename = clusters.filename
                            AND sequences.id_cluster = clusters.id_cluster
                            GROUP BY sequences.id_cluster;
                            """
            clusters_df = pd.read_sql_query(query, self.conn, params=[self.filename])
            clusters_df['filename'] = self.filename
            other_clusters_df = pd.read_sql_query("SELECT * FROM clusters WHERE NOT filename = ?", self.conn,
                                                  params=[self.filename])
            result_df = pd.concat([clusters_df, other_clusters_df], ignore_index=True)
            result_df.to_sql("clusters", con=self.conn, if_exists='replace', index=False)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_sequence_score(self, score_df: pd.DataFrame):
        """
        Updates the risk label of all the sequences as the result of DeepCase analysis.

        Parameters
        ----------
            score_df (pd.DataFrame) : dataframe containing all the new scores for each sequence
        Returns
        -------
            (bool) : False if execution failed, true otherwise
        """
        try:
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
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    ########################################################################
    #                         Data aggregation                             #
    ########################################################################
    def get_input_table(self) -> pd.DataFrame:
        """
        Retrieves info events table corresponding to the initial data passed to DeepCase.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the events in the format initially passed to DeepCase
        """
        # columns: timestamp,machine,event,label
        return pd.read_sql_query('''SELECT * FROM events WHERE filename = ?''', self.conn, params=[self.filename])

    def get_sequences(self) -> pd.DataFrame:
        """
        Retrieves all the sequences main events from database.

        Returns
        -------
            results (pd.DataFrame) : dataframe with all the sequences including the detailed info about each event
        """
        # columns: main_event_name, timestamp, machine,  id_cluster, risk_label
        result = pd.read_sql_query('''SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label 
                                        FROM mapping, sequences, events 
                                        WHERE sequences.mapping_value = mapping.id 
                                        AND events.id_event = sequences.id_sequence
                                        AND sequences.filename = ?
                                        AND events.filename = sequences.filename
                                        AND mapping.filename = sequences.filename''', self.conn, params=[self.filename])

        return result

    def get_sequence_by_id(self, sequence_id: int) -> pd.DataFrame:
        """
        Retrieves the chosen by id sequence's main event from database.
        Parameters:
        -----------
            sequence_id (int) : unique id of a chosen sequence
        Returns
        -------
            result (pd.DataFrame) : dataframe with the specified sequence including the detailed info about each event
        """
        query = """SELECT mapping.name, events.timestamp, events.machine, sequences.id_cluster, sequences.risk_label 
                FROM mapping, sequences, events 
                WHERE sequences.mapping_value = mapping.id 
                AND events.id_event = ?
                AND sequences.id_sequence = ?
                AND sequences.filename = ?
                AND mapping.filename = sequences.filename
                AND events.filename = sequences.filename"""
        result = pd.read_sql_query(query, self.conn, params=[sequence_id,sequence_id, self.filename])

        return result

    def get_context_by_sequence_id(self, sequence_id: int) -> pd.DataFrame:
        """
        Retrieves context events of the chosen sequence from database.
        Parameters:
        -----------
            sequence_id (int) : unique id of a chosen sequence
        Returns
        -------
            result (pd.DataFrame) : dataframe with the specified context events including the detailed info about each event
        """
        # columns:  event_position, event_name, attention
        query = """SELECT context_events.event_position, mapping.name, context_events.attention 
                FROM mapping, context_events 
                WHERE context_events.mapping_value = mapping.id 
                AND context_events.id_sequence = ? 
                AND context_events.filename = ?
                AND context_events.filename = mapping.filename"""

        # parameterized query to avoid sql injection
        result = pd.read_sql_query(query, self.conn, params=[sequence_id, self.filename])
        return result

    def get_clusters(self) -> pd.DataFrame:
        """
        Retrieves all the clusters of specified filename from database.

        Returns
        -------
            result (pd.DataFrame) : dataframe with all the clusters stored in the database related to a specific dataframe
        """
        result = pd.read_sql_query('''SELECT * FROM clusters WHERE filename = ?''', self.conn, params=[self.filename])
        return result

    def get_sequences_per_cluster(self, cluster_id: int) -> pd.DataFrame:
        """
        Retrieves all teh sequences in the selected cluster
        Parameters:
        -----------
            cluster_id (int) : id of a cluster

        Returns
        -------
            result (pd.DataFrame) : dataframe with the specified sequences per cluster
             including the detailed info about each event
        """
        query = """SELECT mapping.id as id_event, sequences.id_sequence, mapping.name, events.timestamp, events.machine, 
                sequences.id_cluster, sequences.risk_label
                FROM mapping, sequences, events 
                WHERE sequences.mapping_value = mapping.id 
                AND events.id_event = sequences.id_sequence 
                AND sequences.id_cluster = ? 
                AND sequences.filename = ?
                AND events.filename = sequences.filename
                AND mapping.filename = sequences.filename"""
        result = pd.read_sql_query(query, self.conn, params=[float(cluster_id), self.filename])
        return result

    def get_mapping(self) -> pd.DataFrame:
        """
        Retrieves the mapping events name of the considered file.

        Returns
        -------
            result (pd.DataFrame) : dataframe with the events' unique mapping
        """
        query = """SELECT  mapping.name, mapping.id 
                FROM mapping 
                WHERE filename = ?"""
        result = pd.read_sql_query(query, self.conn, params=[self.filename])
        return result

    def get_filenames(self):
        """
        Retrieves all the files currently stored in the database.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the files from database
        """
        return pd.read_sql_query('''SELECT custom_name FROM files''', self.conn)

    def is_file_saved(self):
        """
        Checks whether events were stored in the events table from the input file. This check is necessary to confirm
        that input data was transferred from file into a database.

        Returns
        -------
            (bool) : status whether the events of the considered file are stored in the database
        """
        self.conn.commit()
        self.cur.execute("SELECT * FROM events WHERE filename = ?", (self.filename,))
        self.conn.commit()
        result = self.cur.fetchone()
        return result is not None  # may be revisited

    def display_current_file(self) -> str:
        """
        Returns the name of the file DeepCase uses for processing at the moment.

        Returns
        -------
            (str) : teh name of the currently selected file
        """
        return self.filename

    def get_context_for_automatic(self):
        """
        Retrieve the context events by filename

        Returns
        -------
            result_tensor (torch.Tensor) : tensor with all the events
        """
        query = """
        SELECT id_sequence, mapping_value
        FROM context_events
        WHERE filename = ?
        ORDER BY id_sequence, event_position
        """
        # Execute the query and load the results into a pandas DataFrame
        df = pd.read_sql_query(query, self.conn, params=[self.filename])
        grouped = df.groupby('id_sequence')['mapping_value'].apply(lambda x: np.array(x.tolist()))
        result_array = np.stack(grouped.values)
        result_tensor = torch.from_numpy(result_array)
        if torch.cuda.is_available():
            result_tensor = result_tensor.to('cuda')
        return result_tensor

    def get_events_for_automatic(self):
        """
        Retrieve the sequences by filename

        Returns
        -------
            result_tensor (torch.Tensor) : tensor with all the sequences
        """
        query = """
        SELECT id_sequence, mapping_value
        FROM sequences
        WHERE filename = ?
        ORDER BY id_sequence
        """

        df = pd.read_sql_query(query, self.conn, params=[self.filename])
        result_array = np.stack(df["mapping_value"].values)

        result_tensor = torch.from_numpy(result_array)
        if torch.cuda.is_available():
            result_tensor = result_tensor.to('cuda')
        return result_tensor

    def get_run_flag(self):
        """
        Retrieve the run flag of the current file

        Returns
        -------
            (int) : status flag indicating whether DeepCase was run on selected file
        """
        query = "SELECT run FROM files WHERE filename = ?"
        status_df = pd.read_sql_query(query, self.conn, params=[self.filename])
        return status_df.iloc[0]['run']
