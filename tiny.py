import pandas as pd
import os

#Open the file to read and save to the dataframe variable
filename = os.path.join(os.path.dirname(__file__),'work_order.csv')
df = pd.read_csv(filename)

#Print the file to read on screen
print(df)

#View a summary of '0' values in the dataframe
print(df.isnull().sum())
df.fillna(value=0,inplace=True)
print(df.describe())