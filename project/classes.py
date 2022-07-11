import json
import re
import operator

from werkzeug.datastructures import FileStorage

from project.globals import DATA_PATH_ABS, IMG_PATH_ABS, PROJECT_PATH_ABS


class Repository:
    def __init__(self):
        self.posts_file = DATA_PATH_ABS.joinpath('data.json')
        self.bookmarks_file = DATA_PATH_ABS.joinpath('bookmarks.json')
        self.likes_file = DATA_PATH_ABS.joinpath('likes.json')
        self.comments_file = DATA_PATH_ABS.joinpath('comments.json')
        self.users_file = DATA_PATH_ABS.joinpath('users.json')

    # get posts

    def get_all_posts(self):
        with open(self.posts_file) as posts_file:
            all_posts = json.load(posts_file)
        all_posts_parsed = self.parse_post_hashtags(all_posts)
        return all_posts_parsed

    def get_post_by_id(self, searched_post_id):
        all_posts = self.get_all_posts()
        for post in all_posts:
            if post['pk'] == searched_post_id:
                return post

    def get_post_by_search_line(self, search_line):
        all_posts = self.get_all_posts()
        founded_posts = []
        for post in all_posts:
            if search_line.lower() in post['content'].lower():
                founded_posts.append(post)
        return founded_posts

    def get_post_by_user_name(self, user_name):
        all_posts = self.get_all_posts()
        founded_posts = []
        for post in all_posts:
            if post['poster_name'].lower() == user_name.lower():
                founded_posts.append(post)
        return founded_posts

    def get_post_by_tag(self, tag_name: str):
        searched_tag = f"#{tag_name.strip().lower()}"
        all_posts = self.get_all_posts()

        founded_posts = []
        for post in all_posts:
            hashtags_list = post['hashtags']
            if len(hashtags_list) == 0: continue

            for hashtag in hashtags_list:
                if searched_tag == hashtag.strip().lower():
                    founded_posts.append(post)
                    break

        return founded_posts

    def parse_post_hashtags(self, all_posts: list[dict]):
        """Получает контент поста и обворачивает хештеги ссылкой, если такой процедуры с постом не производилось ранее"""
        # Эта функция создана исключительно в этой работе, ибо гораздо проще всё это проделывать в функции добавления постов,
        # которой тут нет, и уже в структуре поста иметь ключ hashtags

        # Маркер на наличие изменений
        is_resave_needed = False

        for post in all_posts:
            # Если в структуре поста есть ключ hashtags, значит данный пост уже был проверен и обработан на наличие хештегов
            if post.get('hashtags') != None:
                continue
            # Дальнейший код уже потребует сохранение изменений в базе постов, поэтому...
            is_resave_needed = True

            # если нет хештегов - добавляем ключ с пустым списком
            if post['content'].count('#') == 0:
                post['hashtags'] = []
                continue

            # данный код выполнится в случае, если в тексте имеются хештеги

            # вычисляются все хештеги в список (после каждого хештега присутствует пробел, это важно, не спрашивайте зачем)
            hashtags = re.findall(r'(#\w+ )', post['content'])
            # каждый хештег в тексте заменяется на ссылку

            hashtags_links = []
            for hashtag in hashtags:
                hashtags_links.append(f"<a href='/tag/{hashtag[1:].strip()}'>{hashtag.strip()}</a>")
                post['content'] = post['content'].replace(hashtag, f"<a href='/tag/{hashtag[1:].strip()}'>{hashtag.strip()}</a> ", 1)
            # удаляем пробелы с концов хештегов для феншуя
            hashtags = list(map(lambda x: x.strip(), hashtags))
            # записываем хештеги и ссылки в ключи,
            post['hashtags'] = hashtags
            post['hashtags_links'] = hashtags_links

        # если были какие-нибудь изменения в базе - перезаписываем базу постов
        if is_resave_needed:
            self.rewrite_all_posts_after_parse_hashtags(all_posts)

        return all_posts

    def rewrite_all_posts_after_parse_hashtags(self, all_posts):
        with open(self.posts_file, 'w', encoding='utf-8') as posts_file:
            json.dump(all_posts, posts_file, ensure_ascii=False, indent=4)

    # comments
    def add_comment(self, post_id, commenter_name, comment):

        all_comments: list[dict] = self.get_all_comments()
        pk = len(all_comments)+1
        new_comment = {
                          "post_id": post_id,
                          "commenter_name": commenter_name,
                          "comment": comment,
                          "pk": pk
                      }
        all_comments.append(new_comment)
        all_comments.sort(key=operator.itemgetter('post_id'))

        with open(self.comments_file, 'w', encoding='utf-8') as comments_file:
            json.dump(all_comments, comments_file, ensure_ascii=False, indent=4)



    def get_all_comments(self):
        with open(self.comments_file) as comments_file:
            all_comments = json.load(comments_file)
        return all_comments

    def get_comments_by_post_id(self, searched_post_id):
        all_comments = self.get_all_comments()

        founded_comments = []
        for comment in all_comments:
            if comment['post_id'] == searched_post_id:
                founded_comments.append(comment)

        return founded_comments

    def get_user_bookmarks(self, user_id):
        with open(self.bookmarks_file) as file:
            all_bookmarks = json.load(file)

        user_bookmarks = all_bookmarks.get(user_id)

        return user_bookmarks

    def set_bookmark_state(self, user_id, post_id):
        user_bookmarks: list = self.get_user_bookmarks(user_id)
        if post_id in user_bookmarks:
            user_bookmarks.remove(post_id)
        else:
            user_bookmarks.append(post_id)

        with open(self.bookmarks_file) as file:
            all_bookmarks = json.load(file)

        all_bookmarks[user_id] = user_bookmarks

        with open(self.bookmarks_file, 'w') as file:
            json.dump(all_bookmarks, file, ensure_ascii=False, indent=4)

    def get_user_likes(self, user_id):
        with open(self.likes_file) as file:
            all_likes = json.load(file)

        user_likes = all_likes.get(user_id)

        return user_likes

    def change_user_like_state(self, user_id, post_id):
        user_likes: list = self.get_user_likes(user_id)
        if post_id in user_likes:
            user_likes.remove(post_id)
        else:
            user_likes.append(post_id)

        with open(self.likes_file) as file:
            all_likes = json.load(file)

        all_likes[user_id] = user_likes

        with open(self.likes_file, 'w') as file:
            json.dump(all_likes, file, ensure_ascii=False, indent=4)

    #users
    def get_all_users(self):
        with open(self.users_file) as users_file:
            users = json.load(users_file)
        return users

    def add_new_user(self, user_id: str, user_name: str):
        new_user_data_export = {user_id: user_name}
        users: dict[dict] = self.get_all_users()
        users.update(new_user_data_export)

        with open(self.users_file, 'w') as users_file:
            json.dump(users, users_file, ensure_ascii=False, indent=4)

    def set_post_likes_counter(self, post_id, accent):
        all_posts: list = self.get_all_posts()
        for index, post in enumerate(all_posts):
            if post['pk']==post_id:
                all_posts[index]['likes_count'] = all_posts[index]['likes_count']+accent
                break
        with open(self.posts_file, 'w') as file:
            json.dump(all_posts, file, ensure_ascii=False, indent=4)

    def set_views_counter(self, post_id):
        all_posts: list = self.get_all_posts()
        for index, post in enumerate(all_posts):
            if post['pk'] == post_id:
                all_posts[index]['views_count'] = all_posts[index]['views_count']+1
                break
        with open(self.posts_file, 'w') as file:
            json.dump(all_posts, file, ensure_ascii=False, indent=4)

    def get_post_by_user_bookmarks(self, user_bookmarks):
        all_posts = self.get_all_posts()
        user_bookmarked_posts = []
        for post in all_posts:
            if post['pk']  in user_bookmarks:
                user_bookmarked_posts.append(post)
        return user_bookmarked_posts

    def add_new_post(self, user_id, user_name, post_image, post_content: str):
        all_posts = self.get_all_posts()
        avatar_path = IMG_PATH_ABS.joinpath(user_id+'.jpeg') if IMG_PATH_ABS.joinpath(user_id+'.jpeg').exists() else IMG_PATH_ABS.joinpath(user_id+'.png')

        file_name = post_image.filename
        file_full_path = IMG_PATH_ABS.joinpath(file_name)
        post_image.save(file_full_path)

        all_posts_parsed = self.parse_post_hashtags(all_posts)
        new_post = {
        "poster_name": user_name,
        "poster_avatar": '/'+str(avatar_path.relative_to(PROJECT_PATH_ABS)),
        "pic": '/'+str(file_full_path.relative_to(PROJECT_PATH_ABS)),
        "content": post_content.replace('\r\n', ' \r\n')+' ',
        "views_count": 0,
        "likes_count": 0,
        "pk": len(all_posts)+1
    }



        # если нет хештегов - добавляем ключ с пустым списком
        if new_post['content'].count('#') == 0:
            new_post['hashtags'] = []

        # данный код выполнится в случае, если в тексте имеются хештеги

        # вычисляются все хештеги в список (после каждого хештега присутствует пробел, это важно, не спрашивайте зачем)
        hashtags = re.findall(r'(#\w+ )', new_post['content'])
        # каждый хештег в тексте заменяется на ссылку

        hashtags_links = []
        for hashtag in hashtags:
            hashtags_links.append(f"<a href='/tag/{hashtag[1:].strip()}'>{hashtag.strip()}</a>")
            new_post['content'] = new_post['content'].replace(hashtag, f"<a href='/tag/{hashtag[1:].strip()}'>{hashtag.strip()}</a> ", 1)
        # удаляем пробелы с концов хештегов для феншуя
        hashtags = list(map(lambda x: x.strip(), hashtags))
        # записываем хештеги и ссылки в ключи,
        new_post['hashtags'] = hashtags
        new_post['hashtags_links'] = hashtags_links





            #######
        all_posts.append(new_post)
        with open(self.posts_file, 'w') as posts_file:
            json.dump(all_posts, posts_file, ensure_ascii=False, indent=4)

        pass



class UserIDentifier:
    """Класс для работы с пользователем (идентификация, добавление в базу данных)"""

    # Как уникальный идентификатор я придумал привязаться к браузеру клиенту, в догонку добавить сумму регистров ip
    # По идее - эти данные постоянные, в то же время с разных браузеров получится "разные клиенты"
    # В общем выглядит вполне уникальным и постоянным ориентиром

    def __init__(self):
        self.users_data_file_path = DATA_PATH_ABS.joinpath('users.json')
        self.bookmarks_data_file_path = DATA_PATH_ABS.joinpath('bookmarks.json')
        self.likes_data_file_path = DATA_PATH_ABS.joinpath('likes.json')
        self.all_registered_users: dict = self.get_all_registered_users()

    def is_user_registered(self, request):
        """Возвращает ТРУ если пользователь есть в базе"""
        user_id = self.get_user_id(request)
        if user_id in self.all_registered_users:
            return True
        return False

    def get_user_name(self, request):
        """возвращает имя пользователя если он есть в базе"""
        user_id = self.get_user_id(request)
        if user_name := self.all_registered_users.get(user_id):
            return user_name
        return None


    def save_new_user_avatar(self, user_id, reg_avatar: FileStorage):
        file_extension = reg_avatar.content_type.split('/')[-1]
        file_full_path = IMG_PATH_ABS.joinpath(f"{user_id}.{file_extension}")
        reg_avatar.save(file_full_path)
        ...

    def get_all_registered_users(self):
        with open(self.users_data_file_path) as users_data:
            data = json.load(users_data)
        return data

    def save_new_user_id(self, user_id, user_name):
        data_to_export = {user_id: user_name}
        self.all_registered_users.update(data_to_export)

        with open(self.users_data_file_path, 'w') as users_file:
            json.dump(self.all_registered_users, users_file, ensure_ascii=False, indent=4)


    def register_new_user(self, request):
        #получили хеш
        new_user_id = self.get_user_id(request)
        #получили имя
        reg_name = request.values.get('reg_name')
        #получили файл
        reg_avatar = request.files.get('reg_avatar')

        #сохранили в базу id-name
        self.save_new_user_id(new_user_id, reg_name)


        #сохранили файл с именем файла = хеш пользователя
        self.save_new_user_avatar(new_user_id, reg_avatar)
        #добавили пользователя в закладки и лайки
        self.add_user_to_bookmarks(new_user_id)
        self.add_user_to_likes(new_user_id)

        print(f"New User ID generated: {new_user_id}")

    def get_user_id(self, request):
        import hashlib
        user_browser_agent = request.environ.get('HTTP_USER_AGENT')
        user_ip_adress_str = request.environ.get('REMOTE_ADDR')
        user_ip_adress_map_int = map(lambda register: int(register), user_ip_adress_str.split('.'))
        user_ip_adress_sum = str(sum(user_ip_adress_map_int))
        user_unique_str = f"{user_browser_agent}__{user_ip_adress_sum}"
        unique_id = hashlib.md5(user_unique_str.encode('utf-8')).hexdigest()
        return unique_id

    def add_user_to_bookmarks(self, new_user_id):
        with open(self.bookmarks_data_file_path) as file:
            all_bookmarks: dict = json.load(file)

        all_bookmarks.update({new_user_id:[]})

        with open(self.bookmarks_data_file_path, 'w') as file:
            json.dump(all_bookmarks, file, ensure_ascii=False, indent=4)

    def add_user_to_likes(self, new_user_id):
        with open(self.likes_data_file_path) as file:
            all_likes: dict = json.load(file)

        all_likes.update({new_user_id:[]})

        with open(self.likes_data_file_path, 'w') as file:
            json.dump(all_likes, file, ensure_ascii=False, indent=4)
