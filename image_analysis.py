import cv2


def get_image_information(image):
    height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "total_pixels": width * height
    }


def summarize_detections(detections):

    summary = {}

    for detection in detections:
        label = detection["label"]

        if label not in summary:
            summary[label] = 0

        summary[label] += 1

    return summary