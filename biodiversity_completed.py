
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[15]:


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[16]:


species = pd.read_csv("species_info.csv")


# Inspect each DataFrame using `.head()`.

# In[17]:


species.head(5)


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[18]:


# Dataframe Information
species.info()
# Dataframe Size
print ('.................................................')


val = species.scientific_name.nunique()
print ('There are:', val, 'Species')



# What are the different values of `category` in `species`?

# In[19]:


unique_conservation_status = species['category'].unique()
print(unique_conservation_status)


# What are the different values of `conservation_status`?

# In[20]:


unique_categories = species['conservation_status'].unique()
print(unique_categories)


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[21]:


species.groupby(['conservation_status']).count().scientific_name.reset_index()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[22]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[23]:


species.groupby(['conservation_status']).count().scientific_name.reset_index()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[24]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')

print (protection_counts.head())


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[25]:


plt.figure(figsize=(10,4))

values = protection_counts.scientific_name
x = protection_counts.conservation_status
plt.bar(range(len(x)), values)

ax = plt.subplot()
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x)
ax.set_ylabel("Number of Species")
ax.set_title("Conservation Status by Species")
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[26]:


species['is_protected'] = np.where(species['conservation_status'] != 'No Intervention', True, False)
species.head()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[27]:


category_counts = species.groupby(['category', 'is_protected']).count().scientific_name.reset_index()


# Examine `category_count` using `head()`.

# In[28]:


category_counts.head(10)


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[29]:


category_pivot = category_counts.pivot(index='category', columns='is_protected', values='scientific_name')


# Examine `category_pivot`.

# In[30]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[31]:


category_pivot.columns = ['not_protected','protected']
category_pivot.head()


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[32]:


category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)


# Examine `category_pivot`.

# In[33]:


category_pivot.head(10)


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[34]:


contingency_mammal_bird = [[38,176],
                           [79,442]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[35]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[36]:


chi2, pval, dof, expected = chi2_contingency(contingency_mammal_bird)
print (pval)


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[37]:


contingency_mammal_reptile = [[38,176],
                              [5,74]]

chi2, pval, dof, expected = chi2_contingency(contingency_mammal_reptile)
print (pval)


# In[38]:


contingency_mammal_amphibian = [[38,176],
                              [7,73]]

chi2, pval, dof, expected = chi2_contingency(contingency_mammal_amphibian)
print (pval)


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[100]:


observations = pd.read_csv("observations.csv")
observations.head(10)


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[77]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[78]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[91]:


species['is_sheep'] = species.apply(lambda row: True 
                                            if 'Sheep' in row['common_names'] 
                                            else False,
                                            axis = 1)

species[species['is_sheep'] == True]


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[92]:


species[species['is_sheep'] == True]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[99]:


sheep_species = species[(species['is_sheep'] == True) & (species['category'] == 'Mammal')]
sheep_species.head()


# In[101]:


observations.head(10)


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[106]:


sheep_observations = pd.merge(sheep_species, observations, how = 'left')
sheep_observations.head(15)


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[147]:


obs_by_park = sheep_observations.groupby(['park_name']).sum().observations.reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[148]:


plt.figure(figsize=(16,4))

values = obs_by_park.observations
x = obs_by_park.park_name
plt.bar(range(len(x)), values)

ax = plt.subplot()
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation = 45, ha="right")
ax.set_ylabel("Number of Observations")
ax.set_title("Observations of Sheep per Week")
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[39]:


minimum_detectable_effect = 100 * 0.05 / 0.15
number_of_sheep = 510
minimum_detectable_effect


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[151]:


Bryce_National_Park = 510 / 250
print (Bryce_National_Park)


# In[149]:


Yellowstone_National_Park = 510 / 507
print (Yellowstone_National_Park)

