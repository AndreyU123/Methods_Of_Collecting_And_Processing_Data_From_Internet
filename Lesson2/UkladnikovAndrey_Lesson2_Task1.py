# Источник https://geekbrains.ru/posts
# Задача:
# Необходимо обойти все записи блога и получить следующую структуру информации:
# {
# "title": заголовок статьи,
# "image": Заглавное изображение статьи (ссылка),
# "text": Текст статьи,
# "pub_date": time_stamp даты публикации,
# "autor": {"name": Имя автора,
#                "url": ссылка на профиль автора,
#                },
# }
# по окончании сбора, полученые данные должны быть сохранены в json файл.
# В структуре должны присутсвовать все статьи на дату парсинга

from bs4 import BeautifulSoup
import requests
import json
import lxml

domain_url="https://geekbrains.ru"
blog_url="https://geekbrains.ru/posts"

def set_author( url, post_dict):
    page_data = requests.get(url)
    soup = BeautifulSoup(page_data.text, 'lxml')
    author_tag = soup.find('div', attrs={'itemprop':'author'})
    if author_tag == None:
        return
    author_txt = author_tag.text
    post_dict["author"]["name"]=author_txt
    author_url_tag = author_tag.parent()
    if author_url_tag == None:
        return
    post_dict["author"]["url"]=f"{domain_url}{author_tag.findParent('a').attrs.get('href')}"



def set_text( url, post_dict):
    page_data = requests.get(url)
    soup = BeautifulSoup(page_data.text, 'lxml')
    content_data = soup.find('div', class_='blogpost-content content_text content js-mediator-article').attrs.get('content')
    soup = BeautifulSoup(content_data,'lxml')

    imgs = soup.find_all('img')
    for img in imgs:
        content_data = content_data.replace(str(img).replace('/>','>'),"")

    refs = soup.find_all('a')
    for ref in refs:
        content_data = content_data.replace(str(ref).replace('/>', '>'), ref.text)

    content_data = content_data.replace('<p>','').replace('</p>','').replace('<h2>','').replace('</h2>','').replace('<strong>','').replace('</strong>','').replace('<li>','').\
        replace('</li>','').replace('</ol>','').replace('<ol>','')
    post_dict["text"]=content_data


def get_posts_list_per_page(soup):
    posts_list=[]
    posts_data=soup.find_all('div',class_='post-item')

    for post in posts_data:
        image=""
        if post.find('img')!= None:
            image = post.find('img').attrs.get('src')

        post_dict = {
            'title': post.find(class_="post-item__title").text,
            "image": image,
            "pub_date": post.find(class_="small m-t-xs").text,
            "text": "",
            "author": {"name": "", "url": "" }
        }
        set_text(f"{domain_url}{post.find('a').attrs.get('href')}",post_dict)
        set_author(f"{domain_url}{post.find('a').attrs.get('href')}",post_dict)
        posts_list.append(post_dict)
    return posts_list

def get_page_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data

def parser(url):
    posts_list=[]

    while True:
        soup = get_page_soup(url)
        posts_list.extend(get_posts_list_per_page(soup))
        try:
            url = soup.find('a',attrs={'rel':'next'},text='›').attrs.get('href')
        except AttributeError as e:
            break
        url = f"{domain_url}{url}"
    return posts_list

result_data = parser(blog_url)
with open("ukladnikov_andrey_lesson2_data.json","w", encoding="utf-8") as jsonfile:
    jsonfile.write(json.dumps(result_data,ensure_ascii=False,separators='\r\n'))



