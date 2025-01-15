import tkinter as tk
from tkinter import messagebox
from transformers import pipeline

# Load Hugging Face models
summarizer = pipeline("summarization")

def generate_summary(input_text):
    """Summarize large text by splitting it into smaller chunks."""
    chunks = split_text_into_chunks(input_text, max_tokens=500)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=25, do_sample=False)[0]["summary_text"]
        summaries.append(summary)
    return " ".join(summaries)

def split_text_into_chunks(text, max_tokens=500):
    """Split the input text into smaller chunks based on word count."""
    words = text.split()
    return [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]

def limit_text_input(event):
    """Limit the character count in the text widget."""
    max_chars = 2000
    current_text = text_input.get("1.0", "end-1c")
    if len(current_text) > max_chars:
        text_input.delete("1.0", "end")
        text_input.insert("1.0", current_text[:max_chars])
        messagebox.showwarning("Input Limit Exceeded", "Input text exceeds the 2000-character limit.")

def summarize_text():
    """Handle the summarization action."""
    input_text = text_input.get("1.0", "end-1c").strip()
    if not input_text:
        messagebox.showwarning("Empty Input", "Please enter some text to summarize.")
        return
    summary = generate_summary(input_text)
    result_text.delete("1.0", "end")
    result_text.insert("1.0", summary)

# Tkinter GUI setup
root = tk.Tk()
root.title("SummarAIser - AI-Powered Educational Assistant")
root.configure(bg="#fdf6e3")

# Input Text
tk.Label(root, text="Enter your study material or topic:", bg="#fdf6e3", font=("Helvetica", 12)).pack(pady=5)
text_input = tk.Text(root, height=10, width=80, bg="#eee8d5", fg="#586e75")
text_input.pack(pady=5)
text_input.bind("<KeyRelease>", limit_text_input)

# Buttons
button_frame = tk.Frame(root, bg="#fdf6e3")
button_frame.pack(pady=10)

summarize_button = tk.Button(button_frame, text="Summarize", command=summarize_text, bg="#b3d9ff", fg="#002b36", font=("Helvetica", 10, "bold"))
summarize_button.grid(row=0, column=0, padx=10)

# Result Text
tk.Label(root, text="Output:", bg="#fdf6e3", font=("Helvetica", 12)).pack(pady=5)
result_text = tk.Text(root, height=15, width=80, bg="#eee8d5", fg="#586e75", state="normal")
result_text.pack(pady=5)

# Footer
tk.Label(root, text="Developed for the NOSU AI Hackathon!", font=("Helvetica", 10, "italic"), bg="#fdf6e3").pack(pady=10)

root.mainloop()
