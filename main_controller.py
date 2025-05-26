# main_controller.py - automatic launch every 3 hours
import os
import subprocess
import time
from datetime import datetime

def run_scripts():
    """Run both scripts sequentially"""
    print(f"\n{'='*50}")
    print(f"🚀 Starting process at {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # 1. Image loading
        print("\nRunning imageloader.py...")
        subprocess.run(["python", "imageloader.py"], check=True)
        
        # 2. TikTok upload
        print("\nRunning tiktokloader.py...")
        subprocess.run(["python", "tiktokloader.py"], check=True)
        
        print(f"\n✅ Process completed successfully at {datetime.now().strftime('%H:%M:%S')}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Script error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    print("🔄 TikTok auto-uploader started")
    print("📌 Script will run every 3 hours")
    print("🛑 Press Ctrl+C to stop\n")
    
    while True:
        run_scripts()
        
        # Wait 3 hours before next run
        print(f"\n⏳ Next run at {(datetime.now() + timedelta(minutes=180)).strftime('%H:%M')}...")
        time.sleep(10800)  # 3 hours = 10800 seconds

if __name__ == "__main__":
    try:
        from datetime import timedelta  # Moved import here for convenience
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")