import face_recognition
import cv2
import numpy as np
import json
from models.employee import Employee
from sqlalchemy.orm import Session

def encode_face(image_path):
    """Encode face from image"""
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0].tolist()
    return None

def recognize_face(known_encodings, unknown_image_path):
    """Recognize face"""
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if not unknown_encodings:
        return None
    unknown_encoding = unknown_encodings[0]
    
    matches = face_recognition.compare_faces(known_encodings, unknown_encoding)
    if True in matches:
        return matches.index(True)
    return None

# Demo usage
def demo_face_attendance(db: Session):
    # Assume employees have encodings
    employees = db.query(Employee).all()
    known_encodings = [json.loads(e.face_encoding) for e in employees if e.face_encoding]
    # Capture from webcam or file
    print("Face recognition demo - implement webcam capture in production")