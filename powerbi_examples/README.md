# Power BI Examples

This folder contains DAX measures and Power Query (M code) transformations demonstrating Power BI development skills.

## Contents

### 1. DAX Measures (`dax_measures.txt`)

Comprehensive collection of DAX formulas organized by category:

#### Sales Metrics
- Total Revenue, Transactions, Units Sold
- Average Transaction Value and Unit Price

#### Time Intelligence
- MTD, QTD, YTD calculations
- Previous period comparisons (PM, PY)
- Growth metrics (MoM, YoY)
- Rolling averages and moving calculations
- Custom period calculations (L30D, L90D)

#### Customer Analytics
- Unique and new customer counts
- Customer retention and churn rates
- Revenue per customer
- Customer Lifetime Value
- Repeat purchase rates

#### Product Performance
- Product rankings and market share
- ABC classification
- Sales velocity metrics
- Product comparison measures

#### Advanced Calculations
- Pareto analysis (80/20 rule)
- Statistical measures (standard deviation, median, percentiles)
- Dynamic measure selectors
- Conditional formatting formulas
- KPI indicators

### 2. Power Query Transformations (`power_query_transformations.txt`)

M code examples for data transformation:

#### Data Import & Basic Transformations
- CSV and Excel file imports
- Column type conversions
- Header promotion

#### Date Table Creation
- Comprehensive date dimension
- Fiscal year calculations
- Day/Week/Month/Quarter attributes
- Weekend and workday flags

#### Data Cleaning
- Duplicate removal
- Text trimming and standardization
- Null value handling
- Data validation and filtering

#### Advanced Transformations
- Customer metrics calculation
- RFM analysis in Power Query
- Aggregations and grouping
- Custom column creation

#### Table Operations
- Merging and joining tables
- Unpivoting data
- Table expansion
- Nested joins

#### Dynamic Features
- Parameter-driven queries
- Error handling
- Custom functions
- Conditional logic

## Skills Demonstrated

### DAX Skills
- Time intelligence functions
- Context manipulation (CALCULATE, FILTER, ALL)
- Iterators (SUMX, AVERAGEX)
- Variables for optimization
- Statistical calculations
- Dynamic measures
- Best practices implementation

### Power Query Skills
- M language proficiency
- ETL operations
- Data modeling
- Performance optimization
- Error handling
- Reusable functions
- Query folding awareness

## How to Use These Examples

### In Power BI Desktop:

1. **DAX Measures:**
   - Open Power BI Desktop
   - Load your data model
   - Create new measures by copying the DAX code
   - Adjust table and column references to match your model
   - Test with different visualizations and filter contexts

2. **Power Query:**
   - Go to Transform Data (Power Query Editor)
   - Advanced Editor
   - Paste M code
   - Update file paths and table references
   - Close & Apply

### Customization:

- Replace table and column names with your actual data model
- Adjust thresholds and business rules as needed
- Modify date ranges and period definitions
- Adapt customer segments and classifications

## Business Value

These measures and transformations enable:

1. **Executive Dashboards**
   - KPIs and performance metrics
   - Trend analysis and forecasting
   - Target vs actual comparisons

2. **Sales Analytics**
   - Revenue tracking and growth analysis
   - Product performance monitoring
   - Store location comparisons

3. **Customer Intelligence**
   - Segmentation and profiling
   - Retention and churn analysis
   - Customer value optimization

4. **Operational Reporting**
   - Daily/weekly/monthly tracking
   - Inventory and sales velocity
   - Resource allocation insights

## Power BI Best Practices Applied

- ✅ Proper use of calculated columns vs measures
- ✅ DIVIDE() function to handle division by zero
- ✅ Variables for better performance and readability
- ✅ Appropriate use of context transition
- ✅ Optimized iterators with filtering
- ✅ Clear naming conventions
- ✅ Documentation and comments
- ✅ Error handling in Power Query
- ✅ Data type optimization
- ✅ Query folding considerations

## Related Projects

These Power BI examples complement:
- SQL Analysis (`/sql_analysis`) - Similar metrics in SQL
- Python Analysis (`/python_analysis`) - Advanced analytics
- ETL Pipeline (`/etl_pipeline`) - Data preparation

## Additional Resources

For learning more about DAX and Power Query:
- SQLBI.com - DAX patterns and best practices
- Microsoft Power BI Documentation
- DAX.guide - Complete DAX function reference
- PowerQuery.how - M language reference

---

**Note:** These examples are templates. Always test thoroughly and adjust to your specific business requirements and data model structure.
