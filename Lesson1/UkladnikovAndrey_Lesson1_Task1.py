#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json

def get_repositories(api_url, target_url):
    result_data=[]
    response = requests.get(api_url+target_url)
    j_data=json.loads(response.text)
    for item in j_data:
        result_data.append(item.get('name'))
    return response.status_code,result_data

github_api_url="https://api.github.com/"
username="AndreyU123"
repositories_url=f"users/{username}/repos"
status,data = get_repositories(github_api_url,repositories_url)

print(status)
print(data)
with open("ukladnikov_andrey_lesson1_data.json","w") as jsonfile:
    jsonfile.write(json.dumps(data))
