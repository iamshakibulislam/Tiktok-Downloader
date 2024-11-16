from bs4 import BeautifulSoup
import json
import re
import random

import requests
import requests

def download_and_save_file(url, new_filename):
    print(f"Downloading file from URL: {url} and saving as: {new_filename}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        print(f"Response status code: {response.status_code}")

        # Check if the response is successful
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type of response: {content_type}")

            # Ensure correct extension based on Content-Type
            if 'audio/mpeg' in content_type and not new_filename.endswith('.mp3'):
                new_filename += '.mp3'

            # Save the file
            with open("media/"+new_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded and saved as {new_filename}")
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def tiktok_link_grab(tiktoklink):

    cookies = {
        '__gads': 'ID=69cf2ea600b80e3ef:T=1728020227:RT=1728020227:S=ALNI_MaiNsaEGBd0sdLaEYTIHdSST1ZtPg',
        '__gpi': 'UID=00000ff23a13abc23:T=1728020227:RT=1728020227:S=ALNI_MZLRG3MDSyKHHuWpSSB3WmmcuDpJQ',
        '__eoi': 'ID=38d4cf3986f7ef27a:T=1728020227:RT=1728020227:S=AA-AfjalY-Ee5cQQFVEpLHrrIS0s',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__gads=ID=69cf2ea600b80e3ef:T=1728020227:RT=1728020227:S=ALNI_MaiNsaEGBd0sdLaEYTIHdSST1ZtPg; __gpi=UID=00000ff23a13abc23:T=1728020227:RT=1728020227:S=ALNI_MZLRG3MDSyKHHuWpSSB3WmmcuDpJQ; __eoi=ID=38d4cf3986f7ef27a:T=1728020227:RT=1728020227:S=AA-AfjalY-Ee5cQQFVEpLHrrIS0s',
        'hx-current-url': 'https://ssstik.io/',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': f'{tiktoklink}',
        'locale': 'en',
        'tt': 'a19Vjdl'+str(random.randint(500,99999)),
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

    return response.content.decode('utf-8')

def extract_tiktok_info(html_string):
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Extract background image URL from style tag
    style_tag = soup.find('style')
    background_image = ''
    if style_tag:
        match = re.search(r'background-image: url\((.*?)\)', style_tag.text)
        if match:
            background_image = match.group(1)
    
    # Extract author image
    author_img = soup.find('img', class_='result_author')
    author_image = author_img['src'] if author_img else ''
    
    # Extract heading text - raw text
    heading = soup.find('h2')
    head_text = heading.text if heading else ''
    
    # Extract main text - raw text
    main_text = soup.find('p', class_='maintext')
    maintext = main_text.text if main_text else ''
    
    # Extract download link
    download_link_tag = soup.find('a', string=lambda text: text and 'Without watermark' in text)
    download_link = download_link_tag['href'] if download_link_tag else ''
    
    # Extract MP3 link - match just "MP3"
    mp3_tag = soup.find('a', string=lambda text: text and 'MP3' in text)
    mp3_link = mp3_tag['href'] if mp3_tag else ''
    
    # Create response dictionary
    response = {
        "background_image": background_image,
        "author_image": author_image,
        "head_text": head_text,
        "maintext": maintext,
        "download_link": download_link,
        "mp3": mp3_link
    }
    
    return response



