#!/usr/bin/env python
# coding: utf-8

# In[272]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import random
import warnings
warnings.simplefilter(action='ignore', category=Warning)


# In[273]:


#Importing and reading csv file
df=pd.read_csv("/Users/pawanpanchal/Downloads/zomato.csv")


# # Exploring Datas

# In[274]:


#Viewing top 5 values of dataframe
df.head()


# # Shape of dataframe

# In[275]:


# Shape of dataframe
df.shape     # we are looking 51717 raws and 17 columns avilable in dataframe. Now we can analyze columns.


# In[276]:


df.columns   


# # Statstics

# In[277]:


#Statstics
df.describe()


# In[278]:


#info regarding dataframe
df.info()     # in this dataframe 1 numerical and 16 categorical columns available


# In[279]:


#Let's find null value
df.isnull().sum()   


# # Observations
# - we can observe "dish_linked"has lot of null values so we can drop null values.
# - in "rate " column we can fill null values.
# - "rate" column in string format so need to convert into float .
# - "phone" column not worth so we can drop
# - "location" & "listed_in(city)" are same so we can drop one column

# # Drop Unwanted Columns

# In[280]:


#Let'S drop unwanted column first 
df=df.drop(["location","phone","menu_item"],axis=1)


# In[281]:


df.info(2) # Dropped 3 columns


# In[282]:


# Drop duplicates
df.drop_duplicates(inplace=True)


# # Shape Of Dataframe

# In[283]:


#Now shape of dataframe
df.shape


# In[284]:


# now start cleaning ---->

# Explore "rate" column
df["rate"].unique()


# ===> we are looking lot of changes required.  need to clean/replace("nan","New","-",/5)

# In[ ]:





# # Removal of  "NEW","-" and "/5" from rate column through function

# In[285]:


#Removal of  "NEW","-" and "/5" from rate column through function
def handle_rate(value):
    if (value =="NEW" or value=="-"):
         return np.nan
    else:
        value=str(value).split("/")
        value=value[0]
        return float (value)
    


# In[286]:


df["rate"]=df["rate"].apply(handle_rate)


# In[287]:


df["rate"].head()  


# In[288]:


#Now handle null values ====> Filling null values with mean of rate column
df["rate"].fillna(df["rate"].mean(),inplace=True)


# In[289]:


# Let's check null values in rate column
df["rate"].isnull().sum()      #0 null value in rate column.Almost done!


# In[290]:


# Explore "listed_in(city) " column.
df["listed_in(city)"].unique()


# In[291]:


#No. of orders according cities
df["listed_in(city)"].value_counts()  #Here are so many locations value. So we will consider top 15 locations


# In[292]:


#Top 15 locations
df["listed_in(city)"].value_counts()[:15]


# In[293]:


# Now we start work on "approx_cost(for two people)" . we will rename but wait.........!
df["approx_cost(for two people)"].unique()


# ===> Ahhhhh......! Lot of values seperated with comma .Now we need to start cleaning .

# In[294]:


# Let's start cleaning work for "approx_cost(for two people)"
def handle_comma(value):
    value=str(value)
    if ',' in value:
        value= value.replace(',','')
        return float(value)
    else:
        return float (value)
        


# In[295]:


df["approx_cost(for two people)"]=df["approx_cost(for two people)"].apply(handle_comma)


# In[296]:


df["approx_cost(for two people)"].unique() #Removed comma with help of function"handle_comma"


# In[297]:


# Now time to rename column 
df1=df.rename(columns={"approx_cost(for two people)":"Cost","listed_in(city)":"City","listed_in(type)":"Type"})   #Now we can check our new column name


# In[298]:


df1.head()


# In[299]:


# Now time to clean "rest_type" column
df["rest_type"].unique()      #Ahhhhh......!


# In[300]:


df["rest_type"].value_counts()          # from here we can observe some restaurents have lot of orders and some few.


# In[ ]:





# In[301]:


Rest=df["rest_type"].value_counts(ascending=False)       #Stored in a variable


# In[302]:


Rest


# In[303]:


rest_above_1000=Rest[Rest>1000]


# In[304]:


rest_above_1000    #Filterd above 1000 orderd restaurents.So we will consider only these restaurents.


# In[305]:


rest_below_1000=Rest[Rest<1000]


# In[306]:


rest_below_1000


# In[307]:


#Now you are thinking what will do below 1000 order restaurents. Relaxxxxxx...................!
#We will consider them in others category.

def handle_rest(value):

    if (value in rest_below_1000):
        return"Others"
    else:
        return value


# In[308]:


df['rest_type']=df['rest_type'].apply(handle_rest)


# In[309]:


#Almost cleaning done...........
df["rest_type"].value_counts()


# In[310]:


df1.head(3)    #viewing now below 1000 considering as others


# In[311]:


# Let's start cleaning for "City"
df1["City"].unique()


# In[312]:


df1["City"].value_counts() #Cities column almost cleand so no need for cleaning.


# In[313]:


#Now time to clean for "Cuisines " column
df1["cuisines"].unique()


# In[314]:


df1["cuisines"].value_counts()   #Here viewing lot of cuisines less than 10.........oppps. Let's clean


# In[315]:


Cuisines=df1["cuisines"].value_counts(ascending=False)


# In[316]:


Cuisines_below100=Cuisines[Cuisines<100]


# In[317]:


Cuisines_below100         #Lot of cuisines less than 100. Again we will consider these in Others category


# In[318]:


def handle_cuisines(value):
    if (value in Cuisines_below100):
        return "Others"
    else:
        return value


# In[319]:


df1["cuisines"]=df1["cuisines"].apply(handle_cuisines)


# In[320]:


df1["cuisines"].value_counts()   #Here we are viewing untill 100 . Below 100 will be consider oin others


# In[321]:


df1.head()     #["cuisines"] also almost done.


# In[322]:


# Start work on "Type"
df1["Type"].unique()


# In[323]:


df1["Type"].value_counts()


# Cleaning part almost done

# # Exploratry Data Analysis & Visualization

# How many chains and outlets in dataframe

# In[324]:


outlets=df1["name"].value_counts()


# In[325]:


outlets  #Viewing outlets


# In[326]:


chains=outlets[outlets>=2]    


# In[327]:


chains #We can observe restaurant chains . 


# In[328]:


#Top 10 restaurant chains
chains.head(10)


# # Visualize top 10 restaurants chain

# In[329]:


#Visualize top 10 restaurants chain
top10_chains=df1["name"].value_counts()[:10].sort_values(ascending=True)


# In[330]:


height=top10_chains.values
bars=top10_chains.index
y_pos = np.arange(len(bars))

fig=plt.figure(figsize=[11,7],frameon=False)
ax=fig.gca()
ax.spines["top"].set_visible("#424242")
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#424242")
ax.spines["bottom"].set_color("#424242")

colors = ["#f9cdac","#f2a49f","#ec7c92","#e65586","#bc438b","#933291","#692398","#551c7b","#41155e","#2d0f41"]
plt.barh(y_pos, height, color=colors)

plt.xticks(color="#424242")

plt.yticks(y_pos, bars, color="#424242")
plt.xlabel("Number of outlets in India")

for i, v in enumerate(height):
    ax.text(v+3, i, str(v), color='#424242')
plt.title("Top 10 Restaurant chain in India (by number of outlets)")




# # Restaurant Types Visualization

# In[331]:


rest_count = df1.groupby("rest_type").count()["name"].sort_values(ascending=False)[:5]


# In[332]:


fig = plt.figure(figsize=[8,5], frameon=False)
ax = fig.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#424242")
ax.spines["bottom"].set_color("#424242")

colors = ["#2d0f41",'#933291',"#e65586","#f2a49f","#f9cdac"]
plt.bar(rest_count.index, rest_count.values, color=colors)

plt.xticks(range(0, 6), color="#424242")
plt.yticks(range(0, 25000, 5000), color="#424242")
plt.xlabel("Top 5 Restaurant types")

for i, v in enumerate(rest_count):
    ax.text(i-0.2, v+500, str(v), color='#424242')
plt.title("Number of restaurants (by Restaurant types)")


# # Average Ratings & Votes

# In[333]:


rating_by_rest = df1.groupby("rest_type").mean()["rate"].sort_values(ascending=False)


# In[334]:


df1.describe()


# In[335]:


df1.groupby("rest_type").mean()["votes"].sort_values(ascending=False)[:10]


# # No.of restaurants by cities

# In[336]:


city_counts = df1.groupby("City").count()["name"].sort_values(ascending=True)[-10:]


# In[337]:


height = pd.Series(city_counts.values)
bars = city_counts.index
y_pos = np.arange(len(bars))

fig = plt.figure(figsize=[11,7], frameon=False)
ax = fig.gca()
ax.spines["top"].set_visible("#424242")
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#424242")
ax.spines["bottom"].set_color("#424242")

colors = ['#dcecc9', '#aadacc', '#78c6d0', '#48b3d3', '#3e94c0', '#3474ac', '#2a5599', '#203686', '#18216b', '#11174b']

plt.barh(y_pos, height, color=colors)

plt.xlim(3)
plt.xticks(color="#424242")
plt.yticks(y_pos, bars, color="#424242")
plt.xlabel("Number of outlets")

for i, v in enumerate(height):
    ax.text(v + 20, i, str(v), color='#424242')
plt.title("Number of restaurants (by city)")


# # No. of Restaurants by Cuisines

# In[338]:


df1["cuisines"].nunique()


# In[339]:


Total_number_of_unique_cuisines=df1["cuisines"].value_counts()[:5]


# In[340]:


Total_number_of_unique_cuisines


# In[341]:


fig = plt.figure(figsize=[8,5], frameon=False)
ax = fig.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#424242")
ax.spines["bottom"].set_color("#424242")

colors = ['#4c3430', '#b04829', '#ec8c41', '#f7c65d','#fded86']
plt.bar(Total_number_of_unique_cuisines.index, Total_number_of_unique_cuisines.values, color=colors)

plt.xticks(range(0, 6), color="#424242")
plt.yticks(range(0, 30000, 5000), color="#424242")
plt.xlabel("Top 5 cuisines")

for i, v in enumerate(Total_number_of_unique_cuisines):
    ax.text(i-0.2, v+500, str(v), color='#424242')
plt.title("Number of restaurants (by cuisine type)")


# # Rating Distribution

# In[342]:


sns.kdeplot(df1['rate'], shade=True)
plt.title("Ratings distribution")
plt.show()


# # Cost Distribution

# In[343]:


sns.kdeplot(df1['Cost'], shade=True)
plt.title("Cost distribution")
plt.show()


# # Online order visualization

# In[344]:


plt.figure(figsize = (6,6))
sns.countplot(x=df1['online_order'],data=df1, palette = 'inferno')


# In[ ]:





# # Table Booking Visualization

# In[345]:


plt.figure(figsize = (6,6))
sns.countplot(x=df1['book_table'],data=df1, palette = 'rainbow')


# # Online Order V/S Rate

# In[346]:


plt.figure(figsize = (6,6))
x=sns.boxplot(x = 'online_order', y = 'rate', data = df1)


# # Table Booking V/S Rate

# In[347]:


plt.figure(figsize = (6,6))
sns.boxplot(x = 'book_table', y = 'rate', data = df1)


# # Restaurants V/S Rate

# In[348]:


plt.figure(figsize = (14, 8))
sns.boxplot(x = 'Type', y = 'rate', data = df1, palette = 'inferno')


# In[ ]:




