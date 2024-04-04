from datetime import datetime
import sqlite3
import pandas as pd
import os
from database import Database

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "deepcase.db")

# conn = sqlite3.connect(db_path)
# cur = conn.cursor()
# cur.execute('''SELECT sequences.id_sequence, temporary.id_cluster
#             FROM sequences, temporary
#             WHERE sequences.id_sequence = temporary.id_sequence''')

# db.drop_database()
#
#
# # Sample data for df1
# data1 = {
#     'id_sequence': [1, 2, 3,172567],
#     'attention': [0.1, 0.2, 0.3, 12]
# }
# df1 = pd.DataFrame(data1)
#
# df2 = attention_old_df = pd.read_sql_query('''SELECT * FROM context_events''', conn)
# print(df2)
#
# # Merging df1 into df2 on 'sequence_id' to fill 'attention' values
# # Note: This creates a new column for attention from df1, we'll handle it next
# merged_df = df2.merge(df1, on='id_sequence', how='left', suffixes=('', '_updated'))
#
# # Ensure 'attention' columns are of a numeric type
# # merged_df['attention'] = pd.to_numeric(merged_df['attention'], errors='coerce')
# # merged_df['attention'] = pd.to_numeric(merged_df['attention_from_df1'], errors='coerce')
# cols_to_convert = ['attention', 'attention_updated']
# merged_df[cols_to_convert] = merged_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
# # Filling null values in 'attention' column with values from 'attention_from_df1'
# merged_df['attention'] = merged_df['attention'].fillna(merged_df['attention_updated'])
# merged_df.drop(columns=['mapping_value'], inplace=True)
# print(merged_df)
# # Dropping the extra 'attention_from_df1' column as it's no longer needed
# merged_df.drop(columns=['attention_updated'], inplace=True)
#
#
# # df = pd.read_sql_query('''SELECT sequences.id_sequence, temporary.id_cluster, sequences.mapping_value, sequences.risk_label
# #             FROM sequences, temporary
# #              WHERE sequences.id_sequence = temporary.id_sequence''', conn)
# # df.to_sql('sequences', con=conn, if_exists='replace', index=False)
#
# # print(df)
#
#
# # rows = cur.fetchall()
# # for row in rows:
# #     print(row)
#
# # UPDATE table1
# # SET status = (SELECT t2.status FROM table2 t2 WHERE t2.trans_id = table1.id) ,
# #     name = (SELECT t2.name FROM table2 t2 WHERE t2.trans_id = table1.id)
# # WHERE id IN (SELECT trans_id FROM table2 t2 WHERE t2.trans_id= table1.id);
#
# # cur.execute('''
# #             UPDATE sequences
# #             SET id_cluster = (SELECT tm.id_cluster
# #                               FROM temporary tm
# #                               WHERE  tm.id_sequence = id_sequence)
# #             WHERE EXISTS (SELECT 1
# #                           FROM temporary tm
# #                           WHERE tm.id_sequence = sequences.id_sequence)
# #             ''')
#
# conn.commit()

# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Create a file path for "example.txt" in the script's directory
# file_path = os.path.join(script_dir, 'deepcase.db')
# conn = sqlite3.connect(file_path, check_same_thread=False)
# cur = conn.cursor()
#
#
# # print(pd.read_sql_query("SELECT sequences.id_cluster, MAX(sequences.risk_label) FROM sequences", conn))
#
# def fill_cluster_table():
#     # take unique ids from sequences table + max score per sequence
#     get_unique_ids_query = "SELECT DISTINCT sequences.id_cluster, sequences.risk_label FROM sequences"
#     get_unique_ids_query = """ SELECT id_cluster, MAX(risk_label) AS risk_label FROM sequences GROUP BY id_cluster;
#     """
#     return pd.read_sql_query(get_unique_ids_query, conn)
#     get_max_sequence_score_query = "SELECT FROM WHERE"
#

filename = "alerts.csv1710771346.185"
# store_attention
att_df_1 = pd.DataFrame([{'id_sequence': 0, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 1, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 2, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 3, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 4, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 5, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 6, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 7, 'event_position': 0, 'attention': 0.010116898454725742}])
att_df_2 = pd.DataFrame([{'id_sequence': 8, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 9, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 10, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 11, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 12, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 13, 'event_position': 0, 'attention': 0.010116898454725742},
                         {'id_sequence': 14, 'event_position': 0, 'attention': 0.003188725560903549},
                         {'id_sequence': 15, 'event_position': 0, 'attention': 0.002493527252227068}])
att_df_3 = pd.DataFrame([{'id_sequence': 16, 'event_position': 0, 'attention': 0.0025230764877051115},
                         {'id_sequence': 17, 'event_position': 0, 'attention': 0.004003714304417372},
                         {'id_sequence': 18, 'event_position': 0, 'attention': 0.0040802680887281895},
                         {'id_sequence': 19, 'event_position': 0, 'attention': 0.004231778439134359}])

# store_clusters
clust_df_1 = pd.DataFrame(
    [{'id_sequence': 0, 'id_cluster': 1}, {'id_sequence': 1, 'id_cluster': 1}, {'id_sequence': 2, 'id_cluster': 0},
     {'id_sequence': 3, 'id_cluster': 0}, {'id_sequence': 4, 'id_cluster': -1}])
clust_df_2 = pd.DataFrame(
    [{'id_sequence': 5, 'id_cluster': -1}, {'id_sequence': 6, 'id_cluster': -1}, {'id_sequence': 7, 'id_cluster': -1},
     {'id_sequence': 8, 'id_cluster': 8}, {'id_sequence': 9, 'id_cluster': 8}, {'id_sequence': 10, 'id_cluster': -1}])
clust_df_3 = pd.DataFrame(
    [{'id_sequence': 11, 'id_cluster': -1}, {'id_sequence': 12, 'id_cluster': 8}, {'id_sequence': 13, 'id_cluster': 8},
     {'id_sequence': 14, 'id_cluster': 10}, {'id_sequence': 15, 'id_cluster': 10},
     {'id_sequence': 16, 'id_cluster': 13}, {'id_sequence': 17, 'id_cluster': 16},
     {'id_sequence': 18, 'id_cluster': 12}, {'id_sequence': 19, 'id_cluster': 12}])

# store_sequences
seq_df_1 = pd.DataFrame([{'mapping_value': 72, 'risk_label': 3}, {'mapping_value': 72, 'risk_label': 3},
                         {'mapping_value': 72, 'risk_label': 3}, {'mapping_value': 72, 'risk_label': 3}])
seq_df_2 = pd.DataFrame([{'mapping_value': 44, 'risk_label': 3}, {'mapping_value': 44, 'risk_label': 3},
                         {'mapping_value': 42, 'risk_label': 3}, {'mapping_value': 42, 'risk_label': 3}])
seq_df_3 = pd.DataFrame([{'mapping_value': 86, 'risk_label': 3}, {'mapping_value': 86, 'risk_label': 3},
                         {'mapping_value': 87, 'risk_label': 3}, {'mapping_value': 87, 'risk_label': 3}])
seq_df_4 = pd.DataFrame([{'mapping_value': 86, 'risk_label': 3}, {'mapping_value': 86, 'risk_label': 3},
                         {'mapping_value': 87, 'risk_label': 3}, {'mapping_value': 87, 'risk_label': 3}])
seq_df_5 = pd.DataFrame([{'mapping_value': 66, 'risk_label': 3}, {'mapping_value': 66, 'risk_label': 3},
                         {'mapping_value': 66, 'risk_label': 3}, {'mapping_value': 66, 'risk_label': 3}])

db = Database()
db.switch_current_file("alerts.csv_2024-04-04 01:08:13 ")

print(db.get_context_by_sequence_id(0))

# db.store_attention(att_df_1)
# db.store_clusters(clust_df_1)
# db.fill_cluster_table()