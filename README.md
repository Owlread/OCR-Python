# OCR Beta 0.2
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
## Installation // วิธีการติดตั้ง
- OpenCV (opencv-python)
- easyocr
- numpy

```
pip install opencv-python
pip install numpy
pip install easyocr
```
### สรุปการใช้งานโค้ด:
1. **เลือกรูปภาพที่ต้องการ**: เมื่อเปิดโปรแกรม จะมีหน้าต่างให้คุณเลือกไฟล์รูปภาพ (รองรับ `.jpg`, `.jpeg`, หรือ `.png`)
2. **เลือกพื้นที่ที่ต้องการตัด (ROI)**: 
   - คลิกซ้ายค้างไว้เพื่อตั้งจุดเริ่มต้น
   - ลากเมาส์เพื่อสร้างพื้นที่ที่ต้องการเลือก
   - ปล่อยเมาส์เพื่อสิ้นสุดการเลือก
3. **ระบบจะแสดงข้อความที่ OCR อ่านได้**: ระบบจะแสดงข้อความที่ดึงได้จากพื้นที่ที่เลือก และบันทึกข้อความนั้นลงไฟล์ `.txt`
4. **กด 'q' เพื่อออกจากโปรแกรม**: เมื่อเสร็จสิ้น กด `q` เพื่อปิดหน้าต่างและออกจากโปรแกรม.

### Summary of Code Usage:

1. **Select the image you want**: When the program starts, a window will pop up for you to choose an image file (supported formats: `.jpg`, `.jpeg`, or `.png`).
2. **Select the area to crop (ROI)**: 
   - Click and hold the left mouse button to define the starting point.
   - Drag to create the desired selection area.
   - Release the mouse button to finish the selection.
3. **OCR will extract text**: The system will display the extracted text from the selected region and save it to a `.txt` file.
4. **Press 'q' to exit the program**: Once finished, press `q` to close the window and end the program.

https://youtu.be/T-Fv02q335g?si=AtLSvZP-WuNLW-4P
