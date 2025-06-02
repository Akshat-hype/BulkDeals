📊 Bulk Deals API
This Flask API provides filtered bulk deal data based on a minimum traded volume percentage of outstanding shares, along with optional high-frequency trade (HFT) filtering. It's useful for investors or analysts interested in significant market movements.

🚀 Features
Filter bulk deals within the last 30 days

Specify minimum volume as a percentage of outstanding shares

Detect and flag high-frequency trades (HFT)

Simple in-memory caching for performance (300s)

Easily extensible with CSV-based data input
📦 Requirements
Python 3.7+

Flask

Flask-Caching

pandas

Install dependencies:

bash
Copy
Edit
pip install flask
pip install pandas

▶️ Run the API
python app.py

It will start on: http://127.0.0.1:5000/bulk-deals

