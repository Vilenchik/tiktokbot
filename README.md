# TikTok Auto-Uploader Bot 🤖🎥

## 📌 Project Description

Automated Python solution for creating and uploading content to TikTok. The system:

1. 🖼️ Downloads images from Pinterest 
2. 🎬 Creates engaging slideshow videos with music
3. ⬆️ Auto-uploads to TikTok with optimized descriptions

Perfect for content creators managing pet/animal/cute content channels.

## 🛠️ Tech Stack

- Python 3.10+
- Selenium (Browser automation)
- MoviePy (Video editing)
- Pandas (Data tracking)
- WebDriverManager (Chrome management)

## 📂 Project Structure
tiktokbot/
├── data/
│ └── image/ # 
│ └── music/ # Background music (MP3)
│ └── downloaded_images.csv # Download history
├── output/ # Final videos
├── README.md
├── tiktokloader.py # TikTok uploader
├── imageloader.py # Pinterest downloader
├── tiktokloader.py # TikTok uploader
└── main_controller.py # Main scheduler

## 🚀 Quick Start

### Prerequisites
- Chrome/Firefox browser
- Python 3.10+
- FFmpeg installed
- Active TikTok account

### Installation

git clone https://github.com/Vilenchik/tiktokbot.git
cd tiktokbot
pip install -r requirements.txt


## Configuration
Edit credentials in imageloader.py:

username = "your@pinterest.email"
password = "yourpassword"
chrome_options.add_argument(r"user-data-dir=./ChromeBotProfile")
search_query = "two cute cats"
Add MP3 files to /music folder
max_images = 7  # Set maximum number of images

Edit credentials in tiktokloader.py:

CHROME_PROFILE_PATH = r"./ChromeBotProfile"
DEFAULT_DURATION = 15
RESOLUTION = (1080, 1920)
TIKTOK_DESCRIPTION = "❤️ #fyp #cutecat #couple #cat"