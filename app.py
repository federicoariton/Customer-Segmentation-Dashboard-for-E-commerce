import streamlit as st
import pandas as pd
import plotly.express as px

# Load the segmented RFM dataset
df = pd.read_csv("segmented_customers_rfm.csv")

# Sidebar filters
st.sidebar.title("🔍 Filter Options")
selected_segment = st.sidebar.multiselect("Select Segment(s):", options=df['SegmentLabel'].unique(), default=df['SegmentLabel'].unique())

# Filtered Data
df_filtered = df[df['SegmentLabel'].isin(selected_segment)]

# Title
st.title("📊 RFM Customer Segmentation Dashboard")

# Segment Distribution
st.subheader("Customer Segment Distribution")
segment_counts = df_filtered['SegmentLabel'].value_counts().reset_index()
segment_counts.columns = ['SegmentLabel', 'Count']
fig_segment = px.bar(segment_counts, x='SegmentLabel', y='Count', color='SegmentLabel', title="Number of Customers per Segment")
st.plotly_chart(fig_segment)

# Average RFM Metrics by Segment
st.subheader("Average RFM Metrics per Segment")
avg_rfm = df_filtered.groupby('SegmentLabel')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
fig_rfm = px.bar(avg_rfm.melt(id_vars='SegmentLabel'), x='SegmentLabel', y='value', color='variable', barmode='group',
                 labels={'value': 'Average Value', 'variable': 'RFM Metric'},
                 title="Average RFM Scores by Segment")
st.plotly_chart(fig_rfm)

# PCA Cluster View
st.subheader("Customer Clusters (PCA 2D View)")
fig_pca = px.scatter(df_filtered, x='PCA1', y='PCA2', color='SegmentLabel',
                     title="Customer Segments Visualized in 2D Space",
                     labels={'PCA1': 'Principal Component 1', 'PCA2': 'Principal Component 2'})
st.plotly_chart(fig_pca)

# Show raw data
with st.expander("📂 View Raw Data"):
    st.dataframe(df_filtered)
