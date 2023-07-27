"""GPT-3.5 Turbo Auto Insights"""

import openai
from generate import data1, time_df, 

# ❕put this in the enviornment
openai.api_key = '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'
openai.organization = "org-3eOC1TnSIDLIpxln1unBtGFo"

# print("OpenAI version:", openai.__version__)
turbo = 'gpt-3.5-turbo'
#gpt4 = "gpt-4"


# Insights for month to date report
def auto_insights(model, report_content):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a marketing expert that reads reports and provides helpful insights about performance in an easy-to-understand and friendly tone. You work for Michael Simon at Appaloosa Marketing LLC. "},
            {"role": "user",
             "content": f"Please review the marketing data and instructions below.\n\nMarketing Data\nPerformance of all channels this month: {data1}\n\nPerformance over time {time_df}\n\nInstructions:\n Provide a short summary (4 sentences max) on the positive aspects of performance, then provide one recommendation of a strategy moving forward."}
        ],
        temperature=0.75,
        max_tokens=300,  # Adjust as needed

    )
    return response['choices'][0]['message']['content']


def improve_readability(model, content):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a readability expert that formats messages in HTML to make them easier to read. "},
            {"role": "user",
             "content": f"Please space out the below content and shorten it to 5 setences max, so it's easier to read, then provide it as HTML:{content}. \n\nNote: Do not use a heading tag larger than an <h4> "}
        ],
        temperature=0.75,
        max_tokens=300,  # Adjust as needed

    )
    return response['choices'][0]['message']['content']



def turbo_insights():
    insights = auto_insights(turbo, report)
    improved_insights = improve_readability(turbo, insights)
    return improved_insights, insights

def run_test():
    improved_insights, insights = turbo_insights()
    print(insights)
    print(improved_insights)
