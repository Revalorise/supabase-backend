from flask import Flask, render_template, request
from supabase_connect import fetch_all_data, get_filtered_data, fetch_all_data_v2

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

    return render_template(
        'main_test.html', data=filtered_data,
        columns=fields, selected_columns=selected_columns)


if __name__ == '__main__':
    app.run(debug=True)
