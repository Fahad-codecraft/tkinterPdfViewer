import tkinter as tk
import fitz
from tkinter import ttk
import math
from PIL import Image, ImageTk
import platform

USE_CUSTOM_TKINTER = False
try:
    import customtkinter as ctk
    USE_CUSTOM_TKINTER = True
except ImportError:
    pass

if not USE_CUSTOM_TKINTER:
    from tkinter import simpledialog

class ShowPdf():
    img_object_li = []
    tkimg_object_li = []
    open_pdf = None  # Store the currently opened PDF

    def close_pdf(self):
        if self.open_pdf is not None:
            self.open_pdf.close()
            self.open_pdf = None
            self.img_object_li.clear()
            self.tkimg_object_li.clear()
            self.frame.destroy() 

    def pdf_view(self, master, width=1200, height=600, pdf_location="", bar=False, load="after", dpi=100):
        self.frame = tk.Frame(master, width=width, height=height, bg="white")
        scroll_y = ttk.Scrollbar(self.frame, orient="vertical")
        scroll_x = ttk.Scrollbar(self.frame, orient="horizontal")
        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")
        percentage_view = 0
        percentage_load = tk.StringVar()
        if bar == True and load == "after":
            self.display_msg = ttk.Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)
            loading = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
            loading.pack(side=tk.TOP, fill=tk.X)
        self.text = tk.Text(self.frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, width=width, height=height)
        self.text.pack(fill="x")
        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)

        def ask_password(title, prompt):
            if USE_CUSTOM_TKINTER:
                return ctk.CTkInputDialog(text=title, title=prompt)
            else:
                return simpledialog.askstring(title, prompt)

        # Method to add images from the PDF
        def add_img(password=None):
            self.close_pdf()  # Close the previously opened PDF if any
            password_attempts = 3  # Allow 3 attempts for entering the correct password
            self.open_pdf = fitz.open(pdf_location)
            if self.open_pdf.is_encrypted:
                while password_attempts > 0:
                    password = ask_password("Password", "Enter password for encrypted PDF:")
                    if USE_CUSTOM_TKINTER:
                        password = password.get_input()
                    else: 
                        pass 
                    if password is None:
                        master.destroy()
                        return
                    if self.open_pdf.is_encrypted and not self.open_pdf.authenticate(password):
                        tk.messagebox.showerror("Error", "Invalid password!")
                        password_attempts -= 1
                    else:
                        # If the password is correct, break the loop and continue processing the PDF
                        break
                else:
                    # If all attempts are used and the correct password is not entered, close the PDF
                    tk.messagebox.showerror("Error", "Maximum attempts reached. Closing PDF.")
                    self.open_pdf = None
                    master.destroy()
                    return
            for page in self.open_pdf:
                pix = page.get_pixmap(dpi=dpi)
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                self.img_object_li.append(img)
                self.tkimg_object_li.append(ImageTk.PhotoImage(img))
                if bar == True and load == "after":
                    percentage_view += 1
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view * 100 / len(self.open_pdf)))}%")
                    loading['value'] = percentage_view * 100 / len(self.open_pdf)
            self.orig_size = self.tkimg_object_li[0].width()
            if bar == True and load == "after":
                loading.pack_forget()
                self.display_msg.pack_forget()
            for im in self.tkimg_object_li:
                self.text.image_create(tk.END, image=im)
                self.text.insert(tk.END, "\n")
            self.text.configure(state="disabled")

        def start_pack(password=None):
            # Call add_img in the main thread
            master.after(0, lambda: add_img(password))

        if load == "after":
            master.after(250, start_pack)
        else:
            start_pack()

        def zoom_in(event=None):
            self.text.configure(state="normal")
            self.text.delete(1.0, tk.END)
            scroll_x_state = scroll_x.get()
            scroll_y_state = scroll_y.get()
            res = 1 + 0.1 * self.orig_size / self.tkimg_object_li[0].width()
            for i, im in enumerate(self.img_object_li):
                self.tkimg_object_li[i] = ImageTk.PhotoImage(
                    im.resize((int(res * self.tkimg_object_li[i].width()), int(res * self.tkimg_object_li[i].height())), Image.Resampling.LANCZOS))
                self.text.image_create(tk.END, image=self.tkimg_object_li[i])
                self.text.insert(tk.END, "\n")
            self.text.update()
            self.text.xview_moveto(scroll_x_state[0])
            self.text.yview_moveto(scroll_y_state[0])
            self.text.update()
            self.text.configure(state="disabled")

        def zoom_out(event=None):
            self.text.configure(state="normal")
            self.text.delete(1.0, tk.END)
            scroll_x_state = scroll_x.get()
            scroll_y_state = scroll_y.get()
            res = 1 - 0.1 * self.orig_size / self.tkimg_object_li[0].width()
            for i, im in enumerate(self.img_object_li):
                self.tkimg_object_li[i] = ImageTk.PhotoImage(
                    im.resize((int(res * self.tkimg_object_li[i].width()), int(res * self.tkimg_object_li[i].height())), Image.Resampling.LANCZOS))
                self.text.image_create(tk.END, image=self.tkimg_object_li[i])
                self.text.insert(tk.END, "\n")
            self.text.update()
            self.text.xview_moveto(scroll_x_state[0])
            self.text.yview_moveto(scroll_y_state[0])
            self.text.update()
            self.text.configure(state="disabled")

        def zooming(event=None):
            if event.delta > 0:
                zoom_in(event)
            else:
                zoom_out(event)

        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            self.text.bind('<Control-plus>', zoom_in)
            self.text.bind('<Control-minus>', zoom_out)
            self.text.bind('<Control-MouseWheel>', zooming)
        elif platform.system() == 'Linux':
            # cant bind neither control + nor control - events on linux for some reason
            self.text.bind('<Control-Button-4>', zoom_in)
            self.text.bind('<Control-Button-5>', zoom_out)
        else:
            pass
    

        return self.frame

def main():
    root = tk.Tk()
    root.geometry("700x780")
    d = ShowPdf().pdf_view(root, pdf_location=r"C:\Users\HP\Desktop\tests\PDF APP\encrypted.pdf", width=100, height=100)
    d.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
