FinSight AI - Intelligent Personal Finance Tracker
FinSight AI is a modern, full-stack web application designed to bring clarity to personal finance management. It goes beyond simple expense tracking by leveraging a smart, adaptive AI engine to automatically categorize transactions, providing users with powerful insights into their spending habits through interactive visualizations, budgeting tools, and predictive forecasting.

Live Demo: https://finsight-ai-web.onrender.com

✨ Key Features
This project is a comprehensive showcase of modern web development and data analysis techniques, featuring:

Secure User Authentication: A sleek and secure system for user registration, login, and session management with a modern glassmorphism UI.

Full CRUD Functionality: Users have complete control over their financial data with the ability to Create, Read, Update, and Delete transactions.

AI-Powered Categorization: A smart suggestion engine that automatically categorizes transactions based on their description, significantly speeding up data entry.

Personalized "Smart Rules" Engine: Users can train the AI by linking their own custom keywords to categories (e.g., "dps fee" -> "Education"), making the system adapt to their unique life.

Interactive Dashboard: A dynamic dashboard featuring:

A doughnut chart visualizing spending breakdowns by category.

Color-coded progress bars to track monthly spending against user-defined budgets.

A predictive forecast of total spending for the next 30 days.

Monthly Budgeting: An intuitive interface for users to set and manage monthly spending goals for each category.

Data Export: Functionality to download all transaction data as a universal .csv file for use in other applications like Excel or Google Sheets.

Responsive Design: A clean and user-friendly interface that works seamlessly on both desktop and mobile devices.

🛠️ Technology Stack
This project was built using a robust and scalable tech stack:

Backend: Python, Django, Gunicorn

Frontend: HTML5, CSS3, JavaScript (ES6)

Database: PostgreSQL

Data Analysis & ML: Pandas, Statsmodels

Visualization: Chart.js

Deployment: Render, Whitenoise

🚀 Local Setup and Installation
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

☁️ Deployment
This application is configured for seamless deployment on Render using a render.yaml blueprint file. The deployment process includes:

Provisioning a free-tier PostgreSQL database.

Installing all dependencies.

Collecting static files using WhiteNoise.

Running database migrations.

Starting the application with the Gunicorn production server.

To deploy, simply create a new "Blueprint" service on Render and connect it to your GitHub repository.

🔮 Future Enhancements
CSV Transaction Upload: Allow users to upload bank statements in CSV format for bulk transaction import.

True Machine Learning Model: Replace the rule-based system with a trainable model (e.g., using Scikit-learn's Naive Bayes classifier) that learns from a user's manual categorizations over time.

Multi-Month Analysis: Add date filters and reporting pages to compare spending across different months or years.

