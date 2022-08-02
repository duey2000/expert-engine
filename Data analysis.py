import seaborn as sns
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt



filename=os.path.join(os.path.dirname(__file__),'hotel_bookings.csv')
df = pd.read_csv(filename)
print(df)

print(df.info())
print(df.describe())

sns.set(style='darkgrid')
sns.relplot(data=df,x='arrival_date_month',y='')
plt.show()

#Figure Level Plots:
#RELPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid')
# sns.relplot(data=penguins, x='bill_length_mm', y='flipper_length_mm',  height=4, aspect=1, hue='sex',
#             row= 'island',col='species')
# plt.show()

#DISPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid')
# sns.displot(data=penguins, x='flipper_length_mm',hue='species',height=4,aspect=1)
# plt.show()

#HISTPLOT
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid')
# sns.displot(data=penguins, x='flipper_length_mm',hue='species',height=4,aspect=1,kind='kde',fill=True)
# plt.show()

#CATPLOT()
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.catplot(data=exercise, x='kind',y='pulse',col='diet',height=4,aspect=1,hue='time')
# plt.show()

#Axes-level plots
#SCATTERPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid',rc={'figure.figsize':(5,5)})
# sns.scatterplot(data=penguins, x='species',y='island')
# plt.show()

#LINEPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid',rc={'figure.figsize':(5,5)})
# sns.lineplot(data=penguins, x='species',y='body_mass_g')
# plt.show()

#HISTPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid',rc={'figure.figsize':(5,5)})
# sns.histplot(data=penguins, x='island',y='species')
# plt.show()

#KDPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid')
# sns.kdeplot(data=penguins, x='bill_length_mm',hue='species',fill=True)
# plt.show()

#ECDFPLOT()
# penguins = sns.load_dataset('penguins')
# print(penguins)
# sns.set(style = 'darkgrid')
# sns.ecdfplot(data=penguins, x='bill_length_mm',hue='species')
# plt.show()

#RUGPLOT()
# tips = sns.load_dataset('tips')
# print(tips)
# sns.set(style = 'darkgrid')
# sns.rugplot(data=tips, x='tip')
# plt.show()

#SWARMPLOT()
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.swarmplot(data=exercise, x='kind',y='pulse',dodge=True)
# plt.show()

#BOXPLOT
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.boxplot(data=exercise, x='kind',y='pulse')
# plt.show()

#VIOLINPLOT()
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.violinplot(data=exercise, x='kind', y='pulse', hue='time',orient='h')
# plt.show()

#BOXENPLOT()
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.boxenplot(data=exercise, x='kind', y='pulse', hue='time')
# plt.show()

#BARPLOT
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.barplot(data=exercise, x='kind', y='pulse', hue='diet')
# plt.show()

#POINTPOLOT
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.pointplot(data=exercise, x='kind', y='pulse', hue='diet')
# plt.show()

#COUNTPLOT
# exercise = sns.load_dataset('exercise')
# print(exercise)
# sns.set(style = 'darkgrid')
# sns.catplot(data=exercise,x='kind',hue='pulse',kind='count',height=4,aspect=4)
# plt.show()

#VISUALIZING THE TITANIC DATASET
# filename = os.path.join(os.path.dirname(__file__),'final_dataset.csv')
# final_data = pd.read_csv(filename)


# #Data Correlation
# data_correlation = final_data.corr()
#print(data_correlation)

# class1 = final_data['Survived'].corr(final_data['Pclass']==1)
# class2 = final_data['Survived'].corr(final_data['Pclass']==2)
# class3 = final_data['Survived'].corr(final_data['Pclass']==3)
# print(class1)
# print(class2)
# print(class3)

# colormap = sns.diverging_palette(230,20, as_cmap=True)
# plt.figure(figsize=(10,10))
# sns.heatmap(final_data.corr(),cmap=colormap,linewidths=.5,annot=True)
# plt.show()

#Univariate Analysis
# survivals = final_data['Survived'].value_counts()
# print(survivals)

# sns.countplot(data=final_data,x='Survived',saturation=3)
# plt.show()

# colors = ['#476a6f','#e63946']
# explode = [.05,.05]
# final_data['Survived'].value_counts().plot.pie(colors=colors,shadow=True,explode=explode,startangle=45)
# plt.show()

#Bivariate Analysis
# survived_classes = final_data.groupby(['Survived','Pclass'])['Survived'].value_counts()
# print(survived_classes)

# sns.catplot(data=final_data,x='Numerical Sex',y='Fare',palette=['red','blue'])
# plt.show()

#Multivariate Analysis
# sex_age = sns.catplot(data=final_data,x='Numerical Sex',y='Age',hue='Survived',col='Pclass',palette=['red','blue'])
#plt.show()

# mix_variables = sns.relplot(data=final_data,x='Age',y='Fare',col='Pclass',row='Numerical Sex')
# plt.show()