import sqlite3
import pandas as pd

# SQL query to obtain the top X views of a specific show type and duration.
def get_top_x_shows(show_type, x, duration):
    conn = sqlite3.connect('../DDBB/DataWarehouse.db')
    if show_type == 'Movie':
        query = f"""
                SELECT s.title, COUNT(*) as num_views
                FROM views v
                JOIN show s ON v.show_id = s.show_id
                WHERE s.type = '{show_type}'
                AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) {'>' if duration == 'Over 90 min' else '<='} 90
                GROUP BY s.title
                ORDER BY num_views DESC
                LIMIT {x}
            """
    elif show_type == 'TV Show':
        seasons = {'1': 1, '2': 2, '3': 3}
        num_seasons = seasons[duration]
        query = f"""
                SELECT s.title, COUNT(*) as num_views
                FROM views v
                JOIN show s ON v.show_id = s.show_id
                WHERE s.type = '{show_type}'
                AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) {'=' if num_seasons <= 2 else '>='} {num_seasons}
                GROUP BY s.title
                ORDER BY num_views DESC
                LIMIT {x}
            """
    df = pd.read_sql_query(query, conn)
    return df

# Type Selection

types = ['Movie','TV Show']
print('Types of audiovisual material available:')
for i, type in enumerate(types):
    print(f'{i+1}. {type}')
type = ''
while type not in types:
    type = input('Enter the desired type (Movie or TV Show): ')
    if type not in types:
        print('Invalid type. Please enter Movie or TV Show.')

# Top Selection

top = int(input('Enter the number of items of the desired top: '))

# Duration Selection

duration = ''
if type == 'Movie':
        while duration not in ['Over 90 min', 'Less or equal to 90 min']:
            duration = input('Do you wish to include films longer than 90 minutes? (y/n): ')
            if duration.lower() == 'y':
                duration = 'Over 90 min'
            elif duration.lower() == 'n':
                duration = 'Less or equal to 90 min'
            else:
                print('Invalid answer. Please enter y or n.')
elif type == 'TV Show':
        while duration not in ['1', '2', '3']:
            print()
            print('Warning: The 3 looks for series with 3 or more seasons.')
            duration = input('How many seasons would you like to include (1, 2, 3):')
            if duration not in ['1', '2', '3']:
                print('Invalid answer. Please enter 1, 2 or 3+.')


# We obtain the result of the SLICE & DICE in a
# data frame and print the result

result = get_top_x_shows(type, top, duration)
print(result)

