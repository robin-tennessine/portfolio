# Customer Segment Flow Analysis - Sankey Visualization

## Overview

This project visualizes customer segment transitions year-over-year using interactive Sankey diagrams. It replicates Power BI DAX logic in Python to create yearly customer snapshots with RFM (Recency, Frequency, Monetary) segmentation and tracks how customers move between segments over time.

## Business Context

In retail analytics, understanding customer lifecycle and segment transitions is crucial for:
- **Targeted Marketing**: Identify at-risk customers before they churn
- **Resource Allocation**: Focus retention efforts on high-value segments
- **Campaign Effectiveness**: Measure success of win-back and loyalty programs
- **Revenue Forecasting**: Predict future revenue based on segment dynamics

This analysis was previously done in Power BI using DAX measures and has been translated to Python for scalability and automation.

## Key Features

### 1. Yearly Snapshot Engine (`yearly_snapshot_engine.py`)
Replicates Power BI DAX `YearlySnapshot` calculation:
- **Transaction Aggregation**: Total spend, quantity, transaction count per member per year
- **Cumulative Metrics**: Running totals of transactions and activity years
- **Point Categorization**: Loyalty point ranges for customer value
- **Recency Segmentation**: Classify customers as Active, At Risk, Inactive, or Dormant
- **Time Intelligence**: Calculate year-end dates and last activity periods

### 2. Interactive Sankey Diagrams (`customer_segment_sankey.ipynb`)
- **Year-to-Year Transitions**: Individual Sankey diagrams for each consecutive year pair
- **Multi-Year Overview**: Combined view showing all transitions in one diagram
- **Interactive Visualization**: Hover details, zoom, and export capabilities
- **Customizable Filters**: Option to focus on specific segments

### 3. Segment Analysis
- **Retention Rates**: Calculate segment-specific retention percentages
- **Churn Analysis**: Track transitions from Active to Inactive states
- **Reactivation Tracking**: Monitor win-back success rates
- **Migration Patterns**: Identify most common segment transitions

## Data Structure

### Member Master Table
| Column | Type | Description |
|--------|------|-------------|
| Member_ID | String | Unique member identifier |
| FIRST_NAME | String | Member first name |
| LAST_NAME | String | Member last name |
| GENDER | String | Gender (M/F) |
| BIRTHDATE | Date | Date of birth |
| Age_Range | String | Age category (18-24, 25-34, etc.) |
| Generation | String | Generation (Gen Z, Millennial, Gen X, Boomer) |
| MOBILE_NO | String | Mobile phone number |
| UUID | String | Unique universal identifier |
| Total_point | Integer | Total loyalty points |
| FirstPurchaseDate | Date | Date of first purchase |

### Member Yearly Transaction Table
| Column | Type | Description |
|--------|------|-------------|
| Member_ID | String | Member identifier |
| YEAR | String | Transaction year |
| TotalTxn | Integer | Number of transactions |
| TotalQty | Integer | Total items purchased |
| TotalSpend | Float | Total revenue from member |
| MaxSaleDate | Date | Last transaction date in year |
| Mode_ProductCategory | String | Most frequently purchased category |

### Yearly Snapshot Table (Generated)
Combines member master and yearly transactions with calculated fields:
- **Cumulative_TotalTxn**: Running total of transactions up to year end
- **Active_Years_Count**: Number of years member has been active
- **Cumulative_Last_Txn**: Most recent transaction date up to year end
- **LAP_Days**: Last Activity Period in days
- **Recency_Text**: Segment classification
- **Point_Range**: Categorized loyalty point ranges

## Segment Definitions

| Segment | LAP Days | Description |
|---------|----------|-------------|
| **Active** | ≤ 90 | Recently purchased, engaged customers |
| **At Risk** | 91-180 | Previously active, showing signs of disengagement |
| **Inactive** | 181-270 | Long period since last purchase, high churn risk |
| **Dormant** | > 270 | Churned customers, need win-back campaigns |
| **Never Purchased** | N/A | Registered but no transaction history |

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Or install specific packages
pip install pandas numpy matplotlib seaborn plotly jupyter
```

## Usage

### 1. Generate Sample Data
```bash
cd data
python generate_member_data.py
```

This creates:
- `member_master.csv` - 2,000 members with demographics
- `member_segment_yearly.csv` - 5,471 member-year transaction records (2021-2025)

### 2. Build Yearly Snapshot
```bash
cd python_analysis
python yearly_snapshot_engine.py
```

This generates:
- `yearly_snapshot.csv` - Complete yearly snapshot with all metrics

### 3. Run Sankey Analysis
Open `customer_segment_sankey.ipynb` in Jupyter:
```bash
jupyter notebook customer_segment_sankey.ipynb
```

Execute all cells to:
- Load yearly snapshot data
- Calculate segment transitions
- Generate interactive Sankey diagrams
- Perform retention and churn analysis

## Output Files

### Visualizations
- `sankey_2021-2022.html` - Year-to-year Sankey (2021→2022)
- `sankey_2022-2023.html` - Year-to-year Sankey (2022→2023)
- `sankey_2023-2024.html` - Year-to-year Sankey (2023→2024)
- `sankey_2024-2025.html` - Year-to-year Sankey (2024→2025)
- `sankey_multiyear.html` - Multi-year combined Sankey
- `segment_distribution_yearly.png` - Customer count and revenue by segment
- `churn_reactivation.png` - Churn vs reactivation comparison

### Data Files
- `yearly_snapshot.csv` - Processed snapshot data
- `customer_segments.csv` - Customer profiles with segments (from existing analysis)

## Key Insights from Analysis

### 1. Segment Distribution Trends
- **Growing Customer Base**: From 384 active customers in 2021 to 1,790 in 2025
- **Maturation Pattern**: Decrease in "Never Purchased" as customers engage
- **Natural Attrition**: Small percentage moving to Dormant over time

### 2. Retention Patterns
- **Active Segment**: Typically 70-80% retention year-over-year
- **At Risk Segment**: 40-50% can be saved with interventions
- **Dormant Segment**: 10-15% reactivation rate

### 3. Migration Patterns
Common transitions:
- Active → Active (retention)
- Active → At Risk (requires intervention)
- At Risk → Active (successful retention)
- At Risk → Dormant (churn)
- Never Purchased → Active (new customer activation)

## Business Applications

### Marketing Strategies
1. **Active Customers**: Loyalty rewards, VIP programs, referral incentives
2. **At Risk**: Targeted discounts, personalized offers, engagement campaigns
3. **Inactive**: Win-back emails, special promotions, feedback surveys
4. **Dormant**: Aggressive reactivation offers, understanding churn reasons

### Operational Insights
- **Churn Prevention**: Identify and target At Risk customers before they become Dormant
- **Resource Optimization**: Allocate marketing budget based on segment value and retention potential
- **Campaign Measurement**: Track segment transitions to measure campaign effectiveness
- **Revenue Forecasting**: Use historical transition rates to predict future revenue

## Technical Implementation

### Replicating Power BI DAX in Python

#### Original DAX (Power BI)
```dax
YearlySnapshot =
ADDCOLUMNS(
    YearTable,
    "TotalTxn",
        VAR _acc = YearTable[accountNumber]
        VAR _yr = YearTable[YEAR]
        RETURN CALCULATE(SUM(member_segment_yearly[TotalTxn]), ...)
)
```

#### Python Equivalent
```python
snapshot = year_table.merge(
    member_yearly,
    on=['Member_ID', 'YEAR'],
    how='left'
)

# Cumulative calculations
for member_id in members:
    for year in years:
        year_end = calculate_year_end_date(year)
        cum_txn = member_data[
            member_data['MaxSaleDate'] <= year_end
        ]['TotalTxn'].sum()
```

### Sankey Diagram Creation
```python
fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=nodes,
        color=node_colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=counts
    )
)])
```

## Performance

- **Data Processing**: ~10,000 member-year records processed in < 5 seconds
- **Visualization**: Interactive Sankey diagrams render instantly in browser
- **Scalability**: Can handle 100,000+ member-year records with minor optimizations

## Future Enhancements

1. **Predictive Modeling**: Use transition patterns to predict future segment movements
2. **Customer Lifetime Value**: Calculate CLV based on segment history
3. **Automated Alerts**: Flag customers transitioning to at-risk segments
4. **Dashboard Integration**: Embed Sankey diagrams in web dashboards
5. **Multi-Dimensional Analysis**: Add product category and geographic dimensions

## Portfolio Value

This project demonstrates:
- **BI Tool Translation**: Converting Power BI DAX logic to Python
- **Data Engineering**: Building complex data transformation pipelines
- **Advanced Visualization**: Creating interactive Sankey diagrams
- **Business Analytics**: Performing customer lifecycle analysis
- **Code Documentation**: Comprehensive README and inline documentation

## References

- [Plotly Sankey Diagrams](https://plotly.com/python/sankey-diagram/)
- [RFM Analysis](https://en.wikipedia.org/wiki/RFM_(market_research))
- [Customer Lifecycle Analytics](https://www.optimizely.com/optimization-glossary/customer-lifecycle/)

## License

This is a portfolio project. Feel free to use as reference for your own analysis.

## Contact

**Robin Phonpakdee**
- Email: robint.phonpakdee@gmail.com
- LinkedIn: [robin-phonpakdee-4a4782251](https://www.linkedin.com/in/robin-phonpakdee-4a4782251)
- GitHub: [robin-tennessine](https://github.com/robin-tennessine)

---

*This project showcases the ability to replicate complex business intelligence calculations from Power BI in Python, creating scalable and automated customer analytics solutions.*
