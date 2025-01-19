import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import api_dogs


class DogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dogs API")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.random_dog = None
        self.user_id = '1'

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        self.img_frame = ttk.Frame(self.root, height=400, width=700)
        self.img_frame.grid(row=0, column=0, padx=10, pady=10)

        self.img_label = ttk.Label(self.img_frame)
        self.img_label.grid(row=0, column=0)

        self.btn_frame = ttk.Frame(self.root, height=400, width=700)
        self.btn_frame.grid(row=1, column=0, padx=10, pady=10)

        self.btn_random = ttk.Button(
            self.btn_frame, text='Get random dog', command=self.get_random_image)
        self.btn_random.grid(row=0, column=0, padx=10, pady=10)

        self.btn_add = ttk.Button(
            self.btn_frame, text='Add to favourites', command=self.add_to_favs)
        self.btn_add.grid(row=0, column=1, padx=10, pady=10)

        self.btn_favs = ttk.Button(
            self.btn_frame, text='Show favourites', command=self.show_favs)
        self.btn_favs.grid(row=0, column=2, padx=10, pady=10)

    def get_random_image(self):
        self.random_dog = api_dogs.get_random_doggo()
        self.show_image(self.random_dog)

    def show_image(self, image_data):
        if 'url' in image_data:
            url = image_data['url']
        elif 'image' in image_data:
            url = image_data['image']['url']

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            img_data = response.raw
            image = Image.open(img_data)
            image.thumbnail((600, 400))
            img = ImageTk.PhotoImage(image)
            self.img_label.config(image=img)
            self.img_label.image = img
        else:
            messagebox.showerror("Error")

    def add_to_favs(self):
        if self.random_dog is not None:
            result = api_dogs.add_to_favourites(
                self.random_dog['id'], self.user_id)
            if result and 'message' in result and result['message'] == 'SUCCESS':
                messagebox.showinfo(
                    message='Image successfully added to favourites.')
            else:
                messagebox.showerror("Error")
        else:
            messagebox.showerror(message="You need to get image first!")

    def show_favs(self):
        favs = api_dogs.get_favourites(self.user_id)
        for image in favs:
            if image['image']:
                self.show_image(image)


if __name__ == '__main__':
    root = tk.Tk()
    app = DogApp(root)
    root.mainloop()
