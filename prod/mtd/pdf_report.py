import pandas as pd
import plotly.graph_objects as go
from weasyprint import HTML
import os

# import process as summary # for running locally

# amazon_df, shopify_df, tacos_df, engagement_df

def generate(amazon_df, shopify_df, tacos_df, engagement_df):
    # Summary of all channels
    df_combined = pd.concat([amazon_df, shopify_df], ignore_index=True)
    df2 = df_combined.copy()
    df2.loc['TOTAL'] = df2.sum(numeric_only=True)
    df2.loc['TOTAL', 'ROAS'] = df2.loc['TOTAL', 'Revenue'] / df2.loc['TOTAL', 'Cost']
    df2['ROAS'] = df2['ROAS'].round(2)
    df2.iloc[-1, df2.columns.get_loc('Channel')] = 'TOTAL'
    df2['Purchases'] = df2['Purchases'].astype(int)
    
    # Creating a copy bc formatting will break the graph.
    df3 = df2.copy()
    
    df3[['Cost', 'Revenue']] = df3[['Cost', 'Revenue']].applymap(lambda x: f'${x:,.2f}')
    df3.loc[df2['Channel'] == 'Amazon - Meta Ads', ['Revenue', 'Purchases', 'ROAS']] = 'n/a'
    #df3['Purchases'] = df3['Purchases'].apply(lambda x: int(float(x)) if pd.notnull(x) and x != 'n/a' else x)
    
    
    # To hide Meta - Amazon Ads
    #df2 = df2[(df2['Channel'] != 'TOTAL') & (~df2['Channel'].str.contains('Amazon -'))] # to remove Amazon - Meta Ads
    #df2.loc[df2['Channel'] == 'Amazon - Meta Ads', 'Purchases'] = '?'
    
    # Hide total from the graph.
    df2 = df2[df2['Channel'] != 'TOTAL']
    
    # Bar Chart of ROAS of all channels
    fig = go.Figure(data=[
        go.Bar(name='Spend', x=df2['Channel'], y=df2['Cost']),
        go.Bar(name='Revenue', x=df2['Channel'], y=df2['Revenue'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.write_image('roas-chart.png')
    #fig.show()
    
    #tACOS table
    #print(tacos_df)
    #tacos_df = tacos_df
    tacos_df['tACOS (%)'] = tacos_df['tACOS (%)'].round(2)
    tacos_df['tACOS (%)'] = tacos_df['tACOS (%)'].apply(lambda x: f'{x:,.2f}%')
    
    #Engagement Data
    #engagement_df = engagement_df
    engagement_df['Click Through Rate (CTR)'] = engagement_df['Click Through Rate (CTR)'].round(2)
    engagement_df['Click Through Rate (CTR)'] = engagement_df['Click Through Rate (CTR)'].apply(lambda x: f'{x:,.2f}%')
    
    # Convert pandas DataFrames to HTML
    summary_html = df3.to_html(index=False)
    tacos_html = tacos_df.to_html(index=False)
    engagement_html = engagement_df.to_html(index=False)
    
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
    
    # GPT-4 Auto Insights
    from draft.main import html_content as report
    import openai
    
    # ❕put this in the enviornment
    openai.api_key = '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'
    openai.organization = "org-3eOC1TnSIDLIpxln1unBtGFo"
    
    # print("OpenAI version:", openai.__version__)
    turbo = 'gpt-3.5-turbo'
    gpt4 = "gpt-4"
    
    # Insights for month to date report
    def auto_insights(model, report_content):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a marketing expert that reads reports and provides helpful insights about performance in an easy-to-understand and friendly tone. You work for Michael Simon at Appaloosa Marketing LLC. "},
                {"role": "user",
                 "content": f"Please review the marketing data and instructions below.\n\nMarketing Data\nPerformance of all channels this month: {df3}\n\ntACOS data: {tacos_df} \n\nEngagement data: {engagement_df}\n\nInstructions:\n You are going to provide a short summary (4 sentences max) on the positive aspects of performance. Things to consider:  the tACOS percentage and compare it to our company's recommendation of 33%. The channel [ex: Shopify - Google Ads] with the highest ROAS then compare it to our company's minimum goal of 3.33x. 3. The best performing channel in terms of revenue. 4. The channel with the best engagement based on click through rate (CTR)" }
            ],
            temperature=0.75,
            max_tokens=300,  # Adjust as needed
    
        )
        return response['choices'][0]['message']['content']
    
    def improve_readability(model, message):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a readability expert that formats messages in HTML to make them easier to read. "},
                {"role": "user",
                 "content": f"Please space out the below content and shorten it to 5 setences max, so it's easier to read, then provide it as HTML:{message}. \n\nNote: Do not use a heading tag larger than an <h4> " }
            ],
            temperature=0.75,
            max_tokens=300,  # Adjust as needed
    
        )
        return response['choices'][0]['message']['content']
    
    
    # ❕NEEDS IMPROVEMENT - turbo needs a ton of instruction, gpt-4 seems to provide too much information but is friendlier...
    
    insights = auto_insights(turbo, report)
    #print(insights)
    improved_insights = improve_readability(turbo, insights)
    #print(improved_insights)
    
    # Insights for an end-of-month report - compares two reports.
    #this_month = report
    def auto_insights2(model, this_month, last_month):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a marketing expert that reads reports and provides helpful insights about performance in an easy-to-understand and friendly tone."},
                {"role": "user",
                 "content": f"Please read the below marketing report and provide 3 bullet points summarizing the positive aspects of performance, comparing this month's report to the previous month's report.\n\nThis month's report: {this_month}\n\nLast month's report: {last_month}\n\n 1. Mention the highest ROAS (specifying the ROAS of this channel) & compare it to our company's minimum of ROAS 3.33x. 2. Mention the best performing channel 3. Mention where there is the best engagement, based on click through rate (CTR)."}
            ],
            temperature=0.75,
            max_tokens=300,  # Adjust as needed
    
        )
        return response['choices'][0]['message']['content']
    
    #compared_insight = auto_insights2(turbo, this_month, last_month)
    
    
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
            <p>{improved_insights}</p>
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


    ## REPORT NAME ###

    # Use WeasyPrint to convert the HTML to PDF
    HTML('report.html').write_pdf('mtd/reports/report.pdf')
    
    # Remove temporary files
    os.remove("roas-chart.png")
    os.remove("report.html")
