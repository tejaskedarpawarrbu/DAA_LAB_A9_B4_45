import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_stock_data(symbol):
    """Fetch 1 year of historical stock data using yfinance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y")
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return pd.DataFrame()


def divide_and_conquer_analysis(data, interval="M"):
    """Divide data into intervals and compute stats."""
    grouped_data = data.groupby(pd.Grouper(freq=interval))
    results = []
    for name, group in grouped_data:
        if group.empty:
            continue
        analysis = {
            "Interval": name.strftime("%Y-%m"),
            "Open": round(group["Open"].iloc[0], 2),
            "Close": round(group["Close"].iloc[-1], 2),
            "High": round(group["High"].max(), 2),
            "Low": round(group["Low"].min(), 2),
            "Volatility": round(group["Close"].std(), 2),
        }
        results.append(analysis)
    return pd.DataFrame(results)


def plot_analysis(results, symbol):
    """Plot closing prices over time."""
    plt.figure(figsize=(10, 5))
    plt.plot(results["Interval"], results["Close"], marker='o', color='blue', label='Closing Price')
    plt.title(f"Stock Trend for {symbol}")
    plt.xlabel("Time Interval (Monthly)")
    plt.ylabel("Closing Price (INR)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def analyze_stock():
    """Main function triggered by the Analyze button."""
    symbol = symbol_entry.get().strip().upper()
    if not symbol:
        messagebox.showwarning("Input Required", "Please enter a stock symbol, e.g., RELIANCE.BO")
        return

    # Fetch and analyze data
    stock_data = fetch_stock_data(symbol)
    if stock_data.empty:
        messagebox.showerror("Error", "No data found for the given symbol.")
        return

    results = divide_and_conquer_analysis(stock_data)
    if results.empty:
        messagebox.showinfo("No Data", "Not enough data to analyze.")
        return

    # Clear old table
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data
    for _, row in results.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Show plot
    plot_analysis(results, symbol)


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Divide and Conquer Stock Analyzer")
root.geometry("750x550")
root.config(bg="#f0f4f7")

# Title label
tk.Label(root, text="📊  Stock Analyzer", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#003366").pack(pady=15)

# Input Frame
frame = tk.Frame(root, bg="#f0f4f7")
frame.pack(pady=10)

tk.Label(frame, text="Enter BSE Stock Symbol (e.g., RELIANCE.BO):", font=("Arial", 12), bg="#f0f4f7").grid(row=0, column=0, padx=5)
symbol_entry = tk.Entry(frame, width=25, font=("Arial", 12))
symbol_entry.grid(row=0, column=1, padx=5)

analyze_btn = tk.Button(frame, text="Analyze", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=analyze_stock)
analyze_btn.grid(row=0, column=2, padx=10)

# Results Table
cols = ("Interval", "Open", "Close", "High", "Low", "Volatility")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=110)
tree.pack(pady=10)

# Footer
tk.Label(root, text="", font=("Arial", 10, "italic"), bg="#f0f4f7", fg="#555").pack(pady=5)

root.mainloop()
