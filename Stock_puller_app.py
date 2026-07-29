import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdvancedStockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Stock Puller Dashboard")
        self.root.geometry("800x600")
        
        # Internal simple watchlist storage
        self.watchlist = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        # Left Column Panel: Controls & Watchlist
        self.left_panel = tk.Frame(root, width=250, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Right Column Panel: Live Interactive Chart
        self.right_panel = tk.Frame(root, bg="white")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add visual components to our user window
        self.create_interface_widgets()
        self.update_watchlist_display()

    def create_interface_widgets(self):
        # Input field header
        tk.Label(self.left_panel, text="Search Stock Ticker:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(10, 2))
        
        # Text input entry box
        self.entry_ticker = tk.Entry(self.left_panel, font=("Arial", 12))
        self.entry_ticker.pack(fill=tk.X, pady=5)
        
        # Action Buttons
        tk.Button(self.left_panel, text="📉 Pull 30-Day History Chart", command=self.plot_stock_history, bg="#007acc", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=5)
        tk.Button(self.left_panel, text="➕ Add to Watchlist", command=self.add_to_watchlist, bg="#28a745", fg="white").pack(fill=tk.X, pady=2)

        # Watchlist Visual ListBox Container
        tk.Label(self.left_panel, text="My Watchlist:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 2))
        self.listbox_watchlist = tk.Listbox(self.left_panel, font=("Arial", 11))
        self.listbox_watchlist.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Double clicking an item in your list triggers chart loading automatically
        self.listbox_watchlist.bind("<Double-1>", lambda event: self.load_selected_watchlist_item())

    def update_watchlist_display(self):
        """Clears list frame box and recalculates names + current real prices."""
        self.listbox_watchlist.delete(0, tk.END)
        for ticker in self.watchlist:
            try:
                ticker_data = yf.Ticker(ticker)
                live_price = ticker_data.fast_info['last_price']
                self.listbox_watchlist.insert(tk.END, f"{ticker} - ${live_price:.2f}")
            except:
                self.listbox_watchlist.insert(tk.END, f"{ticker} - (Offline)")

    def add_to_watchlist(self):
        new_ticker = self.entry_ticker.get().strip().upper()
        if new_ticker and new_ticker not in self.watchlist:
            self.watchlist.append(new_ticker)
            self.update_watchlist_display()
            self.entry_ticker.delete(0, tk.END)
        elif not new_ticker:
            messagebox.showwarning("Warning", "Please type a ticker symbol first!")

    def load_selected_watchlist_item(self):
        selected_text = self.listbox_watchlist.get(tk.ACTIVE)
        if selected_text:
            extracted_ticker = selected_text.split(" - ")[0]
            self.entry_ticker.delete(0, tk.END)
            self.entry_ticker.insert(0, extracted_ticker)
            self.plot_stock_history()

    def plot_stock_history(self):
        ticker_name = self.entry_ticker.get().strip().upper()
        if not ticker_name:
            messagebox.showerror("Error", "Please enter a valid stock ticker symbol.")
            return

        try:
            # Wipe previous charts from display panel
            for widget in self.right_panel.winfo_children():
                widget.destroy()

            # Pull historical stock data structure
            stock = yf.Ticker(ticker_name)
            history_dataframe = stock.history(period="30d") # Targets trailing 30 calendar days

            if history_dataframe.empty:
                raise ValueError("No historical information found.")

            # Create standard trend chart canvas figure using Matplotlib
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.plot(history_dataframe.index, history_dataframe['Close'], label="Closing Price", color="#007acc", linewidth=2)
            
            ax.set_title(f"{ticker_name} - 30 Day Price Trend", fontsize=12, fontweight='bold')
            ax.set_xlabel("Timeline Dates")
            ax.set_ylabel("Price (USD / Local Currency)")
            ax.grid(True, linestyle="--", alpha=0.5)
            fig.autofmt_xdate() # Rotates diagonal dates nicely

            # Embed our external graph window smoothly right inside the Tkinter application
            canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as err:
            messagebox.showerror("Data Fetch Failure", f"Could not draw data for {ticker_name}.\nCheck typing.")

# Execute window loop 
if __name__ == "__main__":
    app_window = tk.Tk()
    run_program = AdvancedStockApp(app_window)
    app_window.mainloop()
