from pathlib import Path

import duckdb
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics Platform",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "retail_analytics" / "dev.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)


# --------------------------------------------------
# Dashboard header
# --------------------------------------------------

st.title("Retail Analytics Platform")
st.caption(
    "Executive analytics dashboard powered by DuckDB and dbt."
)


# --------------------------------------------------
# Executive KPIs
# --------------------------------------------------

sales_kpis = con.sql("""
    SELECT
        SUM(total_orders) AS total_orders,
        SUM(units_sold) AS total_units,
        SUM(revenue) AS total_revenue
    FROM sales_by_channel
""").fetchone()

customer_count = con.sql("""
    SELECT COUNT(*)
    FROM customer_metrics
""").fetchone()[0]

total_orders = sales_kpis[0]
total_units = sales_kpis[1]
total_revenue = sales_kpis[2]


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue / 1_000_000_000:.2f}B"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Units Sold",
    f"{total_units:,}"
)

col4.metric(
    "Customers",
    f"{customer_count:,}"
)


# --------------------------------------------------
# Monthly sales trend
# --------------------------------------------------

st.divider()
st.subheader("Sales Performance Over Time")

monthly_sales = con.sql("""
    SELECT
        month,
        total_orders,
        units_sold,
        revenue
    FROM monthly_sales
    ORDER BY month
""").df()

monthly_chart = px.line(
    monthly_sales,
    x="month",
    y="revenue",
    markers=True,
    labels={
        "month": "Month",
        "revenue": "Revenue"
    }
)

monthly_chart.update_layout(
    xaxis_title=None,
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)

monthly_chart.update_yaxes(
    tickprefix="$",
    tickformat="~s"
)

st.plotly_chart(
    monthly_chart,
    width="stretch"
)


# --------------------------------------------------
# Category and channel performance
# --------------------------------------------------

st.divider()
st.subheader("Sales Breakdown")

category_sales = con.sql("""
    SELECT
        category,
        units_sold,
        revenue
    FROM sales_by_category
    ORDER BY revenue DESC
""").df()

channel_sales = con.sql("""
    SELECT
        sales_channel,
        total_orders,
        units_sold,
        revenue
    FROM sales_by_channel
    ORDER BY revenue DESC
""").df()

left_col, right_col = st.columns(2)


# --------------------------------------------------
# Revenue by category
# --------------------------------------------------

with left_col:

    st.markdown("#### Revenue by Category")

    category_chart = px.bar(
        category_sales,
        x="revenue",
        y="category",
        orientation="h",
        labels={
            "revenue": "Revenue",
            "category": "Category"
        }
    )

    category_chart.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        xaxis_title="Revenue ($)",
        yaxis_title=None
    )

    category_chart.update_xaxes(
        tickprefix="$",
        tickformat="~s"
    )

    st.plotly_chart(
        category_chart,
        width="stretch"
    )


# --------------------------------------------------
# Revenue by sales channel
# --------------------------------------------------

with right_col:

    st.markdown("#### Revenue by Sales Channel")

    channel_chart = px.pie(
        channel_sales,
        names="sales_channel",
        values="revenue",
        hole=0.45
    )

    channel_chart.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        channel_chart,
        width="stretch"
    )


# --------------------------------------------------
# Customer and store performance
# --------------------------------------------------

st.divider()
st.subheader("Customer & Store Performance")


# --------------------------------------------------
# Customer summary
# --------------------------------------------------

customer_summary = con.sql("""
    SELECT
        loyalty_member,
        COUNT(*) AS customers,
        ROUND(AVG(total_spend), 2) AS avg_spend,
        ROUND(AVG(average_order_value), 2) AS avg_order_value
    FROM customer_metrics
    GROUP BY loyalty_member
    ORDER BY loyalty_member DESC
""").df()

customer_summary["customer_type"] = customer_summary[
    "loyalty_member"
].map({
    True: "Loyalty Member",
    False: "Non-Member"
})


# --------------------------------------------------
# Store data
# --------------------------------------------------

store_data = con.sql("""
    SELECT
        store_name,
        city,
        state,
        total_orders,
        units_sold,
        revenue
    FROM store_performance
""").df()


# --------------------------------------------------
# Store state filter
# --------------------------------------------------

states = ["All States"] + sorted(
    store_data["state"].unique().tolist()
)

selected_state = st.selectbox(
    "Filter stores by state",
    states
)

if selected_state == "All States":
    filtered_stores = store_data
else:
    filtered_stores = store_data[
        store_data["state"] == selected_state
    ]

top_stores = (
    filtered_stores
    .sort_values("revenue", ascending=False)
    .head(10)
)


# --------------------------------------------------
# Customer and store charts
# --------------------------------------------------

left_col, right_col = st.columns(2)


# --------------------------------------------------
# Average spend by loyalty status
# --------------------------------------------------

with left_col:

    st.markdown("#### Average Spend by Loyalty Status")

    loyalty_chart = px.bar(
        customer_summary,
        x="customer_type",
        y="avg_spend",
        labels={
            "customer_type": "Customer Type",
            "avg_spend": "Average Spend"
        }
    )

    loyalty_chart.update_layout(
        xaxis_title=None,
        yaxis_title="Average Spend ($)"
    )

    loyalty_chart.update_yaxes(
        tickprefix="$",
        tickformat=",.0f"
    )

    st.plotly_chart(
        loyalty_chart,
        width="stretch"
    )


# --------------------------------------------------
# Top stores
# --------------------------------------------------

with right_col:

    st.markdown("#### Top 10 Stores by Revenue")

    store_chart = px.bar(
        top_stores.sort_values("revenue"),
        x="revenue",
        y="store_name",
        orientation="h",
        hover_data=[
            "city",
            "state",
            "total_orders",
            "units_sold"
        ],
        labels={
            "revenue": "Revenue",
            "store_name": "Store"
        }
    )

    store_chart.update_layout(
        xaxis_title="Revenue ($)",
        yaxis_title=None
    )

    store_chart.update_xaxes(
        tickprefix="$",
        tickformat="~s"
    )

    st.plotly_chart(
        store_chart,
        width="stretch"
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Retail Analytics Platform | "
    "Python • DuckDB • dbt • Apache Iceberg • Parquet • Streamlit"
)