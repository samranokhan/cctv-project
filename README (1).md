
# 🎓 Real-Time Face Detection and Logging System using OpenCV

This project is a real-time CCTV-like **student face recognition system** built using Python and OpenCV. It compares faces captured from the webcam against a folder of known images and logs the entry time. Unknown faces are saved to a separate folder for later review.

---

## 📌 Features

- 📷 Real-time webcam feed with face detection
- 🧠 Compares detected faces against known faces using simple pixel difference
- ✅ Logs the name and timestamp of recognized students
- ❓ Saves images of unknown faces (max 3 images per face)
- 🔴 Displays message for number of unknown faces per frame

---

## 📁 Folder Structure

```
📂 cctvproject/
 ┣ 📁 photos/                 # Folder with known faces (e.g. Ali.jpg, Sara.png)
 ┣ 📁 unknown/                # Auto-created folder for unknown faces
 ┣ 📄 face_recognition.py     # Main script
 ┣ 📄 log.csv                 # Attendance log file (Name, Timestamp)
 ┗ 📄 README.md               # Project documentation
```

---

## 🔧 Requirements

- Python 3.x
- OpenCV
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

---

## 🏃 How to Use

1. **Setup known faces**  
   Place known face images (e.g. `Ali.jpg`, `Sara.png`) in the `photos` folder.  
   File names will be used as names (e.g. `Ali.jpg` → `Ali`).

2. **Run the script**
```bash
python face_recognition.py
```

3. **Use the camera**
   - Webcam starts capturing video.
   - Detected faces are compared with known images.
   - Recognized students' names are shown in green with a rectangle.
   - Unrecognized faces are shown in red and saved (max 3 times each).
   - Press **`q`** to quit.

---

## 🧪 How It Works

- Uses Haar Cascade for face detection.
- Compares detected face (100x100 px) with known faces using absolute pixel difference.
- If similarity is high (score < 40), it considers it a match.
- Matched names are logged in `log.csv` with a timestamp.
- Unknown faces are hashed and saved if not already captured 3 times.

---

## ⚠️ Notes

- You may need to adjust `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)` depending on your camera.
- Image size is resized to 100x100 for comparison simplicity.
- The method used is not deep learning-based, but lightweight and fast for small-scale use.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**Samran Khan**  
GitHub: [@samranokhan](https://github.com/samranokhan)
