from langchain.document_loaders import YoutubeLoader
import json
import time

start_time = time.time()

input_file = "video_urls.json"
output_file = "transcripts.json"

with open(input_file, 'r') as file:
    data = json.load(file)

transcripts_dict = {}

"""
for key, url_list in data.items():
    dict_list = []
    for url in url_list:
        url_dict = {}
        loader = YoutubeLoader.from_youtube_url(
    url, add_video_info=True
)
        transcript = loader.load()
        url_dict[url] = transcript
        dict_list.append(url_dict)

    transcripts_dict[key] = dict_list
"""

url = data["42"][0]
dict_list = []

url_dict = {}
loader = YoutubeLoader.from_youtube_url(
    url, add_video_info=True
)
transcript = loader.load()
url_dict[url] = transcript
dict_list.append(url_dict)
transcripts_dict["42"] = dict_list

text = transcript[0]
start_index = text.find('page_content="') + len('page_content="')
end_index = text.find('"', start_index)
page_content = text[start_index:end_index]
print(page_content)



"""
with open(output_file, 'w') as file:
    json.dump(transcripts_dict, file, indent=2)
"""
print(f"Time elapsed was {time.time() - start_time}")