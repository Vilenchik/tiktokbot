import hashlib
import pandas as pd
import os
import time
import urllib.request
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Pinterest credentials
username = "mail@mail.com"  # Your username
password = "password"  # Your password

# Function to calculate image hash
def get_image_hash(img_url):
    try:
        # Open image and calculate its hash
        response = urllib.request.urlopen(img_url)
        img_data = response.read()
        return hashlib.md5(img_data).hexdigest()
    except Exception as e:
        print(f"Error getting image hash: {e}")
        return None

# Chrome setup with the same profile
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\Vilen\ChromeBotProfile")  # You chrome profile folder
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # Uncomment for headless mode

# Launch Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Initialize variables
count = 0
csv_file = './data/downloaded_images.csv'
if os.path.exists(csv_file):
    image_table = pd.read_csv(csv_file)
else:
    image_table = pd.DataFrame(columns=['image_hash', 'image_path'])

try:
    """ Pinterest login if need
    driver.get("https://www.pinterest.com/login/")   
    time.sleep(7)
    
    # Check if we're already logged in (thanks to user-data-dir)
    if "login" not in driver.current_url.lower():
        print("Already logged in via Chrome profile")
    else:
        email_field = driver.find_element(By.NAME, "id")
        password_field = driver.find_element(By.NAME, "password")
        email_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(7) """

    # Wait for page to load after login
    time.sleep(7)

    # Go to search page with query "two cute cats" or use you complite pintrest board
    search_query = "two cute cats"
    driver.get("https://ru.pinterest.com/villpogosyan/two-cute-cats/")
    #driver.get(f"https://ru.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')}")

    # Wait for page to load
    time.sleep(10)

    # Create download folder with unique name (current date and time)
    folder_name = f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    download_dir = f"./data/image/{folder_name}"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Download images
    max_images = 7  # Set maximum number of images
    while count < max_images:
        images = driver.find_elements(By.TAG_NAME, "img")

        for image in images:
            if count >= max_images:
                break

            try:
                # Get URL from attributes
                img_url = image.get_attribute('srcset') or image.get_attribute('src')
                
                if not img_url:
                    continue
                    
                # If it's srcset with multiple variants
                if ',' in img_url:
                    variants = [v.strip().split(' ') for v in img_url.split(',')]
                    # Sort by density (1x, 2x, 4x)
                    variants.sort(key=lambda x: float(x[1].replace('x','')) if len(x)>1 else 0)
                    img_url = variants[-1][0]  # Take variant with highest density
                else:
                    img_url = img_url.split(' ')[0]
                
                # Add base URL if relative
                if img_url.startswith('/'):
                    img_url = 'https://i.pinimg.com' + img_url
                    
                # Verify URL is valid
                if not img_url.startswith('http'):
                    print(f"Invalid URL: {img_url}")
                    continue
                    
                # Further image processing
                img_hash = get_image_hash(img_url)
                if img_hash and img_hash not in image_table['image_hash'].values:
                    img_name = f"{download_dir}/cat_{count+1}_{datetime.now().strftime('%H%M%S')}.jpg"
                    
                    # Download with headers
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(img_url, img_name)
                    
                    count += 1
                    print(f"Downloaded {count} image: {img_name}")
                    time.sleep(7)
                    # Add record to table
                    new_row = pd.DataFrame({'image_hash': [img_hash], 'image_path': [img_name]})
                    image_table = pd.concat([image_table, new_row], ignore_index=True)
                    image_table.to_csv(csv_file, index=False)

            except Exception as e:
                print(f"Error downloading image: {e}")
                time.sleep(7)
        # Scroll page to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(7)

finally:
    # Close browser when done
    driver.quit()
    print(f"All {count} images downloaded!")