# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 22:41:31 2020

@author: HP
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

df=pd.read_csv('data.csv',na_values=[" "])

#exploring
df.head()
df.tail()
df.dtypes
df.info()


#plottoing method
def bar_plot(df,x,title,xlab,ylab,xlim=None):
    df[x].value_counts()
    df[x].value_counts().plot.bar()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xlim(xlim)
    plt.show()
#preprossesing & exploratory data analysis


#duration
df['dur_mon_week']=df.duration.apply(lambda x:x.split(" ")[-1])
df['dur_mon_week']=df.dur_mon_week.apply(lambda x:x.replace("Months","Month"))
df['dur_mon_week']=df.dur_mon_week.apply(lambda x:x.replace("Weeks","Week"))
df['duration']=df.duration.apply(lambda x:x.split(" ")[0])
df['duration']=df["duration"].astype('int')
df["duraion_in_days"]=np.where(df['dur_mon_week']=="Month",df["duration"]*30,df["duration"]*7)

#average duration of a job is 98 days
#longest duration in 1080 days i.e.,36 months with salary 5000 per month
df.duraion_in_days.mean()
bar_plot(df,"duraion_in_days","Duration in Days","Days","Frequency")

#1173 in month and 27 in week
bar_plot(df,'dur_mon_week','Month vs Week',"Month vs Week",'Frequency')



#salary
df['sal_type']=df.stipend.apply(lambda x:re.split(' |/',x)[-1])
df['stipend']=df.stipend.apply(lambda x:re.split(' |/',x)[0])
df["min_salary"]=df.stipend.apply(lambda x:x.split("-")[0])
df['max_salary']=df.stipend.apply(lambda x:x.split("-")[-1])
#876 internships have a constant pay,324 have a range of salary
df.loc[df["min_salary"]==df['max_salary'],"stipend"].count()

#xclusing all the unpaid and performance based jobs
df['min_salary']=np.where(df['min_salary']=='Unpaid',0,df['min_salary'])
df['min_salary']=np.where(df['min_salary']=='Performance',0,df['min_salary'])
df['max_salary']=np.where(df['max_salary']=='Unpaid',0,df['max_salary'])
df['max_salary']=np.where(df['max_salary']=='Performance',0,df['max_salary'])
df['min_salary']=df.min_salary.astype('int')
df.max_salary=df.max_salary.astype('int')

#mean max and min salaries are 6120 and 5170 respectively
print(df.min_salary.mean())
print(df.max_salary.mean())

#per month 
#monthly are highest 
bar_plot(df,"sal_type","Types os Salary","Types","Frequency")



#title
df.title=df.title.apply(lambda x:x.split(" (")[0])
#top 10 job titles
bar_plot(df,"title","Job Position top 10","Job","Frequency",xlim=(0,10))



#company
#top 10 companies
bar_plot(df,'company',"Companies top 10","Company","frequency",xlim=(0,10))
#top 5 companies
bar_plot(df,'company',"Companies top 5","Company","frequency",xlim=(0,5))


#openings
#only openings have missing data
#lets se if it is MAR or MCAR or MNAR
df.isnull().sum()
df['missing_open']=np.where(df['openings'].isnull(),1,0)
#as we can see the data in MNAR
#all campus ambassador's do not have open position
df.loc[df['missing_open']==1,'title']
df["openings"]=np.where(df['openings'].isnull(),0,df['openings'])
#outliers
#3 outliers
#20000,10000,3000
df['openings'].plot.box()
plt.ylabel("Frequncy")
plt.title("Outliers in openings")
plt.show()
#calculating mean positions is 4
print(np.round(df['openings'].sort_values(ascending=False)[3:].mean(),0))