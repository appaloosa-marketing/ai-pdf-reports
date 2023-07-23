import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image
from weasyprint import HTML
import os

# Mock data for df1: Executive Summary
data1 = {
    'Marketing Channel': ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'],
    'Cost': [1000, 2000, 1500, 1800],
    'Revenue': [4000, 5000, 3500, 4800]
}
df1 = pd.DataFrame(data1)

# Mock data for df2: Channel 1 Performance
data2 = {
    'Metric': ['Impressions', 'Clicks', 'Conversions'],
    'Value': [10000, 200, 50],
}
df2 = pd.DataFrame(data2)

# Mock Last Month
data1_last_month = {
    'Marketing Channel': ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'],
    'Cost': [1000, 2000, 1500, 1800],
    'Revenue': [3500, 4500, 3000, 4300]
}
df1_last_month = pd.DataFrame(data1_last_month)

# Mock data for df2_last_month: Channel 1 Performance
data2_last_month = {
    'Metric': ['Impressions', 'Clicks', 'Conversions'],
    'Value': [9000, 180, 45],
}
df2_last_month = pd.DataFrame(data2_last_month)

# Mock data for the graphs
x_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
y_data = [1000, 1200, 1100, 1300, 1200, 1400, 1500, 1600, 1700, 1800, 1900, 2000]  # Cost
y2_data = [4000, 4500, 4300, 4800, 4700, 5000, 5200, 5400, 5600, 5800, 6000, 6200]  # Revenue

# Create a Plotly bar graph and save as image
fig1 = go.Figure(data=[go.Bar(name='Marketing Channels', x=x_data, y=y_data)])
fig1.write_image('bar.png')

# Create a Plotly line graph and save as image
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x_data, y=y_data, name='Channel 1 Cost'))
fig2.add_trace(go.Scatter(x=x_data, y=y2_data, name='Channel 1 Revenue'))
fig2.update_layout(yaxis2=dict(overlaying='y', side='right'))
fig2.write_image('line.png')

# Convert pandas DataFrames to HTML
df1_html = df1.to_html(index=False)
df2_html = df2.to_html(index=False)

df1_last_month_html = df1_last_month.to_html(index=False)
df2_last_month_html = df2_last_month.to_html(index=False)

# HTML content
html_content = f"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    <style>
        body {{font-family: 'Montserrat', sans-serif;}}
        .gray-background {{background-color: gray;}}
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
        tr:nth-child(even) {{background-color: #f2f2f2;}}
    </style>
</head>
<body>
    <header style="text-align: center;">
        <img src="logo/150px.jpg" alt="Company Logo" style="max-width: 100%;">
        <h1>Marketing Performance Report</h1>
        <p>Overview of marketing channels this month.</p>
        <hr style="width:80%; border: none; border-top: 3px solid #F0E2B6;">
    </header>
    <section>
        <h2>Executive Summary</h2>
        {df1_html}
        <img src="bar.png" alt="Bar Graph">
    </section>
    <section>
        <h3 style="text-decoration: underline">Channel 1 Performance</h3>
        <p>Cost, Revenue, and Engagement</p>
        {df2_html}
    </section>
    <section>
        <h3>Channel 1 History</h3>
        <p>Cost & Revenue of Channel 1 over Time</p>
        <img src="line.png" alt="Line Graph">
    </section>
    <footer style="text-align: center;>
        <p>2023 Appaloosa Marketing LLC</p>
        <img src="logo/100px.jpg" alt="Company Logo" style="max-width: 100%;">
    </footer>
</body>
</html>
"""

# HTML content
last_month_html_content = f"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    <style>
        body {{font-family: 'Montserrat', sans-serif;}}
        .gray-background {{background-color: gray;}}
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
        tr:nth-child(even) {{background-color: #f2f2f2;}}
    </style>
</head>
<body>
    <header style="text-align: center;">
        <img src="logo/150px.jpg" alt="Company Logo" style="max-width: 100%;">
        <h1>Marketing Performance Report</h1>
        <p>Overview of marketing channels this month.</p>
        <hr style="width:80%; border: none; border-top: 3px solid #F0E2B6;">
    </header>
    <section>
        <h2>Executive Summary</h2>
        {df1_last_month_html}
        <img src="bar.png" alt="Bar Graph">
    </section>
    <section>
        <h3 style="text-decoration: underline">Channel 1 Performance</h3>
        <p>Cost, Revenue, and Engagement</p>
        {df2_last_month_html}
    </section>
    <section>
        <h3>Channel 1 History</h3>
        <p>Cost & Revenue of Channel 1 over Time</p>
        <img src="line.png" alt="Line Graph">
    </section>
    <footer style="text-align: center;>
        <p>2023 Appaloosa Marketing LLC</p>
        <img src="logo/100px.jpg" alt="Company Logo" style="max-width: 100%;">
    </footer>
</body>
</html>
"""

# Save the HTML content as an HTML file
with open('report.html', 'w') as f:
    f.write(html_content)

# Use WeasyPrint to convert the HTML to PDF
HTML('report.html').write_pdf('report.pdf')

# Remove temporary files
os.remove("bar.png")
os.remove("line.png")
os.remove("report.html")