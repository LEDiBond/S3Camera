import cv2
import json

pred = json.load(open("result.json"))
image = cv2.imread("CURRENT_IMG.jpg")

colors = (0,255,255)

for objects in pred[0].get('objects'):
    yolo_coordinates = []
    label = objects.get('name')
    confidence = objects.get('confidence')
    center_x = objects.get('relative_coordinates').get('center_x')*image.shape[1]
    center_y = objects.get('relative_coordinates').get('center_y')*image.shape[0]
    width = objects.get('relative_coordinates').get('width')*image.shape[1]
    height = objects.get('relative_coordinates').get('height')*image.shape[0]

    x_start = int(round(center_x - (width / 2)))
    y_start = int(round(center_y - (height / 2)))
    x_end = int(round(center_x + (width / 2)))
    y_end = int(round(center_y + (height / 2)))

    print(str(x_start) + ":"+ str(y_start)+ ":" + str(x_end) + ":"+ str(y_end))
    image = cv2.rectangle(image, (x_start, y_start), (x_end, y_end), colors, 1)
    cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                                   (x_start, y_start - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                   colors, 2)

cv2.imwrite("box_img.jpg", image)
