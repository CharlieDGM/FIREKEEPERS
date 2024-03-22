import tkinter as tk

def on_button_click():
    label.config(text="Hello, " + entry.get())

# Create the main application window
app = tk.Tk()
app.title("Simple GUI Example")

# Create and place widgets (GUI components) in the window
label = tk.Label(app, text="Enter your name:")
label.pack(pady=10)

entry = tk.Entry(app)
entry.pack(pady=10)

button = tk.Button(app, text="Say Hello", command=on_button_click)
button.pack(pady=10)

# Start the main event loop
app.mainloop()