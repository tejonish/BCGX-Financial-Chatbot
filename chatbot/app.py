import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("BCG.csv")

# Add calculated columns
df["Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
df["Debt Ratio"] = df["Liabilities"] / df["Assets"]

# Title
st.title("📊 Financial AI Chatbot")

st.write("Ask about Apple, Microsoft, or Tesla financials")

# Sample questions
st.info(
    """
💡 Try asking:
- What is Microsoft's revenue?
- Show Tesla profit margin
- What is Apple's debt ratio?
- Which company has highest revenue?
"""
)

# Sidebar dataset toggle
st.sidebar.title("📊 Data Panel")

if st.sidebar.checkbox("Show full dataset"):
    st.sidebar.dataframe(
        df.style.format(
            {
                "Revenue": "{:,.0f}",
                "Net Income": "{:,.0f}",
                "Operating Cash Flow": "{:,.0f}",
                "Profit Margin (%)": "{:.2f}",
                "Debt Ratio": "{:.2f}",
            }
        )
    )


# Donut chart function
def create_donut(company_data, company):
    latest = company_data.iloc[-1]

    values = [latest["Revenue"], latest["Net Income"], latest["Operating Cash Flow"]]

    labels = ["Revenue", "Net Income", "Cash Flow"]

    fig = px.pie(
        values=values,
        names=labels,
        hole=0.5,
        title=f"{company} Financial Distribution (Latest Year)",
    )

    return fig


# Chatbot function
def chatbot(query):
    query = query.lower().strip()

    if "apple" in query:
        company = "Apple"
    elif "microsoft" in query:
        company = "Microsoft"
    elif "tesla" in query:
        company = "Tesla"
    else:
        return None, "Please mention a company (Apple, Microsoft, Tesla)."

    data = df[df["Company"] == company].sort_values(by="Year")

    if "revenue" in query:
        value = data.iloc[-1]["Revenue"]
        return company, f"{company}'s latest revenue is {value} million USD."

    elif "net income" in query or "profit" in query:
        latest = data.iloc[-1]["Net Income"]
        prev = data.iloc[-2]["Net Income"]
        change = latest - prev

        if change >= 0:
            return company, f"{company}'s net income increased by {change} million USD."
        else:
            return (
                company,
                f"{company}'s net income decreased by {abs(change)} million USD.",
            )

    elif "profit margin" in query:
        value = data.iloc[-1]["Profit Margin (%)"]
        return company, f"{company}'s profit margin is {round(value,2)}%."

    elif "debt" in query:
        value = data.iloc[-1]["Debt Ratio"]
        return company, f"{company}'s debt ratio is {round(value,2)}."

    elif "highest revenue" in query:
        latest = df[df["Year"] == df["Year"].max()]
        top = latest.loc[latest["Revenue"].idxmax()]
        return (
            None,
            f"{top['Company']} has the highest revenue with {top['Revenue']} million USD.",
        )

    else:
        return (
            company,
            "Try asking like: 'Microsoft revenue', 'Tesla profit', 'Apple debt'.",
        )


# Input
query = st.text_input("Enter your question:")

# Output
if query:
    company, response = chatbot(query)
    st.success(response)

    # Sidebar company-specific data + chart
    if company:
        company_data = df[df["Company"] == company].sort_values(by="Year")

        st.sidebar.subheader(f"{company} Data")
        st.sidebar.dataframe(
            company_data.style.format(
                {
                    "Revenue": "{:,.0f}",
                    "Net Income": "{:,.0f}",
                    "Operating Cash Flow": "{:,.0f}",
                    "Profit Margin (%)": "{:.2f}",
                    "Debt Ratio": "{:.2f}",
                }
            )
        )

        #  Donut chart
        fig = create_donut(company_data, company)
        st.sidebar.plotly_chart(fig, use_container_width=True)
