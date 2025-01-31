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
        try:
            response = requests.get(url, stream=True)
            img_data = response.raw
            image = Image.open(img_data)
            image.thumbnail((600, 400))
            img = ImageTk.PhotoImage(image)
            self.img_label.config(image=img)
            self.img_label.image = img
        except requests.RequestException as e:
            messagebox.showerror(f"Error {e} occured.")

    def add_to_favs(self):
        if self.random_dog is not None:
            result = api_dogs.add_to_favourites(
                self.random_dog['id'], self.user_id)
            if result and 'message' in result and result['message'] == 'SUCCESS':
                messagebox.showinfo(
                    title='Dogs API', message='Image successfully added to favourites.')
            else:
                messagebox.showerror("Error")
        else:
            messagebox.showerror(
                title='Dogs API', message="You need to get image first!")

    def show_favs(self):
        favs = api_dogs.get_favourites(self.user_id)
        self.favs_display(favs)

    def favs_display(self, favs):
        favs_window = tk.Toplevel(self.root)
        favs_window.title("Favourites")
        favs_window.geometry("800x600")

        container = ttk.Frame(favs_window)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container, orient='vertical', command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        window_id = canvas.create_window(
            (0, 0), window=scroll_frame, anchor='nw')

        def on_frame():
            favs_window.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", lambda e: on_frame())
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            window_id, width=canvas.winfo_width()))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        for index, fav in enumerate(favs):
            url = fav['image']['url']
            frame = ttk.Frame(scroll_frame)
            frame.grid(column=index % 3, row=index // 3, padx=10, pady=10)

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                img_data = response.raw
                image = Image.open(img_data)
                image.thumbnail((200, 200))
                img = ImageTk.PhotoImage(image)
                label = ttk.Label(frame, image=img)
                label.image = img
                label.grid(row=0, column=0)

                ttk.Button(frame, text="Remove", command=lambda fav_id=fav['id']: self.remove_from_favs(
                    fav_id, favs_window)).grid(row=1, column=0)
            else:
                messagebox.showerror("Error")

        favs_window.after(100, on_frame)

    def remove_from_favs(self, fav_id, favs_window):
        response = api_dogs.remove_from_favourites(self.user_id, str(fav_id))
        if response and response.get('message') == 'SUCCESS':
            messagebox.showinfo(
                title="Dogs API", message="Image removed from favourites.")
            favs_window.destroy()
            self.show_favs()
        else:
            messagebox.showerror("Error")


if __name__ == '__main__':
    root = tk.Tk()
    app = DogApp(root)
    root.mainloop()
