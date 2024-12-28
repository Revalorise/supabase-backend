from flask import Flask, render_template
from supabase_connect import fetch_data

app = Flask(__name__)
# flask --app app run --debug

@app.route('/')
def hello_world():
    data = fetch_data()
    return render_template(
        'home.html',
        id=data[0], created_at=data[1], mac=data[2], amount=data[3],
        email=data[4], type=data[5], m_name=data[6], success=data[7])


if __name__ == '__main__':
    app.run(debug=True)
