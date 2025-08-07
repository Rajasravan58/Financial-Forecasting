import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from config import (
    HISTORICAL_REVENUE,
    HISTORICAL_COSTS,
    HISTORICAL_OPERATING_EXPENSES,
    FORECAST_PERIOD,
    BUDGET
)
from forecasting import (
    forecast_revenue,
    forecast_costs,
    forecast_operating_expenses,
    forecast_net_income
)
from budget import compare_actual_vs_forecast
from metrics import calculate_metrics
from analysis import calculate_growth_rate, calculate_profit_margin

# Page configuration
st.set_page_config(
    page_title="Financial Forecast Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        color: #2c3e50;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    .insight-box {
        background-color:black;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown('<h1 class="main-header">📊 Financial Forecast Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.header("Dashboard Controls")
show_detailed_metrics = st.sidebar.checkbox("Show Detailed Accuracy Metrics", value=True)
chart_height = st.sidebar.slider("Chart Height", 300, 600, 400)
time_range = st.sidebar.selectbox("Time Range View", ["All Data", "Last 6 Months", "Last Year"])

# Data preparation
@st.cache_data
def prepare_data():
    actual = {
        'Revenue': HISTORICAL_REVENUE[-FORECAST_PERIOD:],
        'Cost_of_Goods_Sold': HISTORICAL_COSTS[-FORECAST_PERIOD:],
        'Operating_Expenses': HISTORICAL_OPERATING_EXPENSES[-FORECAST_PERIOD:]
    }
    actual['Net_Income'] = [r - c - o for r, c, o in zip(
        actual['Revenue'], actual['Cost_of_Goods_Sold'], actual['Operating_Expenses']
    )]
    
    forecast = {
        'Revenue': forecast_revenue(),
        'Cost_of_Goods_Sold': forecast_costs(),
        'Operating_Expenses': forecast_operating_expenses(),
    }
    forecast['Net_Income'] = forecast_net_income(
        forecast['Revenue'], forecast['Cost_of_Goods_Sold'], forecast['Operating_Expenses']
    )
    
    return actual, forecast

actual, forecast = prepare_data()
comparison = compare_actual_vs_forecast(actual, forecast)

# === EXECUTIVE SUMMARY ===
st.markdown('<div class="section-header">🎯 Executive Summary</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Key metrics calculations
total_actual_revenue = sum(actual['Revenue'])
total_forecast_revenue = sum(forecast['Revenue'])
revenue_variance = ((total_forecast_revenue - total_actual_revenue) / total_actual_revenue) * 100

actual_profit_margin = ((sum(actual['Net_Income']) / sum(actual['Revenue'])) * 100) if sum(actual['Revenue']) > 0 else 0
forecast_profit_margin = ((sum(forecast['Net_Income']) / sum(forecast['Revenue'])) * 100) if sum(forecast['Revenue']) > 0 else 0

with col1:
    st.metric(
        "Total Revenue (Forecast)", 
        f"${total_forecast_revenue:,.0f}",
        delta=f"{revenue_variance:+.1f}% vs Actual"
    )

with col2:
    st.metric(
        "Profit Margin (Forecast)", 
        f"{forecast_profit_margin:.1f}%",
        delta=f"{forecast_profit_margin - actual_profit_margin:+.1f}pp"
    )

with col3:
    revenue_growth = calculate_growth_rate(HISTORICAL_REVENUE)
    avg_growth = np.mean(revenue_growth) if len(revenue_growth) > 0 else 0
    st.metric(
        "Avg Revenue Growth", 
        f"{avg_growth:.1f}%"
    )

with col4:
    forecast_accuracy = 100 - (np.mean([abs((f-a)/a) for a, f in zip(actual['Revenue'], forecast['Revenue']) if a != 0]) * 100)
    st.metric(
        "Forecast Accuracy", 
        f"{forecast_accuracy:.1f}%"
    )

# Business insights
if revenue_variance > 10:
    st.markdown(f'<div class="insight-box">💡 <strong>Key Insight:</strong> Forecasted revenue shows strong growth of {revenue_variance:.1f}%, indicating positive business momentum.</div>', unsafe_allow_html=True)
elif revenue_variance < -5:
    st.markdown(f'<div class="warning-box">⚠️ <strong>Attention:</strong> Forecasted revenue is {abs(revenue_variance):.1f}% below actual, suggesting potential challenges ahead.</div>', unsafe_allow_html=True)

# === FINANCIAL OVERVIEW ===
st.markdown('<div class="section-header">💰 Financial Performance Overview</div>', unsafe_allow_html=True)

# Create comprehensive comparison chart
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Revenue', 'Cost of Goods Sold', 'Operating Expenses', 'Net Income'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

metrics = ['Revenue', 'Cost_of_Goods_Sold', 'Operating_Expenses', 'Net_Income']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
positions = [(1,1), (1,2), (2,1), (2,2)]

for i, (metric, color, pos) in enumerate(zip(metrics, colors, positions)):
    # Actual data
    fig.add_trace(
        go.Scatter(
            x=list(range(len(actual[metric]))),
            y=actual[metric],
            name=f'Actual {metric}',
            line=dict(color=color, width=3),
            marker=dict(size=8),
            showlegend=i==0
        ),
        row=pos[0], col=pos[1]
    )
    
    # Forecast data
    fig.add_trace(
        go.Scatter(
            x=list(range(len(forecast[metric]))),
            y=forecast[metric],
            name=f'Forecast {metric}',
            line=dict(color=color, width=2, dash='dash'),
            marker=dict(size=6),
            showlegend=i==0
        ),
        row=pos[0], col=pos[1]
    )

fig.update_layout(
    height=chart_height,
    title_text="Actual vs Forecast Comparison",
    title_x=0.5,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# === DETAILED ANALYTICS ===
st.markdown('<div class="section-header">📈 Detailed Financial Analytics</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Trend Analysis", "🎯 Accuracy Metrics", "💹 Variance Analysis", "📋 Data Summary"])

with tab1:
    # Individual metric charts with trends
    selected_metric = st.selectbox("Select Metric for Detailed Analysis", 
                                 ["Revenue", "Cost_of_Goods_Sold", "Operating_Expenses", "Net_Income"])
    
    # Create detailed trend chart
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=list(range(len(actual[selected_metric]))),
        y=actual[selected_metric],
        name='Actual',
        line=dict(color='#1f77b4', width=4),
        marker=dict(size=10)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=list(range(len(forecast[selected_metric]))),
        y=forecast[selected_metric],
        name='Forecast',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    # Add trend line for actual data
    z = np.polyfit(range(len(actual[selected_metric])), actual[selected_metric], 1)
    p = np.poly1d(z)
    fig_trend.add_trace(go.Scatter(
        x=list(range(len(actual[selected_metric]))),
        y=p(range(len(actual[selected_metric]))),
        name='Trend Line',
        line=dict(color='rgba(255,0,0,0.5)', width=2, dash='dot')
    ))
    
    fig_trend.update_layout(
        title=f"{selected_metric} - Detailed Trend Analysis",
        xaxis_title="Time Period",
        yaxis_title="Amount ($)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Growth analysis
    if len(actual[selected_metric]) > 1:
        growth_rates = [(actual[selected_metric][i] - actual[selected_metric][i-1]) / actual[selected_metric][i-1] * 100 
                       for i in range(1, len(actual[selected_metric])) if actual[selected_metric][i-1] != 0]
        avg_growth = np.mean(growth_rates) if growth_rates else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Growth Rate", f"{avg_growth:.2f}%")
        with col2:
            volatility = np.std(growth_rates) if growth_rates else 0
            st.metric("Growth Volatility", f"{volatility:.2f}%")

with tab2:
    if show_detailed_metrics:
        st.subheader("Forecast Accuracy Metrics")
        
        metrics_data = []
        for key in ['Revenue', 'Cost_of_Goods_Sold', 'Operating_Expenses', 'Net_Income']:
            mse, rmse, mae = calculate_metrics(actual[key], forecast[key])
            mape = np.mean([abs((a-f)/a) for a, f in zip(actual[key], forecast[key]) if a != 0]) * 100
            
            metrics_data.append({
                'Metric': key.replace('_', ' '),
                'MSE': f"{mse:.2f}",
                'RMSE': f"{rmse:.2f}",
                'MAE': f"{mae:.2f}",
                'MAPE': f"{mape:.2f}%"
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
        
        # Accuracy visualization
        fig_accuracy = go.Figure(data=[
            go.Bar(name='MAPE (%)', x=[m['Metric'] for m in metrics_data], 
                   y=[float(m['MAPE'].replace('%', '')) for m in metrics_data])
        ])
        
        fig_accuracy.update_layout(
            title="Mean Absolute Percentage Error by Metric",
            xaxis_title="Financial Metric",
            yaxis_title="MAPE (%)",
            height=300
        )
        
        st.plotly_chart(fig_accuracy, use_container_width=True)

with tab3:
    st.subheader("Variance Analysis")
    
    variance_data = []
    for key in ['Revenue', 'Cost_of_Goods_Sold', 'Operating_Expenses', 'Net_Income']:
        total_actual = sum(actual[key])
        total_forecast = sum(forecast[key])
        variance = total_forecast - total_actual
        variance_pct = (variance / total_actual * 100) if total_actual != 0 else 0
        
        variance_data.append({
            'Metric': key.replace('_', ' '),
            'Actual Total': f"${total_actual:,.0f}",
            'Forecast Total': f"${total_forecast:,.0f}",
            'Variance': f"${variance:,.0f}",
            'Variance %': f"{variance_pct:+.1f}%"
        })
    
    variance_df = pd.DataFrame(variance_data)
    st.dataframe(variance_df, use_container_width=True)
    
    # Variance chart
    fig_variance = go.Figure(data=[
        go.Bar(name='Variance %', 
               x=[v['Metric'] for v in variance_data],
               y=[float(v['Variance %'].replace('%', '').replace('+', '')) for v in variance_data],
               marker_color=['green' if float(v['Variance %'].replace('%', '').replace('+', '')) > 0 else 'red' 
                           for v in variance_data])
    ])
    
    fig_variance.update_layout(
        title="Forecast Variance by Metric",
        xaxis_title="Financial Metric",
        yaxis_title="Variance (%)",
        height=300
    )
    
    st.plotly_chart(fig_variance, use_container_width=True)

with tab4:
    st.subheader("Complete Data Summary")
    
    # Create comprehensive data table
    periods = list(range(1, len(actual['Revenue']) + 1))
    summary_data = pd.DataFrame({
        'Period': periods,
        'Actual Revenue': [f"${x:,.0f}" for x in actual['Revenue']],
        'Forecast Revenue': [f"${x:,.0f}" for x in forecast['Revenue']],
        'Actual COGS': [f"${x:,.0f}" for x in actual['Cost_of_Goods_Sold']],
        'Forecast COGS': [f"${x:,.0f}" for x in forecast['Cost_of_Goods_Sold']],
        'Actual OPEX': [f"${x:,.0f}" for x in actual['Operating_Expenses']],
        'Forecast OPEX': [f"${x:,.0f}" for x in forecast['Operating_Expenses']],
        'Actual Net Income': [f"${x:,.0f}" for x in actual['Net_Income']],
        'Forecast Net Income': [f"${x:,.0f}" for x in forecast['Net_Income']],
    })
    
    st.dataframe(summary_data, use_container_width=True)
    
    # Download option
    csv = summary_data.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="financial_forecast_data.csv",
        mime="text/csv"
    )

# === RECOMMENDATIONS ===
st.markdown('<div class="section-header">🎯 Key Recommendations</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💡 Opportunities")
    if forecast_profit_margin > actual_profit_margin:
        st.write("✅ Profit margins expected to improve")
    if revenue_variance > 5:
        st.write("✅ Strong revenue growth projected")
    st.write("✅ Monitor high-variance metrics closely")

with col2:
    st.markdown("#### ⚠️ Areas of Focus")
    if forecast_accuracy < 85:
        st.write("🔍 Improve forecasting accuracy")
    if forecast_profit_margin < 10:
        st.write("🔍 Focus on cost optimization")
    st.write("🔍 Regular forecast model validation needed")

# Footer
st.markdown("---")
st.markdown("*Dashboard generated with real-time financial data analysis*")
