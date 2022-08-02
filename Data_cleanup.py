from scipy import rand
import seaborn as sns
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import re



filename=os.path.join(os.path.dirname(__file__),'hotel_bookings.csv')
df = pd.read_csv(filename)
# print(df)

# I changed the arrival_date_month column from a string(month name) to an integer(month number)
df['arrival_date_month'] = df.arrival_date_month.replace({'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12})

# I removed the columns that have irrelevant data (21 columns total)
drop_columns_list = ['agent','company','stays_in_weekend_nights','stays_in_week_nights','adults','children','babies','meal','arrival_date_week_number','is_canceled','lead_time','required_car_parking_spaces','total_of_special_requests','days_in_waiting_list','is_repeated_guest','previous_cancellations','previous_bookings_not_canceled','reserved_room_type','assigned_room_type','booking_changes','deposit_type']
df = df.drop(drop_columns_list,axis=1)
# print(final_dataset)

# reservations = sns.load_dataset(final_dataset)
print(df['country'].nunique())
# sns.set(style = 'darkgrid',rc={'figure.figsize':(5,5)})
# sns.countplot(data=df, x='country')
# plt.show()


