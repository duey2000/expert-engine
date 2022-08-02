import pandas as pd
import os

# Load the new csv file
filename = os.path.join(os.path.dirname(__file__),'new_work_order.csv')
df = pd.read_csv(filename)

#Univariate (or single variable) analysis
date_submitted_totals = df['date_submitted'].value_counts()
print(date_submitted_totals)
service_totals = df['service'].value_counts()

#Bivariate (two variable) Analysis
date_floor = df.groupby(['date_submitted','floor'])['date_submitted'].value_counts()
print(date_floor)