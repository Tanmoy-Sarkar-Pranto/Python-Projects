import tkinter as tk
from tkinter import ttk, Tk, PhotoImage, filedialog, RIDGE, Canvas, GROOVE, Scale, colorchooser
import cv2 as cv
import numpy as np
from PIL import Image,ImageTk

class Interface:
    def __init__(self,master) -> None:
        self.master = master
        self.header_frame = tk.Frame(self.master,background="#818a88")
        self.header_frame.pack(side=tk.TOP)
        self.color_code = ((255,255,255),'#ffffff')
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
        ttk.Button(self.menu_frame, text="Crop Image", command=self.crop_action).grid(row=1,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Add Text", command=self.text_action_1).grid(row=2,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Draw Over Image", command=self.draw_fig).grid(row=3,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Apply Filters", command=self.filter_select).grid(row=4,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Blur/Smooth", command=self.blur_action).grid(row=5,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Adjust Levels", command=self.adjust_action).grid(row=6,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Rotate", command=self.rotate_action).grid(row=7,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Flip", command=self.flip_action).grid(row=8,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.menu_frame, text="Save as", command=self.save_action).grid(row=9,column=0,padx=5,pady=5,sticky="sw")

        self.canvas = Canvas(self.menu_frame, background="Gray",height=400,width=400)
        self.canvas.grid(row=0,column=1,rowspan=10)
        # Footer Frame

        self.footer_frame = tk.Frame(self.master,background="#a7c7c1")
        self.footer_frame.pack()

        ttk.Button(self.footer_frame, text="Save Changes", command=self.apply_action).grid(row=0, column=0,padx=10, sticky="sw")
        ttk.Button(self.footer_frame, text="Cancel", command=self.cancel_action).grid(row=0, column=1,padx=10, sticky="sw")
        ttk.Button(self.footer_frame, text="Revert all changes", command=self.revert_action).grid(row=0, column=2,padx=10, sticky="sw")

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
        ttk.Button(self.side_menu, text="Emboss",command=self.emboss_effect).grid(row=4,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Sepia",command=self.sepia_effect).grid(row=5,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Biinary Thresholding",command=self.binary_thresh).grid(row=6,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Erosion",command=self.erosion_effect).grid(row=7,column=0,padx=5,pady=5,sticky="sw")
        ttk.Button(self.side_menu, text="Dilation",command=self.dilation_effect).grid(row=8,column=0,padx=5,pady=5,sticky="sw")

    def blur_action(self):
        self.refresh_side_frame()
        ttk.Label(self.side_menu, text="Averaging Blur").grid(row=0,column=0)
        self.average_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL,command=self.averaging_blur_action)
        self.average_blur.grid(row=1,column=0,sticky="sw",pady=10)

        ttk.Label(self.side_menu, text="Gaussian Blur").grid(row=2,column=0)
        self.gaussian_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL,command=self.gaussian_blur_action)
        self.gaussian_blur.grid(row=3,column=0,sticky="sw",pady=10)

        ttk.Label(self.side_menu, text="Median Blur").grid(row=4,column=0)
        self.median_blur = Scale(self.side_menu, from_=0, to=255, orient=tk.HORIZONTAL,command=self.median_blur_action)
        self.median_blur.grid(row=5,column=0,sticky="sw")

    def rotate_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_menu, text="Rotate Left",command=self.rotate_left).grid(row=0,column=0,sticky="sw")
        ttk.Button(self.side_menu, text="Rotate Right",command=self.rotate_right).grid(row=1,column=0,sticky="sw")

    def flip_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_menu, text="Horizontal Flip",command=self.horizontal_flip).grid(row=0,column=0,sticky="sw")
        ttk.Button(self.side_menu, text="Vertical Flip",command=self.vertical_flip).grid(row=1,column=0,sticky="sw")

    def adjust_action(self):
        self.refresh_side_frame()
        ttk.Label(self.side_menu, text="Brightness").grid(row=0,column=0)
        self.brightness = Scale(self.side_menu, from_=0,to=2,resolution=0.1,orient=tk.HORIZONTAL,command=self.adjust_brightness)
        self.brightness.grid(row=1,column=0)
        ttk.Label(self.side_menu, text="Saturation").grid(row=2,column=0)
        self.saturation = Scale(self.side_menu, from_=-200,to=200,resolution=0.1,orient=tk.HORIZONTAL,command=self.adjust_saturation)
        self.saturation.grid(row=3,column=0)
    
    def text_action_1(self):
        self.text_extracted = "Hello"
        self.refresh_side_frame()
        ttk.Label(self.side_menu, text="Enter your text").grid(row=0,column=0)
        self.text_on_image = ttk.Entry(self.side_menu)
        self.text_on_image.grid(row=1,column=0)

        ttk.Button(self.side_menu, text="Pick a color", command=self.choose_color).grid(row=2,column=0)
        # ttk.Label(self.side_menu, text="Enter fontsize").grid(row=3,column=0)
        # self.text_font = ttk.Entry(self.side_menu)
        # self.text_font.grid(row=4,column=0)
        self.text_action()

    def text_action(self):
        self.rectangle_id = 0
        # self.ratio = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.canvas.bind("<ButtonPress>", self.put_text)

    def put_text(self, event):

        font = int(2*self.ratio)
        if self.text_on_image.get():
            self.text_extracted = self.text_on_image.get()

        start_font = int(event.x*self.ratio), int(event.y*self.ratio)    
        r, g, b = tuple(map(int, self.color_code[0]))
        self.filtered_image = cv.putText(self.edited_image, self.text_extracted, 
                                         start_font, cv.FONT_HERSHEY_SIMPLEX, font,(b,g,r),5)
        self.display_image(self.filtered_image)

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title="Choose Color")
        if self.color_code == (None,None):
            self.color_code = ((255,255,255),'#ffffff')
        # print(self.color_code)
    
    def draw_fig(self):
        self.color_code = ((255, 0, 0), '#ff0000')
        self.refresh_side_frame()
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.draw_color_button = ttk.Button(
            self.side_menu, text="Pick A Color", command=self.choose_color)
        self.draw_color_button.grid(
            row=0, column=2, padx=5, pady=5, sticky='sw')
    
    def start_draw(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_ids = []

    def draw(self, event):
        # print(self.draw_ids)
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
                                                     fill=self.color_code[-1], capstyle=tk.ROUND, smooth=True))

        self.x = event.x
        self.y = event.y
    
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

    def emboss_effect(self):
        kernel = np.array([[0, -1, -1],
                   [1, 0, -1],
                   [1, 1, 0]])

        self.filtered_image = cv.filter2D(self.edited_image, -1, kernel)
        self.display_image(self.filtered_image)

    def sepia_effect(self):
        sepia_matrix = np.array([[0.272, 0.534, 0.131],
                         [0.349, 0.686, 0.168],
                         [0.393, 0.769, 0.189]])

        self.filtered_image = cv.transform(self.edited_image, sepia_matrix)
        self.display_image(self.filtered_image)

    def binary_thresh(self):
        _, self.filtered_image = cv.threshold(self.edited_image, 127, 255, cv.THRESH_BINARY)
        self.display_image(self.filtered_image)

    def erosion_effect(self):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        self.filtered_image = cv.erode(self.edited_image, kernel, iterations=3)
        self.display_image(self.filtered_image)

    def dilation_effect(self):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        self.filtered_image = cv.dilate(self.edited_image, kernel, iterations=3)
        self.display_image(self.filtered_image)

    # Rotate Action
    def rotate_right(self):
        self.filtered_image = cv.rotate(self.filtered_image, cv.ROTATE_90_CLOCKWISE)
        self.display_image(self.filtered_image)

    def rotate_left(self):
        self.filtered_image = cv.rotate(self.filtered_image, cv.ROTATE_90_COUNTERCLOCKWISE)
        self.display_image(self.filtered_image)

    # Flip Action
    def vertical_flip(self):
        self.filtered_image = cv.flip(self.filtered_image, 0)
        self.display_image(self.filtered_image)

    def horizontal_flip(self):
        self.filtered_image = cv.flip(self.filtered_image, 2)
        self.display_image(self.filtered_image)

    # Blur/Smooth Action
    def averaging_blur_action(self,value):
        value = int(value)
        if value % 2 ==0:
            value += 1 
        self.filtered_image = cv.blur(self.edited_image, (value,value))
        self.display_image(self.filtered_image)

    def gaussian_blur_action(self, value):
        value = int(value)
        if value % 2 ==0:
            value += 1 
        self.filtered_image = cv.GaussianBlur(self.edited_image, (value,value), 0)
        self.display_image(self.filtered_image)
        
    def median_blur_action(self, value):
        value = int(value)
        if value % 2 ==0:
            value += 1 
        self.filtered_image = cv.medianBlur(self.edited_image,value)
        self.display_image(self.filtered_image)

    # Adjust Levels action

    def adjust_brightness(self,value):
        self.filtered_image = cv.convertScaleAbs(self.edited_image, alpha=float(value))
        self.display_image(self.filtered_image)
    
    def adjust_saturation(self,value):
        self.filtered_image = cv.convertScaleAbs(self.edited_image, alpha=1, beta=float(value))
        self.display_image(self.filtered_image)

    # Crop

    def crop_action(self):
        self.rectangle_id = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0

        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)
        
        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=1)

    def end_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x*self.ratio)
            start_y = int(self.crop_start_y*self.ratio)
            end_x = int(self.crop_end_x*self.ratio)
            end_y = int(self.crop_end_y*self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x*self.ratio)
            start_y = int(self.crop_start_y*self.ratio)
            end_x = int(self.crop_start_x*self.ratio)
            end_y = int(self.crop_end_y*self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x*self.ratio)
            start_y = int(self.crop_end_y*self.ratio)
            end_x = int(self.crop_end_x*self.ratio)
            end_y = int(self.crop_start_y*self.ratio)
        else:
            start_x = int(self.crop_end_x*self.ratio)
            start_y = int(self.crop_end_y*self.ratio)
            end_x = int(self.crop_start_x*self.ratio)
            end_y = int(self.crop_start_y*self.ratio)
        
        x,y = slice(start_x, end_x, 1), slice(start_y, end_y, 1)
        self.filtered_image = self.edited_image[y,x]
        self.display_image(self.filtered_image)

    def save_action(self):
        self.apply_action()
        original_file_type = self.file.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        print(filename)
        if len(filename)>1:
            filename = filename + "." + original_file_type

            save_as_image = self.edited_image
            cv.imwrite(filename, save_as_image)
            self.filename = filename

    def apply_action(self):
        self.edited_image = self.filtered_image
        self.display_image(self.edited_image)

    def cancel_action(self):
        self.display_image(self.edited_image)

    def revert_action(self):
        self.edited_image = self.original_image.copy()
        self.display_image(self.edited_image)

root = Tk()
root.geometry("750x700")
root.config(background="#a7c7c1")
Interface(root)
root.mainloop()
