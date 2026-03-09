"""
core/vision_engine.py
=====================
Vision AI Engine — يُستدعى من inspections/views.py

الدالة: analyze_cable_image(image_path)
  - تاخد path الصورة
  - ترجع (result_image_path, data_dict)
"""

import os
import cv2
import numpy as np
from ultralytics import YOLO

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
PIXELS_PER_MM = 18.5
CONF_THRESHOLD = 0.01

# Path to YOLO model (stored inside core/ai_models/)
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CORE_DIR, "ai_models", "best.pt")

# Directory to save result images
RESULTS_DIR = os.path.join(CORE_DIR, "..", "media", "inspections", "results")


def _get_cable_specs(diameter_mm: float) -> dict:
    """Return estimated specs based on cable diameter."""
    if diameter_mm >= 40:
        return {
            "Voltage Class": "Medium Voltage (11 kV - 33 kV)",
            "Conductor": "Class 2 (Compacted Copper/Al)",
            "Insulation": "XLPE + Semi-conductive Layer",
            "Sheath Mat.": "HDPE / PVC (Red/Black)",
            "Cable Type": "Heavy Duty Power Feeder"
        }
    elif 15 <= diameter_mm < 40:
        return {
            "Voltage Class": "Low Voltage (0.6/1 kV)",
            "Conductor": "Class 2 (Stranded Copper)",
            "Insulation": "XLPE (Cross-linked PE)",
            "Sheath Mat.": "PVC (Black/UV Resistant)",
            "Cable Type": "Power Cable (Armoured)"
        }
    else:
        return {
            "Voltage Class": "Low Voltage (300/500 V)",
            "Conductor": "Class 1 (Solid Copper)",
            "Insulation": "PVC (Polyvinyl Chloride)",
            "Sheath Mat.": "PVC (Grey/White)",
            "Cable Type": "Control/Light Duty"
        }


def analyze_cable_image(image_path: str):
    """
    Analyze a cable cross-section image using YOLOv8 AI model.

    Args:
        image_path (str): Absolute path to the input image.

    Returns:
        tuple: (result_image_path: str | None, data: dict)
               result_image_path — path to the annotated result image saved to media/
               data — dict with keys: status, diameter_mm, defect_detected,
                      confidence_score, raw_data
    """
    # 1. Check model exists
    if not os.path.exists(MODEL_PATH):
        return None, {
            "status": "ERROR",
            "diameter_mm": None,
            "defect_detected": False,
            "confidence_score": None,
            "raw_data": {"error": f"Model not found at {MODEL_PATH}"}
        }

    # 2. Load YOLO model
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        return None, {
            "status": "ERROR",
            "diameter_mm": None,
            "defect_detected": False,
            "confidence_score": None,
            "raw_data": {"error": f"Model load failed: {str(e)}"}
        }

    # 3. Read Image (robust method for Windows paths)
    try:
        img_stream = np.fromfile(image_path, dtype=np.uint8)
        img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image decoding returned None.")
    except Exception as e:
        return None, {
            "status": "ERROR",
            "diameter_mm": None,
            "defect_detected": False,
            "confidence_score": None,
            "raw_data": {"error": f"Failed to read image: {str(e)}"}
        }

    # 4. Run YOLO Inference
    results = model(img, conf=CONF_THRESHOLD, verbose=False)

    # 5. Process Detections
    all_detections = []
    if results[0].boxes:
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            width_px = x2 - x1
            height_px = y2 - y1
            area = width_px * height_px
            conf = float(box.conf)
            diameter_mm = width_px / PIXELS_PER_MM

            all_detections.append({
                "box": (x1, y1, x2, y2),
                "width_px": width_px,
                "diameter_mm": diameter_mm,
                "area": area,
                "conf": conf
            })

    # 6. Smart Filtering — Take only the largest detection (main cable)
    if not all_detections:
        return None, {
            "status": "FAIL",
            "diameter_mm": None,
            "defect_detected": True,
            "confidence_score": None,
            "raw_data": {"note": "No cable detected in image"}
        }

    all_detections.sort(key=lambda x: x['area'], reverse=True)
    best = all_detections[0]

    x1, y1, x2, y2 = best['box']
    diameter_mm = best['diameter_mm']
    conf = best['conf']

    # 7. Quality Logic
    if diameter_mm > 5.0:
        status = "PASS"
        color = (0, 255, 0)   # Green
        defect = False
    else:
        status = "FAIL"
        color = (0, 0, 255)   # Red
        defect = True

    # 8. Draw Bounding Box on Image
    cable_specs = _get_cable_specs(diameter_mm)
    label = f"Dia: {diameter_mm:.1f} mm"
    (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
    cv2.rectangle(img, (x1, y1 - 30), (x1 + text_w + 20, y1), color, -1)
    cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # 9. Save Result Image
    result_image_path = None
    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        base_name = os.path.basename(image_path)
        result_filename = f"result_{base_name}"
        result_full_path = os.path.join(RESULTS_DIR, result_filename)
        cv2.imwrite(result_full_path, img)
        # Return the relative path from media/ for Django's FileField
        result_image_path = f"inspections/results/{result_filename}"
    except Exception as save_err:
        pass  # Result image is optional, don't fail the whole process

    return result_image_path, {
        "status": status,
        "diameter_mm": round(diameter_mm, 2),
        "defect_detected": defect,
        "confidence_score": round(conf, 4),
        "raw_data": {
            "width_px": best['width_px'],
            "cable_specs": cable_specs,
            "total_detections": len(all_detections),
        }
    }
