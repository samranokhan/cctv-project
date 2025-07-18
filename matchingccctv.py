import cv2
import numpy as np
import os
from datetime import datetime

# ── 1. Paths ─────────────────────────────────────────────
BASE_DIR      = r"C:\Users\pro5\OneDrive\Desktop\cctvproject"
photo_folder  = os.path.join(BASE_DIR, "photos")     # known boys
unknown_dir   = os.path.join(BASE_DIR, "unknown")    # unknown faces
os.makedirs(unknown_dir, exist_ok=True)

# ── 2. Load known faces ─────────────────────────────────
known_faces = {}
for fname in os.listdir(photo_folder):
    if fname.lower().endswith((".jpg", ".png")):
        path = os.path.join(photo_folder, fname)
        img = cv2.imread(path)
        if img is not None:
            face_img = cv2.resize(img, (100, 100))
            name = os.path.splitext(fname)[0].title()
            known_faces[name] = face_img
            print(f"✅ Loaded: {name}")
        else:
            print(f"⚠️ Could not read {fname}")

if not known_faces:
    print("❌ No valid images in photos folder.")
    exit()

# ── 3. Haar Cascade ─────────────────────────────────────
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ── 4. Start webcam ─────────────────────────────────────
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("❌ Cannot open webcam.")
    exit()

print("🎥 Webcam active. Press 'q' to quit.")
logged_names = set()
unknown_face_hashes = {}  # track unknown faces: {hash: count}

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame grab failed.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    unknown_count_this_frame = 0

    for (x, y, w, h) in faces:
        detected = frame[y:y+h, x:x+w]
        detected_resized = cv2.resize(detected, (100, 100))

        best_match = "Unknown"
        lowest_diff = float("inf")

        for name, known_img in known_faces.items():
            diff = cv2.absdiff(detected_resized, known_img)
            score = np.mean(diff)
            if score < lowest_diff:
                lowest_diff = score
                best_match = name

        THRESHOLD = 40
        if lowest_diff < THRESHOLD:
            label = best_match
            color = (0, 255, 0)
            if label not in logged_names:
                with open(os.path.join(BASE_DIR, "log.csv"), "a") as f:
                    f.write(f"{label},{datetime.now()}\n")
                print(f"✅ {label} detected at {datetime.now()}")
                logged_names.add(label)
        else:
            label = "Unknown"
            color = (0, 0, 255)
            unknown_count_this_frame += 1

            face_hash = hash(detected_resized.tobytes())
            count = unknown_face_hashes.get(face_hash, 0)

            if count < 3:  # save only max 3 images per unknown face
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(unknown_dir, f"unknown_{ts}.jpg")
                cv2.imwrite(save_path, detected)
                print(f"📷 Unknown face saved → {save_path}")
                unknown_face_hashes[face_hash] = count + 1

        # Draw label and box
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # ── 5. Show unknown face count message ───────────────
    if unknown_count_this_frame > 0:
        message = f"{unknown_count_this_frame} Unknown Face(s) Detected"
        cv2.putText(frame, message, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Student Scanner (Haar)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ── 6. Cleanup ──────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
print("📴 Session ended.")
