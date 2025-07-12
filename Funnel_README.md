# Funnel Drop-Off Dashboard

This interactive dashboard visualizes the drop-off rates across key stages of a user funnel. It is designed to help product and marketing teams identify where users disengage and explore engagement trends by device and acquisition channel.

## 📊 Features
- KPI banner showing total users, total engaged, and engagement CTR
- Funnel bar chart with user counts at each funnel stage
- Drop-off table with stage-to-stage attrition
- CTR heatmap segmented by device type and acquisition channel
- Filters: Device Type, Channel, Signup Date Range

## 📁 Dataset
Simulated dataset includes:
- `user_id`
- `signup_date`
- `device_type`: Mobile, Desktop, Tablet
- `channel`: Organic, Paid, Referral
- `step_1_landing` to `step_5_engaged_return`: Binary funnel steps

## 🚀 How to Run
```bash
pip install -r requirements.txt
python funnel_dropoff_app.py
```
Visit `http://127.0.0.1:8050` in your browser.

## 📂 Files
- `funnel_dropoff_app.py`: Main Dash app
- `funnel_dropoff_dataset.csv`: Funnel user simulation data
- `requirements.txt`: Package dependencies

## 📌 Screenshot Suggestions
* Add screenshots of the funnel chart, heatmap, and KPI banner here once captured and saved in a /screenshots folder *

## 🎯 Business Insight
This dashboard allows stakeholders to quickly diagnose funnel bottlenecks and compare engagement by segment. It is ideal for marketing, growth, and UX optimization strategies.
