import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

sample_data = supabase.table('users').select("*").execute().model_dump_json(indent=4)
print(sample_data)
file = json.loads(sample_data)
# print(file.get('data')[0].get('id'))
fields = ['id', 'created_at', 'mac', 'amount', 'email', 'type', 'm_name', 'success']

def fetch_all_data():
    data = {field: [] for field in fields}

    for row in file.get('data'):
        for field in fields:
            data[field].append(row.get(field))

    return tuple(data[field] for field in fields)


test = fetch_all_data()
print(test)

"""
data = {field: [] for field in fields}
columns = ['id', 'created_at', 'mac']
columns_string = ', '.join(columns)
filtered_data = supabase.table('users').select(f'{columns_string}').execute().model_dump_json(indent=4)
filtered_file = json.loads(filtered_data)
for row in filtered_file.get('data'):
    for column in columns:
        data[column].append(row.get(column))

result = tuple(data[column] for column in columns)

print(result)
"""

def get_filtered_data(columns):
    data = {field: [] for field in fields}
    columns_string = ', '.join(fields)

    filtered_data = supabase.table('users').select(f'{columns_string}').execute().model_dump_json(indent=4)
    filtered_file = json.loads(filtered_data)

    for row in filtered_file.get('data'):
        for column in columns:
            data[column].append(row.get(column))

    return tuple(data[column] for column in columns)
