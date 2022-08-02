import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Load the new csv file
filename = os.path.join(os.path.dirname(__file__),'new_work_order.csv')
df = pd.read_csv(filename)

sns.countplot(data=df,x='floor')
plt.show()

sns.countplot(data=df,x='date_submitted')
plt.show()