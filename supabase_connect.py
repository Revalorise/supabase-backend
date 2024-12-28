import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

data = supabase.table('users').select("*").execute().model_dump_json(indent=4)
print(data)
file = json.loads(data)
# print(file.get('data')[0].get('id'))


def fetch_data():
    fields = ['id', 'created_at', 'mac', 'amount', 'email', 'type', 'm_name', 'success']
    data = {field: [] for field in fields}

    for row in file.get('data'):
        for field in fields:
            data[field].append(row.get(field))

    return tuple(data[field] for field in fields)


test = fetch_data()
print(test)
