import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_file, render_template, request
import io
import os

app = Flask(__name__)

# Add global variables to store the buffers
global_bar_buf = None
global_pie_buf = None

def create_bar_chart(data, x_column, y_column, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_column], data[y_column])
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def create_pie_chart(data, column, title):
    plt.figure(figsize=(8, 8))
    value_counts = data[column].value_counts()
    plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
    plt.title(title)
    plt.tight_layout()
    
    # Save plot to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global global_bar_buf, global_pie_buf
    
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if not file.filename.endswith('.csv'):
        return 'Please upload a CSV file', 400
    
    # Read CSV file
    df = pd.read_csv(file)
    
    # Get numeric columns for bar chart
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Create bar chart
    if len(numeric_columns) >= 2:
        global_bar_buf = create_bar_chart(df, numeric_columns[0], numeric_columns[1], 
                                 f'{numeric_columns[1]} by {numeric_columns[0]}')
    
    # Create pie chart for the first categorical column
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        global_pie_buf = create_pie_chart(df, categorical_columns[0], 
                                 f'Distribution of {categorical_columns[0]}')
    
    return render_template('charts.html', 
                         bar_chart=True if len(numeric_columns) >= 2 else False,
                         pie_chart=True if len(categorical_columns) > 0 else False)

@app.route('/bar_chart')
def get_bar_chart():
    # Return the last generated bar chart
    if global_bar_buf is None:
        return 'No bar chart available', 404
    global_bar_buf.seek(0)
    return send_file(global_bar_buf, mimetype='image/png')

@app.route('/pie_chart')
def get_pie_chart():
    # Return the last generated pie chart
    if global_pie_buf is None:
        return 'No pie chart available', 404
    global_pie_buf.seek(0)
    return send_file(global_pie_buf, mimetype='image/png')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create HTML templates
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>CSV Visualizer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        form {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        input[type="file"] {
            display: block;
            margin: 20px auto;
            padding: 10px;
            border: 2px dashed #3498db;
            border-radius: 4px;
            width: 80%;
        }
        input[type="submit"] {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <h1>📊 CSV Visualizer</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv">
        <input type="submit" value="Generate Charts">
    </form>
</body>
</html>
        ''')
    
    with open('templates/charts.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Charts</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #2c3e50;
            text-align: center;
        }
        .charts-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }
        .chart-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 30px;
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }
        .back-link:hover {
            color: #2980b9;
        }
    </style>
</head>
<body>
    <h1>📈 Generated Charts</h1>
    <div class="charts-container">
        {% if bar_chart %}
        <div class="chart-box">
            <h2>Bar Chart</h2>
            <img src="{{ url_for('get_bar_chart') }}" alt="Bar Chart">
        </div>
        {% endif %}
        
        {% if pie_chart %}
        <div class="chart-box">
            <h2>Pie Chart</h2>
            <img src="{{ url_for('get_pie_chart') }}" alt="Pie Chart">
        </div>
        {% endif %}
    </div>
    
    <a href="/" class="back-link">← Back to Upload</a>
</body>
</html>
        ''')
    
    app.run(debug=True)
