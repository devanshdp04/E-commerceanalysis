import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

class CustomerVisualizationAnalysis:
    def __init__(self, df):
        self.df = df.copy()
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        self.df['Month'] = self.df['InvoiceDate'].dt.strftime('%Y-%m')
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.day_name()
        
        # Set default matplotlib style
        plt.style.use('default')
        
        # Set seaborn default style parameters
        sns.set_theme(style="whitegrid")  # Using set_theme instead of style.use
        sns.set_palette("husl")

    def plot_sales_trends(self):
        """
        Create monthly and daily sales trends visualization
        """
        try:
            # Monthly sales trend
            monthly_sales = self.df.groupby('Month')['TotalAmount'].sum().reset_index()
            
            fig = make_subplots(rows=2, cols=1, subplot_titles=('Monthly Sales Trend', 'Daily Sales Pattern'))
            
            # Monthly trend
            fig.add_trace(
                go.Scatter(x=monthly_sales['Month'], y=monthly_sales['TotalAmount'],
                          mode='lines+markers', name='Monthly Sales',
                          line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8)),
                row=1, col=1
            )
            
            # Daily pattern
            daily_sales = self.df.groupby('DayOfWeek')['TotalAmount'].mean().reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            
            fig.add_trace(
                go.Bar(x=daily_sales.index, y=daily_sales.values,
                      name='Average Daily Sales',
                      marker_color='#2ecc71'),
                row=2, col=1
            )
            
            fig.update_layout(height=800, showlegend=False,
                            title_text="Sales Trends Analysis",
                            title_x=0.5)
            fig.show()
        except Exception as e:
            print(f"Error in plot_sales_trends: {str(e)}")

    def create_hourly_heatmap(self):
        """
        Create a heatmap showing sales patterns by hour and day
        """
        try:
            hourly_sales = self.df.pivot_table(
                values='TotalAmount',
                index='DayOfWeek',
                columns='Hour',
                aggfunc='sum'
            ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

            plt.figure(figsize=(15, 8))
            
            # Create heatmap with custom parameters
            heatmap = sns.heatmap(hourly_sales, 
                                 cmap='YlOrRd', 
                                 annot=True, 
                                 fmt='.0f',
                                 cbar_kws={'label': 'Total Sales'})
            
            plt.title('Sales Heatmap by Hour and Day of Week', pad=20)
            plt.xlabel('Hour of Day', labelpad=10)
            plt.ylabel('Day of Week', labelpad=10)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=0)
            plt.yticks(rotation=0)
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error in create_hourly_heatmap: {str(e)}")

    def plot_customer_segments(self):
        """
        Create RFM-based customer segmentation visualization
        """
        try:
            # Calculate RFM metrics
            current_date = self.df['InvoiceDate'].max()
            
            rfm = self.df.groupby('Customer ID').agg({
                'InvoiceDate': lambda x: (current_date - x.max()).days,
                'Invoice': 'count',
                'TotalAmount': 'sum'
            }).rename(columns={
                'InvoiceDate': 'Recency',
                'Invoice': 'Frequency',
                'TotalAmount': 'Monetary'
            })
            
            # Log transform for better visualization
            rfm_log = np.log1p(rfm)
            
            fig = px.scatter_3d(rfm_log, 
                               x='Recency', 
                               y='Frequency', 
                               z='Monetary',
                               color='Monetary', 
                               size='Frequency',
                               title='3D Customer Segmentation based on RFM Analysis')
            
            fig.update_layout(
                scene = dict(
                    xaxis_title='Recency (log)',
                    yaxis_title='Frequency (log)',
                    zaxis_title='Monetary (log)'
                )
            )
            
            fig.show()
        except Exception as e:
            print(f"Error in plot_customer_segments: {str(e)}")

    def plot_product_analysis(self):
        """
        Create product-based analysis visualizations
        """
        try:
            # Top products by revenue
            top_products = self.df.groupby('Description')['TotalAmount'].sum()\
                .sort_values(ascending=True).tail(10)

            fig = go.Figure(go.Bar(
                x=top_products.values,
                y=top_products.index,
                orientation='h',
                marker=dict(
                    color=top_products.values,
                    colorscale='Viridis'
                )
            ))
            
            fig.update_layout(
                title='Top 10 Products by Revenue',
                xaxis_title='Total Revenue',
                yaxis_title='Product',
                height=600,
                margin=dict(l=200)  # Add left margin for long product names
            )
            
            fig.show()
        except Exception as e:
            print(f"Error in plot_product_analysis: {str(e)}")

    def plot_customer_geography(self):
        """
        Create geographical analysis of customers
        """
        try:
            country_sales = self.df.groupby('Country')['TotalAmount'].sum().reset_index()
            country_orders = self.df.groupby('Country')['Invoice'].nunique().reset_index()
            
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=('Total Sales by Country', 
                                             'Number of Orders by Country'),
                               specs=[[{"type": "bar"}, {"type": "bar"}]])
            
            # Sales by country
            fig.add_trace(
                go.Bar(x=country_sales.sort_values('TotalAmount', ascending=True).tail(10)['Country'],
                      y=country_sales.sort_values('TotalAmount', ascending=True).tail(10)['TotalAmount'],
                      name='Total Sales',
                      marker_color='#3498db'),
                row=1, col=1
            )
            
            # Orders by country
            fig.add_trace(
                go.Bar(x=country_orders.sort_values('Invoice', ascending=True).tail(10)['Country'],
                      y=country_orders.sort_values('Invoice', ascending=True).tail(10)['Invoice'],
                      name='Number of Orders',
                      marker_color='#e74c3c'),
                row=1, col=2
            )
            
            fig.update_layout(
                height=500, 
                showlegend=True,
                title_text="Geographical Analysis",
                title_x=0.5
            )
            
            fig.show()
        except Exception as e:
            print(f"Error in plot_customer_geography: {str(e)}")

    def plot_basket_analysis(self):
        """
        Create basket size analysis visualization
        """
        try:
            # Calculate basket sizes
            basket_sizes = self.df.groupby('Invoice')['Quantity'].sum()
            
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=('Basket Size Distribution', 
                                             'Average Basket Value by Hour'))
            
            # Basket size distribution
            fig.add_trace(
                go.Histogram(x=basket_sizes, 
                            name='Basket Size',
                            marker_color='#9b59b6',
                            nbinsx=50),  # Adjust number of bins
                row=1, col=1
            )
            
            # Average basket value by hour
            hourly_basket = self.df.groupby('Hour')['TotalAmount'].mean()
            
            fig.add_trace(
                go.Scatter(x=hourly_basket.index, 
                          y=hourly_basket.values,
                          mode='lines+markers', 
                          name='Avg Basket Value',
                          line=dict(color='#2ecc71', width=3)),
                row=1, col=2
            )
            
            fig.update_layout(
                height=500, 
                showlegend=False,
                title_text="Basket Analysis",
                title_x=0.5
            )
            
            fig.show()
        except Exception as e:
            print(f"Error in plot_basket_analysis: {str(e)}")

def main():
    try:
        # Load the processed dataset
        df = pd.read_csv('uk_retail_processed.csv')
        
        # Create visualization object
        viz = CustomerVisualizationAnalysis(df)
        
        # Generate all visualizations
        print("Generating sales trends visualization...")
        viz.plot_sales_trends()
        
        print("Generating hourly heatmap...")
        viz.create_hourly_heatmap()
        
        print("Generating customer segmentation visualization...")
        viz.plot_customer_segments()
        
        print("Generating product analysis...")
        viz.plot_product_analysis()
        
        print("Generating geographical analysis...")
        viz.plot_customer_geography()
        
        print("Generating basket analysis...")
        viz.plot_basket_analysis()
        
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()