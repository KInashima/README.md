import streamlit as st
import pandas as pd
import plotly_express as px

st.header('Sprint 4: SDA US SUV Vehicles Analysis')
# %%
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats as stat
import numpy as np
from matplotlib import pyplot as plt

# %%
veh_info_df=pd.read_csv('vehicles_us.csv')
print(veh_info_df)

# %%
veh_info_df['date_posted']=pd.to_datetime(veh_info_df['date_posted'],format='%Y-%m-%d')
veh_info_df['year']=veh_info_df['date_posted'].dt.year
veh_info_df['age']=veh_info_df['year']-veh_info_df['model_year']

# %%
veh_info_df.info()

veh_info_df=veh_info_df.dropna()

# %%
veh_info_df=veh_info_df.astype({'price':'float64','model_year':'float64','cylinders':'float64','odometer':'float64','is_4wd':'float64','days_listed':'float64'})
veh_info_df=veh_info_df.astype({'price':'int64','model_year':'int64','cylinders':'int64','is_4wd':'int64','days_listed':'int64'})

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

# %%
excellent_car=veh_info_df[veh_info_df['condition']=='excellent']
domesetic_maker=['chrysler','chevrolet','gmc','ram', 'jeep','ford','dodge', 'buick','cadillac']
excellent_car_dom=excellent_car.query("make in @domesetic_maker")
excellent_suv_dom=excellent_car_dom[excellent_car_dom['type']=='SUV']

international_maker=['honda','subaru','nissan','toyota','bmw','hyundai','kia','volkswagen','acura']
excellent_car_int=excellent_car.query("make in @international_maker")
excellent_suv_int=excellent_car_int[excellent_car_int['type']=='SUV']

# %% [markdown]
# Analyzing the mean posting days between domestic and foreign SUV make and their model years

# %%
dom_time=excellent_suv_dom.groupby(['make','model_year'])['days_listed'].mean().reset_index()
int_time=excellent_suv_int.groupby(['make','model_year'])['days_listed'].mean().reset_index()

# %%
fig_dom_time = px.histogram(dom_time, x="model_year", y="days_listed",color='make', barmode='group', labels={"model_year":"Year", "days_listed":"Days"}, title="Days vs SUV Make and Year")
#fig_dom_time.show()

# %%
fig_int_time = px.histogram(int_time, x="model_year", y="days_listed",color='make', barmode='group', labels={"model_year":"Year", "days_listed":"Days"}, title="Days vs SUV Make and Year")
#fig_int_time.show()

# %%
dom_time_mean=dom_time['days_listed'].mean()
int_time_mean=int_time['days_listed'].mean()
dom_time_var = np.var(dom_time['days_listed'])
int_time_var = np.var(int_time['days_listed'])
dom_time_std=np.std(dom_time['days_listed'])
int_time_std=np.std(int_time['days_listed'])

# %% [markdown]
# N0: Foreign Make SUV listing dates are different than domestic
# N1: Foeign and Domestic SUV make listing dates are similar

# %%
alpha = 0.05

results = stat.ttest_ind(dom_time['days_listed'], int_time['days_listed'], equal_var=False)

print('p-value:', results.pvalue)

if results.pvalue < alpha:
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")

# %% [markdown]
# Analyzing the mean price between domestic and foreign SUV make and their model years

# %%
dom_price=excellent_suv_dom.groupby(['make','model_year'])['price'].mean().reset_index()
int_price=excellent_suv_int.groupby(['make','model_year'])['price'].mean().reset_index()

# %%
fig_dom_price = px.scatter(dom_price, x="model_year", y="price",color='make', labels={"model_year":"Year", "price":"USD"}, title="Price vs SUV Make and Year")
#fig_dom_price.show()

# %%
fig_int_price = px.scatter(int_price, x="model_year", y="price",color='make', labels={"model_year":"Year", "price":"USD"}, title="Price vs SUV Make and Year")
#fig_int_price.show()

# %%
dom_price_mean=dom_price['price'].mean()
int_price_mean=int_price['price'].mean()
dom_price_var = np.var(dom_price['price'])
int_price_var = np.var(int_price['price'])
dom_price_std=np.std(dom_price['price'])
int_price_std=np.std(int_price['price'])

# %% [markdown]
# N0: Foreign Make SUV prices are different than domestic
# N1: Foeign and Domestic SUV make prices are similar

# %%
alpha = 0.05

results = stat.ttest_ind(dom_price['price'], int_price['price'], equal_var=False)

print('p-value:', results.pvalue)

if results.pvalue < alpha:
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")

st.plotly_chart(fig_dom_time, theme=None, use_container_width=True)
st.plotly_chart(fig_int_time, theme=None, use_container_width=True)

st.plotly_chart(fig_dom_price, theme=None, use_container_width=True)
st.plotly_chart(fig_int_price, theme=None, use_container_width=True)

different=st.checkbox('Are the analysis between Foreign and Domestic SUV Satistically Different?')
if different:
    st.write('They are not')
