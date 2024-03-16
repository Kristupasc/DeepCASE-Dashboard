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

db = Database()
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


print(db.get_sequences_per_cluster())
print(db.get_sequences_per_cluster().columns)