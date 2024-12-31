from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from supabase_connect import fetch_all_data, fetch_all_data_v2

from routes.auth import auth_bp
from routes.api import api_bp

import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'blackball007'
CORS(app)
# flask --app app run --debug

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

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

test_data = [
    {"name": "Alice", "category": "A", "age": 25},
    {"name": "Bob", "category": "B", "age": 30},
    {"name": "Charlie", "category": "A", "age": 35},
    {"name": "Dave", "category": "C", "age": 40},
]

columns = ["name", "category", "age"]

@app.route('/test', methods=['GET', 'POST'])
def test():
    """
    Handle the '/test' route for both GET and POST requests.

    For GET requests, it renders the 'test.html' template with all columns and data
    For POST requests, it filters the data based on the selected columns from the form

    Returns:
        Rendered HTML template with filtered data and columns.
    """
    # Get the list of selected columns from the form data
    selected_columns = request.form.getlist('columns')

    # If no columns are selected, use all columns
    if not selected_columns:
        selected_columns = columns

    # Filter the data based on the selected columns
    filtered_data = [
        {key: item[key] for key in selected_columns if key in item} for item in test_data
    ]

    return render_template(
        'test.html', data=filtered_data,
        columns=columns, selected_columns=selected_columns)


@app.route('/main_test', methods=['GET', 'POST'])
def main_test():
    """
    Handle the '/main_test' route for both GET and POST requests.

    For GET requests, it renders the 'main_test.html' template with all columns and data
    For POST requests, it filters the data based on the selected columns from the form

    Returns:
        Rendered HTML template with filtered data and columns.
    """
    main_data = fetch_all_data_v2()

    # Get the list of selected columns from the form data
    selected_columns = request.form.getlist('columns')

    # If no columns are selected, use all columns
    if not selected_columns:
        selected_columns = fields

    # Filter the data based on the selected columns
    filtered_data = [
        {key: item[key] for key in selected_columns if key in item} for item in main_data
    ]

    # Example data
    data = px.data.stocks()

    # Create a Plotly line graph
    fig = px.line(data,
                  x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  title='Stock Prices Over Time')

    # Customize the appearance
    fig.update_layout(
        title='Stock Prices Over Time',
        template='plotly_dark',
        title_font=dict(size=24, family='Courier', color='Orange'),
        xaxis=dict(title='[Date]', showgrid=True, gridwidth=1, gridcolor='LightGray'),
        yaxis=dict(title='[Price]', showgrid=True, gridwidth=1, gridcolor='LightGray'),
        legend=dict(title='[Stock]', orientation='h', y=1.1, x=0.5, font=dict(size=14)),
    )

    # Convert the Plotly figure to HTML
    plot_html = pio.to_html(fig, full_html=False)

    return render_template(
            'main_test.html', data=filtered_data,
            columns=fields, selected_columns=selected_columns,
            plot_html=plot_html)


@app.route('/api/login', methods=['POST'])
def login():
    """
    Handle the '/login' route for both GET and POST requests.

    For GET requests, it renders the 'login.html' template
    For POST requests, it retrieves the username and password from the form data

    Returns:
        Rendered HTML template with the username and password.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == 'admin':
        return redirect(url_for('main_test'))
    return jsonify({'message': 'Invalid credentials!'}), 401


if __name__ == '__main__':
    app.run(debug=True)
