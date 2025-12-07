import cv2
from pathlib import Path
from PIL import Image, ImageFilter

TEMPLATE = Path("C:\\Users\\parth\\OneDrive\\Desktop\\pickabook-prototype\\backend\\assets")
OUTPUT = Path("./outputs")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_crop(input_path):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        return input_path
    x, y, w, h = faces[0]
    crop = img[y:y+h, x:x+w]
    crop_path = Path(input_path).with_name("crop.png")
    cv2.imwrite(str(crop_path), crop)
    return str(crop_path)

def stylise(crop_path):
    img = Image.open(crop_path).convert("RGBA")
    img = img.resize((200, 200))
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    out = Path(crop_path).with_name("stylised.png")
    img.save(out)
    return str(out)

def composite(stylised_path):
    base = Image.open(TEMPLATE).convert("RGBA")
    face = Image.open(stylised_path).convert("RGBA")
    base.paste(face, (130, 80), face)
    out = OUTPUT / "final.png"
    base.save(out)
    return out

def process_image(input_path):
    crop = detect_crop(input_path)
    stylised = stylise(crop)
    final = composite(stylised)
    return final
