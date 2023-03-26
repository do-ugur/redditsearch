import praw
import tkinter as tk
import webbrowser

reddit = praw.Reddit(client_id="PgslQ3wqKoA3hmzJdlHANA",
                     client_secret="0",
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
        results_text.insert(tk.END, f"{post.title}\n", "bold_black")
        title_end = results_text.index(tk.END)
        results_text.insert(tk.END, f"{post.url}\n")
        results_text.tag_configure("bold_black", font=("TkDefaultFont", 12, "bold"), foreground="black")
        results_text.tag_add("url", title_start, title_end)

        # Erstelle den Knopf zum Öffnen des ursprünglichen Links
        open_button = tk.Button(results_text, text="Open in Browser", command=lambda url=post.url: open_url(url))
        results_text.window_create(title_end, window=open_button)

        # Erstelle den Knopf zum Öffnen des Quellenlinks
        source_button = tk.Button(results_text, text="Open Source", command=lambda url=post.permalink: open_url(f"https://www.reddit.com{url}"))
        results_text.window_create(title_end, window=source_button)

    results_text.insert(tk.END, "\n\n")

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

results_text = tk.Text(root, width=int(root.winfo_screenwidth()*0.75), height=int(root.winfo_screenheight()*0.75))
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