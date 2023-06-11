import tkinter as tk

def on_button_press(event):
    # Set the cursor icon to indicate dragging
    root.config(cursor="exchange")

def on_button_release(event):
    # Reset the cursor icon to the default
    root.config(cursor="")
    
    # Check if the mouse release occurred within the frame
    if frame.winfo_containing(event.x_root, event.y_root) == frame:
        # Create a label in the frame
        placed_label = tk.Label(frame, text="Placed")
        placed_label.pack()

# Create the main window
root = tk.Tk()

# Set the window size
root.geometry("400x300")

# Create the frame
frame = tk.Frame(root, width=200, height=200, bg="lightgray")
frame.pack(padx=10, pady=10)

# Create a button representing a file
button_width = 100
button_height = 30
button = tk.Button(root, text="File 1", width=button_width, height=button_height)
button.bind("<ButtonPress-1>", on_button_press)
button.bind("<ButtonRelease-1>", on_button_release)
button.place(x=10, y=10)

root.mainloop()
