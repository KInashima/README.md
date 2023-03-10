import streamlit as st
import pandas as pd
import plotly_express as px

st.header('Sprint 4: SDA US Vehicles Analysis')

veh_info_df=pd.read_csv(r'vehicles_us.csv')

st.plotly_chart(fig_dom_time, theme=None, use_container_width=True)
st.plotly_chart(fig_int_time, theme=None, use_container_width=True)

st.plotly_chart(fig_dom_price, theme=None, use_container_width=True)
st.plotly_chart(fig_int_price, theme=None, use_container_width=True)