from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import os
from tkinter import filedialog
import shutil
import numpy as np
import cv2
from scipy import ndimage
from skimage.io import imread
from skimage.feature import hog
from skimage import exposure
import matplotlib.pyplot as plt


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        master.title("Yatzy - The Game")
        x = (master.winfo_screenwidth()//2)-(1280//2)
        y = (master.winfo_screenheight()//2)-(720//2)
        master.geometry('{}x{}+{}+{}'.format(1280, 720, x, y))
        #master.state('zoomed')
        self.pack(expand=True, fill='both')
        self.my_label = None
        self.my_label2 = None
        self.my_label3 = None
        self.Frame1 = None
        self.Frame2 = None
        self.Frame3 = None
        self.FrameTool = None
        self.btnSave = None
        self.btnUpload = None
        self.comboCanh = None
        self.comboLoc = None
        self.comboND = None
        self.button_back = None
        self.button_forward = None
        self.number = 0
        self.origin_name = []
        self.image_list = []
        self.clickedBien = StringVar()
        self.clickedCanh = StringVar()
        self.clickedND = StringVar()
        self._x = 600
        self._y = 600
        
        #self.connect()
        self.insert()
        
        status = Label(self, text="Image 1 of " + str(len(self.image_list)))

        # Create grid index for the window
        for r in range(20):
            self.rowconfigure(r, weight=1)

        for c in range(60):
            self.columnconfigure(c, weight=1)


        # Place Frame 1
        self.Frame1 = LabelFrame(self, text="Ảnh đầu vào", labelanchor="n")
        self.Frame1.grid(row = 0, column = 0, rowspan = 20, columnspan = 20, sticky=W+E+N+S)
        self.Frame1.grid_propagate(False) # Stop grid() from resizing container
        self.Frame1.rowconfigure(0, weight=10)
        self.Frame1.rowconfigure(1, weight=10)
        self.Frame1.rowconfigure(2, weight=10)
        self.Frame1.columnconfigure(0, weight=1)
        self.Frame1.columnconfigure(1, weight=1)
        self.Frame1.columnconfigure(2, weight=1)


        # Place Frame 2
        self.Frame2 = Frame(self)
        self.Frame2.grid(row=0, column=20, rowspan=20, columnspan=20, sticky = W+E+N+S)
        self.Frame2.grid_propagate(False) # Stop grid() from resizing container
        self.Frame2.rowconfigure(0, weight=10)
        self.Frame2.rowconfigure(1, weight=1)
        self.Frame2.rowconfigure(2, weight=1)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)

        # Place Frame tools for Frame 2
        self.FrameTool = LabelFrame(self.Frame2, text="Thuật toán xử lý ảnh", labelanchor="n")
        self.FrameTool.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S)
        self.FrameTool.grid_propagate(False)
        for r in range(10):
            self.FrameTool.rowconfigure(r, weight=1)
        self.FrameTool.columnconfigure(0, weight=1)
        self.FrameTool.columnconfigure(1, weight=1)
        
        self.toolsFrame()
        self.btnProcess = Button(self.Frame2, text="Cập nhật", command=lambda: self.reset())
        self.btnProcess.grid(row=1, column=0, columnspan=2, sticky = W+E+N+S)
        self.btnUpload = Button(self.Frame2, text="Tải lên", command=lambda: self.upload_image())
        self.btnUpload.grid(row=2, column=0, sticky = W+E+N+S)
        self.btnDelete = Button(self.Frame2, text="Xóa", command=lambda: self.delete())
        self.btnDelete.grid(row=2, column=1, sticky = W+E+N+S)

        # Place Frame 3
        self.Frame3 = LabelFrame(self, text="Ảnh đầu ra", labelanchor="n")
        self.Frame3.grid(row=0, column=40, rowspan=20, columnspan=20, sticky = W+E+N+S)
        self.Frame3.grid_propagate(False)
        self.Frame3.rowconfigure(0, weight=10)
        self.Frame3.rowconfigure(1, weight=10)
        self.Frame3.rowconfigure(2, weight=10)
        self.Frame3.columnconfigure(0, weight=1)
        self.Frame3.columnconfigure(1, weight=1)
        self.Frame3.columnconfigure(2, weight=1)
        self.setImage()
    
    def setImage(self):
        self.button_back = Button(self.Frame1, text="<<", command=self.back, state=DISABLED)
        self.button_forward = Button(self.Frame1, text=">>", command=lambda: self.forward(2))
        self.button_back.grid(row=1, column=0)
        self.button_forward.grid(row=1, column=2)
        status = Label(self.Frame1, text="Image 1 of " + str(len(self.image_list)))
        status.grid(row=2, column=0, columnspan=3)
        self.my_label = Label(self.Frame1, image=self.image_list[0])
        self.my_label.grid(row=0, column=0, columnspan=3)
    
    # Define the function to upload and save the image
    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            save_dir = "images"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            filename = os.path.basename(file_path)
            if not os.path.exists("images/" + filename):
                shutil.copy(file_path, os.path.join(save_dir, filename))
                messagebox.showinfo("Success", "Tải ảnh thành công")
                self.insert()

    def insert(self):
        path = "images"
        image = os.listdir(path)
        self.image_list.clear()
        self.origin_name.clear()
        for i in image:
            self.origin_name.append(i)
            my_img = Image.open("images\\" + i)
            my_img = my_img.resize((self._x, self._y))
            my_img = ImageTk.PhotoImage(my_img)
            
            self.image_list.append(my_img)
        
        
    def reset(self):
        self.master.update()
        self.master.update_idletasks()
        self.setImage()
        messagebox.showinfo("Success", "Cập nhật thành công")

    def process(self):
        self.selectCBB()

    def robert(self):
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)

        kernel_x = np.array([[1, 0], [0, -1]])
        kernel_y = np.array([[0, 1], [-1, 0]])

        # Áp dụng filter Roberts để phát hiện biên cạnh theo hướng x và y
        edge_x = cv2.filter2D(img, -1, kernel_x)
        edge_y = cv2.filter2D(img, -1, kernel_y)

        # Kết hợp kết quả từ cả hai hướng
        edge_combined = cv2.addWeighted(edge_x, 0.5, edge_y, 0.5, 0)

        self.my_label = Image.fromarray(edge_combined)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Robert_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label)
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)
        

    def sobel(self):
        # Load an color image
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)

        # Áp dụng lọc Sobel với đạo hàm theo x và y
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

        # Chuyển đổi giá trị âm thành dương
        sobel_x = np.uint8(np.absolute(sobel_x))
        sobel_y = np.uint8(np.absolute(sobel_y))

        # Kết hợp cả hai đạo hàm
        sobel_combined = cv2.bitwise_or(sobel_x, sobel_y)

        self.my_label = Image.fromarray(sobel_combined)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Sobel_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)

    def laplace(self):
        # Load an color image
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)
        # Áp dụng phương pháp Laplace
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        # Chuyển đổi giá trị âm thành dương
        laplacian = np.uint8(np.absolute(laplacian))

        self.my_label = Image.fromarray(laplacian)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Laplace_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)
    
    def gaussian(self):
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)
        #blur = cv2.GaussianBlur(img, (5, 5), 0)

        blurred_image_a = ndimage.gaussian_filter(img, sigma=0.5, mode="constant")
        blurred_image_b = ndimage.gaussian_filter(img, sigma=1, mode="constant")
        blurred_image_c = ndimage.gaussian_filter(img, sigma=3, mode="constant")

        self.my_label = Image.fromarray(blurred_image_a)
        self.my_label = self.my_label.resize((350, 350))
        self.my_label.save("save_images\Gaussian_image_A.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)

        self.my_label2 = Image.fromarray(blurred_image_b)
        self.my_label2 = self.my_label2.resize((350, 350))
        self.my_label2.save("save_images\Gaussian_image_B.png")
        self.my_label2 = ImageTk.PhotoImage(image=self.my_label2) 
        output = Label(self.Frame3, image=self.my_label2)
        output.grid(row=1, column=0, columnspan=3)

        self.my_label3 = Image.fromarray(blurred_image_c)
        self.my_label3 = self.my_label3.resize((350, 350))
        self.my_label3.save("save_images\Gaussian_image_C.png")
        self.my_label3 = ImageTk.PhotoImage(image=self.my_label3) 
        output = Label(self.Frame3, image=self.my_label3)
        output.grid(row=2, column=0, columnspan=3)

    def canny(self):
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)
        
        # Áp dụng thuật toán Canny
        edges = cv2.Canny(img, 100, 200)

        self.my_label = Image.fromarray(edges)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Canny_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)

    def gradient(self):
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)

        # Tính toán gradient theo hướng x và y bằng phương pháp Sobel
        gradient_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

        self.my_label = Image.fromarray(cv2.convertScaleAbs(gradient_x))
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Gradient_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)

        self.my_label2 = Image.fromarray(cv2.convertScaleAbs(gradient_y))
        self.my_label2 = self.my_label2.resize((self._x, self._y))
        self.my_label2 = ImageTk.PhotoImage(image=self.my_label2) 
        output2 = Label(self.Frame3, image=self.my_label2)
        output2.grid(row=1, column=0, columnspan=3)
    
    def sift(self):
        # Đọc ảnh
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)

        # Tạo đối tượng SIFT
        sift = cv2.SIFT_create()
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

        # Tìm keypoint và descriptor
        keypoints, descriptors = sift.detectAndCompute(img, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(img, None)

        matches = bf.match(descriptors, descriptors_2)
        matches = sorted(matches, key= lambda x:x.distance)

        # Vẽ các keypoint trên ảnh
        image_with_keypoints = cv2.drawMatches(img, keypoints, img, keypoints_2, matches[:5000], img, flags=2)

        self.my_label = Image.fromarray(image_with_keypoints)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Sift_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)
    
    def suft(self):
        imgPath = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)
        orb = cv2.ORB_create()
        keypoints = orb.detect(imgPath, None)
        imgGray = cv2.drawKeypoints(
            imgPath, keypoints, imgPath, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        self.my_label = Image.fromarray(imgGray)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Suft_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)
    
    def hog(self):
        # Đọc ảnh và chuyển đổi sang định dạng NumPy và kiểu dữ liệu nguyên thủy
        img = imread("images\\" + self.origin_name[self.number], as_gray=False).astype(np.uint8)

        # Tính toán đặc trưng HOG và hình ảnh HOG
        hogfv, hog_image = hog(img, orientations=9, pixels_per_cell=(16,16), 
                                cells_per_block=(2,2), visualize=True, channel_axis=-1)

        # Chuẩn hóa hình ảnh HOG
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
        hog_image_rescaled_uint8 = (hog_image_rescaled * 255).astype(np.uint8)

        self.my_label = Image.fromarray(hog_image_rescaled_uint8)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\Hog_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)
        plt.tight_layout()
    
    def cnn(self):
        img = cv2.imread("images\\" + self.origin_name[self.number], cv2.IMREAD_GRAYSCALE)
        _, black_pixels_mask = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
        image = cv2.bitwise_and(img, img, mask=black_pixels_mask)

        image = cv2.bitwise_not(image)
        #resized_image = cv2.resize(image, (28, 28))
        self.my_label = Image.fromarray(image)
        self.my_label = self.my_label.resize((self._x, self._y))
        self.my_label.save("save_images\CNN_image.png")
        self.my_label = ImageTk.PhotoImage(image=self.my_label) 
        output = Label(self.Frame3, image=self.my_label)
        output.grid(row=0, column=0, columnspan=3)

    def selectCBB(self, mycbb):
        if mycbb.get() == "Robert":
            self.robert()
        elif mycbb.get() == "Sobel":
            self.sobel()
        elif mycbb.get() == "Laplace":
            self.laplace()
        elif mycbb.get() == "Gaussian":
            self.gaussian()
        elif mycbb.get() == "Canny":
            self.canny()
        elif mycbb.get() == "Gradient":
            self.gradient()
        elif mycbb.get() == "SIFT":
            self.sift()
        elif mycbb.get() == "SURF":
            self.suft()
        elif mycbb.get() == "HOG":
            self.hog()
        elif mycbb.get() == "CNN":
            self.cnn()

    def toolsFrame(self):
        lblTitle = Label(self.FrameTool, text="Các thuật toán xử lý ảnh")
        lblTitle.config(font=('Roboto', 18))
        lblTitle.grid(row=0, column=0, columnspan=3)
        loc = [
            "",
            "Robert",
            "Sobel",
            "Laplace",
            "Gaussian",

        ]
        canh = [
            "",
            "Canny",
            "Gradient",
        ]
        nhandang = [
            "",
            "SIFT",
            "SURF",
            "HOG",
            "CNN"
        ]
        lblBien = Label(self.FrameTool, text="Lọc ảnh", width=15, anchor="w", justify="left")
        lblBien.grid(row=1, column=0)
        self.comboLoc = ttk.Combobox(self.FrameTool, value=loc)
        self.comboLoc.current(0)
        self.comboLoc.bind("<<ComboboxSelected>>")
        self.comboLoc.grid(row=1, column=1)
        self.btnProcess = Button(self.FrameTool, text="Xử lý lọc ảnh", command=lambda: self.selectCBB(self.comboLoc))
        self.btnProcess.grid(row=2, column=0, columnspan=2, sticky=W+E)

        lblCanh = Label(self.FrameTool, text="Phát hiện cạnh", width=15, anchor="w", justify="left")
        lblCanh.grid(row=3, column=0)
        self.comboCanh = ttk.Combobox(self.FrameTool, value=canh)
        self.comboCanh.current(0)
        self.comboCanh.bind("<<ComboboxSelected>>")
        self.comboCanh.grid(row=3, column=1)
        self.btnProcess = Button(self.FrameTool, text="Xử lý phát hiện cạnh", command=lambda: self.selectCBB(self.comboCanh))
        self.btnProcess.grid(row=4, column=0, columnspan=2, sticky=W+E)

        lblND = Label(self.FrameTool, text="Nhận dạng", width=15, anchor="w", justify="left")
        lblND.grid(row=5, column=0)
        self.comboND = ttk.Combobox(self.FrameTool, value=nhandang)
        self.comboND.current(0)
        self.comboND.bind("<<ComboboxSelected>>")
        self.comboND.grid(row=5, column=1)
        self.btnProcess = Button(self.FrameTool, text="Xử lý nhận dạng", command=lambda: self.selectCBB(self.comboND))
        self.btnProcess.grid(row=6, column=0, columnspan=2, sticky=W+E)

    def delete(self):
        for widget in self.Frame3.winfo_children():
            widget.destroy()

    def forward(self, image_number):
        global button_forward
        global button_back

        self.my_label = Label(self.Frame1, image=self.image_list[image_number-1])
        self.number = image_number-1
        self.button_forward = Button(self.Frame1, text=">>", command=lambda: self.forward(image_number+1))
        self.button_back = Button(self.Frame1, text="<<", command=lambda: self.back(image_number-1))

        if image_number == len(self.image_list):
            self.button_forward = Button(self.Frame1, text=">>", state=DISABLED)

        self.my_label.grid(row=0, column=0, columnspan=3)

        self.button_back.grid(row=1, column=0)    
        self.button_forward.grid(row=1, column=2)

        status = Label(self.Frame1, text="Image " + str(image_number) + " of " + str(len(self.image_list)))
        status.grid(row=2, column=0, columnspan=3)
        

    def back(self, image_number):
        global button_forward
        global button_back

        self.my_label = Label(self.Frame1, image=self.image_list[image_number-1])
        self.number = image_number-1
        self.button_forward = Button(self.Frame1, text=">>", command=lambda: self.forward(image_number+1))
        self.button_back = Button(self.Frame1, text="<<", command=lambda: self.back(image_number-1))

        if image_number == 1:
            self.button_back = Button(self.Frame1, text="<<", state=DISABLED)
        
        self.my_label.grid(row=0, column=0, columnspan=3)

        self.button_back.grid(row=1, column=0)    
        self.button_forward.grid(row=1, column=2)

        status = Label(self.Frame1, text="Image " + str(image_number) + " of " + str(len(self.image_list)))
        status.grid(row=2, column=0, columnspan=3)


root = Tk()
app = Window(master=root)
app.mainloop()
