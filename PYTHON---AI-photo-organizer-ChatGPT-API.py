import os
import shutil
from PIL import Image
import openai

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

# Function to analyze a photo and get its topic
def analyze_photo(photo_path):
    with open(photo_path, "rb") as image_file:
        content = image_file.read()
        # Send a prompt to ChatGPT describing the photo
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a photo categorizer."},
                {"role": "user", "content": "Categorize this image into a topic: Family, Nature, Beach, Pets, or Others."},
            ]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        return topic

# Function to organize photos by topics
def organize_photos(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Create a directory for organized photos
    organized_dir = os.path.join(folder_path, "Organized_Photos")
    os.makedirs(organized_dir, exist_ok=True)

    for photo in os.listdir(folder_path):
        photo_path = os.path.join(folder_path, photo)

        if not os.path.isfile(photo_path):
            continue

        try:
            topic = analyze_photo(photo_path)
            print(f"Photo: {photo}, Topic: {topic}")

            # Create topic folder
            topic_folder = os.path.join(organized_dir, topic)
            os.makedirs(topic_folder, exist_ok=True)

            # Move photo to topic folder
            shutil.move(photo_path, os.path.join(topic_folder, photo))
        except Exception as e:
            print(f"Error processing {photo}: {e}")

    print(f"Photos organized in {organized_dir}")

# Run the tool
folder_to_organize = "/path/to/your/photos"
organize_photos(folder_to_organize)
