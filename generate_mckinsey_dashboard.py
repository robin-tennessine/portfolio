"""
McKinsey-Style Sales Analytics Dashboard
Professional formatting with clean, minimalist design
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Set seed
np.random.seed(42)
random.seed(42)

# McKinsey Color Palette
COLORS = {
    'navy': '#003366',
    'charcoal': '#444444',
    'teal': '#008080',
    'green': '#2d7a5e',
    'red': '#CC0000',
    'light_gray': '#CCCCCC',
    'text': '#333333',
    'bg_gray': '#F5F5F5'
}

# Constants
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime.now()
ANNUAL_TARGET = 160_000_000  # $160M

# Data configuration
PRODUCTS = [
    ('Laptop Pro', 'Electronics', 1200),
    ('Wireless Mouse', 'Electronics', 45),
    ('Monitor 27"', 'Electronics', 450),
    ('Office Chair', 'Furniture', 350),
    ('Standing Desk', 'Furniture', 800),
    ('Printer MX500', 'Office Supplies', 350),
    ('Paper Ream A4', 'Office Supplies', 8),
    ('Cloud Storage Pro', 'Software', 120),
    ('Security Suite', 'Software', 200)
]

REGIONS = ['North', 'South', 'East', 'West', 'Central']
SALES_PEOPLE = [
    'Alice Johnson', 'Bob Smith', 'Carol Martinez', 'David Chen',
    'Emma Wilson', 'Frank Brown', 'Grace Lee', 'Henry Taylor',
    'Ivy Anderson', 'Jack Robinson'
]

def format_currency(value):
    """Format currency in McKinsey style"""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"

def format_percent(value):
    """Format percentage as whole number"""
    return f"{value:.0f}%"

def growth_indicator(value):
    """Return growth indicator with arrow"""
    if value > 0:
        return f"↑ {abs(value):.0f}%"
    elif value < 0:
        return f"↓ {abs(value):.0f}%"
    else:
        return f"→ 0%"

def generate_sales_data():
    """Generate mock sales data"""
    print("Generating mock sales data...")

    transactions = []
    current_date = START_DATE

    while current_date <= END_DATE:
        is_weekend = current_date.weekday() >= 5
        month = current_date.month

        # Seasonal factors
        if month in [11, 12]:
            seasonal_factor = 1.5
        elif month in [5, 6]:
            seasonal_factor = 0.7
        else:
            seasonal_factor = 1.0

        # Year-over-year growth
        year_factor = 1.12 if current_date.year >= 2025 else 1.0

        base_transactions = 15 if not is_weekend else 8
        num_transactions = int(base_transactions * seasonal_factor * year_factor * random.uniform(0.8, 1.2))

        for _ in range(num_transactions):
            product, category, base_price = random.choice(PRODUCTS)

            quantity = random.randint(1, 10) if category != 'Office Supplies' else random.randint(5, 50)
            unit_price = base_price * random.uniform(0.95, 1.05)
            total_amount = unit_price * quantity * random.uniform(0.85, 0.95)

            transaction = {
                'Date': current_date,
                'Product': product,
                'Category': category,
                'Region': random.choice(REGIONS),
                'Sales Person': random.choice(SALES_PEOPLE),
                'Amount': round(total_amount, 2),
                'Quantity': quantity
            }
            transactions.append(transaction)

        current_date += timedelta(days=1)

    df = pd.DataFrame(transactions)
    print(f"✅ Generated {len(df):,} transactions")
    return df

def calculate_kpis(df):
    """Calculate McKinsey-style KPIs"""
    today = datetime.now()

    # YTD this year
    ytd_start = datetime(today.year, 1, 1)
    ytd_data = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)]
    ytd_revenue = ytd_data['Amount'].sum()

    # YTD last year
    ytd_start_ly = datetime(today.year - 1, 1, 1)
    ytd_end_ly = datetime(today.year - 1, today.month, today.day)
    ytd_data_ly = df[(df['Date'] >= ytd_start_ly) & (df['Date'] <= ytd_end_ly)]
    ytd_revenue_ly = ytd_data_ly['Amount'].sum()

    # Growth
    ytd_growth = ((ytd_revenue - ytd_revenue_ly) / ytd_revenue_ly * 100) if ytd_revenue_ly > 0 else 0

    # Days calculations
    days_elapsed = (today - ytd_start).days + 1
    days_in_year = 366 if today.year % 4 == 0 else 365
    days_remaining = days_in_year - days_elapsed

    # Forecast
    daily_avg = ytd_revenue / days_elapsed
    forecast = daily_avg * days_in_year
    forecast_growth = ((forecast - ytd_revenue_ly * (days_in_year/days_elapsed)) / (ytd_revenue_ly * (days_in_year/days_elapsed)) * 100) if ytd_revenue_ly > 0 else 0

    # Target achievement
    target_pace = (days_elapsed / days_in_year) * ANNUAL_TARGET
    target_achievement = (ytd_revenue / ANNUAL_TARGET) * 100
    on_pace = (ytd_revenue / target_pace) * 100

    return {
        'ytd_revenue': ytd_revenue,
        'ytd_revenue_ly': ytd_revenue_ly,
        'ytd_growth': ytd_growth,
        'forecast': forecast,
        'forecast_growth': forecast_growth,
        'target_achievement': target_achievement,
        'on_pace': on_pace,
        'days_remaining': days_remaining,
        'days_elapsed': days_elapsed
    }

def create_header_kpis(kpis):
    """Create executive summary KPI cards"""
    html = """
    <div class="kpi-section">
        <div class="kpi-card">
            <div class="kpi-title">YTD Revenue</div>
            <div class="kpi-value">{ytd_revenue}</div>
            <div class="kpi-comparison positive">↑ {growth} vs Last Year</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">YTD Sales Growth</div>
            <div class="kpi-value">{growth_pct}</div>
            <div class="kpi-comparison {growth_class}">{growth_ind} vs Target</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Forecast (Full Year)</div>
            <div class="kpi-value">{forecast}</div>
            <div class="kpi-comparison positive">↑ {forecast_growth} vs LY Projection</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Target Achievement</div>
            <div class="kpi-value">{target_pct}</div>
            <div class="kpi-comparison neutral">On Pace to Hit {pace}% Target</div>
        </div>
    </div>
    """.format(
        ytd_revenue=format_currency(kpis['ytd_revenue']),
        growth=format_percent(kpis['ytd_growth']),
        growth_pct=format_percent(kpis['ytd_growth']),
        growth_class='positive' if kpis['ytd_growth'] > 0 else 'negative',
        growth_ind=growth_indicator(kpis['ytd_growth'] - 10),  # vs 10% target
        forecast=format_currency(kpis['forecast']),
        forecast_growth=format_percent(kpis['forecast_growth']),
        target_pct=format_percent(kpis['target_achievement']),
        pace=format_percent(kpis['on_pace'])
    )
    return html

def create_monthly_vs_target(df):
    """Monthly sales vs target bar chart"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)

    monthly_data = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].copy()
    monthly_data['Month'] = monthly_data['Date'].dt.month
    monthly_sales = monthly_data.groupby('Month')['Amount'].sum()

    # Monthly targets (proportional)
    monthly_target = ANNUAL_TARGET / 12

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x_months = [months[m-1] for m in monthly_sales.index]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_months,
        y=monthly_sales.values / 1_000_000,
        name='Actual',
        marker_color=COLORS['navy'],
        width=0.4
    ))

    fig.add_trace(go.Bar(
        x=x_months,
        y=[monthly_target / 1_000_000] * len(x_months),
        name='Target',
        marker_color=COLORS['light_gray'],
        width=0.4
    ))

    fig.update_layout(
        title='Monthly Sales vs Target',
        xaxis_title='',
        yaxis_title='Revenue ($M)',
        barmode='group',
        height=350,
        font=dict(family='Arial, sans-serif', size=11, color=COLORS['text']),
        title_font=dict(family='Georgia, serif', size=14, color=COLORS['text']),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=50, r=20, t=60, b=50)
    )

    fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor=COLORS['light_gray'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#EEEEEE', showline=True, linewidth=1, linecolor=COLORS['light_gray'])

    return fig

def create_ytd_comparison(df):
    """YTD comparison line chart"""
    today = datetime.now()

    # This year
    ytd_start_this = datetime(today.year, 1, 1)
    df_this = df[(df['Date'] >= ytd_start_this) & (df['Date'] <= today)].copy()
    df_this = df_this.sort_values('Date')
    df_this['Cumulative'] = df_this['Amount'].cumsum()
    df_this['DayOfYear'] = df_this['Date'].dt.dayofyear

    # Last year
    ytd_start_last = datetime(today.year - 1, 1, 1)
    ytd_end_last = datetime(today.year - 1, today.month, today.day)
    df_last = df[(df['Date'] >= ytd_start_last) & (df['Date'] <= ytd_end_last)].copy()
    df_last = df_last.sort_values('Date')
    df_last['Cumulative'] = df_last['Amount'].cumsum()
    df_last['DayOfYear'] = df_last['Date'].dt.dayofyear

    # Projection
    current_cumulative = df_this['Cumulative'].iloc[-1]
    days_elapsed = df_this['DayOfYear'].iloc[-1]
    daily_avg = current_cumulative / days_elapsed
    days_in_year = 365
    projection_x = list(range(days_elapsed, days_in_year + 1))
    projection_y = [current_cumulative + daily_avg * (d - days_elapsed) for d in projection_x]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_last['DayOfYear'],
        y=df_last['Cumulative'] / 1_000_000,
        mode='lines',
        name='2024',
        line=dict(color=COLORS['charcoal'], width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df_this['DayOfYear'],
        y=df_this['Cumulative'] / 1_000_000,
        mode='lines',
        name='2025',
        line=dict(color=COLORS['navy'], width=3)
    ))

    fig.add_trace(go.Scatter(
        x=projection_x,
        y=[y / 1_000_000 for y in projection_y],
        mode='lines',
        name='2025 Projection',
        line=dict(color=COLORS['navy'], width=2, dash='dash')
    ))

    fig.update_layout(
        title='YTD Cumulative Revenue: 2024 vs 2025',
        xaxis_title='Day of Year',
        yaxis_title='Cumulative Revenue ($M)',
        height=350,
        font=dict(family='Arial, sans-serif', size=11, color=COLORS['text']),
        title_font=dict(family='Georgia, serif', size=14, color=COLORS['text']),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=50, r=20, t=60, b=50)
    )

    fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor=COLORS['light_gray'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#EEEEEE', showline=True, linewidth=1, linecolor=COLORS['light_gray'])

    return fig

def create_regional_table(df):
    """Create regional performance table HTML"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)
    ytd_start_ly = datetime(today.year - 1, 1, 1)
    ytd_end_ly = datetime(today.year - 1, today.month, today.day)

    # This year
    regional_ytd = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].groupby('Region')['Amount'].sum()

    # Last year
    regional_ytd_ly = df[(df['Date'] >= ytd_start_ly) & (df['Date'] <= ytd_end_ly)].groupby('Region')['Amount'].sum()

    # Regional targets (proportional)
    regional_target = ANNUAL_TARGET / len(REGIONS)

    rows = []
    for region in regional_ytd.sort_values(ascending=False).index[:5]:
        ytd = regional_ytd[region]
        ly = regional_ytd_ly.get(region, 0)
        growth = ((ytd - ly) / ly * 100) if ly > 0 else 0
        pct_target = (ytd / regional_target) * 100
        forecast = ytd * (365 / ((today - ytd_start).days + 1))

        growth_class = 'positive' if growth > 0 else 'negative'
        growth_str = f'<span class="{growth_class}">{growth_indicator(growth)}</span>'

        rows.append(f"""
        <tr>
            <td>{region}</td>
            <td class="number">{format_currency(ytd)}</td>
            <td class="number">{format_currency(regional_target)}</td>
            <td class="number">{format_percent(pct_target)}</td>
            <td class="number">{growth_str}</td>
            <td class="number">{format_currency(forecast)}</td>
        </tr>
        """)

    table_html = f"""
    <table class="data-table">
        <thead>
            <tr>
                <th>Region</th>
                <th class="number">YTD Sales</th>
                <th class="number">Target</th>
                <th class="number">% of Target</th>
                <th class="number">Growth vs LY</th>
                <th class="number">Forecast</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
    """
    return table_html

def create_sales_leaderboard(df):
    """Create sales team leaderboard HTML"""
    today = datetime.now()
    ytd_start = datetime(today.year, 1, 1)
    ytd_start_ly = datetime(today.year - 1, 1, 1)
    ytd_end_ly = datetime(today.year - 1, today.month, today.day)

    # This year
    team_ytd = df[(df['Date'] >= ytd_start) & (df['Date'] <= today)].groupby('Sales Person')['Amount'].sum()

    # Last year
    team_ytd_ly = df[(df['Date'] >= ytd_start_ly) & (df['Date'] <= ytd_end_ly)].groupby('Sales Person')['Amount'].sum()

    # Individual targets
    individual_target = ANNUAL_TARGET / len(SALES_PEOPLE)

    rows = []
    for rank, person in enumerate(team_ytd.sort_values(ascending=False).head(10).index, 1):
        ytd = team_ytd[person]
        ly = team_ytd_ly.get(person, 0)
        growth = ((ytd - ly) / ly * 100) if ly > 0 else 0
        pct_target = (ytd / individual_target) * 100
        forecast = ytd * (365 / ((today - ytd_start).days + 1))

        growth_class = 'positive' if growth > 0 else 'negative'
        growth_str = f'<span class="{growth_class}">{growth_indicator(growth)}</span>'

        bg_class = 'alt-row' if rank % 2 == 0 else ''

        rows.append(f"""
        <tr class="{bg_class}">
            <td class="number">{rank}</td>
            <td>{person}</td>
            <td class="number">{format_currency(ytd)}</td>
            <td class="number">{format_currency(individual_target)}</td>
            <td class="number">{format_percent(pct_target)}</td>
            <td class="number">{growth_str}</td>
            <td class="number">{format_currency(forecast)}</td>
        </tr>
        """)

    table_html = f"""
    <table class="data-table">
        <thead>
            <tr>
                <th class="number">Rank</th>
                <th>Sales Person</th>
                <th class="number">YTD Sales</th>
                <th class="number">Target</th>
                <th class="number">% of Target</th>
                <th class="number">Growth</th>
                <th class="number">Forecast</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
    """
    return table_html

def create_dashboard():
    """Generate complete McKinsey-style dashboard"""
    print("\n" + "="*70)
    print("MCKINSEY-STYLE SALES ANALYTICS DASHBOARD")
    print("="*70 + "\n")

    # Generate data
    df = generate_sales_data()

    # Calculate KPIs
    print("Calculating KPIs...")
    kpis = calculate_kpis(df)

    # Create visualizations
    print("Creating visualizations...")
    monthly_chart = create_monthly_vs_target(df)
    ytd_chart = create_ytd_comparison(df)

    # Create tables
    regional_table = create_regional_table(df)
    leaderboard_table = create_sales_leaderboard(df)

    # Create KPI cards
    kpi_html = create_header_kpis(kpis)

    today = datetime.now()

    # Generate HTML
    print("Generating dashboard HTML...")

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Performance Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, Helvetica, sans-serif;
            color: {COLORS['text']};
            background: white;
            padding: 40px;
            line-height: 1.6;
        }}

        h1, h2, h3 {{
            font-family: Georgia, serif;
            font-weight: normal;
        }}

        .header {{
            margin-bottom: 40px;
            border-bottom: 2px solid {COLORS['navy']};
            padding-bottom: 20px;
        }}

        .header h1 {{
            font-size: 28px;
            color: {COLORS['navy']};
            margin-bottom: 8px;
        }}

        .header .metadata {{
            font-size: 12px;
            color: {COLORS['charcoal']};
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section-title {{
            font-size: 16px;
            color: {COLORS['navy']};
            margin-bottom: 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi-section {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }}

        .kpi-card {{
            background: {COLORS['bg_gray']};
            padding: 25px;
            border-left: 4px solid {COLORS['navy']};
        }}

        .kpi-title {{
            font-size: 11px;
            color: {COLORS['charcoal']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            font-weight: bold;
        }}

        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            color: {COLORS['navy']};
            margin-bottom: 8px;
        }}

        .kpi-comparison {{
            font-size: 12px;
            font-weight: bold;
        }}

        .positive {{
            color: {COLORS['green']};
        }}

        .negative {{
            color: {COLORS['red']};
        }}

        .neutral {{
            color: {COLORS['charcoal']};
        }}

        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}

        .chart-container {{
            background: white;
            padding: 20px;
            border: 1px solid {COLORS['light_gray']};
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}

        .data-table thead {{
            background: {COLORS['navy']};
            color: white;
        }}

        .data-table th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .data-table th.number {{
            text-align: right;
        }}

        .data-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid {COLORS['light_gray']};
        }}

        .data-table td.number {{
            text-align: right;
            font-family: 'Courier New', monospace;
        }}

        .data-table .alt-row {{
            background: {COLORS['bg_gray']};
        }}

        .insight-box {{
            background: {COLORS['bg_gray']};
            border-left: 4px solid {COLORS['teal']};
            padding: 25px;
            font-size: 13px;
            line-height: 1.8;
        }}

        .insight-box h3 {{
            font-size: 14px;
            color: {COLORS['navy']};
            margin-bottom: 15px;
            font-weight: bold;
        }}

        .insight-box ul {{
            list-style: none;
            padding-left: 0;
        }}

        .insight-box li {{
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }}

        .insight-box li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {COLORS['teal']};
            font-weight: bold;
        }}

        @media print {{
            body {{
                padding: 20px;
            }}
            .section {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Sales Performance Dashboard</h1>
        <div class="metadata">
            Jan 1 - {today.strftime('%b %d, %Y')} | Last updated: {today.strftime('%B %d, %Y at %I:%M %p')}
        </div>
    </div>

    <div class="section">
        <div class="section-title">Executive Summary</div>
        {kpi_html}
    </div>

    <div class="section">
        <div class="section-title">Performance vs Target</div>
        <div class="two-column">
            <div class="chart-container">
                {monthly_chart.to_html(include_plotlyjs='cdn', div_id='monthly', config={'displayModeBar': False})}
            </div>
            <div>
                <div class="insight-box">
                    <h3>Annual Target Progress</h3>
                    <ul>
                        <li>Annual Target: {format_currency(ANNUAL_TARGET)}</li>
                        <li>Current YTD: {format_currency(kpis['ytd_revenue'])}</li>
                        <li>Remaining: {format_currency(ANNUAL_TARGET - kpis['ytd_revenue'])}</li>
                        <li>% of Target: {format_percent(kpis['target_achievement'])}</li>
                        <li>Days Left: {kpis['days_remaining']}</li>
                        <li>Daily Run Rate Needed: {format_currency((ANNUAL_TARGET - kpis['ytd_revenue']) / kpis['days_remaining'])}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">YTD Comparison (2024 vs 2025)</div>
        <div class="chart-container">
            {ytd_chart.to_html(include_plotlyjs=False, div_id='ytd', config={'displayModeBar': False})}
        </div>
    </div>

    <div class="section">
        <div class="section-title">Regional Performance</div>
        {regional_table}
    </div>

    <div class="section">
        <div class="section-title">Sales Team Leaderboard</div>
        {leaderboard_table}
    </div>

    <div class="section">
        <div class="section-title">Forecast & Insights</div>
        <div class="insight-box">
            <h3>Based on current YTD performance and historical trends:</h3>
            <ul>
                <li>Projected Full Year Revenue: {format_currency(kpis['forecast'])} ({growth_indicator(kpis['forecast_growth'])} vs 2024)</li>
                <li>Probability of Hitting {format_currency(ANNUAL_TARGET)} Target: {format_percent(min(95, kpis['on_pace']))}</li>
                <li>Gap to Close: {format_currency(max(0, ANNUAL_TARGET - kpis['forecast']))} ({format_currency((ANNUAL_TARGET - kpis['forecast']) / kpis['days_remaining'])} per day)</li>
                <li>Recommendation: Focus on high-growth regions and accelerate Q4 sales initiatives</li>
            </ul>
        </div>
    </div>

    <div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid {COLORS['light_gray']}; font-size: 11px; color: {COLORS['charcoal']};">
        Sales Analytics Dashboard | Robin Phonpakdee - Data Analyst | {today.year}
    </div>
</body>
</html>
"""

    # Save file
    output_file = 'sales_dashboard_mckinsey.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Dashboard saved to: {output_file}")
    print(f"📁 File size: {len(html_content) / 1024:.1f} KB")

    print("\n" + "="*70)
    print("DASHBOARD SUMMARY")
    print("="*70)
    print(f"YTD Revenue: {format_currency(kpis['ytd_revenue'])}")
    print(f"YTD Growth: {format_percent(kpis['ytd_growth'])}")
    print(f"Forecast: {format_currency(kpis['forecast'])}")
    print(f"Target Achievement: {format_percent(kpis['target_achievement'])}")
    print("\n" + "="*70)
    print("✅ MCKINSEY-STYLE DASHBOARD COMPLETE!")
    print("="*70)
    print(f"\n🌐 To view: open {output_file}\n")

if __name__ == "__main__":
    create_dashboard()
