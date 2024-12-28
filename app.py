from flask import Flask, render_template, request
from supabase_connect import fetch_all_data, get_filtered_data

app = Flask(__name__)
# flask --app app run --debug

fields = ['id', 'created_at', 'mac', 'amount', 'email', 'type', 'm_name', 'success']

@app.route('/')
def hello_world():
    data = fetch_all_data()
    return render_template(
        'home.html',
        id=data[0], created_at=data[1], mac=data[2], amount=data[3],
        email=data[4], type=data[5], m_name=data[6], success=data[7],
        fields=fields)

"""
@app.route('/filter', methods=['POST'])
def filtered_data_page():
    id = request.form.get('id')
    created_at = request.form.get('created_at')
    mac = request.form.get('mac')
    amount = request.form.get('amount')
    email = request.form.get('email')
    type = request.form.get('type')
    m_name = request.form.get('m_name')
    success = request.form.get('success')
    filtered_column = [
        column for column in
        [id, created_at, mac, amount, email, type, m_name, success]
        if column is not None]

    data = get_filtered_data(filtered_column)
    return render_template('home.html', data=data, fields=fields)
"""

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
