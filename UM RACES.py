#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing libraries 


# In[1]:


import pandas as pd
import seaborn as sns


# In[3]:


#creating our data frame
df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")


# In[4]:


#looking into the data that has been imported
df.head(10)


# In[6]:


df.shape


# In[7]:


df.dtypes


# In[8]:


#50 km races


# In[9]:


df[df['Event distance/length'] == '50km']


# In[ ]:


#50 miles races


# In[10]:


df[df['Event distance/length'] == '50mi']


# In[ ]:


#combine 50k/50mi with isin (isntead of an OR statement as isin is more efficient)


# In[11]:


df[df['Event distance/length'].isin(['50mi','50km'])]


# In[ ]:


#adding a condition to choose only 2020 data from this


# In[12]:


df[(df['Event distance/length'].isin(['50mi','50km'])) & (df['Year of event'] == 2020)]


# In[13]:


#adding the condition to look into USA races specifically


# In[14]:


df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA']


# In[15]:


#combining all the filters together
df[(df['Event distance/length'].isin(['50mi','50km'])) & (df['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[16]:


df2 = df[(df['Event distance/length'].isin(['50mi','50km'])) & (df['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[17]:


df.head(10)


# In[18]:


df2.shape


# In[19]:


#remove (USA) from event name
df2['Event name'] = df2['Event name'].str.split('(').str.get(0)


# In[20]:


df2.head(10)


# In[21]:


# cleaning up athlete age (year 2020 - athlete year of birth = approx. age)
df2['athlete_age'] = 2020 - df2['Athlete year of birth']


# In[23]:


#removing 'h' from atlete performance
df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)


# In[24]:


df2.head(10)


# In[25]:


#dropping unecessary columns: athlete year of birth, athelete age category
df2= df2.drop(['Athlete year of birth', 'Athlete age category'], axis = 1)


# In[26]:


df2.head()


# In[27]:


#checking for null values
df2.isna().sum()


# In[28]:


#dropping column athlete club as it is not as important and has too many null values
df2= df2.drop(['Athlete club'], axis = 1)


# In[29]:


df2.isna().sum()


# In[30]:


#taking a look at the entries with missing athlete ages
df2[df2['athlete_age'].isna()== 1]


# In[31]:


#dropping these 233 rows specifically
df2 = df2.dropna()


# In[33]:


df2.shape


# In[34]:


#checking for duplicate values
df2[df2.duplicated() == True]


# In[ ]:


#the above implies that there are no duplicate values


# In[35]:


#reset index
df2.reset_index(drop = True)


# In[37]:


#fixing data types
#checking the different data types
df2.dtypes


# In[40]:


df2['athlete_age'] = df2['athlete_age'].astype(int)
df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)


# In[41]:


#renaming the columns
df2 = df2.rename(columns = {'Year of event':'year',
                           'Event dates': 'race_day',
                           'Event name': 'race_name',
                           'Event distance/length':'race_length',
                           'Event number of finishers':'race_number_of_finishers',
                           'Athlete performance':'athlete_performance',
                            'Athlete country':'athlete_country',
                           'Athlete gender':'athlete_gender',
                           'Athlete average speed':'average_speed',
                           'Athlete ID':'athlete_id'})


# In[42]:


df2.head()


# In[43]:


#reorder columns
df3 = df2[['race_day', 'race_name', 'race_length', 'race_number_of_finishers', 'athlete_id','athlete_country', 'athlete_gender', 'athlete_age', 'athlete_performance', 'average_speed', ]]


# In[44]:


df3.head()


# In[47]:


#charts and graphs
#HISTOGRAM
sns.histplot(df3['race_length'])


# In[48]:


sns.histplot(df3, x = 'race_length', hue = 'athlete_gender')


# In[51]:


#taking a look at the distribution of average speed when distance is 50 miles
sns.displot(df3[df3['race_length']== '50mi']['average_speed'])


# In[52]:


#violin plot
sns.violinplot(data = df3, x='race_length', y = 'average_speed', hue = 'athlete_gender')


# In[53]:


sns.violinplot(data = df3, x='race_length', y = 'average_speed', hue = 'athlete_gender', splie = True, inner = 'quart', linewidth = 1)


# In[54]:


sns.lmplot(data=df3, x = 'athlete_age', y = 'average_speed') #without hue


# In[56]:


sns.lmplot(data=df3, x = 'athlete_age', y = 'average_speed', hue = 'athlete_gender') #with hue


# In[ ]:


#questions I want to find out from the data


# In[57]:


#difference in speed between male and female for 50km and 50mi.
df3.groupby(['race_length', 'athlete_gender']) ['average_speed'].mean()


# In[58]:


#what age groups are the best in the 50mi race (age is 20+ in order to eliminate skewness in data)


# In[60]:


df3.query('race_length == "50mi"').groupby('athlete_age')['average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False). query('count>19')


# In[61]:


#lowest speed to fastest (i.e. ascending = true)
df3.query('race_length == "50mi"').groupby('athlete_age')['average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = True). query('count>19')


# In[ ]:


#are runners slower in summer than in winter?

#spring 3-5
#summer 6-8
#fall 9-11
#winter 12-2

#split between two decimals 
#using lambda function


# In[62]:


df3['race_month'] = df3['race_day'].str.split('.').str.get(1).astype(int)


# In[63]:


df3.head()


# In[64]:


df3['race_season'] = df3['race_month'].apply(lambda x: 'Winter' if x > 11 else 'Fall' if x > 8 else 'Summer' if x > 5 else 'Spring' if x > 2 else 'Winter')


# In[65]:


df3.head(25)


# In[67]:


df3.groupby('race_season')['average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:


#50 miler only


# In[69]:


df3.query('race_length == "50mi"').groupby('race_season')['average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)

