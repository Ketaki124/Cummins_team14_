# XRate Analyzer

This project is an application that is GUI-based for displaying currency exchange rates, calculating risk based on volatility, and plotting custom currency baskets. The data is fetched from the MySQL database, the application uses Tkinter for the user interface and Matplotlib for graph plotting. Preprocessing includes filling missing values in the dataset.

## Features

- Data Preprocessing: The method fills missing exchange rate data using forward fill, backward fill, and linear interpolation, ensuring continuity in the time-series.
- Currency exchange rate visualization : Displays the weekly, monthly, or quarterly exchange rate of a chosen currency against a base currency.
- Risk Assessment: The application computes the volatility of a currency and flags it to be "High Risk" or "Low Risk" based on the standard deviation.
- Custom Basket of Currencies: Build a custom basket of currencies, assigning the weights, and then plot its value against a base currency.
- Peak and Low Identify: It features the highest and lowest exchange rates within the period considered.
- A dedicated tab for displaying key terminologies such as "risk factor", "volatility","Appreciation" and "Depreciation" providing users with a better understanding of important financial concepts.
- Users can save the generated exchange rate graphs directly to their system for future reference, allowing them to keep track of trends and analyses over time.

## Requisites 
- Ensure you have the following dependencies installed:
Python 3.x
- pandas (for data manipulation)
- mysql-connector-python (for MySQL database connectivity)
- matplotlib (for plotting graphs)
- tkinter (for GUI development)
- numpy (for math operations)

## Deployment

To deploy this project run
- Clone the repository - 
git clone [https://github.com/Ketaki124/Cummins_team14_XRate-Analyzer.git]
- Install the required dependencies
pip install pandas mysql-connector-python matplotlib numpy
- Set up the MySQL database as ->
[Setup document link](https://docs.google.com/document/d/16WgipFAB8WUTriX2_8TnmiCFMasgfEgfPfu1kADcSRI/edit?usp=sharing)
- Open the project folder and run the main.py file:
python main.py

## Usage/Examples

- Select Currency: Choose the currency you want to visualize from the dropdown.
- Select Base Currency: Choose the base currency to compare against.
- Select Year: Choose the year for which you want to visualize the exchange rates.
- Plot Data: Click on "Plot Weekly Data", "Plot Monthly Data", or "Plot Quarterly Data" to visualize the exchange rates.
- Custom Currency Basket: In the "Custom Currency Basket" tab, you can select up to three currencies, assign weights, and plot the basket value against a base currency.
- Risk Level: The app automatically calculates the volatility and indicates if the currency is "High Risk" or "Low Risk".

## Future Improvements

- Add more currencies to the database and allow dynamic import of new currency data.
- Introduce more complex risk assessments based on additional financial indicators.
- Improve UI and make it more responsive.
- Implement predictive models (like ARIMA, LSTM) to forecast future exchange rates.
  
