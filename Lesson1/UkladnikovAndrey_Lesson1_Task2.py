#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
import requests
import json

def get_repositories_authorization(api_url, target_url,username,password):
    result_data=[]
    response = requests.get(api_url+target_url, auth=(username, password))
    j_data=json.loads(response.text)
    for item in j_data:
        result_data.append(item.get('name'))
    return response.status_code,result_data


github_api_url="https://api.github.com/"
username="AndreyU123"
password="somepassword"
repositories_url=f"users/{username}/repos"
status,data = get_repositories_authorization(github_api_url,repositories_url,username,password)

print(status)
print(data)
with open("ukladnikov_andrey_lesson1_data.json","w") as jsonfile:
    jsonfile.write(json.dumps(data))