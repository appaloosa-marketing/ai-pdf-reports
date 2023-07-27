import pandas as pd
import v2.process as data
import plotly.graph_objects as go
from weasyprint import HTML
import os
import chatgpt
from data import df2, df3, tacos_df, engagement_df
    
# remember to put openai key & org in the enviornment
# consider setting these df = 0 by default so the function will work without all the data.


def generate(amazon_df, shopify_df, tacos_df, engagement_df):

    # Bar Chart of ROAS of all channels
    fig = go.Figure(data=[
        go.Bar(name='Spend', x=df2['Channel'], y=df2['Cost']),
        go.Bar(name='Revenue', x=df2['Channel'], y=df2['Revenue'])
    ])

    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.write_image('roas-chart.png')


  
    # Convert pandas DataFrames to HTML
    summary_html = df3.to_html(index=False)
    tacos_html = tacos_df.to_html(index=False)
    engagement_html = engagement_df.to_html(index=False)
    
    
    ## Get insights with ChatGPT ##
    insights = chatgpt.turbo_insights()
    
    # Report content to be read by GPT-4
    report_content = f"""<section>
            <h2>Executive Summary</h2>
            {summary_html}
            <p>Disclaimer: Currently, our reports cannot track Amazon purchases using Meta Ads due to platform limitations.</p>
            <img src="roas-chart.png" alt="Bar Graph">
            <p>Disclaimer: Currently, our reports cannot track Amazon purchases using Meta Ads due to platform limitations.</p>
        </section>
        <section class='boring'>
            <h3 style="text-decoration: underline">tACOS - Total Advertising Cost of Spend</h3>
            <p>Your advertising spend relative to your sales. The lower the better. </p>
            {tacos_html}
        </section>
        <section class='boring'>
            <h3 style="text-decoration: underline">Engagement</h3>
            <p>Clicks, Impressions, and Click Through Rate (CTR) </p>
            {engagement_html}
        </section>"""
    
 
    # HTML content
    html_report = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
        <style>
            body {{font-family: 'Montserrat', sans-serif;}}
            .gray-background {{background-color: gray;}}
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
            tr:nth-child(even) {{background-color: #f2f2f2;}}
            tr:last-child {{background-color: #ffffa1; font-weight: bold;}}
            tr:first-child {{background-color: #ffffff;}}
            .boring tr:last-child {{background-color: white; font-weight: normal;}}
        </style>
    </head>
    <body>
        <header style="text-align: center;">
            <img src="logo/150px.jpg" alt="Company Logo" style="max-width: 100%;">
            <h1>Marketing Performance Report</h1>
            <p>Overview of marketing channels this month.</p>
            <hr style="width:80%; border: none; border-top: 3px solid #F0E2B6;">
        </header>
        {report_content}
        
            <h3>Insights</h3>
            <p>{insights}</p>
            <section>
            <h3>Definitions</h3>
            <ul>
                <li><strong>Click Through Rate (CTR)</strong>: The percentage of individuals who click on a presented link from total viewers.</li>
                <li><strong>ROAS - Return on Advertising Spend</strong>: The revenue earned per dollar spent on advertising.</li>
                <li><strong>Engagement</strong>: Any interaction a customer has with a brand or its content.</li>
                <li><strong>Omnichannel Marketing</strong>: A strategy providing a seamless customer experience across all channels.</li>
            </ul>
    
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
        f.write(html_report)
    
    # Use WeasyPrint to convert the HTML to PDF
    HTML('report.html').write_pdf('v2/mock-report.pdf')
    
    # Remove temporary files
    os.remove("roas-chart.png")
    os.remove("report.html")
