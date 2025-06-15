import os
import time
import pyautogui
import requests
from botcity.core import DesktopBot
from botcity.maestro import *

# Enable BotMaestro even if not connected
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Directory to save files
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "tjm-project")
os.makedirs(SAVE_DIR, exist_ok=True)


# Function to fetch posts from API
def fetch_posts(limit=10):
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        response.raise_for_status()
        return response.json()[:limit]
    except requests.RequestException as e:
        print("Failed to fetch posts:", e)
        return []


# Function to open Notepad
def open_notepad():
    os.system("start notepad")
    time.sleep(2)  # Wait for Notepad to open


# Function to type post content into Notepad and save it
def type_and_save(post_id, title, body):
    content = f"Title: {title}\n\n{body}"

    pyautogui.write(content, interval=0.15)

    # Save the file
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    filepath = os.path.join(SAVE_DIR, f"post_{post_id}.txt")
    pyautogui.write(filepath)
    pyautogui.press("enter")
    time.sleep(1)

    # Close Notepad
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)


# Main function
def main():
    # Maestro integration
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID: {execution.task_id}")
    print(f"Parameters: {execution.parameters}")

    bot = DesktopBot()

    posts = fetch_posts()
    for post in posts:
        open_notepad()
        type_and_save(post["id"], post["title"], post["body"])

    # Optional: Mark task as finished
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="All posts saved successfully.",
    #     total_items=len(posts),
    #     processed_items=len(posts),
    #     failed_items=0
    # )


# Not-found handler
def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
