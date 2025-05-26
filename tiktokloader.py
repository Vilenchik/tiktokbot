import os
import glob
import random
import time
import numpy as np
from PIL import Image
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip

# Settings
CHROME_PROFILE_PATH = r"C:\Users\Vilen\ChromeBotProfile" # You chrome profile folder
IMAGE_FOLDER = max(glob.glob("./data/image/images_*"), key=os.path.getmtime)
MUSIC_FOLDER = "./data/music" # You music folder
OUTPUT_FOLDER = "output"
DEFAULT_DURATION = 15  # Total video duration in seconds
RESOLUTION = (1080, 1920)  # Video resolution (vertical format)
TIKTOK_DESCRIPTION = "❤️ #fyp #cutecat #couple #cat" # You description

def setup_driver():
    """Configures Chrome browser"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def create_slideshow():
    """Creates a slideshow from images with music"""
    # Verify folders exist
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(MUSIC_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get list of images
    images = glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")) + \
             glob.glob(os.path.join(IMAGE_FOLDER, "*.jpeg")) + \
             glob.glob(os.path.join(IMAGE_FOLDER, "*.png"))
    
    if not images:
        raise ValueError(f"No images found in folder {IMAGE_FOLDER} (jpg, jpeg, png)")

    # Get list of music files
    music_files = glob.glob(os.path.join(MUSIC_FOLDER, "*.mp3"))
    if not music_files:
        print("⚠ No MP3 files found in music folder, video will be silent")

    # Create slides
    clips = []
    slide_duration = DEFAULT_DURATION / len(images)
    
    for img_path in images:
        img = Image.open(img_path).resize(RESOLUTION)
        clip = ImageSequenceClip([np.array(img)], durations=[slide_duration])
        clips.append(clip)
    
    video = concatenate_videoclips(clips)

    # Add music (if available)
    if music_files:
        music_path = random.choice(music_files)
        audio = AudioFileClip(music_path)
        
        # Trim music to match video duration
        audio = audio.subclip(20, DEFAULT_DURATION + 20)
        
        video = video.set_audio(audio)

    # Save video
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_FOLDER, f"slideshow_{timestamp}.mp4")
    
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    
    return output_path

def upload_to_tiktok(driver, video_path, description=TIKTOK_DESCRIPTION):
    """Uploads video to TikTok"""
    try:
        print("Opening TikTok upload page...")
        driver.get("https://www.tiktok.com/upload")
        time.sleep(10)
        
        # Check if logged in
        if "login" in driver.current_url.lower():
            input("❗ Please login to TikTok manually and press Enter...")
            time.sleep(5)
            driver.get("https://www.tiktok.com/upload")
            time.sleep(10)
        
        print("Uploading video...")
        upload_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_input.send_keys(os.path.abspath(video_path))
        time.sleep(15)
        
        # Add description
        print("Adding description...")
        caption_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        
        # Clear and enter text
        caption_box.send_keys(Keys.CONTROL + "a")
        caption_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        
        for char in description:
            caption_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
        
        # Publish
        print("Publishing video...")
        publish_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Публикация')]"))
        )
        publish_btn.click()
        
        # Wait for completion
        WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//button[contains(., 'Публикация')]")))
        print("✅ Video published successfully!")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        driver.save_screenshot("upload_error.png")
        raise

def main():
    try:
        # 1. Create slideshow
        print("Creating slideshow from images...")
        video_path = create_slideshow()
        print(f"Video created: {video_path}")
        
        # 2. Upload to TikTok
        print("Starting TikTok upload...")
        driver = setup_driver()
        try:
            upload_to_tiktok(driver, video_path)
        finally:
            driver.quit()
            
        print("🎉 Done! Video published to TikTok!")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()