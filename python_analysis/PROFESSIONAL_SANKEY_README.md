# Professional Customer Segment Sankey - Start & End Year Analysis

## Overview

This enhanced Sankey visualization shows customer segment transitions with **start-of-year** and **end-of-year** snapshots, tracking how customers move through the lifecycle **within** and **between** years.

## Key Features

### ✅ 1. **Four Time Points Per Year Pair**
```
2024 Start → 2024 End → 2025 Start → 2025 End
```

Each snapshot shows:
- **LAP (Last Activity Period)** calculated at that specific date
- **Segment classification** based on LAP at that moment
- **Member counts and percentages**

### ✅ 2. **New Member Tracking**
- **New Members** appear as a separate source at the start of each year
- Shows acquisition of members who made their first purchase during the year
- Flows from "New Members" node to initial segments

### ✅ 3. **Percentage Labels**
- Every flow shows **count and percentage** (e.g., "1,079 (87.9%)")
- Node labels show **total members and % of database**
- Hover shows detailed transition information

### ✅ 4. **Professional Styling**
- Clean, sankeyart.com-inspired design
- Color-coded by segment type
- Clear labels and annotations
- Interactive tooltips

## How to Read the Visualization

### **Time Points Explained**

#### 2024 Start (Jan 1, 2024)
- Members categorized by LAP on January 1, 2024
- Shows initial state when CRM system started tracking
- "Never Purchased" = no purchase before Jan 1, 2024

#### 2024 End (Dec 31, 2024 or last transaction date)
- Members re-categorized by LAP at year-end
- Shows how segments changed during the year
- Accounts for all transactions through Dec 31

#### 2025 Start (Jan 1, 2025)
- **Existing members**: Carry forward from 2024 End status
- **New Members**: First-time purchasers in 2025 (separate source)
- Combined total shows complete customer base

#### 2025 End (Latest date in data)
- Final status as of most recent data
- Shows current segment distribution
- Used for forecasting and planning

### **Flow Interpretation**

**Example Flows:**

1. **Active (2024 Start) → Active (2024 End): 977 (88.0%)**
   - 977 customers were Active at start of 2024
   - 88.0% of them stayed Active through end of 2024
   - Strong retention within the year

2. **Active (2024 End) → Active (2025 Start): 1,438 (100%)**
   - All Active members at 2024 End carry forward to 2025 Start
   - Status preserved between years (recalculated at Jan 1)

3. **New Members (2025) → Active (2025 Start): 352 (100%)**
   - 352 new members joined in 2025
   - All were classified as Active when they joined
   - Separate from existing member flows

## Segment Definitions

| Segment | LAP Days | Color | Meaning |
|---------|----------|-------|---------|
| **Active** | ≤ 90 | 🔵 Blue | Recently purchased, engaged |
| **At Risk** | 91-180 | 🟠 Orange | Warning signs, need intervention |
| **Inactive** | 181-270 | 🟣 Purple | Long dormant, high churn risk |
| **Dormant** | > 270 | 🔴 Red | Churned, need win-back |
| **Never Purchased** | N/A | ⚫ Gray | Registered but no transactions |
| **New Members** | N/A | 🟢 Green | First purchase in this period |

## Business Insights

### 1. **Within-Year Retention**
Track how well segments retain members during the year:
- Active (2024 Start) → Active (2024 End) = **retention rate**
- Active (2024 Start) → At Risk (2024 End) = **early warning**

### 2. **Year-over-Year Stability**
Compare year-end to next year-start:
- Shows natural segment persistence
- Helps forecast beginning-of-year status

### 3. **New Member Acquisition**
Separate flow for new members shows:
- **Acquisition volume** (how many new members)
- **Initial segment distribution** (where they land)
- **Activation rate** (% who become Active)

### 4. **Churn and Reactivation**
- Active → Dormant = churn
- Dormant → Active = reactivation success
- Track across multiple time points

## Technical Implementation

### Snapshot Calculation

```python
# For each member at each time point:
1. Get reference_date (Jan 1 or Dec 31)
2. Find last transaction before reference_date
3. Calculate LAP = reference_date - last_txn_date
4. Classify segment based on LAP
5. Track if member is "new" (first purchase in this period)
```

### Transition Building

```python
# Three transition types:
1. Year Start → Year End (within-year changes)
2. Year End → Next Year Start (year boundary)
   - Existing members carry forward
   - New members appear as separate source
3. Next Year Start → Next Year End (within-year changes)
```

### Percentage Calculation

```python
# For each flow:
percentage = (flow_count / source_total) × 100

# For each node:
node_pct = (node_count / total_members) × 100
```

## Files Generated

### Visualizations
- `sankey_professional_2024_2025.html` - Interactive Sankey diagram
- `sankey_professional_2024_2025.png` - Static image for GitHub

### Data Files
- `snapshots_start_end.csv` - All start/end year snapshots

### Code Files
- `enhanced_snapshot_engine.py` - Calculates start/end snapshots
- `professional_sankey.py` - Generates Sankey visualization

## Usage

### Generate New Visualizations

```bash
# 1. Generate start/end snapshots
cd python_analysis
python enhanced_snapshot_engine.py

# 2. Create professional Sankey
python professional_sankey.py

# 3. Open in browser
open ../visualizations/sankey_professional_2024_2025.html
```

### Customize for Your Data

**Change year range:**
```python
builder = ProfessionalSankeyBuilder('../data/snapshots_start_end.csv')
fig = builder.create_sankey(2023, 2024, show_percentages=True)
```

**Adjust segment thresholds:**
Edit `enhanced_snapshot_engine.py`:
```python
def calculate_recency_segment(self, lap_days):
    if lap_days <= 60:  # Change from 90 to 60 days
        return "Active"
    # ...
```

**Modify colors:**
Edit `professional_sankey.py`:
```python
segment_colors = {
    'Active': 'rgba(0, 255, 0, 0.8)',  # Bright green
    # ...
}
```

## Comparison with Original Sankey

| Feature | Original Sankey | Professional Sankey |
|---------|----------------|---------------------|
| **Time Points** | 2 per year pair (End → End) | 4 per year pair (Start → End → Start → End) |
| **New Members** | Not tracked separately | Separate source node |
| **Percentages** | Not shown | On every flow |
| **Node Labels** | Basic segment names | Segment + count + % |
| **Snapshot Logic** | End-of-year only | Start AND end of year |
| **Within-Year Changes** | Not visible | Clearly shown |

## Real-World Application

### Marketing Campaign Timing

**Use Start-of-Year Snapshots:**
- Plan Q1 campaigns based on Jan 1 segment status
- Target At Risk members before they become Dormant
- Welcome New Members with onboarding campaigns

**Use End-of-Year Snapshots:**
- Measure annual performance
- Calculate retention rates
- Plan budget for next year

### Forecasting

**Historical Pattern Analysis:**
- Compare 2024 Start/End with 2025 Start/End
- Identify seasonal trends
- Project future segment distribution

### Resource Allocation

**Budget by Segment:**
- Active: Loyalty programs (high retention)
- At Risk: Retention campaigns (prevent churn)
- Dormant: Win-back offers (reactivation)
- New Members: Onboarding (activation)

## Advanced Features

### Multi-Year Sankey

Create continuous flow across multiple years:
```python
# 2023 Start → 2023 End → 2024 Start → 2024 End → 2025 Start → 2025 End
builder.create_sankey_multi_year([2023, 2024, 2025])
```

### Demographic Segmentation

Add demographic dimensions:
```python
# Separate Sankey by age group or gender
builder.create_sankey(2024, 2025, filter_by={'Age_Range': '25-34'})
```

### Revenue-Weighted Flows

Show flows weighted by revenue instead of customer count:
```python
# Thicker flows = higher revenue
builder.create_sankey(2024, 2025, weight_by='Total_Spend')
```

## Example Insights from 2024-2025 Data

### Key Findings:

1. **Strong Active Retention**: 88% of Active members in 2024 Start stayed Active through 2024 End
2. **New Member Acquisition**: 352 new members joined in 2025
3. **Minimal Churn**: Only small flows to Dormant segment
4. **Never Purchased Conversion**: ~50% of Never Purchased members converted to Active in 2024

### Recommendations:

1. **Maintain Current Retention Strategy**: Active retention rate is excellent
2. **Focus on At Risk**: Set up automated alerts for members entering At Risk
3. **Optimize New Member Onboarding**: Ensure all new members become Active quickly
4. **Win-Back Campaigns**: Target Never Purchased members with special offers

---

## Portfolio Value

This visualization demonstrates:

- ✅ **Advanced Data Engineering**: Multi-point snapshot calculations
- ✅ **Business Analytics**: Cohort analysis and lifecycle tracking
- ✅ **Data Visualization**: Professional, interactive Sankey diagrams
- ✅ **BI Tool Translation**: Replicating Power BI DAX in Python
- ✅ **Stakeholder Communication**: Clear, actionable insights

---

**Created by: Robin Phonpakdee**
**Contact**: robint.phonpakdee@gmail.com
**LinkedIn**: [robin-phonpakdee-4a4782251](https://www.linkedin.com/in/robin-phonpakdee-4a4782251)

*Professional Sankey visualization inspired by sankeyart.com, built with Python and Plotly*
