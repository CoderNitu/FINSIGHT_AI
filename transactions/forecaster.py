import pandas as pd
import statsmodels.api as sm
from django.utils import timezone
import warnings

# Ignore warnings from statsmodels for cleaner output
warnings.filterwarnings("ignore")

class SpendingForecaster:
        def __init__(self, transactions_queryset):
            """
            Initializes the forecaster with the user's transaction data.
            'transactions_queryset' should be a queryset of the user's Transaction objects.
            """
            # We only care about expenses for forecasting spending
            self.expenses = transactions_queryset.filter(transaction_type='expense').order_by('date')

        def _prepare_daily_data(self):
            """
            Transforms the raw transaction data into a daily spending time series using pandas.
            """
            if not self.expenses.exists():
                return None

            # Convert queryset to a pandas DataFrame
            df = pd.DataFrame(list(self.expenses.values('date', 'amount')))
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Resample the data into daily totals. 'D' means daily frequency.
            # .sum() adds up all expenses for a given day.
            # .fillna(0) fills in days with no spending with a 0 instead of NaN (Not a Number).
            daily_spending = df['amount'].resample('D').sum().fillna(0)
            
            return daily_spending

        def forecast_next_30_days(self):
            """
            Forecasts the total spending for the next 30 days.
            Returns a single number (the forecasted total) or None if not possible.
            """
            daily_data = self._prepare_daily_data()

            # --- Edge Case Handling ---
            # We need enough data to make a meaningful forecast.
            # If we have less than 30 days of data, a complex model is unreliable.
            if daily_data is None or len(daily_data) < 30:
                # Fallback to a simpler projection: calculate the average daily spending and multiply by 30.
                if daily_data is not None and len(daily_data) > 0:
                    avg_daily_spend = daily_data.mean()
                    return avg_daily_spend * 30
                return None # Not enough data to even calculate an average

            try:
                # --- The Time Series Model (SARIMA) ---
                # SARIMA is a powerful model for data with a seasonal component (e.g., weekly spending patterns).
                # We use some common default parameters. In a real data science project, these would be carefully tuned.
                # The (7) at the end tells the model to look for a weekly (7-day) pattern.
                model = sm.tsa.statespace.SARIMAX(daily_data,
                                                  order=(1, 1, 1),
                                                  seasonal_order=(1, 1, 0, 7),
                                                  enforce_stationarity=False,
                                                  enforce_invertibility=False)
                
                results = model.fit(disp=False)
                
                # --- Prediction ---
                # Get the forecast for the next 30 days
                forecast = results.get_forecast(steps=30)
                
                # The forecast can sometimes be negative for days with zero spending. We'll treat those as 0.
                predicted_spending = forecast.predicted_mean
                predicted_spending[predicted_spending < 0] = 0
                
                # Return the sum of the 30-day forecast
                return predicted_spending.sum()

            except Exception as e:
                # If the model fails for any reason, return None
                print(f"Forecasting error: {e}")
                return None
    
