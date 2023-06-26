import pandas as pd
import sqlite3

# Connect to SQLite database
db_path = 'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe_data.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List of CSV file paths
csv_files = [
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_Trans.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_User.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Map_Trans.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Map_User.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_Trans.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_Trans_Pin.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_User_Dist.csv',
    'C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_User_Pin.csv'
]

# Import CSV data into SQLite database
for file in csv_files:
    table_name = file.split('/')[-1].split('.')[0]  # Extract table name from file name
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Define pandas dataframes
Agg_Trans_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_Trans.csv')
Agg_Trans_df.drop_duplicates(subset=['State', 'Year', 'Quarter', 'Transaction_type', 'Region'],
                             keep='first', inplace=True)
Agg_User_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_User.csv')
Map_Trans_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Map_Trans.csv')
Map_User_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Map_User.csv')
Top_Trans_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_Trans.csv')
Top_Trans_Pin_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_Trans_Pin.csv')
Top_User_Dist_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_User_Dist.csv')
Top_User_Pin_df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Top_User_Pin.csv')

# Create tables in SQLite database
cursor.execute('''CREATE TABLE IF NOT EXISTS agg_trans (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    Transaction_type VARCHAR(255),
                    Transaction_count INTEGER,
                    Transaction_amount FLOAT,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, Transaction_type, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS agg_user (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    Brand VARCHAR(255),
                    Transaction_count INTEGER,
                    Percentage FLOAT,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, Brand, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS map_trans (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    District VARCHAR(255),
                    Transaction_count INTEGER,
                    Transaction_amount FLOAT,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, District, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS map_user (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    District VARCHAR(255),
                    Registered_users INTEGER,
                    App_opens INTEGER,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, District, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS top_trans_dist (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    District VARCHAR(255),
                    Transaction_count INTEGER,
                    Transaction_amount FLOAT,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, District, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS top_trans_pin (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    Pincode VARCHAR(255),
                    Transaction_count INTEGER,
                    Transaction_amount FLOAT,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, Pincode, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS top_user_dist (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    District VARCHAR(255),
                    Registered_users INTEGER,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, District, Region)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS top_user_pin (
                    State VARCHAR(255),
                    Year YEAR,
                    Quarter INTEGER,
                    Pincode VARCHAR(255),
                    Registered_users INTEGER,
                    Region VARCHAR(255),
                    PRIMARY KEY (State, Year, Quarter, Pincode, Region)
                 )''')

# Commit changes and close the connection
conn.commit()
conn.close()


def push_data_into_sqlite(conn, cursor, dfs, table_columns):
    for table_name in dfs.keys():
        df = dfs[table_name]
        columns = table_columns[table_name]
        placeholders = ', '.join(['?'] * len(columns))
        query = f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        for _, row in df.iterrows():
            data = tuple(row[column] for column in columns)
            cursor.execute(query, data)
        conn.commit()


# Mapping my_sql tables to pandas dataframes that we have created earlier
dfs = {
    'agg_trans': Agg_Trans_df,
    'agg_user': Agg_User_df,
    'map_trans': Map_Trans_df,
    'map_user': Map_User_df,
    'top_trans_dist': Top_Trans_df,
    'top_trans_pin': Top_Trans_Pin_df,
    'top_user_dist': Top_User_Dist_df,
    'top_user_pin': Top_User_Pin_df
}

# Mapping table name to associated columns for each table
table_columns = {
    'agg_trans': list(Agg_Trans_df.columns),
    'agg_user': list(Agg_User_df.columns),
    'map_trans': list(Map_Trans_df.columns),
    'map_user': list(Map_User_df.columns),
    'top_trans_dist': list(Top_Trans_df.columns),
    'top_trans_pin': list(Top_Trans_Pin_df.columns),
    'top_user_dist': list(Top_User_Dist_df.columns),
    'top_user_pin': list(Top_User_Pin_df.columns)
}

# Push data into SQLite tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
push_data_into_sqlite(conn, cursor, dfs, table_columns)
conn.close()

print("Data successfully pushed into SQLite tables.")
