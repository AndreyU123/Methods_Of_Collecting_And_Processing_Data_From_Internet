# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy
from scrapy.loader import ItemLoader

from InstagramExplorer.InstagramExplorer.items import InstagramExplorerItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    variables_posts_base = {'first' : 100}
    variables_post_base = {'include_reel': 'true','first': 100}
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    followings = {}
    base_url='https://www.instagram.com/'
    user_url_posts_suffix='/?__a=1'
    folowings_passed_posts={}

    def __init__(self, login, pwd, pars_users, posts_count_per_user, *args, **kwargs):
        self.login = login
        self.pwd = pwd
        self.pars_user_names = pars_users
        self.posts_count_per_user = posts_count_per_user
        self.query_hash = 'd04b0a864b4b54837c0d870b0e77e076'
        self.posts_query_hash='2c5d4d8b70cad329c4a6ebe3abb6eedd'
        self.post_query_hash='d5d763b1e2acf209d62d22d184488e57'
        self.exit_from_app=False
        super().__init__(*args, *kwargs)

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

        yield scrapy.FormRequest(
            inst_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def parse_users(self, response: HtmlResponse):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for pars_user_name in self.pars_user_names:
                yield response.follow(urljoin(self.start_urls[0], pars_user_name),
                                      callback=self.parse_user,
                                      cb_kwargs={'user': pars_user_name}
                                      )

    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars),
                              callback=self.parse_followings,
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )

    def parse_followings(self, response: HtmlResponse, user_vars, user):
        data = json.loads(response.body)
        if self.followings.get(user):
            self.followings[user]['user_data'].update({ f'{edge["node"]["username"]}'.replace(".","@") : {'full_name' : edge['node']['full_name'],'posts_with_comments' : []} for edge in data['data']['user']['edge_follow']['edges']})
        else:
            self.followings[user] = {'user_data': { f'{edge["node"]["username"]}'.replace(".","@") : {'full_name' : edge['node']['full_name'],'posts_with_comments' : []} for edge in data['data']['user']['edge_follow']['edges']}}

        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars)
            yield response.follow(next_page,
                                  callback=self.parse_followings,
                                  cb_kwargs={'user_vars': user_vars, 'user': user}
                                  )
        else:
            for following in self.followings[user]['user_data'].keys():
                self.folowings_passed_posts[following.replace("@",".")]=0
            for following in self.followings[user]['user_data'].keys():
                following_user=following.replace("@",".")
                yield response.follow(f'{self.start_urls[0]}{following_user}',
                                      callback=self.parse_following,
                                      cb_kwargs={'user' : user,'following_user' : following_user}
                                      )


    def parse_following(self,response: HtmlResponse, user, following_user):
        following_user_id = self.fetch_user_id(response.text, following_user)
        user_vars = deepcopy(self.variables_posts_base)
        user_vars.update({'id': following_user_id})
        url=f'{self.base_url}{following_user}{self.user_url_posts_suffix}'
        yield response.follow(url,
                              callback=self.parse_posts,
                              cb_kwargs={'user_vars': user_vars, 'user' : user, 'following_user': following_user}
                              )

    def parse_posts(self, response: HtmlResponse, user_vars, user, following_user):
        data = json.loads(response.body)
        if(data.get('graphql')):
            start_teg=data['graphql']
        else:
            start_teg=data['data']

        real_post_count=len(start_teg['user']['edge_owner_to_timeline_media']['edges'])
        for edge in start_teg['user']['edge_owner_to_timeline_media']['edges']:
            shortcode = edge['node']['shortcode']
            post_user_vars=deepcopy(self.variables_post_base)
            post_user_vars.update({'shortcode': shortcode})
            post_url=self.make_post_graphql_url(post_user_vars)


            yield response.follow(post_url,
                                  callback=self.parse_post,
                                  cb_kwargs={'user_vars': post_user_vars, 'user': user, 'following_user': following_user,'real_post_count':real_post_count}
                                  )
        if start_teg['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
            user_vars.update({'after': start_teg['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']})
            next_page = self.make_posts_graphql_url(user_vars)
            yield response.follow(next_page,
                                  callback=self.parse_posts,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,'following_user': following_user}
                                  )


    #likes - comments handled same, only query_hash other and additional variables
    def parse_post(self, response: HtmlResponse, user_vars, user, following_user,real_post_count):
        if self.folowings_passed_posts[following_user] > self.posts_count_per_user:
            return
        data = json.loads(response.body)
        shortcode=data['data']['shortcode_media']['shortcode']
        for edge in data['data']['shortcode_media']['edge_liked_by']['edges']:
            user_who_liked = edge['node']['username']
            if user == user_who_liked:
                if self.followings[user]['user_data'].get(following_user):
                    self.followings[user]['user_data'][following_user]['posts_with_comments'].append(f'{self.base_url}p/{shortcode}/')
                else:
                    self.followings[user]['user_data'][following_user]={'posts_with_comments' : [f'{self.base_url}p/{shortcode}/']}

        self.folowings_passed_posts[following_user] += 1
        is_exit = True
        for key in self.folowings_passed_posts.keys():
            if self.folowings_passed_posts[key] < min(self.posts_count_per_user,real_post_count):
                is_exit = False
                break
        if is_exit:  # and not self.exit_from_app: #for many users user we can do update in DB, if it exists
            #self.exit_from_app=True
            item = ItemLoader(InstagramExplorerItem(), response)
            item.add_value('user', user)
            item.add_value('following_users', self.followings[user])
            yield item.load_item()

        if data['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']})
            next_page = self.make_post_graphql_url(user_vars)
            yield response.follow(next_page,
                                  callback=self.parse_post,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,'following_user': following_user}
                                  )


    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        )
        if matched is not None:
            matched=matched.group()
        else:
            matched = re.search(
                '\"id\":\"\\d+\"', text
            ).group()
            matched="{"+matched+"}"
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        """Используя регулярные выражения парсит переданную строку на наличие
        `csrf_token` и возвращет его."""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def make_graphql_url(self, user_vars):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=self.query_hash,
            variables=urlencode(user_vars)
        )
        return result

    def make_posts_graphql_url(self, user_vars):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=self.posts_query_hash,
            variables=urlencode(user_vars)
        )
        return result

    def make_post_graphql_url(self, user_vars):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=self.post_query_hash,
            variables=urlencode(user_vars)
        )
        return result