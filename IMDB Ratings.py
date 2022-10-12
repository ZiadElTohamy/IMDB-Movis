#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import matplotlib as plt


# In[3]:


import re
 
# reading given tsv file
with open('title.akas.tsv', 'r') as myfile: 
  with open("title.akas.csv", 'w') as csv_file:
    for line in myfile:
        
         # Replace every tab with comma
      fileContent = re.sub("\t", ",", line)
       
      # Writing into csv file
      csv_file.write(fileContent)


# In[4]:


df=pd.read_csv('title.akas.csv',error_bad_lines=False) #importing title of media name and skipping errored data


# In[5]:


df #changing the name of the titled to tconst to be the same as the other table to enable join 


# In[6]:



dict = {'titleId' :'tconst',}


# In[7]:


df.rename(columns=dict,
          inplace=True)


# In[8]:


df #changed succesfuly


# In[9]:


Ratings=pd.read_csv('title.ratings.csv') #importing the ratings data to combine it later


# In[10]:


Ratings


# In[11]:


df3=pd.merge(df,Ratings,on='tconst', how='inner') #merging the two tables
df3


# In[12]:


df3.dtypes


# In[13]:


df3['tconst']=df3['tconst'].astype('string') #chaning the 'tconst' column from object to string 


# In[14]:


df3.dtypes #changed to stroing succesfuly 


# In[15]:


df3['tconst'].value_counts(ascending=False) #checking as i saw after the mergingof two tables, the number of rows are way above the smaller table(nearly 1M rows) hence the title names has more than one value


# In[16]:


df3.drop(columns =['ordering', 'language','isOriginalTitle','attributes','language']) #dropping columns from the created dataframe for easier regression and more pleasing view of tables 


# In[17]:


df3.region.unique()


# In[18]:


df3['region'].isna().sum()


# In[19]:


item_counts = df3["region"].value_counts()
item_counts


# In[20]:


df3


# In[21]:


df3['region']=df3['region'].astype('string')


# In[22]:


df3


# In[23]:


df3.dtypes


# In[24]:


#df['region'].value_counts()['\\N'] #fuckk


# In[25]:


df3 = df3[~df3['region'].isin(['\\N'])] #removing the '\N' emoty data in region cell
df3


# In[26]:


#no more'\N' in title column
if '\\N' not in df3.region :
   print("Yes, '\\N' found in List : " , df3.region) #no more'\N' in region column


# In[27]:


#no more'\N' in title column 
if '\\N' not in df3.title :
    print("Yes, '\\N' found in List : " , df3.title)


# In[28]:


#dropping attributes column as we don't need it

df_high_rate=df3.drop(columns =['attributes','language','types','ordering']) 


# In[29]:


df_high_rate


# In[30]:


#filtering the rate for easier analysis
df_high_rate = df_high_rate[df_high_rate["averageRating"] > 7] 


# In[31]:


df_high_rate


# In[32]:


#removing replacing all \N values with null as some other programs can't identfy it such as SQL
df_high_rate['tconst'].replace('\\n', 'null' , inplace=True) 

df_high_rate.replace(to_replace=" \\N",
           value="null")


# In[33]:


#filtering the region to only contain string lenth of two,otherwise it is fault data

df_region_index = (df_high_rate['region'].str.len() == 2)
df_high_rate = df_high_rate.loc[df_region_index]


# In[34]:


df_high_rate


# In[53]:


df_high_rate


# In[51]:


#df_new = df_high_rate[df_high_rate.title.apply(detect).eq('en')]


# In[ ]:


df_high_rate.to_csv('combined_ratings_high.csv', index=False)


# In[55]:


df_high_rate


# In[54]:


df_high_rate = df_high_rate["numVotes"].mean()


# In[47]:


#conda install -c conda-forge langdetect


# In[46]:


#from langdetect import detect


# In[45]:


#df_high_rate['title']=df_high_rate['title'].astype('string')


# In[44]:


#df_new = df_high_rate[df_high_rate.title.apply(detect).eq('en')]

