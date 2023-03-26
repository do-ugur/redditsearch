import requests
import praw
import tkinter as tk
import webbrowser
from PIL import ImageTk, Image
import io

reddit = praw.Reddit(client_id="ngqv32dxrlqzWHbBcj4W7A",
                     client_secret="pBaS9sZpFfS7zLcH67T_9zhhLZ8kxw",
                     user_agent="exqo")


def search_posts():
    query = query_input.get()
    time_filter = time_filter_var.get()
    results_text.delete("1.0", tk.END)

    # Suchanfrage nach den relevantesten Beiträgen
    relevant_posts = reddit.subreddit("all").search(query, sort="relevance", time_filter=time_filter, limit=10)
    # Suchanfrage nach den am meisten aufgerufenen Beiträgen
    popular_posts = reddit.subreddit("all").search(query, sort="top", time_filter=time_filter, limit=10)
    # Kombinieren der Ergebnisse
    all_posts = set(list(relevant_posts) + list(popular_posts))

    # Anzeigen der Ergebnisse im Textfeld
    for post in all_posts:
        title_start = results_text.index(tk.END)
        results_text.insert(tk.END, f"{post.title}\n\n", "bold_black")
        title_end = results_text.index(tk.END)

        # Anzeigen von Metadaten
        meta_data = f"Upvotes: {post.score}, Author: {post.author.name}, Subreddit: {post.subreddit.display_name}"
        results_text.insert(tk.END, meta_data + "\n\n", "gray")

        # Anzeigen von Bildern
        if post.url.endswith('.jpg') or post.url.endswith('.png'):
            try:
                image_data = requests.get(post.url).content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((300, 500), Image.ANTIALIAS)
                photo_image = ImageTk.PhotoImage(image)
                image_label = tk.Label(results_text, image=photo_image)
                results_text.window_create(title_end, window=image_label)
                image_label.image = photo_image  # To avoid garbage collection
            except:
                pass

        # Anzeigen von Links zum Originalbeitrag und zum Subreddit
        original_button = tk.Button(results_text, text="Original post",
                                    command=lambda url="https://redd.it/" + post.id: open_url(url))
        subreddit_button = tk.Button(results_text, text="Subreddit",
                                     command=lambda subreddit=post.subreddit.display_name:
                                     open_url(f"https://www.reddit.com/r/{subreddit}"))

        results_text.window_create(title_end, window=original_button)
        results_text.insert(tk.END, "\n")
        results_text.window_create(tk.END, window=subreddit_button)
        results_text.insert(tk.END, "\n\n")

    results_text.insert(tk.END, "\n")


def on_link_click(event):
    tag_ranges = results_text.tag_ranges("url")
    for i in range(0, len(tag_ranges), 2):
        if tag_ranges[i] <= event.widget.index(tk.CURRENT) <= tag_ranges[i+1]:
            url_start = f"{tag_ranges[i]} + 1c"
            url_end = f"{tag_ranges[i+1]} - 1c"
            url = results_text.get(url_start, url_end)
            open_url(url)

    button_ranges = results_text.tag_ranges("button")
    for i in range(0, len(button_ranges), 2):
        if button_ranges[i] <= event.widget.index(tk.CURRENT) <= button_ranges[i+1]:
            button_start = f"{button_ranges[i]} + 1c"
            button_end = f"{button_ranges[i+1]} - 1c"
            button_text = results_text.get(button_start, button_end)
            if button_text == "Original post":
                url_start = f"{button_ranges[i-1]} + 24c"
                url_end = f"{button_ranges[i-1]} + {len(button_ranges[i-1])}c"
                url = results_text.get(url_start, url_end)
                open_url(url)
            elif button_text == "Subreddit":
                url_start = f"{button_ranges[i-1]} + 17c"
                url_end = f"{button_ranges[i-1]} + {len(button_ranges[i-1])}c"
                subreddit = results_text.get(url_start, url_end)
                open_url(f"https://www.reddit.com/r/{subreddit}")

    results_text.tag_configure("url", foreground="blue", underline=True)
    results_text.tag_configure("button", foreground="blue", underline=True)
    results_text.tag_bind("url", "<Button-1>", on_link_click)
    results_text.tag_bind("button", "<Button-1>", on_link_click)

def open_url(url):
    webbrowser.open(url)


root = tk.Tk()
root.title("Reddit Search")

query_label = tk.Label(root, text="Enter a search query:")
query_label.pack()

query_input = tk.Entry(root)
query_input.pack()

time_filter_var = tk.StringVar()
time_filter_var.set("week")
time_filter_menu = tk.OptionMenu(root, time_filter_var, "hour", "day", "week", "month", "year", "all")
time_filter_menu.pack()

search_button = tk.Button(root, text="Search", command=search_posts)
search_button.pack()

results_text = tk.Text(root, width=int(root.winfo_screenwidth()*0.95), height=int(root.winfo_screenheight()*0.95))
results_text.pack()

def on_link_click(event):
    tag_ranges = results_text.tag_ranges("url")
    for i in range(0, len(tag_ranges), 2):
        if tag_ranges[i] <= event.widget.index(tk.CURRENT) <= tag_ranges[i+1]:
            url_start = f"{tag_ranges[i]} + 1c"
            url_end = f"{tag_ranges[i+1]} - 1c"
            url = results_text.get(url_start, url_end)
            open_url(url)

results_text.tag_configure("url", foreground="blue", underline=True)
results_text.tag_bind("url", "<Button-1>", on_link_click)

root.mainloop()
