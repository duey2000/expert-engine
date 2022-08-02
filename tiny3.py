import pandas as pd
import os

#Open the file
filename = os.path.join(os.path.dirname(__file__),'work_order.csv')
df = pd.read_csv(filename)
#Fill in the empty 'details' fields
df.details=df.details.replace('Null','No details given')
df.details=df.details.replace('0','No details given')
df.details=df.details.replace('NaN','No details given')

#Fill in all remaining 'Null' values in the 
df.time_submitted=df.time_submitted.replace('Null','00:00:00')
df.date_submitted=df.date_submitted.replace('Null','2022-07-28')
df.date_completed=df.date_completed.replace('Null','2022-07-28')
df.time_completed=df.time_completed.replace('Null','00:00:00')
#Corrects a typo that exists in the values
df.floor=df.floor.replace('1st FLoor','1st Floor')
print(df.tail(20))

#Create a new csv file using the altered data
new_work_order = df
new_work_order.to_csv('new_work_order.csv')