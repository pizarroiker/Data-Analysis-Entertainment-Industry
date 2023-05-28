import pandas as pd
import sqlite3

# Connection to the database
con = sqlite3.connect('../DDBB/DataWarehouse.db')

# Query to obtain the display data and user_id
query = '''SELECT show.type,show.country,show.release_year,show.listed_in,CAST(show.duration as 
integer) as duration, COUNT(views.show_id) as num_views, 
AVG(views.avg_rating) as avg_user_rating FROM show LEFT JOIN views ON show.show_id = 
views.show_id GROUP BY show.show_id'''

# Reading the result in a dataframe
df = pd.read_sql(query, con)

# Convert NaN values to strings
df = df.fillna('')
df = df.replace('\n', ' ', regex=True)

# Convert to a number
df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0)
df['avg_user_rating'] = pd.to_numeric(df['avg_user_rating'], errors='coerce').fillna(0)

# Create columns for each show type in listed_in
df['listed_in'] = df['listed_in'].str.strip()
df_listed_in = df['listed_in'].str.get_dummies(', ')
df = pd.concat([df, df_listed_in], axis=1)
df = df.drop('listed_in', axis=1)

# Create columns for each country in country
df['country'] = df['country'].str.strip()
df_listed_in = df['country'].str.get_dummies(', ')
df = pd.concat([df, df_listed_in], axis=1)
df = df.drop('country', axis=1)

# Add class attribute {good(>7),bad(<4),average(rest)} by rating

df.loc[df['avg_user_rating'] > 7, 'class'] = 'good'
df.loc[df['avg_user_rating'] < 4, 'class'] = 'bad'
df.loc[(df['avg_user_rating'] >= 4) & (df['avg_user_rating'] <= 7), 'class'] = 'mid'

df = df.drop('avg_user_rating', axis=1)



# Convert Pandas DataFrame to ARFF file
with open('shows_data.arff', 'w', encoding='utf-8') as f:
    f.write('@relation shows_data\n\n')
    # Type the column names as attributes
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_values = [str(x) if x is not None else '' for x in set(df[col].tolist())]
            if col == "class":
                f.write('@attribute ' + col + ' {' + ','.join(filter(None, unique_values)) + '}\n')
            else:
                f.write('@attribute "' + col + '" {"' + '","'.join(filter(None, unique_values)) + '"}\n')
        else:
            f.write('@attribute "' + col + '" numeric\n')
    f.write('\n@data\n')
    # Write the data for each row in the file
    for i, row in df.iterrows():
        values = []
        for col in df.columns:
            if df[col].dtype == 'object':
                values.append("'" + str(row[col]) + "'")
            else:
                values.append(str(row[col]))
        f.write(','.join(values) + '\n')


