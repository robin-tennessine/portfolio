# Getting Started Guide

This guide will help you set up and explore the Data Analytics Portfolio.

## Quick Start (5 minutes)

### Step 1: Generate Sample Data
```bash
cd data
python generate_sample_data.py
```

This creates:
- `sales_data.csv` (10,000 transactions)
- `customer_data.csv` (1,000 customers)

### Step 2: Explore SQL Analysis
```bash
cd ../sql_analysis
```

Open any SQL file and run queries in your preferred SQL environment:
- PostgreSQL
- MySQL
- SQLite
- Or any SQL-compatible database

### Step 3: Run Python Notebooks
```bash
# Install dependencies first
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

Open and run:
1. `python_analysis/sales_dashboard.ipynb` - Sales analytics and visualizations
2. `python_analysis/customer_segmentation.ipynb` - RFM analysis and clustering

### Step 4: Execute ETL Pipeline
```bash
cd etl_pipeline
python data_pipeline.py
```

Check output in `data/processed/` folder.

### Step 5: Review Power BI Examples
```bash
cd powerbi_examples
```

- Open `dax_measures.txt` for DAX formulas
- Open `power_query_transformations.txt` for M code

## Detailed Setup

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package manager)

**Optional:**
- PostgreSQL or MySQL (for SQL examples)
- Power BI Desktop (for Power BI examples)
- Git (for version control)

### Installation

1. **Clone or download this repository:**
```bash
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('All packages installed successfully!')"
```

## Project Exploration Guide

### For Recruiters (15-minute overview)

**Best files to review:**
1. `/README.md` - Project overview and skills
2. `/sql_analysis/02_customer_insights.sql` - Advanced SQL
3. `/python_analysis/customer_segmentation.ipynb` - Python & ML
4. `/powerbi_examples/dax_measures.txt` - Power BI skills
5. `/etl_pipeline/data_pipeline.py` - ETL capabilities

### For Technical Review (45-minute deep dive)

**Recommended sequence:**
1. Generate sample data
2. Run ETL pipeline to understand data transformation
3. Execute SQL queries to see analytical thinking
4. Run Jupyter notebooks for end-to-end Python analysis
5. Review Power BI examples for BI tool proficiency

### For Learning (Self-paced)

**Start here:**
1. `/data/generate_sample_data.py` - Understand the dataset
2. `/sql_analysis/README.md` - SQL overview
3. Follow numbered SQL files (01, 02, 03)
4. Move to Python notebooks
5. Study ETL pipeline architecture
6. Explore Power BI examples

## Working with the Data

### Understanding the Dataset

**Sales Data (sales_data.csv):**
- 10,000 transactions
- Date range: Last 12 months
- Products: Mobile phones, accessories, cafe items
- Stores: 6 locations across Thailand

**Customer Data (customer_data.csv):**
- 1,000 customers
- Demographics: age, gender, city
- Segments: Premium, Regular, Occasional, New
- Registration dates over 3 years

### Customizing the Analysis

**To use your own data:**
1. Replace CSV files in `/data/` folder
2. Update column names in scripts and notebooks
3. Adjust SQL queries to match your schema
4. Modify DAX measures for your data model

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. Jupyter notebook won't start**
```bash
pip install jupyter notebook
jupyter notebook
```

**3. CSV files not found**
```bash
cd data
python generate_sample_data.py
```

**4. SQL queries don't run**
- Check your database connection
- Ensure data is imported
- Verify table/column names match

**5. Visualizations don't display**
```bash
# If using Jupyter
%matplotlib inline

# Reinstall matplotlib
pip install --upgrade matplotlib
```

## Next Steps

### Extend the Portfolio

Ideas for expansion:
- Add more advanced ML models
- Create Tableau dashboards
- Build interactive web apps with Streamlit
- Add predictive analytics
- Implement A/B testing analysis
- Create automated reporting

### Share Your Portfolio

**On GitHub:**
1. Create a new repository
2. Push this portfolio
3. Add a professional README
4. Include screenshots of visualizations

**On LinkedIn:**
- Share project highlights
- Post insights discovered
- Link to GitHub repository

## Resources

### Learning More

**SQL:**
- Mode Analytics SQL Tutorial
- SQLZoo
- LeetCode SQL Problems

**Python:**
- Python for Data Analysis (book)
- Kaggle Learn
- DataCamp

**Power BI:**
- Microsoft Learn Power BI
- SQLBI.com
- Guy in a Cube (YouTube)

**Statistics:**
- Khan Academy Statistics
- StatQuest (YouTube)
- Seeing Theory

## Support

Questions or issues?
- Check the README files in each folder
- Review the comments in code files
- Open an issue on GitHub

## Contributing

Suggestions for improvement are welcome! Feel free to:
- Fork this repository
- Create a feature branch
- Submit a pull request

---

**Happy analyzing!** 📊
