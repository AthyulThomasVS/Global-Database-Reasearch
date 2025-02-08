import json
import tkinter as tk
from tkinter import ttk, Canvas, Scrollbar, Toplevel, Button, messagebox
import requests
from datachart import datachart
from comparative_analysis import comparative_analysis


class JsonViewer:
    def __init__(self, master, urls):
        self.master = master
        self.master.title("JSON Viewer")
        self.master.geometry("1000x500")

        # Fetch JSON data from both sources
        self.data = self.fetch_json_data(urls)

        # Create Treeview
        self.tree = ttk.Treeview(master, columns=("Source", "ID", "Description", "More Info", "Statistical Report","similar vulnerabilities"), show='headings')
        self.tree.heading("Source", text="Source")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("More Info", text="More Info")
        self.tree.heading("Statistical Report", text="Statistical Report")
        self.tree.heading("similar vulnerabilities", text="similar vulnerabilities")

        # Adjust column widths
        self.tree.column("Source", width=100, anchor="center")
        self.tree.column("ID", width=120, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("More Info", width=120, anchor="center")
        self.tree.column("Statistical Report", width=150, anchor="center")
        self.tree.column("similar vulnerabilities", width=150, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert data into Treeview
        for idx, item in enumerate(self.data):
            source = item.get("db", "Unknown")
            item_id = item.get("id", item.get("identifier", "N/A"))
            description = item.get("description", item.get("title", "No description"))
            self.tree.insert("", "end", iid=idx, values=(source, item_id, description, "🔍 View More", "📊 Report","similar vulnerabilities"))

        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def fetch_json_data(self, urls):
        """ Fetch JSON data from both JVN and USNVD sources """
        combined_data = []
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                combined_data.extend(response.json())
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to load data from {url}: {e}")
        return combined_data

    def on_item_double_click(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        col = self.tree.identify_column(event.x)
        item_index = int(selected_item)
        item_data = self.data[item_index]

        if col == "#4":
            self.show_more_info_table(item_data)
        elif col == "#5":
            self.show_statistical_report(item_data)
        elif col == "#6":
            self.comparative_analysis_fun(item_data)


    def show_more_info_table(self, item_data):
        """ Display detailed information """
        info_window = Toplevel(self.master)
        info_window.title("More Info")
        info_window.geometry("700x500")

        frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(frame, text="Detailed Information", font=("Arial", 14, "bold"), fg="black", bg="white")
        title_label.pack(pady=10)

        for key, value in item_data.items():
            row_frame = tk.Frame(frame, bg="white")
            row_frame.pack(fill=tk.X, pady=2)

            tk.Label(row_frame, text=key.capitalize(), font=("Arial", 11, "bold"), width=20, anchor="w", bg="white").pack(side=tk.LEFT, padx=10)
            tk.Label(row_frame, text=str(value), font=("Arial", 11), anchor="w", bg="white").pack(side=tk.LEFT)

    def show_statistical_report(self,item_data):
        datachart(item_data)
         
    def comparative_analysis_fun(self,item_data):
        value =comparative_analysis(item_data)
        info_window = Toplevel(self.master)
        info_window.title("More Info")
        info_window.geometry("700x500")

        frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(frame, text="Detailed Information", font=("Arial", 14, "bold"), fg="black", bg="white")
        title_label.pack(pady=10)
        row_frame = tk.Frame(frame, bg="white")
        row_frame.pack(fill=tk.X, pady=2)
        tk.Label(row_frame, text="Matched Vulnerability", font=("Arial", 11, "bold"), width=20, anchor="w", bg="white").pack(side=tk.LEFT, padx=10)
        if value == None:
            tk.Label(row_frame, text="Match Not Found", font=("Arial", 11), anchor="w", bg="white").pack(side=tk.LEFT)
        else:
            tk.Label(row_frame, text=str(value), font=("Arial", 11), anchor="w", bg="white").pack(side=tk.LEFT)
                
if __name__ == "__main__":
    root = tk.Tk()
    

    urls = [
        'http://127.0.0.1:5000/api/jvndata',  # JVN Data
        'http://127.0.0.1:5000/api/usdata'  # USNVD Data
    ]
    
    app = JsonViewer(root, urls)
    root.mainloop()
