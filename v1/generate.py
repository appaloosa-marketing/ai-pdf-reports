import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image
from weasyprint import HTML
import os
from data import df1, df2, x_data, y_data, y2_data, time_df
# from data import df1_last_month, df2_last_month # if comparing data
import chatgpt

def mock_report():
    
    ## Get insights with ChatGPT ##
    insights = chatgpt.turbo_insights()
    
    ## Create bar graoh with Plotly (for HTML) ##
    
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

    
    ## HTML content of report with styling ##
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
        <section>
            <h3>Insights</h3>
                <p>{insights}</p>
        </section>
        <footer style="text-align: center;>
            <p>2023 Appaloosa Marketing LLC</p>
            <img src="logo/100px.jpg" alt="Company Logo" style="max-width: 100%;">
        </footer>
    </body>
    </html>
    """

    
    ## Export HTML as local PDF ##
    with open('report.html', 'w') as f:
        f.write(html_content)
    
    # Use WeasyPrint to convert the HTML to PDF
    HTML('report.html').write_pdf('v1/mock-report.pdf')
    
    # Remove temporary files
    os.remove("bar.png")
    os.remove("line.png")
    os.remove("report.html")
