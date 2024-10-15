import cv2
import numpy as np
import easyocr
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def select_roi(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, scroll_y, window_height

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        roi = visible_image[y_start:y_end, x_start:x_end]
        roi = preprocess_image(roi)
        cv2.imshow("Cropped", roi)

        results = reader.readtext(roi)
        extracted_text = " ".join([result[1] for result in results])
        print("Extracted Text: ", extracted_text)
        
        append_text_to_file(extracted_text)

    #หมุนล้อเมาส์
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Scroll ขึ้น
            scroll_y -= scroll_step
        else:  # Scroll ลง
            scroll_y += scroll_step

def append_text_to_file(text):
    filename = "extracted_text.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"Text appended to {filename}")

def resize_image(image, max_width=800):
    height, width = image.shape[:2]
    if width > max_width:
        scaling_factor = max_width / width
        image = cv2.resize(image, (int(width * scaling_factor), int(height * scaling_factor)))
    return image

def get_visible_image(image, scroll_y, window_height):
    height, _ = image.shape[:2]
    if scroll_y + window_height > height:
        scroll_y = height - window_height
    if scroll_y < 0:
        scroll_y = 0
    return image[scroll_y:scroll_y + window_height], scroll_y

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) 
    sharpened = cv2.filter2D(binary_image, -1, sharpen_kernel)
    return sharpened

def open_image_file():
    Tk().withdraw()
    filename = askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    return filename

image_path = open_image_file()
if image_path:
    image = cv2.imread(image_path)

    image = resize_image(image)
    clone = image.copy()

    # กำหนดความสูงของหน้าต่างแสดงผล
    window_height = 600

    # ค่าการเลื่อน
    scroll_y = 0
    scroll_step = 50

    reader = easyocr.Reader(['en'])

    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    cropping = False

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", select_roi)

    while True:
        visible_image, scroll_y = get_visible_image(image, scroll_y, window_height)
        i = visible_image.copy()

        if not cropping:
            cv2.imshow("image", visible_image)
        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.imshow("image", i)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
