import cv2
import httpx
import asyncio

def get_payload(image_path, plate_diameter):
    # Open and encode image
    img = cv2.imread(image_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    byte_array = img_encoded.tobytes()

    # Prepare request payload
    payload = {
        'img': list(byte_array),
        'plate_diameter': plate_diameter,
    }
    return payload

async def make_request(image_path, plate_diameter):
    payload = get_payload(image_path, plate_diameter)

    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:5000/predict', json=payload, timeout=60.0)

    # Parse response
    if response.status_code == 200:
        result = response.json()
        print("Picture: ", image_path.split('/')[-1])
        print("Plate diameter: ", payload['plate_diameter'])
        print("Volume:", result['volume'][0])
    else:
        print("Error:", response.status_code)

if __name__ == '__main__':
    asyncio.run(make_request('assets/readme_assets/own_pics/one_potato.jpg', 0.3))

