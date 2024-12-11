import tkinter as tk
import requests
from tkinter import messagebox
import warnings

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def search_keyword():
    keyword = keyword_entry.get()
    results.delete(1.0, tk.END)  # Clear previous results

    urls = urls_text.get("1.0", tk.END).strip().splitlines()  # Get all URLs from the text area

    if not urls or all(url.strip() == "" for url in urls):
        messagebox.showwarning("Warning", "Please enter at least one URL.")
        return

    for url in urls:
        url = url.strip()  # Remove any whitespace or newline characters
        if url:  # Proceed only if the line is not empty
            results.insert(tk.END, f"Searching in: {url}\n")  # Debug output
            try:
                # First try HTTPS
                response = requests.get(url, verify=False, timeout=20)
                response.raise_for_status()  # Raise an error for bad responses
                content = response.text

                if keyword in content:
                    results.insert(tk.END, f'Keyword "{keyword}" found in: {url}\n', 'found')
                else:
                    results.insert(tk.END, f'Keyword "{keyword}" not found in: {url}\n', 'not_found')

            except requests.exceptions.Timeout:
                # If HTTPS fails due to a timeout, try HTTP
                http_url = url.replace("https://", "http://", 1)
                try:
                    response = requests.get(http_url, verify=False, timeout=20)
                    response.raise_for_status()
                    content = response.text

                    if keyword in content:
                        results.insert(tk.END, f'Keyword "{keyword}" found in: {http_url}\n', 'found')
                    else:
                        results.insert(tk.END, f'Keyword "{keyword}" not found in: {http_url}\n', 'not_found')
                except requests.exceptions.RequestException as e:
                    results.insert(tk.END, f'Error with {http_url}: {e}\n')

            except requests.exceptions.RequestException as e:
                results.insert(tk.END, f'Error with {url}: {e}\n')

# Setting up the main window
root = tk.Tk()
root.title("Keyword Search in URLs")

# Keyword Entry
tk.Label(root, text="Enter Keyword to Search:").pack(pady=5)
keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack(pady=5)

# Text area for URLs input
tk.Label(root, text="Enter URLs (one per line):").pack(pady=5)
urls_text = tk.Text(root, width=70, height=10)
urls_text.pack(pady=5)

# Search Button
search_button = tk.Button(root, text="Search", command=search_keyword)
search_button.pack(pady=20)

# Results Text Area
results = tk.Text(root, width=70, height=15)
results.pack(pady=5)

# Configuring tags for colored output
results.tag_configure('found', foreground='blue')    # Color for found keywords
results.tag_configure('not_found', foreground='red')  # Color for not found keywords

# Run the Tkinter event loop
root.mainloop()
