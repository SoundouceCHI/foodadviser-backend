from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('yolov8n.pt')

def detect_ingredients(image_path):
    """
    Effectue la détection d'objets sur une image donnée et formate les résultats.
    Args:
        image_path (str): Chemin de l'image.
    Returns:
        list: Liste unique des objets détectés.
    """
    
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image non trouvée au chemin : {image_path}")

    results = model(image)

    detected_objects = []
    for r in results[0].boxes.data:  
        _, _, _, _, confidence, class_id = r.cpu().numpy()
        label = results[0].names[int(class_id)]  

        detected_objects.append({"name": label})

    unique_detected_objects = list({obj["name"]: obj for obj in detected_objects}.values())

    return unique_detected_objects 
