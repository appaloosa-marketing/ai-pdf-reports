import pandas as pd
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

# Mock data for 'Last Month' to compare performance
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

time_dict = {
    'Month': x_data,
    'Cost': y_data,
    'Revenue': y2_data
}

time_df = pd.DataFrame(time_dict)

