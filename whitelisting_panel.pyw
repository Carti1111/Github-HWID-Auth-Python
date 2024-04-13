import tkinter as tk
import tkinter.font as tkFont
import requests
import base64
import subprocess
import os
from colorama import Fore
import time

#Strings
hardwareid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
site = requests.get('https://raw.githubusercontent.com/Carti1111/HWID-Auth/main/auth.txt')

try:
    if hardwareid in site.text:
        pass
    else:
        print(f'{Fore.RED}[ERROR] {Fore.WHITE}Whitelist Secret Not Found')
        print(f'{Fore.RED}[HWID] {Fore.WHITE}Your HWID:' + hardwareid)
        time.sleep(1.35) 
        os._exit()
except:
    print(f'{Fore.RED}[ERROR] {Fore.WHITE}Code: 404')
    time.sleep(1.35) 
    os._exit() 

# GitHub repository information
GITHUB_TOKEN = 'github_pat_'
REPO_OWNER = 'Carti1111'
REPO_NAME = 'HWID-Auth'
BRANCH_NAME = 'main'  # Or whatever branch you want to modify
FILE_NAME = 'auth.txt'

def update_repository(content):
    try:
        # Prepare headers for GitHub API
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Get the existing file content
        existing_content_response = requests.get(
            f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}?ref={BRANCH_NAME}',
            headers=headers
        )

        if existing_content_response.status_code == 200:
            existing_content = existing_content_response.json()
            existing_content_decoded = base64.b64decode(existing_content['content']).decode('utf-8')
            updated_content = existing_content_decoded + '\n\n' + content
            content_bytes = updated_content.encode('utf-8')
            content_base64 = base64.b64encode(content_bytes).decode('utf-8')

            # Prepare data for updating the file
            update_data = {
                'message': 'Update file via Tkinter app',
                'content': content_base64,
                'sha': existing_content['sha'],  # SHA of the existing file
                'branch': BRANCH_NAME
            }

            # Update the file
            response = requests.put(
                f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}',
                headers=headers,
                json=update_data
            )

            if response.status_code == 200:
                return f'Whitelisted HWID: {content}'
            else:
                return f'Error Whitelisting HWID: {content}'
        else:
            return f'Error Getting Existing File Content: {existing_content_response.text}'

    except Exception as e:
        return f'Error: {str(e)}'

def whitelist():
    content = entry.get()
    response = update_repository(content)
    result_label.config(text=response)

# Create Tkinter window
window = tk.Tk()
window.title("HWID Whitelisting")

# Set window size and position
window_width = 400
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Create custom font
font_style = tkFont.Font(family="Helvetica", size=12)

# Input field for HWID
entry_label = tk.Label(window, text="Enter HWID:", font=font_style)
entry_label.pack(pady=10)
entry = tk.Entry(window, font=font_style)
entry.pack(pady=5)

# Button to whitelist HWID
whitelist_button = tk.Button(window, text="Whitelist", command=whitelist, font=font_style, bg="#4CAF50", fg="white")
whitelist_button.pack(pady=10)

# Label to display result
result_label = tk.Label(window, text="", font=font_style)
result_label.pack()

# Run the Tkinter event loop
window.mainloop()