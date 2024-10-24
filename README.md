# UK Retail Data Analysis Tool

## Overview
This repository contains a comprehensive Python-based analysis toolkit for processing and visualizing UK retail e-commerce data. The toolkit includes data preprocessing, exploratory data analysis (EDA), and advanced visualization capabilities for customer behavior analysis.

## Dataset Structure
The analysis is built for the UK Retail Dataset with the following key fields:
- `Invoice`: Unique invoice number for each transaction
- `StockCode`: Product code
- `Description`: Product name/description
- `Quantity`: Number of items purchased
- `InvoiceDate`: Date and time of the transaction
- `Price`: Unit price of the product
- `Customer ID`: Unique identifier for each customer
- `Country`: Country where the transaction occurred

## Project Structure
The project consists of two main Python modules:

### 1. Data Processing Module (`Analysis.py`)
- Data loading and validation
- Initial data cleaning and preprocessing
- Basic statistical analysis
- Dataset exploration capabilities
- Data export functionality

### 2. Visualization Analysis Module (`VisualizationAnalysis.py`)
- Customer segmentation analysis
- Sales trend visualization
- Hourly sales patterns
- Geographical analysis
- Product performance analysis
- Basket size analysis

## Features

### Data Processing
- Automated data cleaning and validation
- Removal of invalid entries (negative quantities, prices)
- Handling of missing values
- Cancelled order filtering
- Derived metrics calculation

### Visualizations
- Interactive sales trend analysis
- Hour-by-day sales heatmaps
- 3D customer segmentation using RFM analysis
- Product performance charts
- Geographical distribution analysis
- Basket size and value analysis

## Requirements
```python
pandas
numpy
matplotlib
seaborn
plotly
openpyxl
```

## Installation
1. Clone the repository:
```bash
[git clone https://github.com/devanshdp04/E-commerceanalysis.git]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Data Processing
```python
from data_processing import main as process_data

# Process the dataset
processed_df = process_data()
```

### Visualization Analysis
```python
from visualization_analysis import CustomerVisualizationAnalysis

# Create visualization object
viz = CustomerVisualizationAnalysis(processed_df)

# Generate specific visualizations
viz.plot_sales_trends()
viz.create_hourly_heatmap()
viz.plot_customer_segments()
```

## Output Examples
- Sales trends analysis with monthly and daily patterns
- Customer segmentation in 3D space based on RFM metrics
- Product performance analysis with revenue breakdowns
- Geographical distribution of sales and orders
- Basket size analysis with hourly patterns

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Dataset source: UK Retail Dataset
- Built with Python data science libraries
- Visualization powered by Plotly and Seaborn
