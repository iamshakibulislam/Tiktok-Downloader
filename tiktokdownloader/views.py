from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from .custom import *
import json
from django.conf import settings
import os
from threading import Thread

def download_content_final(request):
	file_name = request.GET.get("name")
	file_path = os.path.join(settings.MEDIA_ROOT, f'{file_name}')
	return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{file_name}')

def index(request):
	return render(request,"index.html")


def download(request):

	if request.method == "GET":

		url = request.GET.get("url")

		url = url.strip()

		html = tiktok_link_grab(url)
		
		extracted_info = extract_tiktok_info(html)

		random_string = random.randint(473,993899)

		final_result = extracted_info

		print(final_result)
		print(type(final_result))

		mp4_url = final_result["download_link"]
		mp3_url = final_result["mp3"]

		print(mp4_url," and ",mp3_url)

		domain_name = request.get_host()

		mp4_name = str(domain_name)+"-"+str(random_string)+".mp4"
		mp3_name = str(domain_name)+"-"+str(random_string)+".mp3"


		mp4_thread = Thread(target=download_and_save_file,args=(mp4_url,mp4_name))
		mp3_thread = Thread(target=download_and_save_file,args=(mp3_url,mp3_name))

		mp4_thread.start()
		mp3_thread.start()

		mp4_thread.join()
		mp3_thread.join()

		extracted_info["download_link"] = mp4_name
		extracted_info["mp3"] = mp3_name

		data = json.dumps(extracted_info)

		return JsonResponse(extracted_info)

