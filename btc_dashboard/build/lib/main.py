import streamlit as st
from streamlit_card import card
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import numpy as np
import streamlit_lightweight_charts.dataSamples as data



priceVolumeChartOptions = {
    "height": 400,
    "width": 700,
    "rightPriceScale": {
        "scaleMargins": {
            "top": 0.2,
            "bottom": 0.25,
        },
        "borderVisible": False,
    },
    "overlayPriceScales": {
        "scaleMargins": {
            "top": 0.7,
            "bottom": 0,
        }
    },
    "layout": {
        "background": {
            "type": 'solid',
            "color": '#131722'
        },
        "textColor": '#d1d4dc',
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(42, 46, 57, 0)',
        },
        "horzLines": {
            "color": 'rgba(42, 46, 57, 0.6)',
        }
    }
}

priceVolumeSeries = [
    {
        "type": 'Area',
        "data": data.priceVolumeSeriesArea,
        "options": {
            "topColor": 'rgba(38,198,218, 0.56)',
            "bottomColor": 'rgba(38,198,218, 0.04)',
            "lineColor": 'rgba(38,198,218, 1)',
            "lineWidth": 2,
        }
    },
]

style_config = {"card": {"width": "150px", "height": "150px", "padding": "15px", "border": "1px solid #ccc"}, "title": {"fontSize": "18px", "fontWeight": "bold"}, "text": {"fontSize": "16px"}}

def main():
    
    # utilize containers for layout control 
    
    # Title: 
    st.title("₿ Bitcoin Dashboard ₿", text_alignment="center")
    
    # Generate some fake data for the line chart
    # This will be replaced by real-time data from Kafka later
    
    # FAKE DATA FOR SHOW Generate by AI. #####################
    # Generate time series data
    num_points = 100
    start_time = pd.Timestamp.now() - pd.Timedelta(hours=num_points)
    times = [start_time + pd.Timedelta(hours=i) for i in range(num_points)]
    
    # Generate price data with some fluctuations
    base_price = 30000
    prices = [base_price + np.sin(i/10) * 1000 + np.random.randn() * 500 for i in range(num_points)]
    
    # Create a DataFrame for Streamlit's line_chart
    chart_data = pd.DataFrame({"time": times, "price": prices})
    
    with st.container(width=700):
        st.title("Bitcoin Price Tracker", text_alignment="center")
        with st.container():
            st.line_chart(chart_data, x="time", y="price", width="stretch", height=400)

    #####################################################################################3
        #renderLightweightCharts([
        #    {
        #        "chart": priceVolumeChartOptions,
        #        "series": priceVolumeSeries
        #    }
        #], 'Price Series Chart')
        

        
    # Need a styles config.
    
    with st.container(width=700):
        
        st.title("Bitcoin Key Metrics", text_alignment="center")


        with st.container(horizontal_alignment="center", gap="medium", horizontal=True):
            row1 = st.columns(5)
            index = 0
            metrics = ("Min Price", "Max Price", "Avg Price", "24h Volume", "Price Change")

            for col in row1:
                if metrics[index] is None:
                    continue
                tile = col.container(height=150, width=200, horizontal_alignment="center")
                tile.text(f"{metrics[index]}", text_alignment="center", width="content")
                tile.text("$15,000", text_alignment="center", width="content")
                index += 1
        #col1, col2, col3, col4 = st.columns(4, gap="small")

        #with col1:
        #    min_price = card(title="Minimum Price", text="$14,000", styles=style_config)
#
        #with col2:
        #    max_price = card(title="Maximum Price", text="$18,000", styles=style_config)
        #with col3:
        #    avg_price = card(title="Average Price", text="$16,000", styles=style_config) 
#
        #with col4: 
        #    volume = card(title="24h Volume", text="$2.5B", styles=style_config)
  
    print("Hello from the dashboard!")

if __name__ == "__main__":
    main()
