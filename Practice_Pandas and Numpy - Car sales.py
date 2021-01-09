#!/usr/bin/env python
# coding: utf-8

# In[88]:


import numpy as np
import pandas as pd


# In[89]:


autos=pd.read_csv('C:/Users/Jesse/Desktop/Autos.csv',encoding='Latin-1')
autos.info()
autos.head(5)
autos.shape


# The dataset contains 20 columns and 50000 rows.15 columns have the data type as strings, and the other five columns are integers. There are some columns with null values. 

# # Editing Columns Name

# 1. Change the columns from camelcase to snakecase.
# 2. Make the name of the columns describe the columns more acurately.

# In[90]:


autos.columns


# In[91]:


autos.columns=['date_crawled','name','seller','offer_type','price','ab_test','vehicle_type','registration_year',
               'gearbox','power_ps','model','odometer','registration_month', 'fuel_type', 'brand','unrepaired_damage',
               'ad_created', 'num_photos', 'postal_code','last_seen']


# In[92]:


autos.columns
autos.head()


# # Data Exploration and Cleaning

# We will check if all or almost all values are the same within a column and decide whether to drop it as they might not give useful information for analysis. We will also check if the numeric data stored as strings need to be converted.

# In[93]:


autos.describe(include='all')


# We see that the number of photos column might only contains value '0'. Also, the price and the odometer columns are numeric values stored as strings.Let's take a closer look at these columns.

# In[94]:


autos['num_photos'].value_counts()


# In[95]:


# drop the num_photos column
autos=autos.drop(['num_photos'],axis=1)
autos.head()


# The number of photos column contains only one value "0" and we eliminated this column since it does not give useful information.

# In[96]:


autos['price']


# In[97]:


autos['price']=(autos['price']
               .str.replace("$","")
               .str.replace(",","")
               .astype(int)
              )
autos['price']


# In[98]:


autos['odometer'].head()


# In[99]:


autos['odometer']=(autos['odometer']
                   .str.replace('km','')
                   .str.replace(',','')
                   .astype(int)
                  )
autos['odometer'].head()


# In[100]:


# rename odometer to odometer_km
autos.rename({'odometer':'odometer_km'},axis=1,inplace=True)
# axis=1 means column axis,inplace=True means replace the original 'odometer'
autos['odometer_km'].head()


# In[101]:


# Exploring odometer_km and price columns


# In[102]:


autos['odometer_km'].max()


# In[103]:


autos['odometer_km'].min()


# In[104]:


autos['odometer_km'].value_counts()


# From the result, we notice that the values are rounded and there are more high mileage vehicles than low mileage.

# In[105]:


autos["price"].unique().shape


# In[106]:


autos["price"].describe()


# In[107]:


autos["price"].value_counts().head(10)


# There are 1421 cars listed with $0 price and it is only about 2% of the cars,we might consider to remove these rows. The maximum price is 100 million dollars, it is not reasonable.

# In[108]:


price_d=autos["price"].value_counts().sort_index(ascending=False).head(30)


# In[109]:


autos["price"].value_counts().sort_index(ascending=True).head(30)


# There are 14 listings are over $1 million.
# We will remove any price above 350000, since the price increases too fast above this value. We will keep the 1 dollar listings, since eBay is an auction site and the opening bid is 1 dollar.

# In[110]:


autos=autos[autos["price"].between(1,351000)]
autos["price"].describe()


# # Date Exploring

# 5 columns contain date information:
# 1. date_crawled
# 2. registration_month
# 3. registration_year
# 4. ad_created
# 5. last_seen

# In[111]:


autos[['date_crawled','ad_created','last_seen','registration_month','registration_year']].head(10)


# As we can see that the first 10 characters from the date_crawled, ad_created, last_seen columns represent the date.

# In[112]:


(autos['date_crawled']
 .str[:10]
 .value_counts(normalize=True,dropna=False)
 .sort_index()
)


# In[113]:


(autos["date_crawled"]
 .str[:10]
 .value_counts(normalize=True, dropna=False)
 .sort_values()
)


# The site was crawled daily over one month period.The distribution of listings crawled on each day is roughly uniform.

# In[114]:


(autos["last_seen"]
.str[:10]
.value_counts(normalize=True,dropna=False)
.sort_index()
)


# The data from the last three days are not reasonable since they are much higher than the previous days. It might because the crawling period ends and does not have car sales.

# In[115]:


autos["ad_created"].str[:10].unique().shape


# In[116]:


(autos["ad_created"]
.str[:10]
.value_counts(normalize=True,dropna=False)
.sort_index()
)


# Most fall within 1-2 months of the listing date.

# In[117]:


autos[["registration_year","registration_month"]].describe()


# The minimum year of registration year is 1000 and the maximum year of registration year is 9999. These values are not reasonable.

# In[118]:


(~autos["registration_year"].between(1900,2016)).sum()/autos.shape[0]


# In[119]:


# Select only the rows that have registration_year within the range(1900,2016)
autos=autos[autos["registration_year"].between(1900,2016)]
autos["registration_year"].describe()


# # Price and Brand Exploring

# In[120]:


autos["brand"].value_counts()


# In[121]:


autos["brand"].value_counts(normalize=True)


# Volkswagen is the most popular brand. We will focus on brands representing more than 5% of total listings.

# In[122]:


brand_counts=autos["brand"].value_counts(normalize=True)
selected_brands=brand_counts[brand_counts>0.05].index
print(selected_brands)


# In[123]:


mean_price={}

for brand in selected_brands:
    brand_series=autos[autos["brand"]== brand]
    mean_p=brand_series["price"].mean()
    mean_price[brand]=int(mean_p)
print(mean_price)


# BMW, Mercedes Benz and Audi are more expensive; Ford and Opel are less expensive; Volkswagen is in between.

# In[133]:


# make the dictionary to a dataframe
mean_price_series=pd.Series(mean_price)
pd.DataFrame(mean_price_series,columns=["mean_price"])


# # Brand and Mileage

# In[128]:


mean_mileage={}

for brand in selected_brands:
    brand_series=autos[autos["brand"]==brand]
    mileage_m=brand_series["odometer_km"].mean()
    mean_mileage[brand]=int(mileage_m)

print(mean_mileage)


# In[130]:


mean_mileage_series=pd.Series(mean_mileage)
pd.DataFrame(mean_mileage_series,columns=["mean_mileage"])


# In[134]:


mean_mileage=pd.Series(mean_mileage_series).sort_values(ascending=False)
mean_prices=pd.Series(mean_price_series).sort_values(ascending=False)


# In[136]:


brand_menu=pd.DataFrame(mean_mileage,columns=['mean_mileage'])
print(brand_menu)


# In[138]:


brand_menu["mean_price"]=mean_prices
brand_menu


# The top brands are more expensive even with higher average mileage.
