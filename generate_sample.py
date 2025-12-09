import cv2
import numpy as np

# Create a white image
img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Draw a black rectangle
cv2.rectangle(img, (100, 100), (400, 400), (0, 0, 0), 5)

# Draw a black circle
cv2.circle(img, (250, 250), 100, (0, 0, 0), 5)

# Draw some eyes
cv2.circle(img, (200, 220), 20, (0, 0, 0), -1)
cv2.circle(img, (300, 220), 20, (0, 0, 0), -1)

# Draw a mouth
cv2.ellipse(img, (250, 300), (60, 30), 0, 0, 180, (0, 0, 0), 5)

# Save the image
cv2.imwrite(r"C:\Users\adamb\Downloads\Github\RobotArtist\image_to_draw.jpg", img)
print("Sample image created: image_to_draw.jpg")
