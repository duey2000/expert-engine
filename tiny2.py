import pandas as pd
import os

#Open the file to read and save to the dataframe variable
filename = os.path.join(os.path.dirname(__file__),'work_order.csv')
df = pd.read_csv(filename)

#Replace the '0' values and replace 'Null' values in the details column
df.details=df.details.replace('Null','No details given')
df.details=df.details.replace('0','No details given')
missing_details = df[df['details']=='No details given' ]
print(missing_details)