"""
Processes data for use in a pdf report.

Loads data from a .env file, which contains variables that are set to hyperlinks. These hyperlinks are hosted csv files.
"""


"""
Proccesses data for a month to date report. List of available data below:

Combined Dataframes:
amazon_df
shopify_df

Individual Shopify Dataframes:
google_conversions_mtd
meta_conversions_mtd

Individual Amazon Dataframes:
amazonads_mtd_total
amazon_meta_conversions_mtd

Revenue Only Dataframes:
amazon_sales
mtd_sales

tACOS data:
tacos_df
amazon_spend
amazon_total_sales
shopify_spend
shopify_total_sales
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os


## LOAD DATA ##
load_dotenv()  # take environment variables from .env.


#AMAZON
sellercentral_monthly = os.getenv("AMAZON_SALES_MONTHLY")
sellercentral_mtd = os.getenv("AMAZON_SALES_MTD")
amazonads_mtd = os.getenv("AMAZON_ADS_MTD")
amazon_meta_conversions_mtd = os.getenv("AMAZON_META_CONVERSIONS_MTD")

# SHOPIFY
shopify_report = os.getenv("SHOPIFY_REPORT_MTD")

#META
meta_conversions_mtd = os.getenv("META_CONVERSIONS_MTD")
last_month_meta_df = os.getenv("LAST_MONTH_META")

#GOOGLE
google_conversions_mtd = os.getenv("GOOGLE_CONVERSIONS_MTD")


#DATA
try:
    sellercentral_monthly = pd.read_csv(sellercentral_monthly)
except:
    print('sellercentral_monthly df is empty.')

try:
    meta_conversions_mtd = pd.read_csv(meta_conversions_mtd)
except:
    print('meta_conversions_mtd is empty or does not exist')

try:
    amazon_meta_conversions_mtd = pd.read_csv(amazon_meta_conversions_mtd)
except:
    print('amazon_meta_conversions_mtd is empty or does not exist')


sellercentral_mtd = pd.read_csv(sellercentral_mtd)
amazonads_mtd = pd.read_csv(amazonads_mtd)
last_month_meta_df = pd.read_csv(last_month_meta_df)
google_conversions_mtd = pd.read_csv(google_conversions_mtd)
shopify_report = pd.read_csv(shopify_report)

# AMAZON MTD SALES #
sellercentral_mtd['Platform'] = 'Amazon USA'
sellercentral_mtd.rename(columns={"unitCount":"Units Ordered","orderCount":"Orders","Total Sales":"Revenue"}, inplace=True)
sellercentral_mtd.drop(columns={"month"}, inplace=True)
sellercentral_mtd = sellercentral_mtd[['Platform', 'Revenue']]
#sellercentral_mtd = sellercentral_mtd[['Platform', 'Revenue', 'Orders', 'Units Ordered', 'Avg. Unit Price']]




# SHOPIFY MTD SALES#
total_revenue = shopify_report['totalPrice'].astype(float).sum()
total_tax = shopify_report['totalTax'].astype(float).sum()
total_refund = shopify_report['totalRefunded'].astype(float).sum()
total_revenue_adjusted = total_revenue - total_tax - total_refund

data = {'Platform': ['Shopify'], 'Revenue': [total_revenue_adjusted]}


shopify_mtd = pd.DataFrame(data)

mtd_sales = pd.concat([sellercentral_mtd, shopify_mtd], axis=0).fillna('')
#mtd_sales[['Revenue']] = mtd_sales[['Revenue']].applymap(lambda x: f'${x:,.2f}')

sales_df = mtd_sales.copy()
sales_df.set_index('Platform', inplace=True)

shopify_total_sales = sales_df.loc['Shopify', 'Revenue']
amazon_total_sales = sales_df.loc['Amazon USA', 'Revenue']

# Combined seller central & shopify sales
#print(mtd_sales)



### ADVERTISING ###

## AMAZON Advertising MTD ##
amazonads_mtd.rename(columns={'Campaign': 'Channel', 'Sales':'Revenue'}, inplace=True)
amazonads_mtd_total = amazonads_mtd[['Channel', 'Cost', 'Revenue', 'Purchases']]
amazonads_mtd_total = (amazonads_mtd_total.iloc[-1:]).replace('TOTAL', 'Amazon Ads')
amazonads_mtd_total['ROAS'] = amazonads_mtd_total['Revenue']/amazonads_mtd_total['Cost']



# FB ADS to Ammazon MTD #
# 3. Change TOTAL row
amazon_meta_conversions_mtd = amazon_meta_conversions_mtd[amazon_meta_conversions_mtd['Adset'].str.contains('TOTAL')]
amazon_meta_conversions_mtd.rename(columns={'Adset': 'Channel', 'Spend':'Cost'}, inplace=True)

amazon_meta_conversions_mtd = (amazon_meta_conversions_mtd.iloc[-1:]).replace('TOTAL', 'Amazon - Meta Ads')
#print(amazon_meta_conversions_mtd)

#print(amazon_meta_conversions_mtd)


## SHOPIFY Advertising MTD ##

# Shopify - Meta Ads Performance MTD #
try:
    meta_conversions_mtd.fillna('', inplace=True)

except:
    pass

try:
    meta_conversions_mtd = meta_conversions_mtd[meta_conversions_mtd['Adset'].str.contains('TOTAL')]
    meta_conversions_mtd.rename(columns={'Adset': 'Channel', 'Spend':'Cost'}, inplace=True)
    #meta_conversions_mtd = meta_conversions_mtd[['Channel', 'Cost', 'Revenue', 'Purchases', 'ROAS', 'Click Through Rate (CTR)']]

    meta_conversions_mtd = (meta_conversions_mtd.iloc[-1:]).replace('TOTAL', 'Shopify - Meta Ads')
    # ready #
    #print(meta_conversions_mtd)
except:
    print('No data for meta_conversions_mtd.')

""" Meta Conversions MTD """
# print(meta_conversions_mtd)

# Shopify - Google Ads Performance MTD #
google_conversions_mtd = google_conversions_mtd[google_conversions_mtd['Campaign'].str.contains('TOTAL')]

if 'Revenue' in google_conversions_mtd.columns and (google_conversions_mtd['Revenue'] > 0).any():
    try:
        google_conversions_mtd = google_conversions_mtd.iloc[-1:].replace('TOTAL', 'Shopify - Google Ads')
        google_conversions_mtd = google_conversions_mtd.rename(columns={'Campaign': 'Channel'})


    except:
        print('No purchase data or something is broken.')
    pass
else:
    # If there's no purchase data, create empty purchase metric columns & set val = 0
    for column_name in ['Purchases', 'Revenue', 'ROAS']:
        if column_name not in google_conversions_mtd.columns:
            google_conversions_mtd[column_name] = 0
    try:
        google_conversions_mtd = google_conversions_mtd.iloc[-1:].replace('TOTAL', 'Shopify - Google Ads')
        #google_conversions_mtd = google_conversions_mtd.drop(columns=['Clicks', 'Impressions'])
        google_conversions_mtd = google_conversions_mtd.rename(columns={'Campaign': 'Channel'})
        # ready #
        print(google_conversions_mtd)
    except:
        'Something wrong (Line 92)'

"""Google Conversions MTD """
# print(google_conversions_mtd)

try:
    combined_df = pd.concat([amazonads_mtd_total, amazon_meta_conversions_mtd, meta_conversions_mtd, google_conversions_mtd], axis=0, ignore_index=True)

    # ENGAGEMENT
    engagement_df = pd.concat([amazon_meta_conversions_mtd, meta_conversions_mtd, google_conversions_mtd], axis=0, ignore_index=True)
    combined_df = combined_df.drop(columns=['Clicks', 'Impressions', 'Click Through Rate (CTR)'])
except:
    combined_df = pd.concat([amazonads_mtd_total, amazon_meta_conversions_mtd, google_conversions_mtd], axis=0, ignore_index=True)
    engagement_df = pd.concat([amazon_meta_conversions_mtd, google_conversions_mtd], axis=0,
                              ignore_index=True)
    # ENGAGEMENT
    combined_df = combined_df.drop(columns=['Clicks', 'Impressions', 'Click Through Rate (CTR)'])


# ENGAGEMENT
try:
    engagement_df = engagement_df[['Channel', 'Clicks', 'Impressions', 'Click Through Rate (CTR)']]
except:
    print('The engagement dataframe broke.')


# select rows where 'Channel' contains 'Amazon'
amazon_df = combined_df[combined_df['Channel'].str.contains('Amazon')]
amazon_df2 = amazon_df.copy()
amazon_df2.loc['TOTAL'] = amazon_df2.sum(numeric_only=True)
amazon_df2.loc['TOTAL', 'ROAS'] = amazon_df2['ROAS'].mean()
amazon_df2.iloc[-1, amazon_df2.columns.get_loc('Channel')] = 'TOTAL'

# Format as currency
#amazon_df[['Cost', 'Revenue']] = amazon_df[['Cost', 'Revenue']].applymap(lambda x: f'${x:,.2f}')
# ready #

"""Combined advertising on Amazon"""
#print(amazon_df)
# Shopify Advertising Spend

amazon_spend = amazon_df2.loc['TOTAL', 'Cost']



# select rows where 'Channel' contains 'Amazon'
shopify_df = combined_df[combined_df['Channel'].str.contains('Shopify')]
shopify_df2 = shopify_df.copy()
shopify_df2.loc['TOTAL'] = shopify_df2.sum(numeric_only=True)
shopify_df2.loc['TOTAL', 'ROAS'] = shopify_df2['ROAS'].mean()
shopify_df2.iloc[-1, shopify_df2.columns.get_loc('Channel')] = 'TOTAL'

# Format as currency
#shopify_df[['Cost', 'Revenue']] = shopify_df[['Cost', 'Revenue']].applymap(lambda x: f'${x:,.2f}')

# Shopify Advertising Spend
shopify_spend = shopify_df2.loc['TOTAL', 'Cost']

"""Combined advertising on Shopify"""
#print(shopify_df)


#tACOS
data = [
    {
        "Platform": "Amazon",
        "Total Sales": amazon_total_sales,  # replace this with your variable
        "Spend": amazon_spend,  # replace this with your variable
    },
    {
        "Platform": "Shopify",
        "Total Sales": shopify_total_sales,  # replace this with your variable
        "Spend": shopify_spend,  # replace this with your variable
    },
]

# Create the DataFrame
tacos_df = pd.DataFrame(data)

# If the sales and spend data are string type and formatted as currency (e.g., "$100.00"),
# we'll need to remove the dollar signs and convert to float.
tacos_df["Total Sales"] = tacos_df["Total Sales"].replace('[\$,]', '', regex=True).astype(float)
tacos_df["Spend"] = tacos_df["Spend"].replace('[\$,]', '', regex=True).astype(float)

# Calculate tACOS column
tacos_df["tACOS (%)"] = (tacos_df["Spend"] / tacos_df["Total Sales"]) * 100  # Now this will give you a percentage

# Convert back to currency format
tacos_df[["Total Sales", "Spend"]] = tacos_df[["Total Sales", "Spend"]].applymap(lambda x: '${:,.2f}'.format(x))


## Summary of all channels
df_combined = pd.concat([data.amazon_df, data.shopify_df], ignore_index=True)
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
# df3['Purchases'] = df3['Purchases'].apply(lambda x: int(float(x)) if pd.notnull(x) and x != 'n/a' else x)


# To hide Meta - Amazon Ads
# df2 = df2[(df2['Channel'] != 'TOTAL') & (~df2['Channel'].str.contains('Amazon -'))] # to remove Amazon - Meta Ads
# df2.loc[df2['Channel'] == 'Amazon - Meta Ads', 'Purchases'] = '?'

# Hide total from the graph.
df2 = df2[df2['Channel'] != 'TOTAL']

## tACOS table

tacos_df = data.tacos_df
tacos_df['tACOS (%)'] = tacos_df['tACOS (%)'].round(2)
tacos_df['tACOS (%)'] = tacos_df['tACOS (%)'].apply(lambda x: f'{x:,.2f}%')

## Engagement Data
engagement_df = data.engagement_df
engagement_df['Click Through Rate (CTR)'] = engagement_df['Click Through Rate (CTR)'].round(2)
engagement_df['Click Through Rate (CTR)'] = engagement_df['Click Through Rate (CTR)'].apply(lambda x: f'{x:,.2f}%')

