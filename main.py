
# coding: utf-8

# # Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (82%). There also exists, a smaller, but notable proportion of female players (16%).
# 
# * Our peak age demographic falls between 20-24 (42%) with secondary groups falling between 15-19 (17.80%) and 25-29 (15.48%).
# 
# * Our players are putting in significant cash during the lifetime of their gameplay. Across all major age and gender demographics, the average purchase for a user is roughly $491.   
# -----

# In[ ]:


import os
import pandas as pd


# In[2]:


purchase_data_path = os.path.join("Resources", "purchase_data.json")

purchase_data = pd.read_json(purchase_data_path)
purchase_data.head()


# ## Player Count

# In[3]:


num_player = len(purchase_data['SN'].unique())
Player_Count_table = pd.DataFrame({'Total Players': [num_player]})
Player_Count_table


# ## Purchasing Analysis (Total)

# In[4]:


num_Items = len(purchase_data['Item ID'].unique())
average_purchase_Price= purchase_data['Price'].mean()
num_Purchases = purchase_data['Price'].count()
total_Revenue = purchase_data['Price'].sum()

purchasing_analysis_table = pd.DataFrame({'Number of Unique Items': [num_Items], 'Average Price': [average_purchase_Price],
                                          'Number of Purchases':[num_Purchases], 'Total Revenue': [total_Revenue]},
                                        columns=['Number of Unique Items','Average Price', 'Number of Purchases', 'Total Revenue'])
purchasing_analysis_table


# ## Gender Demographics

# In[5]:


duplicates_removed = purchase_data.drop_duplicates(subset=['SN'])
gender_count = duplicates_removed.groupby('Gender')['Gender'].count()
df_gender_count = pd.DataFrame(gender_count)
df_gender_count

df_gender_count.columns = ['Total Count']
df_gender_count['Percentage of Players'] = (gender_count/num_player*100).round(2)
df_gender_count


# 
# ## Purchasing Analysis (Gender)

# In[6]:


purchase_value_gender = purchase_data.groupby('Gender')['Price'].sum()
purchase_count_gender = purchase_data.groupby('Gender')['SN'].count()
mean_price_gender = purchase_data.groupby('Gender')['Price'].mean()

normalized_total_gender = purchase_data.groupby(['Gender','SN'])['Price'].sum()
df_normalized_total_gender = pd.DataFrame(normalized_total_gender)
df_normalized_total_gender.columns = ['Price']
normal=df_normalized_total_gender.groupby('Gender')['Price'].mean().map('${:.2f}'.format)

df = pd.DataFrame(purchase_count_gender)
df.columns = ['Purchase Count']
df['Average Purchase Price']= mean_price_gender.map('${:.2f}'.format)
df['Total Purchase Value']= purchase_value_gender.map('${:.2f}'.format)
df['Normalized Total'] = normal

df


# ## Age Demographics

# In[7]:


group_names=["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
bins=[0,9,14,19,24,29,34,39,100]
duplicates_removed['Age Demographics'] = pd.cut(duplicates_removed['Age'], bins, labels = group_names)
age_count = duplicates_removed.groupby('Age Demographics')['SN'].count()
df_age_count = pd.DataFrame(age_count)

df_age_count.columns = ['Total Count']
df_age_count['Percentage of Players'] = (age_count/num_player*100).map('${:.2f}'.format)
df_age_count


# ## Purchasing Analysis (Age)

# In[8]:


purchase_data['Purchasing Analysis'] = pd.cut(purchase_data['Age'], bins, labels = group_names)

purchase_count = purchase_data.groupby('Purchasing Analysis')['SN'].count().rename('Purchase Count')
df_purchase_count = pd.DataFrame(purchase_count)
df_purchase_count['Total Purchase Value'] = purchase_data.groupby('Purchasing Analysis')['Price'].sum()
df_purchase_count['Average Purchase Price'] = (df_purchase_count['Total Purchase Value'] / df_purchase_count['Purchase Count']).round(2)

normalized_age_group = purchase_data.groupby(['Purchasing Analysis','SN'])['Price'].sum()
df_normalized_age_group = pd.DataFrame(normalized_age_group)

df_purchase_count['Nomalized Total']=df_normalized_age_group.groupby('Purchasing Analysis')['Price'].mean().round(2)
df_purchase_count


# ## Top Spenders

# In[9]:


purchase_data_price = purchase_data.groupby('SN')['Price'].sum().nlargest(5).rename('Total Purchase Value')
df_purchase_data_price = pd.DataFrame(purchase_data_price)
df_purchase_data_price['Purchase Count']= purchase_data.groupby('SN')['SN'].count()
df_purchase_data_price['Average Price']= (df_purchase_data_price['Total Purchase Value'] / df_purchase_data_price['Purchase Count']).map('${:.2f}'.format)
df_purchase_data_price


# ## Most Popular Items

# In[10]:


popular_item = purchase_data.groupby(['Item ID','Item Name'])['Item ID'].count().nlargest(5).rename('Purchase Count')
df_popular_item = pd.DataFrame(popular_item)
df_popular_item['Item Price'] = purchase_data.groupby(['Item ID','Item Name'])['Price'].max().map('${:}'.format)
df_popular_item['Total Purchase Value']= purchase_data.groupby(['Item ID','Item Name'])['Price'].sum().map('${:.2f}'.format)
df_popular_item


# ## Most Profitable Items

# In[11]:


profitable_item = purchase_data.groupby(['Item ID','Item Name'])['Price'].sum().nlargest(5).rename('Total Purchase Value').map('${:.2f}'.format)
df_profitable_item = pd.DataFrame(profitable_item)
df_profitable_item['Purchase Count'] = purchase_data.groupby(['Item ID','Item Name'])['Item ID'].count()
df_profitable_item['Item Price'] = purchase_data.groupby(['Item ID','Item Name'])['Price'].max().map('${:}'.format)
df_profitable_item

