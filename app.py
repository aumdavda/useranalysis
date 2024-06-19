import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRddBCGuZIZZBlpOx2WR_sD6IN9HF-Ah04p-BTSrOoAENWfP8zPQxm5TrKSr7ljABnZVhnPA2N_H3HI/pub?gid=304981720&single=true&output=csv")

# Preprocess data 
df = df.fillna({
    'socialNbFollowers': 0,
    'socialNbFollows': 0,
    'productsListed': 0,
    'productsSold': 0,
    'productsPassRate': df['productsPassRate'].mean(),
    'socialProductsLiked': 0,
    'productsWished': 0,
    'productsBought': 0,
    'daysSinceLastLogin': df['daysSinceLastLogin'].median(),
    'seniorityAsMonths': df['seniorityAsMonths'].median()
})

df = df.drop_duplicates()

# Set page config
st.set_page_config(page_title="E-commerce User Insights", page_icon=":bar_chart:")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    .sidebar .sidebar-content .sidebar-top {
        background-color: #4682B4;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        color: white;
        font-size: 18px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stButton button {
        background-color: #4682B4 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        margin-right: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #3A6884 !important;
    }
    .stSelectbox:hover .stSelectbox-label {
        background-color: #3A6884 !important;
    }
    .stSelectbox {
        width: 100%;
    }
    .stSelectbox-label {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("E-commerce User Insights")

# Sidebar Navigation
st.sidebar.title("Navigation")
options = st.sidebar.selectbox("Select an option", ["User Analysis", "Dataset", "Code"])

if options == "User Analysis":
    # Insights and Actions with Visualizations
    st.header("E-commerce User Analysis")

    # Insight: Number of Active Users
    st.subheader("Number of Active Users")
    st.markdown("""
    **Insight:** The number of active users is determined by filtering users with recent login activity (e.g., within the last 30 days).  
    **Actionable:** Focus on retention strategies to keep these users engaged, such as personalized recommendations and loyalty programs.
    """)
    fig, ax = plt.subplots()
    active_users = df[df['daysSinceLastLogin'] <= 30]
    sns.histplot(active_users['daysSinceLastLogin'], bins=30, ax=ax)
    ax.set_title('Distribution of Days Since Last Login for Active Users')
    st.pyplot(fig)

    # Insight: Common Themes Among Active Users
    st.subheader("Common Themes Among Active Users")
    st.markdown("""
    **Insight:** Active users tend to have higher engagement metrics, such as more products listed, sold, and a higher number of social interactions.  
    **Actionable:** Enhance features that promote user engagement, like social sharing, easy product listing processes, and community-building tools.
    """)
    fig, ax = plt.subplots()
    sns.scatterplot(x='socialNbFollowers', y='productsSold', data=active_users, ax=ax)
    ax.set_title('Products Sold vs. Social Followers for Active Users')
    st.pyplot(fig)

    # Insight: Number of Churned Users
    st.subheader("Number of Churned Users")
    st.markdown("""
    **Insight:** A significant portion of users have churned, defined by a long period since the last login (e.g., more than 180 days).  
    **Actionable:** Implement re-engagement campaigns, such as targeted emails or app notifications, to bring back inactive users.
    """)
    fig, ax = plt.subplots()
    churned_users = df[df['daysSinceLastLogin'] > 180]
    sns.histplot(churned_users['daysSinceLastLogin'], bins=30, ax=ax)
    ax.set_title('Distribution of Days Since Last Login for Churned Users')
    st.pyplot(fig)

    # Insight: Common Themes Among Churned Users
    st.subheader("Common Themes Among Churned Users")
    st.markdown("""
    **Insight:** Churned users often have low engagement metrics and minimal transactions (products sold or bought).  
    **Actionable:** Conduct user surveys to understand their pain points and improve the user experience to prevent future churn.
    """)
    fig, ax = plt.subplots()
    sns.scatterplot(x='socialNbFollowers', y='productsSold', data=churned_users, ax=ax)
    ax.set_title('Products Sold vs. Social Followers for Churned Users')
    st.pyplot(fig)

    # Insight: Time to Churn
    st.subheader("Time to Churn")
    st.markdown("""
    **Insight:** Many users tend to churn after a specific period (e.g., 6 months of inactivity).  
    **Actionable:** Introduce mid-lifecycle engagement strategies, such as special offers or incentives, around the identified churn period.
    """)
    fig, ax = plt.subplots()
    sns.histplot(df['seniorityAsMonths'], bins=30, ax=ax)
    ax.set_title('Distribution of Seniority in Months')
    st.pyplot(fig)

    # Insight: User Segmentation
    st.subheader("User Segmentation")
    st.markdown("""
    **Insight:** Users can be segmented based on their engagement levels, such as heavy users, moderate users, and light users.  
    **Actionable:** Tailor marketing and product strategies for each segment, ensuring heavy users are rewarded, and light users are encouraged to become more active.
    """)
    # Define user segments
    heavy_users = df[df['productsSold'] > 50]
    moderate_users = df[(df['productsSold'] > 10) & (df['productsSold'] <= 50)]
    light_users = df[df['productsSold'] <= 10]

    # Plot segmentation
    fig, ax = plt.subplots()
    sns.scatterplot(x='productsListed', y='productsSold', hue=df['productsSold'] > 50, data=df, ax=ax)
    ax.set_title('User Segmentation Based on Products Listed vs. Products Sold')
    st.pyplot(fig)

    # Insight: Average Likes Before a Product is Sold
    st.subheader("Average Likes Before a Product is Sold")
    st.markdown("""
    **Insight:** There is a noticeable trend in the number of likes a product receives before it is sold.  
    **Actionable:** Promote popular products based on social interactions and highlight them to potential buyers.
    """)
    fig, ax = plt.subplots()
    sns.scatterplot(x='socialProductsLiked', y='productsSold', data=df, ax=ax)
    ax.set_title('Products Sold vs. Products Liked')
    st.pyplot(fig)

elif options == "Dataset":
    # Display Dataset
    st.header("Dataset")
    st.write(df)

elif options == "Code":
    # Display Code
    st.write("Here is the code on Kaggle:", unsafe_allow_html=True)
    st.markdown("[Kaggle Code](https://www.kaggle.com/code/fluffyfingers/notebook98052fdca3)", unsafe_allow_html=True)
