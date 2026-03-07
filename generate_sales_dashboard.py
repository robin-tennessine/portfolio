"""
Professional Sales Dashboard with Forecasting & YTD Analysis
Generates interactive HTML dashboard with mock data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime.now()
ANNUAL_TARGET = 5000000  # $5M target

# Master data
PRODUCTS = [
    ('Laptop Pro', 'Electronics', 1200),
    ('Wireless Mouse', 'Electronics', 45),
    ('USB-C Hub', 'Electronics', 89),
    ('Monitor 27"', 'Electronics', 450),
    ('Mechanical Keyboard', 'Electronics', 120),
    ('Office Chair', 'Furniture', 350),
    ('Standing Desk', 'Furniture', 800),
    ('Conference Table', 'Furniture', 1200),
    ('Filing Cabinet', 'Furniture', 250),
    ('Printer MX500', 'Office Supplies', 350),
    ('Paper Ream A4', 'Office Supplies', 8),
    ('Toner Cartridge', 'Office Supplies', 75),
    ('Notebook Set', 'Office Supplies', 15),
    ('Pen Pack 50ct', 'Office Supplies', 25),
    ('Cloud Storage Pro', 'Software', 120),
    ('Security Suite', 'Software', 200),
    ('Project Manager', 'Software', 150),
    ('Analytics Platform', 'Software', 500)
]

REGIONS = ['North', 'South', 'East', 'West', 'Central']
SALES_PEOPLE = [
    'Alice Johnson', 'Bob Smith', 'Carol Martinez', 'David Chen',
    'Emma Wilson', 'Frank Brown', 'Grace Lee', 'Henry Taylor',
    'Ivy Anderson', 'Jack Robinson'
]
CUSTOMER_TYPES = ['Enterprise', 'SMB', 'Individual']

def generate_sales_data():
    """Generate realistic sales data with seasonal patterns"""
    print("Generating mock sales data...")

    transactions = []
    current_date = START_DATE

    while current_date <= END_DATE:
        # Determine number of transactions for this day
        # More transactions on weekdays, fewer on weekends
        is_weekend = current_date.weekday() >= 5
        month = current_date.month

        # Seasonal adjustment (Q4 peaks, Q2 dips)
        if month in [11, 12]:  # Nov, Dec
            seasonal_factor = 1.5
        elif month in [5, 6]:  # May, Jun
            seasonal_factor = 0.7
        else:
            seasonal_factor = 1.0

        # Year-over-year growth (2025 is ~15% higher than 2024)
        year_factor = 1.15 if current_date.year >= 2025 else 1.0

        base_transactions = 3 if is_weekend else 8
        num_transactions = int(base_transactions * seasonal_factor * year_factor * random.uniform(0.7, 1.3))

        for _ in range(num_transactions):
            # Select product
            product, category, base_price = random.choice(PRODUCTS)

            # Determine quantity
            if category == 'Office Supplies':
                quantity = random.randint(5, 50)
            elif category == 'Electronics':
                quantity = random.randint(1, 5)
            else:
                quantity = random.randint(1, 10)

            # Calculate amount
            price_variation = random.uniform(0.95, 1.05)
            unit_price = base_price * price_variation

            # Apply discount
            customer_type = random.choice(CUSTOMER_TYPES)
            if customer_type == 'Enterprise':
                discount = random.uniform(0.10, 0.20)
            elif customer_type == 'SMB':
                discount = random.uniform(0.05, 0.15)
            else:
                discount = random.uniform(0, 0.10)

            subtotal = unit_price * quantity
            discount_amount = subtotal * discount
            total_amount = subtotal - discount_amount

            transaction = {
                'Date': current_date,
                'Product': product,
                'Category': category,
                'Region': random.choice(REGIONS),
                'Sales Person': random.choice(SALES_PEOPLE),
                'Amount': round(total_amount, 2),
                'Quantity': quantity,
                'Discount': round(discount * 100, 1),
                'Customer Type': customer_type,
                'Unit Price': round(unit_price, 2)
            }

            transactions.append(transaction)

        current_date += timedelta(days=1)

    df = pd.DataFrame(transactions)
    print(f"✅ Generated {len(df):,} transactions from {START_DATE.date()} to {END_DATE.date()}")
    return df

def calculate_kpis(df):
    """Calculate all KPIs for dashboard"""
    today = datetime.now()

    # Current month
    current_month_start = datetime(today.year, today.month, 1)
    current_month_data = df[df['Date'] >= current_month_start]
    current_month_sales = current_month_data['Amount'].sum()

    # Last month
    if today.month == 1:
        last_month = 12
        last_month_year = today.year - 1
    else:
        last_month = today.month - 1
        last_month_year = today.year

    last_month_start = datetime(last_month_year, last_month, 1)
    if today.month == 1:
        last_month_end = datetime(today.year, 1, 1) - timedelta(days=1)
    else:
        last_month_end = current_month_start - timedelta(days=1)

    last_month_data = df[(df['Date'] >= last_month_start) & (df['Date'] <= last_month_end)]
    last_month_sales = last_month_data['Amount'].sum()

    # MoM growth
    mom_growth = ((current_month_sales - last_month_sales) / last_month_sales * 100) if last_month_sales > 0 else 0

    # YTD this year
    ytd_start = datetime(today.year, 1, 1)
    ytd_data_this_year = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)]
    ytd_sales_this_year = ytd_data_this_year['Amount'].sum()

    # YTD last year (same period)
    ytd_start_last_year = datetime(today.year - 1, 1, 1)
    ytd_end_last_year = datetime(today.year - 1, today.month, today.day)
    ytd_data_last_year = df[(df['Date'] >= ytd_start_last_year) & (df['Date'] <= ytd_end_last_year)]
    ytd_sales_last_year = ytd_data_last_year['Amount'].sum()

    # YTD growth
    ytd_growth = ((ytd_sales_this_year - ytd_sales_last_year) / ytd_sales_last_year * 100) if ytd_sales_last_year > 0 else 0

    # Days calculations
    days_elapsed = (today - ytd_start).days + 1
    days_in_year = 366 if today.year % 4 == 0 else 365
    days_remaining = days_in_year - days_elapsed

    # Run rate and projections
    daily_average = ytd_sales_this_year / days_elapsed
    run_rate = daily_average * days_in_year
    projected_annual = run_rate

    # Target achievement
    target_achievement = (ytd_sales_this_year / ANNUAL_TARGET) * 100
    target_pace = (days_elapsed / days_in_year) * 100

    # Determine trend
    if target_achievement > target_pace + 5:
        trend = "Accelerating ↗"
    elif target_achievement < target_pace - 5:
        trend = "Declining ↘"
    else:
        trend = "On Pace →"

    return {
        'current_month_sales': current_month_sales,
        'last_month_sales': last_month_sales,
        'mom_growth': mom_growth,
        'ytd_sales_this_year': ytd_sales_this_year,
        'ytd_sales_last_year': ytd_sales_last_year,
        'ytd_growth': ytd_growth,
        'days_elapsed': days_elapsed,
        'days_remaining': days_remaining,
        'run_rate': run_rate,
        'projected_annual': projected_annual,
        'target_achievement': target_achievement,
        'target_pace': target_pace,
        'trend': trend,
        'annual_target': ANNUAL_TARGET
    }

def create_kpi_cards(kpis):
    """Create KPI summary cards"""
    fig = make_subplots(
        rows=2, cols=4,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=(
            "Current Month Sales", "YTD Sales (This Year)", "YTD Growth %", "Target Achievement",
            "Projected Annual", "Days Remaining", "Run Rate", "Trend Status"
        )
    )

    # Current Month Sales
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis['current_month_sales'],
        delta={'reference': kpis['last_month_sales'], 'relative': True, 'valueformat': '.1%'},
        number={'prefix': "$", 'valueformat': ',.0f'},
    ), row=1, col=1)

    # YTD Sales This Year
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['ytd_sales_this_year'],
        number={'prefix': "$", 'valueformat': ',.0f'},
    ), row=1, col=2)

    # YTD Growth %
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis['ytd_growth'],
        delta={'reference': 0, 'relative': False},
        number={'suffix': "%", 'valueformat': '.1f'},
    ), row=1, col=3)

    # Target Achievement
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=kpis['target_achievement'],
        delta={'reference': kpis['target_pace'], 'relative': False},
        number={'suffix': "%", 'valueformat': '.1f'},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': 'green' if kpis['target_achievement'] >= kpis['target_pace'] else 'orange'},
               'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': kpis['target_pace']}}
    ), row=1, col=4)

    # Projected Annual
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis['projected_annual'],
        delta={'reference': kpis['annual_target'], 'relative': False, 'valueformat': '$,.0f'},
        number={'prefix': "$", 'valueformat': ',.0f'},
    ), row=2, col=1)

    # Days Remaining
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['days_remaining'],
        number={'suffix': " days"},
    ), row=2, col=2)

    # Run Rate
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['run_rate'],
        number={'prefix': "$", 'valueformat': ',.0f'},
    ), row=2, col=3)

    # Trend Status
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['target_achievement'] - kpis['target_pace'],
        number={'suffix': "%", 'valueformat': '+.1f'},
        title={'text': kpis['trend']},
    ), row=2, col=4)

    fig.update_layout(
        height=500,
        paper_bgcolor='#f8f9fa',
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def create_ytd_comparison(df):
    """YTD comparison chart"""
    today = datetime.now()

    # This year YTD
    ytd_start_this = datetime(today.year, 1, 1)
    df_this_year = df[(df['Date'] >= ytd_start_this) & (df['Date'] <= today)].copy()
    df_this_year['Month'] = df_this_year['Date'].dt.month
    this_year_monthly = df_this_year.groupby('Month')['Amount'].sum()

    # Last year YTD
    ytd_start_last = datetime(today.year - 1, 1, 1)
    ytd_end_last = datetime(today.year - 1, today.month, today.day)
    df_last_year = df[(df['Date'] >= ytd_start_last) & (df['Date'] <= ytd_end_last)].copy()
    df_last_year['Month'] = df_last_year['Date'].dt.month
    last_year_monthly = df_last_year.groupby('Month')['Amount'].sum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(range(1, len(last_year_monthly) + 1)),
        y=last_year_monthly.values,
        name=f'{today.year - 1} YTD',
        marker_color='lightblue'
    ))

    fig.add_trace(go.Bar(
        x=list(range(1, len(this_year_monthly) + 1)),
        y=this_year_monthly.values,
        name=f'{today.year} YTD',
        marker_color='darkblue'
    ))

    fig.update_layout(
        title='YTD Monthly Comparison: This Year vs Last Year',
        xaxis_title='Month',
        yaxis_title='Sales ($)',
        barmode='group',
        height=400,
        template='plotly_white'
    )

    return fig

def create_cumulative_ytd(df):
    """Cumulative YTD line chart"""
    today = datetime.now()

    # This year
    ytd_start_this = datetime(today.year, 1, 1)
    df_this = df[(df['Date'] >= ytd_start_this) & (df['Date'] <= today)].copy()
    df_this = df_this.sort_values('Date')
    df_this['Cumulative'] = df_this['Amount'].cumsum()

    # Last year (same period)
    ytd_start_last = datetime(today.year - 1, 1, 1)
    ytd_end_last = datetime(today.year - 1, today.month, today.day)
    df_last = df[(df['Date'] >= ytd_start_last) & (df['Date'] <= ytd_end_last)].copy()
    df_last = df_last.sort_values('Date')
    df_last['Cumulative'] = df_last['Amount'].cumsum()

    # Align dates for comparison
    df_this['DayOfYear'] = df_this['Date'].dt.dayofyear
    df_last['DayOfYear'] = df_last['Date'].dt.dayofyear

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_last['DayOfYear'],
        y=df_last['Cumulative'],
        mode='lines',
        name=f'{today.year - 1}',
        line=dict(color='lightblue', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=df_this['DayOfYear'],
        y=df_this['Cumulative'],
        mode='lines',
        name=f'{today.year}',
        line=dict(color='darkblue', width=3)
    ))

    fig.update_layout(
        title='Cumulative Revenue YTD: 2024 vs 2025',
        xaxis_title='Day of Year',
        yaxis_title='Cumulative Sales ($)',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )

    return fig

def create_regional_performance(df):
    """Regional performance analysis"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)

    regional_ytd = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].groupby('Region')['Amount'].sum().sort_values(ascending=True)

    fig = go.Figure(go.Bar(
        x=regional_ytd.values,
        y=regional_ytd.index,
        orientation='h',
        marker_color='teal',
        text=regional_ytd.values,
        texttemplate='$%{text:,.0f}',
        textposition='outside'
    ))

    fig.update_layout(
        title='YTD Revenue by Region',
        xaxis_title='Sales ($)',
        yaxis_title='Region',
        height=400,
        template='plotly_white'
    )

    return fig

def create_category_distribution(df):
    """Category distribution pie chart"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)

    category_sales = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].groupby('Category')['Amount'].sum()

    fig = go.Figure(data=[go.Pie(
        labels=category_sales.index,
        values=category_sales.values,
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3
    )])

    fig.update_layout(
        title='YTD Sales by Category',
        height=400,
        template='plotly_white'
    )

    return fig

def create_sales_team_leaderboard(df):
    """Sales team leaderboard"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)

    team_ytd = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].groupby('Sales Person')['Amount'].sum().sort_values(ascending=True).tail(10)

    fig = go.Figure(go.Bar(
        x=team_ytd.values,
        y=team_ytd.index,
        orientation='h',
        marker_color='green',
        text=team_ytd.values,
        texttemplate='$%{text:,.0f}',
        textposition='outside'
    ))

    fig.update_layout(
        title='Top 10 Sales People (YTD)',
        xaxis_title='Sales ($)',
        yaxis_title='Sales Person',
        height=500,
        template='plotly_white'
    )

    return fig

def create_dashboard():
    """Main dashboard generation"""
    print("\n" + "="*70)
    print("SALES DASHBOARD WITH FORECASTING & YTD ANALYSIS")
    print("="*70 + "\n")

    # Generate data
    df = generate_sales_data()

    # Calculate KPIs
    print("\nCalculating KPIs and forecasts...")
    kpis = calculate_kpis(df)

    # Create visualizations
    print("Creating visualizations...")
    kpi_fig = create_kpi_cards(kpis)
    ytd_comparison_fig = create_ytd_comparison(df)
    cumulative_fig = create_cumulative_ytd(df)
    regional_fig = create_regional_performance(df)
    category_fig = create_category_distribution(df)
    leaderboard_fig = create_sales_team_leaderboard(df)

    # Generate HTML
    print("\nGenerating dashboard HTML...")

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Dashboard - Forecasting & YTD Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f2f5;
            color: #333;
            padding: 20px;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .summary-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .summary-box h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .kpi-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .kpi-label {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
        }}

        .kpi-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
        }}

        .positive {{
            color: #10b981;
        }}

        .negative {{
            color: #ef4444;
        }}

        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .forecast-box {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .forecast-box h2 {{
            font-size: 1.8rem;
            margin-bottom: 15px;
        }}

        .forecast-item {{
            margin: 10px 0;
            font-size: 1.1rem;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Sales Dashboard</h1>
        <p>Forecasting & Year-to-Date Analysis | Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>

    <div class="summary-box">
        <h2>Executive Summary</h2>
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Current Month Sales</div>
                <div class="kpi-value">${kpis['current_month_sales']:,.0f}</div>
                <div class="{'positive' if kpis['mom_growth'] > 0 else 'negative'}">{kpis['mom_growth']:+.1f}% MoM</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">YTD Sales (This Year)</div>
                <div class="kpi-value">${kpis['ytd_sales_this_year']:,.0f}</div>
                <div class="{'positive' if kpis['ytd_growth'] > 0 else 'negative'}">{kpis['ytd_growth']:+.1f}% YoY</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Projected Annual</div>
                <div class="kpi-value">${kpis['projected_annual']:,.0f}</div>
                <div>Based on run rate</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Target Achievement</div>
                <div class="kpi-value">{kpis['target_achievement']:.1f}%</div>
                <div>of ${kpis['annual_target']:,.0f} target</div>
            </div>
        </div>
    </div>

    <div class="forecast-box">
        <h2>🔮 Forecast Analysis</h2>
        <div class="forecast-item">
            <strong>Trend:</strong> {kpis['trend']}
        </div>
        <div class="forecast-item">
            <strong>Days Remaining in Year:</strong> {kpis['days_remaining']} days
        </div>
        <div class="forecast-item">
            <strong>Projected Full Year Revenue:</strong> ${kpis['projected_annual']:,.0f}
            {' (Above Target ✓)' if kpis['projected_annual'] >= kpis['annual_target'] else f" (Gap: ${kpis['annual_target'] - kpis['projected_annual']:,.0f})"}
        </div>
        <div class="forecast-item">
            <strong>Probability of Hitting Target:</strong> {'High (>90%)' if kpis['target_achievement'] > kpis['target_pace'] else 'Moderate (50-90%)' if kpis['target_achievement'] > kpis['target_pace'] - 10 else 'Low (<50%)'}
        </div>
    </div>

    <div class="chart-container">
        {kpi_fig.to_html(include_plotlyjs='cdn', div_id='kpi')}
    </div>

    <div class="chart-container">
        {ytd_comparison_fig.to_html(include_plotlyjs=False, div_id='ytd_comparison')}
    </div>

    <div class="chart-container">
        {cumulative_fig.to_html(include_plotlyjs=False, div_id='cumulative')}
    </div>

    <div class="chart-container">
        {regional_fig.to_html(include_plotlyjs=False, div_id='regional')}
    </div>

    <div class="chart-container">
        {category_fig.to_html(include_plotlyjs=False, div_id='category')}
    </div>

    <div class="chart-container">
        {leaderboard_fig.to_html(include_plotlyjs=False, div_id='leaderboard')}
    </div>

    <div class="footer">
        <p>© 2025 Sales Dashboard | Robin Phonpakdee - Data Analyst</p>
        <p>Mock data generated for demonstration purposes</p>
    </div>
</body>
</html>
"""

    # Save to file
    output_file = 'sales_dashboard.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Dashboard saved to: {output_file}")
    print(f"\n📁 File size: {len(html_content) / 1024:.1f} KB")

    # Print summary
    print("\n" + "="*70)
    print("DASHBOARD SUMMARY")
    print("="*70)
    print(f"Total Transactions: {len(df):,}")
    print(f"Date Range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"YTD Sales (This Year): ${kpis['ytd_sales_this_year']:,.2f}")
    print(f"YTD Sales (Last Year): ${kpis['ytd_sales_last_year']:,.2f}")
    print(f"YTD Growth: {kpis['ytd_growth']:+.1f}%")
    print(f"Projected Annual: ${kpis['projected_annual']:,.2f}")
    print(f"Target Achievement: {kpis['target_achievement']:.1f}%")
    print(f"Trend: {kpis['trend']}")
    print("\n" + "="*70)
    print("✅ DASHBOARD GENERATION COMPLETE!")
    print("="*70)
    print(f"\n🌐 To view: open {output_file}\n")

if __name__ == "__main__":
    create_dashboard()
