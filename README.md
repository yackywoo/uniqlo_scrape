# Uniqlo Product Tracker

This project is a web application that tracks product availability, prices, and sale statuses from Uniqlo's online store. It scrapes data using the Uniqlo API, stores the information in a local SQLite database, and allows users to monitor changes over time. The app is built using Flask for the web framework and SQLAlchemy for database management.

## Features

- **Product Tracking**: Track Uniqlo products by their Product ID (PID) and view details such as price, availability, and sale status.
- **Sale Group Monitoring**: Detects and displays product variations, including different color groups and sizes.
- **Automatic Updates**: Automatically updates product information and highlights changes in price, stock, and sale status.
- **User-Friendly Interface**: View tracked products and their details through a simple web interface.

## Installation
1. **Clone the repository**: 
   `git clone https://github.com/your-username/uniqlo-product-tracker.git`
   `cd uniqlo-product-tracker`
2. **Create and activate a virtual environment**:
   `python -m venv venv`
   Activate virtual environment: 
      ```Linux 
      source venv/bin/activate
      
      ```Windows
      venv\Scripts\activate
3. **Install the required dependencies**:
   `pip install -r requirements.txt`
4. **Set up the database**: 
   The database is automatically created when you run the Flask app for the first time.
5. **Run the application**: 
   `python app.py`
6. **Access the web interface**:
   Open your web browser and goto `http://127.0.0.1:5000/` to start using the tracker.

Disclaimer : For educational purposes only
