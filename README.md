# Robin Phonpakdee - Data Analytics Portfolio

## About Me

Junior Data Analyst with 1 year of experience in retail analytics and business intelligence. Currently working at **Cube Analytics Consulting** for **Jaymart Holding** (Jaymart Mobile, Casa Lapin).

**Background:**
- Bachelor's degree in Business English
- Specializing in customer segmentation, dashboard creation, and data-driven insights
- Experience building ETL pipelines and automated reporting systems
- Translating complex data into actionable business recommendations

**Portfolio Website:** https://robin-tennessine.github.io/portfolio/

---

## Technical Skills

### Data Analysis & BI
- **SQL:** PostgreSQL, MySQL - Complex queries, window functions, CTEs
- **Python:** pandas, numpy, matplotlib, seaborn, scikit-learn, plotly
- **Power BI:** DAX, Power Query (M), data modeling, dashboard design
- **RapidMiner:** ETL pipeline development and automation

### Analysis Specializations
- Customer Segmentation (RFM, K-means clustering)
- Customer Lifecycle Analysis (Sankey diagrams, cohort analysis)
- Trend Analysis & Forecasting
- KPI Development & Reporting
- Statistical Analysis

### Tools & Technologies
- Jupyter Notebooks for interactive analysis
- Git for version control
- Flask API development
- Data visualization (matplotlib, seaborn, plotly)

---

## Featured Projects

### 1. Customer Segment Flow - Professional Sankey Visualization
**Location:** `/python_analysis/`

Advanced customer lifecycle analysis with interactive Sankey diagrams:
- **Start/End year snapshots** showing customer status transitions
- **Percentage labels** on all flows showing transition rates
- **New member tracking** with separate visualization
- **Professional sankeyart.com-style** design
- Replicates Power BI DAX logic in Python

**Key Features:**
- 4 time points per year (Start → End → Start → End)
- Segment retention analysis (88% Active retention rate)
- Churn and reactivation tracking
- Business-ready insights and recommendations

**Technologies:** Python, Plotly, pandas, matplotlib

### 2. Advanced SQL Analytics - Retail Sales
**Location:** `/sql_analysis/`

Comprehensive SQL queries for business intelligence:
- Sales performance analysis with window functions
- Customer behavior insights and cohort analysis
- Product performance metrics
- Time-series trend analysis with CTEs
- 200+ production-ready queries

**Technologies:** PostgreSQL, MySQL

### 3. Python Customer Analytics
**Location:** `/python_analysis/customer_segmentation.ipynb`

End-to-end customer segmentation analysis:
- RFM (Recency, Frequency, Monetary) analysis
- K-means clustering with optimal cluster selection
- Customer profiling and demographics analysis
- Actionable marketing strategies per segment

**Technologies:** Python, scikit-learn, pandas, matplotlib, seaborn

### 4. ETL Data Pipeline
**Location:** `/etl_pipeline/`

Production-ready automated data pipeline:
- Multi-source data extraction
- Data transformation and cleaning
- Data validation and quality checks
- Comprehensive logging and error handling
- Analytics-ready output format

**Technologies:** Python, pandas, RapidMiner

### 5. Power BI Business Intelligence
**Location:** `/powerbi_examples/`

Power BI development examples:
- 60+ DAX measures for sales, customer, and product analytics
- Time intelligence calculations
- Power Query (M) transformations
- Data modeling best practices

**Technologies:** Power BI, DAX, Power Query (M)

### 6. Flask API Export Service
**Location:** `/flask_api_export/`

PDPA-compliant data export API:
- RESTful API for Power BI integration
- Data masking for privacy compliance
- Automated email exports
- VPN-only access security
- Production deployment for Jaymart Holding

**Technologies:** Python, Flask, REST API

---

## Project Highlights

### Customer Segment Sankey Analysis
- **Business Impact:** Identified 88% retention rate for Active customers, 12.1% early warning for At Risk segment
- **New Member Tracking:** 352 new members acquired in 2025, all activated successfully
- **Reactivation Success:** 85.5% of Dormant customers reactivated

### Customer Segmentation (RFM + K-means)
- **Segments Identified:** Champions, Loyal Customers, At Risk, Lost Customers
- **Revenue Concentration:** Top 20% of customers drive 60%+ of revenue
- **Actionable Insights:** Specific marketing strategies for each segment

---

## Technical Capabilities

**Data Processing:**
- ETL pipeline development and automation
- Data cleaning and validation
- Multi-source data integration
- Large dataset handling (100K+ records)

**Analysis & Modeling:**
- Customer segmentation and clustering
- Cohort analysis and lifecycle tracking
- Statistical analysis and hypothesis testing
- Predictive modeling (regression, classification)

**Visualization & Reporting:**
- Interactive dashboards (Power BI, Python)
- Sankey diagrams for flow analysis
- KPI reporting and executive summaries
- Data storytelling for stakeholders

**Business Applications:**
- Customer lifecycle management
- Churn prediction and prevention
- Marketing campaign optimization
- Revenue forecasting

---

## Getting Started

### Prerequisites
```bash
Python 3.8+
Jupyter Notebook
```

### Installation
```bash
# Clone the repository
git clone https://github.com/robin-tennessine/portfolio.git
cd portfolio

# Install required packages
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook
```

### Quick Start - Professional Sankey
```bash
# Generate snapshot data
cd data
python generate_member_data.py

# Create snapshots
cd ../python_analysis
python enhanced_snapshot_engine.py

# Generate Sankey visualization
python professional_sankey.py

# Open visualization
open ../visualizations/sankey_professional_2024_2025.html
```

---

## Project Structure

```
portfolio/
│
├── data/                          # Sample datasets
│   ├── sales_data.csv
│   ├── customer_data.csv
│   ├── member_master.csv         # Customer demographics
│   ├── member_segment_yearly.csv # Transaction data
│   ├── snapshots_start_end.csv   # Yearly snapshots
│   └── generate_member_data.py
│
├── python_analysis/               # Python analysis
│   ├── customer_segmentation.ipynb
│   ├── sales_dashboard.ipynb
│   ├── enhanced_snapshot_engine.py    # Snapshot calculator
│   ├── professional_sankey.py         # Sankey builder
│   └── PROFESSIONAL_SANKEY_README.md
│
├── sql_analysis/                  # SQL queries
│   ├── 01_sales_analysis.sql
│   ├── 02_customer_insights.sql
│   ├── 03_product_performance.sql
│   └── README.md
│
├── etl_pipeline/                  # ETL automation
│   ├── data_pipeline.py
│   └── README.md
│
├── powerbi_examples/              # Power BI assets
│   ├── dax_measures.txt
│   ├── power_query_transformations.txt
│   └── README.md
│
├── flask_api_export/              # Flask API
│   ├── app.py
│   ├── data_masking.py
│   └── README.md
│
├── visualizations/                # Charts and diagrams
│   ├── sankey_professional_2024_2025.html
│   └── README.md
│
├── website/                       # Portfolio website
│   └── index.html
│
└── requirements.txt               # Python dependencies
```

---

## Documentation

Each project folder contains:
- Detailed README with methodology
- Business insights and recommendations
- Code documentation and comments
- Example outputs and visualizations

---

## Contact

**Robin Phonpakdee**

- **Portfolio Website:** https://robin-tennessine.github.io/portfolio/
- **LinkedIn:** [robin-phonpakdee-4a4782251](https://www.linkedin.com/in/robin-phonpakdee-4a4782251)
- **GitHub:** [robin-tennessine](https://github.com/robin-tennessine)
- **Email:** robint.phonpakdee@gmail.com

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Showcasing data analytics expertise through real-world business scenarios and production-ready solutions.*
