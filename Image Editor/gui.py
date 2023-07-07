import tkinter as tk
from tkinter import ttk, Tk, PhotoImage, filedialog, RIDGE, Canvas, GROOVE, Scale
import cv2 as cv
import numpy as np
from PIL import Image,ImageTk

class Interface:
    def __init__(self,master) -> None:
        self.master = master
        self.header_frame = tk.Frame(self.master,background="#818a88")
        self.header_frame.pack(side=tk.TOP)
        
        # Header Frame

        self.logo = PhotoImage(file="1.png").subsample(5,5)
        ttk.Label(self.header_frame,text="This is an Image Editor",font=4,background="#0f4f42",foreground="White").grid(row=0,column=1)
        ttk.Label(self.header_frame,text="Upload, modify and save your image as you like",background="#0f4f42",foreground="White").grid(row=1,column=1)
        ttk.Label(self.header_frame,image=self.logo).grid(row=0,column=0,rowspan=2)

        # Menu Frame

        self.menu_frame = tk.Frame(self.master,borderwidth=2,background="#a7c7c1")
        self.menu_frame.pack(padx=50,pady=50)
        self.menu_frame.config(relief=RIDGE)

        ttk.Button(self.menu_frame, text="Upload an Image", command=self.upload_action).grid(row=0,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Crop Image", command=self.image_select).grid(row=1,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Add Text", command=self.image_select).grid(row=2,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Draw Over Image", command=self.image_select).grid(row=3,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Apply Filters", command=self.filter_select).grid(row=4,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Blur/Smooth", command=self.blur_action).grid(row=5,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Adjust Levels", command=self.image_select).grid(row=6,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Rotate", command=self.rotate_action).grid(row=7,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Flip", command=self.flip_action).grid(row=8,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Save as", command=self.image_select).grid(row=9,column=0,padx=5,pady=5,sticky="sw")

        self.canvas = Canvas(self.menu_frame, background="Gray",height=400,width=400)
        self.canvas.grid(row=0,column=1,rowspan=10)
        # Footer Frame

        self.footer_frame = tk.Frame(self.master,background="#a7c7c1")
        self.footer_frame.pack()

        ttk.Button(self.footer_frame, text="Save Changes", command=self.image_select).grid(row=0, column=0,padx=10, sticky="sw")
        ttk.Button(self.footer_frame, text="Cancel", command=self.image_select).grid(row=0, column=1,padx=10, sticky="sw")
        ttk.Button(self.footer_frame, text="Revert all changes", command=self.image_select).grid(row=0, column=2,padx=10, sticky="sw")

    # Side Menu Frame
    def refresh_side_frame(self):
        try:
            self.side_menu.grid_forget()
        except:
            pass
    
        self.side_menu = tk.Frame(self.menu_frame)    
        self.side_menu.grid(row=0,column=2,rowspan=10)
        self.side_menu.config(relief=GROOVE,borderwidth=2)

    def upload_action(self):
        self.refresh_side_frame()
        ttk.Label(self.side_menu, text="Upload an Image").grid(row=5,column=0,padx=5,pady=5)

        self.canvas.delete("all")
        self.file = filedialog.askopenfilename()
        self.original_image = cv.imread(self.file)
        self.edited_image = cv.imread(self.file)
        self.filtered_image = cv.imread(self.file)

        self.display_image(self.edited_image)

    def display_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.edited_image.copy()
        else:
            image = image

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > 400 or width > 300:
            if ratio < 1:
                new_width = 300
                new_height = int(new_width * ratio)
            else:
                new_height = 400
                new_width = int(new_height * (width / height))

        self.ratio = height / new_height
        self.new_image = cv.resize(image, (new_width, new_height))

        self.new_image = ImageTk.PhotoImage(
            Image.fromarray(self.new_image))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
            new_width / 2, new_height / 2,  image=self.new_image)


    def filter_select(self):
        self.refresh_side_frame()
        ttk.Button(self.side_menu, text="Negative",command=self.negative_image).grid(row=0,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Black and White",command=self.black_white_image).grid(row=1,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Stylization",command=self.stylized_image).grid(row=2,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Sketch Effect",command=self.sketch_image).grid(row=3,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Emboss").grid(row=4,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Sepia").grid(row=5,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Biinary Thresholding").grid(row=6,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Erosion").grid(row=7,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Dilation").grid(row=8,column=0,padx=5,pady=5,sticky="sw")

    def blur_action(self):
        self.refresh_side_frame()
        ttk.Label(self.side_menu, text="Averaging Blur").grid(row=0,column=0)
        self.average_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL)
        self.average_blur.grid(row=1,column=0,sticky="sw",pady=10)

        ttk.Label(self.side_menu, text="Gaussian Blur").grid(row=2,column=0)
        self.gaussian_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL)
        self.gaussian_blur.grid(row=3,column=0,sticky="sw",pady=10)

        ttk.Label(self.side_menu, text="Median Blur").grid(row=4,column=0)
        self.median_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL)
        self.median_blur.grid(row=5,column=0,sticky="sw")

    def rotate_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_menu, text="Rotate Left").grid(row=0,column=0,sticky="sw")
        ttk.Button(self.side_menu, text="Rotate Right").grid(row=1,column=0,sticky="sw")

    def flip_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_menu, text="Horizontal Flip").grid(row=0,column=0,sticky="sw")
        ttk.Button(self.side_menu, text="Vertical Flip").grid(row=1,column=0,sticky="sw")


    # Filter Actions

    def negative_image(self):
        self.filtered_image = cv.bitwise_not(self.edited_image)
        self.display_image(self.filtered_image)

    def black_white_image(self):
        self.filtered_image = cv.cvtColor(self.edited_image, cv.COLOR_BGR2GRAY)
        self.display_image(self.filtered_image)

    def stylized_image(self):
        self.filtered_image = cv.stylization(self.edited_image, sigma_s=150, sigma_r=0.25)
        self.display_image(self.filtered_image)

    def sketch_image(self):
        gray_image = cv.cvtColor(self.filtered_image, cv.COLOR_BGR2GRAY)
        blurred_image = cv.GaussianBlur(gray_image, (5, 5), 0)
        edges = cv.Canny(blurred_image, 30, 100)
        self.filtered_image = cv.bitwise_not(edges)   
        self.display_image(self.filtered_image)  

    def image_select(self):
        pass

root = Tk()
root.geometry("750x700")
root.config(background="#a7c7c1")
Interface(root)
root.mainloop()
