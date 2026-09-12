## FinSight — Personal Finance Tracker with Automated Categorisation and Forecasting

FinSight is a deployed Django web application for recording income and expenses, organising transactions, monitoring monthly budgets, and exploring spending patterns through interactive visualisations.

It combines personalised rule-based transaction categorisation with a statistical spending forecast, showing how backend development and data analysis can work together in a practical product.

Live Demo: https://finsight-ai-web.onrender.com

* The application is hosted on Render and may take several seconds to wake after a period of inactivity.

## Business problem

Manually categorising transactions and comparing expenses against multiple budgets can become repetitive. FinSight provides one place to:

- Record and organise financial transactions
- Automatically suggest categories from transaction descriptions
- Create personal categorisation rules
- Track spending against category budgets
- Visualise where money is being spent
- Export transaction records for further analysis
- Estimate upcoming spending from historical activity

## ✨ Key Features

- Secure user registration, login, logout, and session management
- Create, view, update, and delete income and expense transactions
- Default keyword-based category suggestions
- Personal smart rules that map the user's own keywords to categories
- Monthly category budgets and progress indicators
- Category-level spending visualisation using Chart.js
- CSV export for Excel, Google Sheets, or other analysis tools
- Thirty-day spending forecast
- Responsive interface for desktop and mobile screens
- PostgreSQL-backed deployment on Render

## How automated categorisation works

FinSight uses an explainable rule-based categoriser rather than claiming that keyword matching is a machine-learning model.

The categoriser checks:

1. The user's personalised keyword rules
2. A fallback dictionary of common transaction descriptions
3. The user's available categories

For example, a user can map dps fee to Education, and later transactions containing that phrase can receive the corresponding category suggestion.

## Forecasting approach

Expense transactions are aggregated into a daily time series with pandas. When at least 30 days of data are available, the application fits a SARIMA model with weekly seasonality and estimates total spending for the next 30 days.

When the history is shorter, the application uses an average-daily-spending projection. The forecast is an experimental planning aid and should not be treated as financial advice or a guaranteed prediction
## 🛠️ Technology Stack
This project was built using a robust and scalable tech stack:

Backend: Python, Django, Gunicorn

Frontend: HTML5, CSS3, JavaScript (ES6)

Database: PostgreSQL

Data processing: Pandas

Forecasting: statsmodels, SARIMA

Visualization: Chart.js

Deployment: Render, Whitenoise

## Project structure

```

FINSIGHT_AI/
├── core/                  # Shared views and application routes
├── transactions/          # Transactions, budgets, rules and forecasting
├── finsight_project/      # Django configuration
├── templates/             # Server-rendered user interface
├── static/                # CSS and JavaScript assets
├── render.yaml            # Render deployment blueprint
├── requirements.txt
└── manage.py

```

## 🚀 Local Setup and Installation
To run this project on your local machine, follow these steps:

Clone the Repository:

git clone [https://github.com/](https://github.com/)[YourUsername]/finsight-ai.git
cd finsight-ai

Create and Activate a Virtual Environment:

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Set Up Environment Variables:
Create a file named .env in the project root directory. This file will hold your secret key. Do not commit this file to Git.

# .env file
SECRET_KEY='your-super-secret-django-key-here'
DEBUG=True

You can generate a new secret key using an online tool or a simple Python script.

Run Database Migrations:
This will set up your local db.sqlite3 database with all the necessary tables.

python manage.py migrate

Create a Superuser:
This will allow you to access the Django admin panel.

python manage.py createsuperuser

Run the Development Server:

python manage.py runserver

The application will be available at http://127.0.0.1:8000/.

## ☁️ Deployment
This application is configured for seamless deployment on Render using a render.yaml blueprint file. The deployment process includes:

Provisioning a free-tier PostgreSQL database.

Installing all dependencies.

Collecting static files using WhiteNoise.

Running database migrations.

Starting the application with the Gunicorn production server.

To deploy, simply create a new "Blueprint" service on Render and connect it to your GitHub repository.

## 🔮 Current limitations

- Categorisation is rule-based and does not learn a statistical model from user corrections.
- The SARIMA configuration uses predefined parameters rather than per-user model selection and validation.
- Automated test coverage should be expanded before production use.
- Uploaded bank-statement import is not currently included.

## Future improvements

- Bulk CSV bank-statement import
- Date-range and year-over-year reporting
- Categorisation model trained from user corrections
- Forecast evaluation and confidence intervals
- Expanded automated tests

## Author

Developed by CoderNitu.

