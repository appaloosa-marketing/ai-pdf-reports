"""GPT-3.5 Turbo Auto Insights"""

import openai
from data import df3, tacos_df,engagement_df

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
             "content": f"Please review the marketing data and instructions below.\n\nMarketing Data\nPerformance of all channels this month: {df3}\n\ntACOS data: {tacos_df} \n\nEngagement data: {engagement_df}\n\nInstructions:\n You are going to provide a short summary (4 sentences max) on the positive aspects of performance. Things to consider:  the tACOS percentage and compare it to our company's recommendation of 33%. The channel [ex: Shopify - Google Ads] with the highest ROAS then compare it to our company's minimum goal of 3.33x. 3. The best performing channel in terms of revenue. 4. The channel with the best engagement based on click through rate (CTR)"}
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
             "content": f"Please space out the below content and shorten it to 5 setences max, so it's easier to read, then provide it as HTML:{message}. \n\nNote: Do not use a heading tag larger than an <h4> "}
        ],
        temperature=0.75,
        max_tokens=300,  # Adjust as needed

    )
    return response['choices'][0]['message']['content']


# Insights comparing two reports (variables should be HTML content)
# Note: You can feed GPT a section of HTML, as opposed to the entire document. This will
#       save tokens while explaining the data with HTML instead of sentences.

def compared_insights(model, this_month, last_month):
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



def turbo_insights():
    insights = auto_insights(turbo, report)
    improved_insights = improve_readability(turbo, insights)
    return insights, improved_insights


# compared_insight = auto_insights2(turbo, this_month, last_month)


def run_test():
    insights, improved_insights = turbo_insights()
    print(insights)
    print(improved_insights)