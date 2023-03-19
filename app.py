# %% [markdown]
# Sprint 4: SDA US SUV Vehicles Analysis

# %% [markdown]
# This notebook is going to follow through the process of how the vehicle data is imported, preprocessed through the data for adequate processing, data are grouped, and analysed for statistical significance.
# 
# The vehicle data is analyzed through the condition of the vehicle, to compare between following factors:
# 
# 1. The posting length vs foreign or dommestic SUV make and model year
# 2. The price vs foreign or domestic SUV make and model year
# 3. Last an option of comparing these variables for SUV model within the last 10 years.
# 

# %%
import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np
from scipy import stats as stat
from matplotlib import pyplot as plt

# %% [markdown]
# Necessary packages are imported

# %%
st.header('Sprint 4: SDA US SUV Vehicles Analysis')
txt = st.text_area('Analysis description', 'SUV is a popular type of vehicle, like its name, suggests it has a wide utility. This project is going to analyze how domestic and foreign make SUVs compare in a couple of factors. The first is how long they are posted before being sold. Second, is how the price of the SUV compares. Finally, they were both compared through the SUV condition')


# %%
veh_info_df=pd.read_csv('vehicles_us.csv')
print(veh_info_df)

# %%
veh_info_df['date_posted']=pd.to_datetime(veh_info_df['date_posted'],format='%Y-%m-%d')

# %%
veh_info_df=veh_info_df.dropna(subset=['model_year'])
veh_info_df=veh_info_df.fillna(0)
veh_info_df['paint_color']=veh_info_df['paint_color'].replace([0],'missing')
veh_info_df.info()

# %%
veh_info_df=veh_info_df.astype({'price':'float64','model_year':'float64','cylinders':'float64','odometer':'float64','is_4wd':'float64','days_listed':'float64'})
veh_info_df=veh_info_df.astype({'price':'int64','model_year':'int64','cylinders':'int64','is_4wd':'int64','days_listed':'int64'})

# %% [markdown]
# Up to this point the format of the data are reviewed, and the data type of certain columns are changed for appropriate processing. Especially certain data type that were object are changed to integers. The missing data were selectively modified. The model_year were removed due to being an important factor in the analysis. The other missing datas are either changed to 0, or stringed as 'missing'

# %%
veh_info_df['model'] = veh_info_df['model'].astype(str)
veh_info_df['make'] = veh_info_df['model'].apply(lambda x: x.split()[0])

# %%
print(veh_info_df['make'].unique())

# %%
unique_model=veh_info_df['model'].unique()
print(sorted(unique_model))

# %%
f150_wrong_names=['ford f-150']
f250_wrong_names=['ford f-250', 'ford f-250 sd', 'ford f-250 super duty','ford f250 super duty']
f350_wrong_names=['ford f-350 sd','ford f350 super duty']
f150='ford f150'
f250='ford f250'
f350='ford f350'

# %%
def replace_wrong_values(wrong_values, correct_value):
    for wrong_value in wrong_values:
        veh_info_df['model'] = veh_info_df['model'].replace(wrong_value, correct_value)

replace_wrong_values(f150_wrong_names, f150)
replace_wrong_values(f250_wrong_names, f250)
replace_wrong_values(f350_wrong_names, f350)

# %% [markdown]
# New column for make of Vehicle was created. Then viewed the unique names of make, and model, and corrected the model name that were repeated multiple times in multiple variance. This was most present with Fords names. 

# %% [markdown]
# 

# %% [markdown]
# Analyzing the mean days posted between domestic and foreign SUV make and their model years

# %%
states=['good', 'like new', 'fair', 'excellent', 'salvage', 'new']
cond_suv=st.selectbox("Condition of SUV", states)

# %%
recent=st.checkbox('SUV within Last 10 years')
if recent:
    veh_info_df=veh_info_df[veh_info_df['model_year']>2009]

# %% [markdown]
# Checkbox was added to compare recent car models within the 10 years of the data which is 2009.

# %%
domesetic_maker=['chrysler','chevrolet','gmc','ram', 'jeep','ford','dodge', 'buick','cadillac']
car_dom=veh_info_df.query("make in @domesetic_maker")
suv_dom=car_dom[car_dom['type']=='SUV']
suv_dom = suv_dom[suv_dom["condition"] == cond_suv]
dom_time=suv_dom.groupby(['make','model_year'])['days_listed'].mean().reset_index()
fig_dom_time = px.histogram(dom_time, x="model_year", y="days_listed",color='make', barmode='group', labels={"model_year":"Year", "days_listed":"Days"}, title="Days vs Domestic SUV Make and Year")
st.plotly_chart(fig_dom_time, theme=None, use_container_width=True)

# %%
international_maker=['honda','subaru','nissan','toyota','bmw','hyundai','kia','volkswagen','acura']
car_int=veh_info_df.query("make in @international_maker")
suv_int=car_int[car_int['type']=='SUV']
suv_int = suv_int[car_int["condition"] == cond_suv]
int_time=suv_int.groupby(['make','model_year'])['days_listed'].mean().reset_index()
fig_int_time= px.histogram(int_time, x="model_year", y="days_listed",color='make', barmode='group', labels={"model_year":"Year", "days_listed":"Days"}, title="Days vs Foreign SUV Make and Year")
st.plotly_chart(fig_int_time, theme=None, use_container_width=True)

# %%
dom_time_mean=dom_time['days_listed'].mean()
int_time_mean=int_time['days_listed'].mean()
dom_time_var = np.var(dom_time['days_listed'])
int_time_var = np.var(int_time['days_listed'])
dom_time_std=np.std(dom_time['days_listed'])
int_time_std=np.std(int_time['days_listed'])

# %% [markdown]
# N0: Foreign and Domestic SUV make listing dates are similar
# N1: Foreign Make SUV listing dates are statistically different than domestic

# %%
alpha = 0.05

hypo_results = stat.ttest_ind(dom_time['days_listed'], int_time['days_listed'], equal_var=False)

print('p-value:', hypo_results.pvalue)

if hypo_results.pvalue < alpha:
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")

# %%
st.text('N0: Foreign and Domestic SUV make listing dates are similar \nN1: Foreign Make SUV listing dates are statistically different than domestic')
st.text_area('P Value, if below 0.05 reject null hypothesis', hypo_results.pvalue)

# %% [markdown]
# Unique list for condition of the car was isolated. Then Select box was created to filter through the condition of the cars. The vehicles data were queried to group between foreign and domestic make of cars, and filtered for SUV type cars. The filtered and quired data was then filtered through the selectbox condition to filter through the condition of the cars. 
# 
# The make and model year data were correlated with the days listed, and get their mean. This was used to make a histogram, and passed through streamlit.
# 
# The data was passed through statistical analysis, to find mean, variance,  standard deviation, and t tested.

# %% [markdown]
# 

# %% [markdown]
# Analyzing the mean price between domestic and foreign SUV make and their model years

# %%
dom_price=suv_dom.groupby(['make','model_year'])['price'].mean().reset_index()
fig_dom_price = px.scatter(dom_price, x="model_year", y="price",color='make', labels={"model_year":"Year", "price":"USD"}, title="Price vs Domestic SUV Make and Year")
st.plotly_chart(fig_dom_price, theme=None, use_container_width=True)


# %%
int_price=suv_int.groupby(['make','model_year'])['price'].mean().reset_index()
fig_int_price = px.scatter(int_price, x="model_year", y="price",color='make', labels={"model_year":"Year", "price":"USD"}, title="Price vs Foreign SUV Make and Year")
st.plotly_chart(fig_int_price, theme=None, use_container_width=True)

# %%
dom_price_mean=dom_price['price'].mean()
int_price_mean=int_price['price'].mean()
dom_price_var = np.var(dom_price['price'])
int_price_var = np.var(int_price['price'])
dom_price_std=np.std(dom_price['price'])
int_price_std=np.std(int_price['price'])

# %% [markdown]
# N0: Foreign and Domestic SUV make prices are similar
# N1: Foreign Make SUV prices are statistically different than domestic

# %%
alpha = 0.05

hypo2_results = stat.ttest_ind(dom_price['price'], int_price['price'], equal_var=False)

print('p-value:', hypo2_results.pvalue)

if hypo2_results.pvalue < alpha:
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")

# %%
st.text('N0: Foreign and Domestic SUV make prices are similar \nN1: Foreign Make SUV prices are statistically different than domestic')
st.text_area('P Value, if below 0.05 reject null hypothesis', hypo2_results.pvalue)

# %% [markdown]
# The prior analysis continued, except processing the relationship of the price of the SUV make and their model year. The data was then modeled in a scatter plot.

# %% [markdown]
# Conclusion:
# 
# The selectbox appropriately filters through the conditions of the cars, and changes the behavior of the charts. The chart thats created appropriately represents the conditions set. The analytical data and the t test varies based upon the condition of the SUV.
# 
# The analysis indicates that there is no statistical difference in the days listed between foreign and domestic make of the SUV, through all the conditions. In retrospect, for the pricing there is statistical difference in the price between foreign and domestic make SUV, for the excellent and like new conditioned SUV. 
# 
# Within the last 10 years of the recent models price difference between the foreign and domestic make SUV were significant for like new, excellent, and good. 
# 
# Though, a large amount of data were removed due to the missing model years, the removal of those data were necessary for further processing of the data. 


