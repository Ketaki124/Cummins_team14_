# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import mysql.connector

# Database connection
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='currency_rates'
)

query = 'select * from exchange_rates;'
data = pd.read_sql(query, db_connection)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

def plot_target_graph(selected_currency,target_currency ,selected_year, selected_interval, second_page):
    if not selected_currency or not selected_year or not selected_interval:
        result_label.config(text="Please select currency and year.")
        return

    try:
        filtered_data = data[data['Date'].dt.year == int(selected_year)]
        if selected_currency not in filtered_data.columns:
            result_label.config(text=f"Currency '{selected_currency}' not found in the dataset.")
            return

        filtered_data.set_index('Date', inplace=True)
        if selected_interval == 'Weekly':
            resampled_data = filtered_data[selected_currency].resample('W').mean()
        elif selected_interval == 'Monthly':
            resampled_data = filtered_data[selected_currency].resample('M').mean()
        elif selected_interval == 'Quarterly':
            resampled_data = filtered_data[selected_currency].resample('Q').mean()

        # standard deviation for the risk factor
        std_dev = np.std(resampled_data)
        
        risk_threshold = 0.05
        if std_dev > risk_threshold:
            color = 'red'  # High risk
            risk_level = "High Risk"
            volatility_text = "High Volatility"
        else:
            color = 'green'  # Low risk
            risk_level = "Low Risk"
            volatility_text = "Low Volatility"

        # Create a Matplotlib figure
        plt.figure(figsize=(10, 6))
        plt.plot(resampled_data.index, resampled_data, label=f'{selected_currency} Exchange Rate', color=color)
        plt.xlabel('Date')
        plt.ylabel(f'Exchange Rate ({selected_currency}/{target_currency})')
        plt.title(f'{selected_currency} Exchange Rate vs {target_currency} in {selected_year} ({risk_level})')
        plt.grid(True)
        plt.legend()

        # Add volatility text on the plot
        plt.text(x=0.5, y=0.95, s=volatility_text, fontsize=12, ha='center', transform=plt.gca().transAxes,
                 color=color, bbox=dict(facecolor='white', alpha=0.5, edgecolor=color, boxstyle='round,pad=0.3'))

        for widget in plot_frame.winfo_children():
            widget.destroy()  # Clear previous plots

        canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_frame)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0) 

        # Find peak and lowest values
        peak_value = resampled_data.max()
        lowest_value = resampled_data.min()
        peak_date = resampled_data.idxmax()
        lowest_date = resampled_data.idxmin()

        # Display peak, lowest rates, and risk level on the screen
        peak_info = f"Peak Rate: {peak_value:.2f} on {peak_date.date()}"
        lowest_info = f"Lowest Rate: {lowest_value:.2f} on {lowest_date.date()}"
        result_label.config(text=f"{peak_info}\n{lowest_info}\nVolatility: {std_dev:.2f} ({risk_level})")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def plot_custom_basket():
    selected_currencies = [currency_combobox1.get(), currency_combobox2.get(), currency_combobox3.get()]
    weights = [float(weight_entry1.get()), float(weight_entry2.get()), float(weight_entry3.get())]
    base_currency = base_currency_combobox.get()
    selected_year = year_combobox_basket.get()

    # Check if all inputs are selected and valid
    if not all(selected_currencies) or not selected_year or not base_currency:
        result_label_basket.config(text="Please select currencies, weights, base currency, and year.")
        return

    try:
        filtered_data = data[data['Date'].dt.year == int(selected_year)]
        
        for currency in selected_currencies + [base_currency]:
            if currency not in filtered_data.columns:
                result_label_basket.config(text=f"Currency '{currency}' not found in the dataset.")
                return

        # Set index to Date for easy resampling
        filtered_data.set_index('Date', inplace=True)

        # Calculate weighted sum for the basket
        basket_value = sum(filtered_data[curr] * weight for curr, weight in zip(selected_currencies, weights))
        basket_value_in_base = basket_value / filtered_data[base_currency]

        basket_value_resampled = basket_value_in_base.resample('W').mean()
        plt.figure(figsize=(10, 6))
        plt.plot(basket_value_resampled.index, basket_value_resampled, label='Basket Value in Base Currency', color='purple')
        plt.xlabel('Date')
        plt.ylabel(f'Basket Value in {base_currency}')
        plt.title(f'Custom Currency Basket Value in {base_currency} ({selected_year})')
        plt.grid(True)
        plt.legend()

        for widget in plot_frame_basket.winfo_children():
            widget.destroy()  # Clear previous plots

        canvas_basket = FigureCanvasTkAgg(plt.gcf(), master=plot_frame_basket)
        canvas_basket.draw()
        canvas_basket.get_tk_widget().grid(row=0, column=0)  

        result_label_basket.config(text=f"Custom basket plotted successfully.")

    except Exception as e:
        result_label_basket.config(text=f"Error: {str(e)}")

def switch_to_custom_basket():
    notebook.select(third_page)

# Initialize the main application window
root = tk.Tk()
root.title("Currency Exchange Rate Viewer")
width = root.winfo_screenwidth()
height2 = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height2))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the notebook (tabs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=1, sticky="nsew")

# Left frame for user inputs
left_frame = tk.Frame(root, width=300, height=height2, bg="#7FA1C3")
left_frame.grid(row=0, column=0, sticky="ns")
left_frame.grid_propagate(False)

# Currency selection
tk.Label(left_frame, text="Select Currency:").grid(row=0, column=0, padx=10, pady=10)
currency_combobox = ttk.Combobox(left_frame)
currency_combobox['values'] = [col for col in data.columns if col != 'Date']
currency_combobox.grid(row=0, column=1, padx=10, pady=10)

tk.Label(left_frame, text="Select base Currency:").grid(row=1, column=0, padx=10, pady=10)
currency_combobox2 = ttk.Combobox(left_frame)
currency_combobox2['values'] = [col for col in data.columns if col != 'Date']
currency_combobox2.grid(row=1, column=1, padx=10, pady=10)

# Year selection
tk.Label(left_frame, text="Select Year:").grid(row=2, column=0, padx=10, pady=10)
year_combobox = ttk.Combobox(left_frame)
year_combobox['values'] = data['Date'].dt.year.unique()
year_combobox.grid(row=2, column=1, padx=10, pady=10)

tk.Button(left_frame, text="Plot Weekly Data", command=lambda: plot_target_graph(currency_combobox.get(), currency_combobox2.get(),year_combobox.get(), "Weekly", None)).grid(row=3, column=0, columnspan=2, padx=10, pady=5)
tk.Button(left_frame, text="Plot Monthly Data", command=lambda: plot_target_graph(currency_combobox.get(),currency_combobox2.get(), year_combobox.get(), "Monthly", None)).grid(row=4, column=0, columnspan=2, padx=10, pady=5)
tk.Button(left_frame, text="Plot Quarterly Data", command=lambda: plot_target_graph(currency_combobox.get(), currency_combobox2.get(),year_combobox.get(), "Quarterly", None)).grid(row=5, column=0, columnspan=2, padx=10, pady=5)
# Second page for plots
second_page = ttk.Frame(notebook)
notebook.add(second_page, text="Currency Data")

plot_frame = tk.Frame(second_page)
plot_frame.grid(row=0, column=0, sticky="nsew")

result_label = tk.Label(second_page, text="")
result_label.grid(row=1, column=0, padx=10, pady=10)

# Third page for custom currency basket
third_page = ttk.Frame(notebook)
notebook.add(third_page, text="Custom Currency Basket")

# Inputs for custom basket
tk.Label(third_page, text="Currency 1:").grid(row=0, column=0, padx=10, pady=10)
currency_combobox1 = ttk.Combobox(third_page)
currency_combobox1['values'] = [col for col in data.columns if col != 'Date']
currency_combobox1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(third_page, text="Currency 2:").grid(row=1, column=0, padx=10, pady=10)
currency_combobox2 = ttk.Combobox(third_page)
currency_combobox2['values'] = [col for col in data.columns if col != 'Date']
currency_combobox2.grid(row=1, column=1, padx=10, pady=10)

tk.Label(third_page, text="Currency 3:").grid(row=2, column=0, padx=10, pady=10)
currency_combobox3 = ttk.Combobox(third_page)
currency_combobox3['values'] = [col for col in data.columns if col != 'Date']
currency_combobox3.grid(row=2, column=1, padx=10, pady=10)

tk.Label(third_page, text="Weight 1:").grid(row=0, column=2, padx=10, pady=10)
weight_entry1 = tk.Entry(third_page)
weight_entry1.grid(row=0, column=3, padx=10, pady=10)

tk.Label(third_page, text="Weight 2:").grid(row=1, column=2, padx=10, pady=10)
weight_entry2 = tk.Entry(third_page)
weight_entry2.grid(row=1, column=3, padx=10, pady=10)

tk.Label(third_page, text="Weight 3:").grid(row=2, column=2, padx=10, pady=10)
weight_entry3 = tk.Entry(third_page)
weight_entry3.grid(row=2, column=3, padx=10, pady=10)

tk.Label(third_page, text="Select Base Currency:").grid(row=3, column=0, padx=10, pady=10)
base_currency_combobox = ttk.Combobox(third_page)
base_currency_combobox['values'] = [col for col in data.columns if col != 'Date']
base_currency_combobox.grid(row=3, column=1, padx=10, pady=10)

tk.Label(third_page, text="Select Year:").grid(row=4, column=0, padx=10, pady=10)
year_combobox_basket = ttk.Combobox(third_page)
year_combobox_basket['values'] = data['Date'].dt.year.unique()
year_combobox_basket.grid(row=4, column=1, padx=10, pady=10)

# Plot custom basket button
tk.Button(third_page, text="Plot Custom Basket", command=plot_custom_basket).grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Frame to hold plot for custom basket
plot_frame_basket = tk.Frame(third_page)
plot_frame_basket.grid(row=6, column=0, columnspan=4, sticky="nsew")

result_label_basket = tk.Label(third_page, text="", wraplength=400)
result_label_basket.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
