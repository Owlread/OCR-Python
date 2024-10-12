import cv2
import numpy as np
import easyocr
from datetime import datetime
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
        cv2.imshow("Cropped", roi)

        results = reader.readtext(roi)
        extracted_text = " ".join([result[1] for result in results])
        print("Extracted Text: ", extracted_text)
        
        save_text_to_file(extracted_text)

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  
            scroll_y -= scroll_step
        else:  
            scroll_y += scroll_step

def save_text_to_file(text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extracted_text_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text saved to {filename}")

# เปิดไฟล์รูปภาพ
def open_image_file():
    Tk().withdraw()
    filename = askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    return filename

# ปรับขนาดภาพ
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

# เลือกรูปภาพ
image_path = open_image_file()
if image_path:
    image = cv2.imread(image_path)

    image = resize_image(image)
    clone = image.copy()

    window_height = 600

    scroll_y = 0
    scroll_step = 50 

    # สร้างอ็อบเจ็กต์ EasyOCR Reader
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
