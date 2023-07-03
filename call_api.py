import requests
import cv2
import numpy as np
import json

# Open and encode image
image_path = './assets/readme_assets/own_pics/two_potato.jpg'
img = cv2.imread(image_path)
_, img_encoded = cv2.imencode('.jpg', img)
byte_array = img_encoded.tobytes()

# Prepare request payload
payload = {
    'img': list(byte_array),
    'plate_diameter': 0.35,
}
# payload = {
#     'img': [1,2,3],
#     'plate_diameter': 0.35,
# }

# Send request to server
response = requests.post('http://localhost:8000/predict', json=payload)

# Parse response
if response.status_code == 200:
    result = response.json()
    print("Picture: ", image_path.split('/')[-1])
    print("Plate diameter: ", payload['plate_diameter'])
    #print("Food Type Match:", result['food_type_match'])
    #print("Weight:", result['weight'])
    print("Volume:", result['volume'])
    #print("Density:", result['density'])
else:
    print("Error:", response.status_code)
