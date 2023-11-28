import tkinter as tk
from PIL import Image, ImageTk

def open_image():
    image_path = entry.get()  # Get the image path from an entry widget or any other source
    if image_path:
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))  # Resize the image if needed
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk  # Keep a reference to the image to prevent garbage collection
        except IOError:
            print(f"Unable to open image '{image_path}'.")

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Entry widget for image path
entry = tk.Entry(root)
entry.pack()

# Button to open the image
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Label to display the image
label = tk.Label(root)
label.pack()

root.mainloop()
