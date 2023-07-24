import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px


# Function to load data from SQLite into a pandas dataframe
def load_data_from_sqlite(table_name):
    conn = sqlite3.connect('phonepe_data.db')
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Load data into pandas dataframes
agg_trans_df = load_data_from_sqlite('agg_trans')
agg_user_df = load_data_from_sqlite('agg_user')
map_trans_df = load_data_from_sqlite('map_trans')
map_user_df = load_data_from_sqlite('map_user')
top_trans_dist_df = load_data_from_sqlite('top_trans_dist')
top_trans_pin_df = load_data_from_sqlite('top_trans_pin')
top_user_dist_df = load_data_from_sqlite('top_user_dist')
top_user_pin_df = load_data_from_sqlite('top_user_pin')

# Rest of the code for creating the Streamlit app and defining the dashboards
st.set_page_config(
    page_title='PhonePe Data Visualization', layout='wide',
    page_icon='C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\phonepe_logo.png'
)

#Overview Dashboard 
def create_overview_dashboard():
    st.title(':violet[Phonepe Data Visualization] :smile')
    st.subheader('Dashboard Overview')
    st.write('The PhonePe data visualization dashboard provides comprehensive insights into the transactional and user'
             'data for the specified time period. It offers a visual representation of key metrics, enabling data '
             'analysis and informed decision-making. '
             'The dashboard is designed to facilitate an in-depth understanding of transaction patterns, user behavior,'
             'and regional trends.')
    st.subheader('Summary')
    summary = '- Transaction Trends: Visualize the overall transaction trends over time, such as the total number of' \
              'transactions and transaction amounts. Identify the quarters or years with the highest transaction ' \
              'volumes and track the growth or decline over the specified period. Highlight the most common ' \
              'transaction types, such as peer-to-peer transfers, bill payments, or online purchases. ' \
              'Analyze the distribution of transaction types and identify any emerging trends or shifts in ' \
              'user preferences.\n\n' \
              '- User Engagement: Showcase user engagement metrics, including the number of registered users, ' \
              'app opens,and user activity patterns. Highlight any notable trends, such as periods of increased ' \
              'user engagement or changes in user behavior.\n\n' \
              '- Regional Insights: Explore regional variations in transactional activity and user behavior. ' \
              'Identify regions or districts with the highest transaction volumes, user registrations, or app opens. ' \
              'Analyze the geographical distribution of transactions and users to uncover any regional patterns or ' \
              'anomalies.\n\n' \
              '- Key Performance Indicators: Present the key performance indicators (KPIs) that are critical for ' \
              'measuring the success of the platform. This may include metrics like transaction conversion rates, ' \
              'user retention rates, or average transaction amounts.\n\n' \
              '- Insights for Decision-Making: Provide actionable insights and observations based on the data ' \
              'analysis. Identify areas of improvement, potential growth opportunities, or any operational ' \
              'challenges that require attention. These insights can help guide strategic decision-making and ' \
              'optimize business performance\n\n.'
    st.write(summary)
    st.subheader('App Performance Overview')
    col1, col2, col3 = st.columns(3)

    total_reg_users = top_user_dist_df['Registered_users'].sum()
    col1.metric(
        label='Total Registered Users',
        value='{:.2f} Cr'.format(total_reg_users / 100000000),
        delta='Forward Trend'
    )

    total_app_opens = map_user_df['App_opens'].sum()
    col2.metric(
        label='Total App Opens', value='{:.2f} Cr'.format(total_app_opens / 100000000),
        delta='Forward Trend'
    )

    total_trans_count = agg_trans_df['Transaction_count'].sum()
    col3.metric(label='Total Transaction Count', value='{:.2f} Cr'.format(total_trans_count / 10000000),
                delta='Forward Trend')

    # Use the loaded dataframes to create visualizations and insights

#Transaction Trends Dashboard
def transaction_trends_dashboard():
    st.title("Transaction Trends Dashboard")
    st.write("Visualize transaction trends using maps.")

    # Your data
    data = {
        'State': ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                  'Chhattisgarh', 'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                  'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                  'Uttarakhand', 'West Bengal'],
        'Transaction_count': [7747331, 5321987775, 27274484, 528422472, 2745429444, 90820816, 941074354, 43966520,
                              3274904754, 98849639, 2052224247, 1870596824, 170818031, 164904607, 1008027640,
                              9570042576, 822459542, 7123601, 166804, 4463695860, 10389479956, 45147601, 20197849,
                              5796340, 17180851, 2561254352, 59384639, 582273955, 5130073858, 18750367, 2742806151,
                              9143814959, 32364668, 4636625871, 440122775, 2687915807]
    }

    df = pd.DataFrame(data)

    # Create a choropleth map using Plotly
    fig = px.choropleth(
        df,
        geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
        locations='State',  # Column in 'df' that corresponds to the states
        featureidkey='properties.ST_NM',  # Key in GeoJSON properties that corresponds to the states
        color='Transaction_count',  # Column in 'df' containing the data to be visualized
        color_continuous_scale='YlGnBu',  # Color scale (adjust as needed)
        projection='mercator',  # Map projection (you can choose other projections as well)
        hover_name='State',  # Column in 'df' to be shown on hover
        hover_data={'Transaction_count': True},  # Additional data on hover
        labels={'Transaction_count': 'Transaction Count'},  # Label for the colorbar
    )

    # Update the layout of the map
    fig.update_geos(
        scope='asia',  # Set the scope to 'asia' for Indian states
        center=dict(lat=20, lon=77),  # Set the center to approximate latitude and longitude of India
        projection_scale=3.5,  # Adjust the projection scale for zooming
    )

    fig.update_layout(
        title_text='Transaction count by State',
        title_x=0.5,
        geo=dict(
            showcoastlines=True,
            coastlinewidth=0.5,
            showland=True,
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showocean=True,
            oceancolor='rgb(230, 230, 230)',
        ),
    )

    # Show the map using st.plotly_chart
    st.plotly_chart(fig)

    # Convert filtered data to a DataFrame
    filtered_df = pd.DataFrame(agg_trans_df, columns=['Year', 'Quarter', 'Transaction_count', 'Transaction_amount'])

    # Convert transaction amount to crores
    filtered_df['Transaction_amount_crores'] = filtered_df['Transaction_amount'] / 10000000
    filtered_df['Transaction_count_crores'] = filtered_df['Transaction_count'] / 10000000

    # Bar plot for transaction count over time
    st.subheader("Transaction Count (in Crores)")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=filtered_df, x='Year', y='Transaction_count_crores', ax=ax1)
    ax1.set_xlabel('Quarter')
    ax1.set_ylabel('Transaction Count')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

    # Add data labels to the bar chart
    for p in ax1.patches:
        value = p.get_height()
        ax1.annotate(f"{value:.2f}", (p.get_x() + p.get_width() / 2., value), ha='center', va='bottom', fontsize=10)

    st.pyplot(fig1)

    # Bar plot for transaction amount over time in crores
    st.subheader("Transaction Amount (in Crores)")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=filtered_df, x='Year', y='Transaction_amount_crores', ax=ax2)
    ax2.set_xlabel('Quarter')
    ax2.set_ylabel('Transaction Amount (in Crores)')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

    # Add data labels to the bar chart in crores
    for p in ax2.patches:
        value = p.get_height()
        ax2.annotate(f"{value:.2f}", (p.get_x() + p.get_width() / 2., value), ha='center', va='bottom', fontsize=10)

    st.pyplot(fig2)

    def autopct_format(pct):
        if pct >= threshold:
            return f"{pct:.1f}%"
        else:
            return ""

    # Define a custom formatting function for crores
    def format_crores(value):
        crore_value = value / 10000000  # Divide by 10 million to get the value in crores
        formatted_value = '{:,.2f} Cr'.format(crore_value)  # Format the value with two decimal places and 'Cr' suffix
        return formatted_value

    # Bar plot for quarters with highest transaction volumes
    st.subheader("Quarters with Highest Transaction Volumes")
    max_quarters = agg_trans_df.groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
    max_quarters = max_quarters.sort_values('Transaction_count', ascending=False).head(10)

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figure size as per your preference
    ax.bar(max_quarters['Year'].apply(str) + '-' + max_quarters['Quarter'].apply(str),
           max_quarters['Transaction_count'])

    # Add data labels to the bar chart with formatted values in crores
    for i, value in enumerate(max_quarters['Transaction_count']):
        formatted_value = format_crores(value)
        ax.text(i, value, formatted_value, ha='center', va='bottom')

    # Customize the chart appearance
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Transaction Count (in Crores)')
    ax.set_title('Quarters with Highest Transaction Volumes')

    # Rotate the x-axis labels if needed
    plt.xticks(rotation=45)

    # Display the bar chart
    st.pyplot(fig)

    # Popular transaction types
    st.subheader("Popular Transaction Types by Transaction Count")

    popular_transaction_types = agg_trans_df.groupby('Transaction_type')['Transaction_count'].sum().reset_index()
    popular_transaction_types = popular_transaction_types.sort_values('Transaction_count', ascending=False).head(10)

    # Create data for the pie chart
    labels = popular_transaction_types['Transaction_type']
    values = popular_transaction_types['Transaction_count']

    # Set a threshold for hiding values
    threshold = 0.5

    # Filter the values and labels to exclude small values
    filtered_values = values[values >= threshold]
    filtered_labels = labels[values >= threshold]

    # Calculate the sum of small values
    small_values_sum = values[values < threshold].sum()

    # Calculate the percentage of small values
    small_values_percentage = (small_values_sum / values.sum()) * 100

    # Create the pie chart with custom autopct function
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjust the figure size as per your preference
    wedges, texts, autotexts = ax.pie(filtered_values, autopct=autopct_format, startangle=90)

    # Hide small values from the chart
    for i, autotext in enumerate(autotexts):
        if filtered_values[i] / values.sum() < small_values_percentage / 100:
            autotext.set_text('')  # Hide the autopct text

    # Adjust the chart text properties
    for text in texts:
        text.set_fontsize(10)  # Set the font size for labels

    # Adjust the position of the chart to avoid label overlapping
    ax.legend(wedges, filtered_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Display the pie chart
    st.pyplot(fig)

#Top performers dashboard
def create_top_performers_dashboard():
    st.title("Top Performers Dashboard")

    # Load the data
    df = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_Trans.csv')
    df1 = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Agg_User.csv')
    df2 = pd.read_csv('C:\\Users\\admin\\PycharmProjects\\pythonProject\\phonepe\\Map_User.csv')

    # Define the dropdown options for each subheader
    options = {
        "Top Performing States by Transaction Count": df.groupby('State')['Transaction_count'].sum().nlargest(10),
        "Top Performing States by Transaction Amount": df.groupby('State')['Transaction_amount'].sum().nlargest(10),
        "Top Performing Brands by Transaction Count": df1.groupby('Brand')['Transaction_count'].sum().nlargest(10),
        "Top Performing States by Registered Users": df2.groupby('State')['Registered_users'].sum().nlargest(10),
        "Top Performing States by App Opens": df2.groupby('State')['App_opens'].sum().nlargest(10),
        "Low Performing States by Transaction Count": df.groupby('State')['Transaction_count'].sum().nsmallest(10),
        "Low Performing States by Registered Users": df2.groupby('State')['Registered_users'].sum().nsmallest(10),
        "Low Performing States by App Opens": df2.groupby('State')['App_opens'].sum().nsmallest(10)
    }

    # Create dropdown for user to select subheader
    selected_subheader = st.selectbox("Select Subheader", list(options.keys()))

    # Display the selected subheader
    st.subheader(selected_subheader)

    # Get the data based on selected subheader
    data_to_plot = options[selected_subheader]

    # Plot the data
    fig, ax = plt.subplots()
    data_to_plot.plot(kind='bar', ax=ax)
    ax.set_ylabel(selected_subheader.split(" by ")[-1])
    st.pyplot(fig)

    # Add option to view data in table
    if st.checkbox("View Data as Table"):
        st.write(data_to_plot)

    # Download data as CSV
    st.subheader("Download Data")
    st.download_button("Download Data as CSV", data_to_plot.to_csv(), file_name="performance_data.csv")

#User engagement dashboard
def create_user_engagement_dashboard():
    st.title("User Engagement Dashboard")
    st.write("Showcasing user engagement metrics and activity patterns.")

    # Calculate total registered users in crore
    total_reg_users = map_user_df['Registered_users'].sum() / 10000000

    # Calculate total app opens in crore
    total_app_opens = map_user_df['App_opens'].sum() / 10000000

    # Filter data for 2018 and 2022
    reg_users_2018 = map_user_df.loc[map_user_df['Year'] == 2018, 'Registered_users'].sum() / 10000000
    reg_users_2022 = map_user_df.loc[map_user_df['Year'] == 2022, 'Registered_users'].sum() / 10000000

    app_opens_2019 = map_user_df.loc[map_user_df['Year'] == 2019, 'App_opens'].sum() / 10000000
    app_opens_2022 = map_user_df.loc[map_user_df['Year'] == 2022, 'App_opens'].sum() / 10000000

    # Calculate percentage increase
    reg_users_increase = (reg_users_2022 - reg_users_2018) / reg_users_2018 * 100
    app_opens_increase = (app_opens_2022 - app_opens_2019) / app_opens_2019 * 100

    # Create columns for registered users and app opens
    col1, col2 = st.columns(2)

    # Display metrics for registered users
    with col1:
        st.subheader("Registered Users")
        st.metric(label="Total", value=total_reg_users)
        st.metric(label="Increase from 2018 to 2022", value=f"{reg_users_increase:.2f}%")

    # Display metrics for app opens
    with col2:
        st.subheader("App Opens")
        st.metric(label="Total", value=total_app_opens)
        st.metric(label="Increase from 2019 to 2022", value=f"{app_opens_increase:.2f}%")

    # User activity patterns
    st.subheader("User Activity Patterns")
    st.write("Visualize user activity patterns over time.")

    # Group the data by Year and Quarter and calculate the sum of Registered_users
    activity_df = map_user_df.groupby(['Year', 'Quarter'])['Registered_users'].sum().reset_index()

    # Convert Registered_users values to crores
    activity_df['Registered_users'] = activity_df['Registered_users'] / 10000000

    # Create the area plot with hover over data
    chart = alt.Chart(activity_df).mark_area().encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year - Quarter')),
        y=alt.Y('Registered_users:Q', axis=alt.Axis(title='Registered Users (in Crores)')),
        color='Quarter:N',
        tooltip=['Year:O', 'Quarter:N', 'Registered_users:Q']
    ).properties(
        width=800,
        height=600,
        title='Registered Users by Year and Quarter'
    )

    # Display the plot
    st.altair_chart(chart)

    # Group the data by Year and Quarter and calculate the sum of App_opens
    activity_df = map_user_df.groupby(['Year', 'Quarter'])['App_opens'].sum().reset_index()

    # Convert App_opens values to crores
    activity_df['App_opens'] = activity_df['App_opens'] / 10000000

    # Create the area plot for App_opens
    chart_app_opens = alt.Chart(activity_df).mark_area().encode(x=alt.X('Year:O',
                                                                        axis=alt.Axis(title='Year - Quarter')),
                                                                y=alt.Y('App_opens:Q',
                                                                        axis=alt.Axis(title='App Opens (in Crores)')),
                                                                color='Quarter:N',
                                                                tooltip=['Year:O', 'Quarter:N',
                                                                         'App_opens:Q']).properties(width=600,
                                                                            height=400,
                                                                            title='App Opens by Year and Quarter')
    st.altair_chart(chart_app_opens)

#Regional Analysis Dashboard
def create_regional_analysis_dashboard():
    st.title("Regional Analysis Dashboard")
    st.write("Explore regional variations in transactional activity and user behavior.")

    # Highest transaction volumes by region
    st.subheader("Region-wise Transaction Count")
    # Your data
    data = {
        'State': ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                  'Chhattisgarh', 'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                  'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                  'Uttarakhand', 'West Bengal'],
        'Transaction_count': [7747331, 5321987775, 27274484, 528422472, 2745429444, 90820816, 941074354, 43966520,
                              3274904754, 98849639, 2052224247, 1870596824, 170818031, 164904607, 1008027640,
                              9570042576, 822459542, 7123601, 166804, 4463695860, 10389479956, 45147601, 20197849,
                              5796340, 17180851, 2561254352, 59384639, 582273955, 5130073858, 18750367, 2742806151,
                              9143814959, 32364668, 4636625871, 440122775, 2687915807]
    }

    df = pd.DataFrame(data)

    # Create a choropleth map using Plotly
    fig = px.choropleth(
        df,
        geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
        locations='State',  # Column in 'df' that corresponds to the states
        featureidkey='properties.ST_NM',  # Key in GeoJSON properties that corresponds to the states
        color='Transaction_count',  # Column in 'df' containing the data to be visualized
        color_continuous_scale='YlGnBu',  # Color scale (adjust as needed)
        projection='mercator',  # Map projection (you can choose other projections as well)
        hover_name='State',  # Column in 'df' to be shown on hover
        hover_data={'Transaction_count': True},  # Additional data on hover
        labels={'Transaction_count': 'Transaction Count'},  # Label for the colorbar
    )

    # Update the layout of the map
    fig.update_geos(
        scope='asia',  # Set the scope to 'asia' for Indian states
        center=dict(lat=20, lon=77),  # Set the center to approximate latitude and longitude of India
        projection_scale=3.5,  # Adjust the projection scale for zooming
    )

    fig.update_layout(
        title_text='Transaction count by State',
        title_x=0.5,
        geo=dict(
            showcoastlines=True,
            coastlinewidth=0.5,
            showland=True,
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showocean=True,
            oceancolor='rgb(230, 230, 230)',
        ),
    )

    # Show the map using st.plotly_chart
    st.plotly_chart(fig)

    # User registrations by district
    st.subheader("Region-wise Registered Users")
    # Your data
    data = {
        'State': ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                  'Chhattisgarh', 'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                  'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                  'Uttarakhand', 'West Bengal'],
        'Registered_users': [877060, 304846445, 3923777, 54501884, 229268557, 7131413, 73784322, 5320467,
                             178712854, 9295395, 244859978, 164747824, 26540895, 19270617, 88022237,
                             394779919, 106421188, 1146737, 71071, 246227007, 612264427, 4848047, 3004396,
                             1312099, 3139352, 155003118, 5541871, 90691887, 293660644, 2565902, 265650824,
                             285384608, 7243586, 486403492, 46392181, 279162592]
    }

    df = pd.DataFrame(data)

    # Create a choropleth map using Plotly
    fig = px.choropleth(
        df,
        geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
        locations='State',  # Column in 'df' that corresponds to the states
        featureidkey='properties.ST_NM',  # Key in GeoJSON properties that corresponds to the states
        color='Registered_users',  # Column in 'df' containing the data to be visualized
        color_continuous_scale='YlGnBu',  # Color scale (adjust as needed)
        projection='mercator',  # Map projection (you can choose other projections as well)
        hover_name='State',  # Column in 'df' to be shown on hover
        hover_data={'Registered_users': True},  # Additional data on hover
        labels={'Registered_users': 'Registered Users'},  # Label for the colorbar
    )

    # Update the layout of the map
    fig.update_geos(
        scope='asia',  # Set the scope to 'asia' for Indian states
        center=dict(lat=20, lon=77),  # Set the center to approximate latitude and longitude of India
        projection_scale=3.5,  # Adjust the projection scale for zooming
    )

    fig.update_layout(
        title_text='Registered Users by State',
        title_x=0.5,
        geo=dict(
            showcoastlines=True,
            coastlinewidth=0.5,
            showland=True,
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showocean=True,
            oceancolor='rgb(230, 230, 230)',
        ),
    )

    # Show the map using st.plotly_chart
    st.plotly_chart(fig)

    # App opens by district
    st.subheader("Region-wise App Opens")
    # Your data
    data = {
        'State': ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                  'Chhattisgarh', 'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                  'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                  'Uttarakhand', 'West Bengal'],
        'App_opens': [30239151, 13722337399, 237984577, 1928702082, 4949547310, 83551087, 3153154188, 97314971,
                      2711944871, 215475239, 5084900499, 3528637433, 626953495, 505143796, 2878737423,
                      18270997380, 1499175282, 67243395, 540213, 11819718275, 20014077598, 132111479, 132352572,
                      67447633, 132657865, 5625191927, 94230447, 1358705390, 16708044297, 87220065, 6434234065,
                      12684892712, 147632668, 10226840000, 1142274072, 4288352279]
    }

    df = pd.DataFrame(data)

    # Create a choropleth map using Plotly
    fig = px.choropleth(
        df,
        geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
        locations='State',  # Column in 'df' that corresponds to the states
        featureidkey='properties.ST_NM',  # Key in GeoJSON properties that corresponds to the states
        color='App_opens',  # Column in 'df' containing the data to be visualized
        color_continuous_scale='YlGnBu',  # Color scale (adjust as needed)
        projection='mercator',  # Map projection (you can choose other projections as well)
        hover_name='State',  # Column in 'df' to be shown on hover
        hover_data={'App_opens': True},  # Additional data on hover
        labels={'App_opens': 'App Opens'},  # Label for the colorbar
    )

    # Update the layout of the map
    fig.update_geos(
        scope='asia',  # Set the scope to 'asia' for Indian states
        center=dict(lat=20, lon=77),  # Set the center to approximate latitude and longitude of India
        projection_scale=3.5,  # Adjust the projection scale for zooming
    )

    fig.update_layout(
        title_text='App Opens by State',
        title_x=0.5,
        geo=dict(
            showcoastlines=True,
            coastlinewidth=0.5,
            showland=True,
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showocean=True,
            oceancolor='rgb(230, 230, 230)',
        ),
    )

    # Show the map using st.plotly_chart
    st.plotly_chart(fig)


# Use the loaded dataframes to perform regional analysis and generate insights


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Overview Dashboard", "Transaction Trends",
                                      "Top Performers Dashboard", "User Engagement Dashboard",
                                      "Regional Analysis Dashboard"))

    if page == "Overview Dashboard":
        create_overview_dashboard()
    elif page == "Transaction Trends":
        transaction_trends_dashboard()
    elif page == "Top Performers Dashboard":
        create_top_performers_dashboard()
    elif page == "User Engagement Dashboard":
        create_user_engagement_dashboard()
    elif page == "Regional Analysis Dashboard":
        create_regional_analysis_dashboard()


if __name__ == '__main__':
    main()
