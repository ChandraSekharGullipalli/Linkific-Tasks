# Day 15 – Python Data Visualization

## 1. Project Overview

This project focuses on learning and implementing Python data visualization techniques using Matplotlib, Seaborn, and Plotly.

The main objective is to transform raw sales data into meaningful visual representations, statistical insights, and interactive dashboards.

## 2. Learning Objectives

- Create visualizations using Matplotlib.
- Perform statistical visualization using Seaborn.
- Develop interactive charts using Plotly.
- Build interactive dashboards.
- Understand visualization best practices.
- Analyze sales trends and business performance.
- Select appropriate chart types for different datasets.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Static visualizations |
| Seaborn | Statistical visualizations |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |

## 4. Project Structure

```text
Data-Visualization/
│
├── datasets/
│   ├── create_dataset.py
│   └── sales_data.csv
│
├── outputs/
│   ├── PNG chart images
│   └── HTML interactive charts
│
├── visualizations/
│   ├── 01_matplotlib_charts.py
│   ├── 02_seaborn_charts.py
│   ├── 03_plotly_charts.py
│   └── 04_statistical_visualizations.py
│
├── dashboard/
│   └── app.py
│
└── README.md
```

## 5. Dataset Description

The project uses a sample sales dataset containing 300 records.

Dataset columns:

- Date
- Product
- Region
- Category
- Sales
- Quantity
- Profit
- Discount
- Customer Age
- Rating

The dataset is used to analyze product performance, regional sales, profit distribution, and customer-related patterns.

## 6. Matplotlib Chart Guide

Matplotlib is used to create static charts and customize visual representations.

| Chart | Purpose |
|---|---|
| Line Plot | Analyze trends over time |
| Bar Chart | Compare categories |
| Horizontal Bar | Compare categories horizontally |
| Scatter Plot | Analyze relationships |
| Histogram | Understand data distribution |
| Pie Chart | Show proportions |
| Box Plot | Identify outliers |
| Area Chart | Display trends and magnitude |
| Stem Plot | Show individual observations |
| Subplots | Display multiple charts together |
| Step Plot | Show step-wise changes |

## 7. Seaborn Chart Guide

Seaborn is used for statistical data visualization.

| Chart | Purpose |
|---|---|
| Distribution Plot | Analyze distributions |
| Violin Plot | Understand distribution density |
| Count Plot | Count categorical observations |
| Box Plot | Identify statistical outliers |
| Heatmap | Display correlations |
| Pair Plot | Compare multiple numerical variables |
| Bar Plot | Compare statistical summaries |
| Regression Plot | Visualize relationships |
| Swarm Plot | Display individual observations |
| Strip Plot | Display individual data points |
| ECDF Plot | Show cumulative distributions |
| Joint Plot | Analyze two variables together |

## 8. Plotly Interactive Chart Guide

Plotly supports interactive charts with zooming, hovering, and filtering.

Implemented chart types:

1. Interactive Line Chart
2. Interactive Scatter Plot
3. 3D Scatter Plot
4. Animated Bar Chart
5. Interactive Bar Chart
6. Treemap

Interactive charts are exported as HTML files and can be opened in a web browser.

## 9. Interactive Sales Dashboard

The project includes a Streamlit dashboard.

Dashboard features:

- Total Sales KPI
- Total Profit KPI
- Total Quantity KPI
- Total Orders KPI
- Region filters
- Product filters
- Daily sales trend
- Product sales comparison
- Regional sales distribution
- Sales versus profit analysis
- Dataset preview
- Filtered CSV download

## 10. Statistical Visualization Concepts

### Mean
The average of numerical values.

### Median
The middle value in an ordered dataset.

### Standard Deviation
Measures the spread of values around the mean.

### Correlation
Measures the strength and direction of a relationship between two numerical variables.

### Outliers
Observations that differ significantly from the rest of the data.

### Regression
Models the relationship between variables.

### KDE
Kernel Density Estimation provides a smooth estimate of a data distribution.

## 11. Visualization Best Practices

- Select the correct chart for the data.
- Use clear and meaningful titles.
- Label the X-axis and Y-axis.
- Choose appropriate colors.
- Avoid unnecessary visual effects.
- Maintain readable chart dimensions.
- Avoid misleading axis scales.
- Display legends when necessary.
- Avoid overcrowding charts.
- Use interactive charts when they improve exploration.

## 12. How to Install Dependencies

```bash
python -m pip install pandas numpy matplotlib seaborn plotly streamlit
```

## 13. How to Execute the Project

Generate the dataset:

```bash
python datasets/create_dataset.py
```

Run Matplotlib charts:

```bash
python visualizations/01_matplotlib_charts.py
```

Run Seaborn charts:

```bash
python visualizations/02_seaborn_charts.py
```

Run Plotly charts:

```bash
python visualizations/03_plotly_charts.py
```

Run statistical visualizations:

```bash
python visualizations/04_statistical_visualizations.py
```

Launch interactive dashboard:

```bash
python -m streamlit run dashboard/app.py
```

## 14. Expected Outputs

- Static chart images in the outputs folder.
- Interactive Plotly HTML visualizations.
- Statistical analysis and correlation results.
- Interactive Streamlit sales dashboard.
- Filtered sales data downloadable as CSV.

## 15. Conclusion

Successfully practiced Python data visualization using Matplotlib, Seaborn, Plotly, and Streamlit.

The project demonstrates the ability to transform sales data into static charts, statistical visualizations, interactive charts, and dashboards.

These techniques help understand data patterns, compare business performance, identify relationships, and communicate analytical findings effectively.

## 16. Internship Deliverable

**Day 15: Python Data Visualization**

Deliverables:
- 20+ different chart types.
- Matplotlib visualizations.
- Seaborn statistical plots.
- Plotly interactive visualizations.
- Interactive sales dashboard.
- Statistical visualization guide.
- Project documentation and GitHub submission.