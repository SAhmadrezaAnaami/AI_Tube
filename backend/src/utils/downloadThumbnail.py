import os
import requests

def download_thumbnail(image_url, filename):
    # Ensure the "thumbnails" directory exists
    os.makedirs('files/thumbnails', exist_ok=True)
    
    # Full path to save the file
    file_path = os.path.join('files/thumbnails', filename)
    
    # Download the image
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Write the image content to a file
    with open(file_path + ".jpg", 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Image downloaded successfully: {file_path}")