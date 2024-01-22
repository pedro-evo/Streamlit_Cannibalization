import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load data
shared_clients = pd.read_parquet('shared_clients.parquet')
missing_clients = pd.read_parquet('missing_clients.parquet')
all_purchases_df = pd.read_parquet('all_purchases.parquet')

missing_clients_unique_count = missing_clients.groupby(['StoreID'])['StoresOfMissingClients'].nunique().reset_index()

# Streamlit App
st.title('Store Analysis App')

# Shared Clients Percentage
st.header('Shared Clients Percentage')
fig_shared_clients = px.bar(shared_clients, x='StoreID', y='SharedClientsPercentage', title='Shared Clients Percentage')
st.plotly_chart(fig_shared_clients, use_container_width=True)

# Heatmap: Total Count of Unique Missing Clients for Each Store
st.header('Heatmap: Total Count of Unique Missing Clients for Each Store')
fig_heatmap = px.imshow(missing_clients_unique_count[['StoresOfMissingClients']], x=['StoresOfMissingClients'],
                        y=missing_clients_unique_count['StoreID'],
                        labels=dict(color='Total Missing Clients'),
                        color_continuous_scale='viridis')

st.plotly_chart(fig_heatmap)

# All Purchases
st.header('All Purchases')
all_purchases_df_sorted = all_purchases_df.sort_values(by='DayOfYear')
fig_all_purchases = px.line(all_purchases_df_sorted, x='DayOfYear', y='Amount', color='StoreID',
                            title='All Purchases Over Days (Sorted)', labels={'Amount': 'Purchase Amount'},
                            category_orders={'StoreID': sorted(all_purchases_df['StoreID'].unique())})
st.plotly_chart(fig_all_purchases, use_container_width=True)

# Purchases Dataframe
st.header('Purchases Dataframe')
st.write(all_purchases_df)