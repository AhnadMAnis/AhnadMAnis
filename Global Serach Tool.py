import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import webbrowser
import socket
from googlesearch import search
import random

# دالة التحقق من اتصال الإنترنت
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# دالة البحث عن الصور باستخدام Unsplash API
def search_images(query, limit=10):
    access_key = 'G6BMWbZbXQ8cY-0kfod05Y3jZk-RSykylgK2d3RRZV0'  # ضع هنا مفتاح API الخاص بك
    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&per_page={limit}&client_id={access_key}"

    try:
        response = requests.get(url)
        data = response.json()
        return [photo['urls']['regular'] for photo in data['results']]
    except Exception as e:
        print(f"Error: {e}")
        return []

# دالة البحث عن الأخبار باستخدام NewsAPI
def search_news(query, limit=10):
    api_key = 'a77d7c08d6454f01a2c86744144b50e8'  # ضع هنا مفتاح API الخاص بك
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={limit}&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        return [article['title'] for article in data['articles']]
    except Exception as e:
        print(f"Error: {e}")
        return []

def perform_search():
    query = search_entry.get()
    limit = limit_entry.get() or "10"  # لو المستخدم لم يدخل حد للبحث، يكون 10
    search_type = type_combobox.get()

    if not query:
        messagebox.showerror("Error", "Please enter a search query!")
        return

    if not limit.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for search limit!")
        return

    result_list.delete(0, tk.END)

    if not check_internet():
        messagebox.showerror("Error", "No internet connection!")
        return

    try:
        if search_type == "All":
            results = list(search(query, stop=int(limit)))[:int(limit)]
        elif search_type == "Images":
            results = search_images(query, int(limit))
        elif search_type == "Videos":
            results = list(search(query + " site:youtube.com", stop=int(limit)))[:int(limit)]
        elif search_type == "News":
            results = search_news(query, int(limit))

        if not results:
            messagebox.showinfo("No Results", "No search results found!")
            return

        for idx, result in enumerate(results, start=1):
            result_list.insert(tk.END, f"{idx}. {result}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_link(event):
    try:
        selected_index = result_list.curselection()[0]
        link = result_list.get(selected_index).split(" ", 1)[1]
        webbrowser.open(link)
    except IndexError:
        pass

def copy_link(event):
    try:
        selected_index = result_list.curselection()[0]
        link = result_list.get(selected_index).split(" ", 1)[1]
        root.clipboard_clear()
        root.clipboard_append(link)
        messagebox.showinfo("Copied", "Link copied to clipboard!")
    except IndexError:
        pass

root = tk.Tk()
root.title("Global Search Tool 🌍")
root.geometry("600x500")
root.configure(bg="#1c1c1c")

# العنوان الرئيسي
title_label = tk.Label(root, text="🔎 Global Search Tool", font=("Helvetica", 18, "bold"), bg="#272727", fg="#ffffff", pady=10)
title_label.pack(fill=tk.X)

# إطار المدخلات
frame = tk.Frame(root, bg="#1c1c1c")
frame.pack(pady=20)

query_label = tk.Label(frame, text="🔍 Search Query:", bg="#1c1c1c", fg="#e6e6e6", font=("Arial", 12, "bold"))
query_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
search_entry = tk.Entry(frame, width=40, font=("Arial", 12), fg="#000000", bg="#e6e6e6")
search_entry.grid(row=0, column=1, padx=5, pady=5)

limit_label = tk.Label(frame, text="📝 Result Limit:", bg="#1c1c1c", fg="#e6e6e6", font=("Arial", 12, "bold"))
limit_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
limit_entry = tk.Entry(frame, width=10, font=("Arial", 12), fg="#000000", bg="#e6e6e6")
limit_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

type_label = tk.Label(frame, text="🔎 Search Type:", bg="#1c1c1c", fg="#e6e6e6", font=("Arial", 12, "bold"))
type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

type_combobox = ttk.Combobox(frame, values=["All", "Images", "Videos", "News"], width=15, font=("Arial", 12), state="readonly")
type_combobox.set("All")
type_combobox.grid(row=2, column=1, padx=5, pady=5)

search_button = tk.Button(root, text="Search 🔍", command=perform_search, font=("Arial", 12, "bold"), bg="#ff5722", fg="white", pady=5)
search_button.pack(pady=10)

result_frame = tk.Frame(root, bg="#1c1c1c")
result_frame.pack(pady=5)
result_list = tk.Listbox(result_frame, width=60, height=10, font=("Courier", 10), selectbackground="#ff5722", selectforeground="white", fg="#f8f9fa", bg="#333333")
result_list.pack(side="left", fill="y")

scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_list.yview, bg="#333333", troughcolor="#1c1c1c")
scrollbar.pack(side="right", fill="y")
result_list.config(yscrollcommand=scrollbar.set)

def on_button_hover(event):
    search_button.config(bg="#ff3d00")

def on_button_leave(event):
    search_button.config(bg="#ff5722")

search_button.bind("<Enter>", on_button_hover)
search_button.bind("<Leave>", on_button_leave)

result_list.bind("<Double-1>", open_link)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy Link", command=copy_link)

def show_context_menu(event):
    try:
        result_list.selection_clear(0, tk.END)
        result_list.select_set(result_list.nearest(event.y))
        context_menu.post(event.x_root, event.y_root)
    except IndexError:
        pass

result_list.bind("<Button-3>", show_context_menu)

# العلامة المائية
def change_watermark_color():
    colors = ["#ff5733", "#33ff57", "#3357ff", "#ff33aa", "#ff9933"]
    watermark_label.config(fg=random.choice(colors))
    root.after(1000, change_watermark_color)

def enlarge_watermark(event):
    watermark_label.config(font=("Arial", 12, "bold"))

def shrink_watermark(event):
    watermark_label.config(font=("Arial", 10, "bold"))

watermark_label = tk.Label(root, text="Ahmed Anis - Test Project", font=("Arial", 10, "bold"), bg="#1c1c1c", fg="#ff5733")
watermark_label.pack(pady=10)
watermark_label.bind("<Enter>", enlarge_watermark)
watermark_label.bind("<Leave>", shrink_watermark)

change_watermark_color()

# تشغيل البرنامج
root.mainloop()
