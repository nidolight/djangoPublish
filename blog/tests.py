from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag

class TestView(TestCase):
    def setUp(self):
        self.client = Client() # Client는 장고에서 테스트를 위한 가상의 사용자
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World!!!',
            category=self.category_programming,
            author=self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='Nice to meet you.',
            category=self.category_music,
            author=self.user_obama,
        )
        self.post_002.tags.add(self.tag_python_kor)
        self.post_002.tags.add(self.tag_python)

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='Nice to meet you too.',
            author=self.user_obama,
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})',
                      categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        # self.assertIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertIn(self.tag_python.name, post_002_card.text)
        self.assertIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertNotIn(self.tag_python.name, post_003_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)


    def test_post_detail(self):
        # # 1.1 포스트가 하나 있다.
        # post_001 = Post.objects.create(
        #     title='첫 번째 포스트입니다.',
        #     content='hello world!',
        #     author=self.user_trump,
        # )

        # 1.2 그 포스트의 ulr은 '/blog/1/1'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(status code:200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)


        # 카테고리 카드 테스트
        self.category_card_test(soup)

        # Tag 기능 테스트
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)



    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)


    # def test_post_list(self):
    #     # 1.1 포스트 목록 페이지 가져온다.
    #     response = self.client.get('/blog/')
    #
    #     # 1.2 정상적으로 페이지가 로드 된다.
    #     self.assertEqual(response.status_code, 200)
    #
    #     # 1.3 페이지 타이틀은 'Blog'다.
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     self.assertEqual(soup.title.text, 'Blog')
    #
    #     # # 1.4 내비게이션 바가 있다.
    #     # navbar = soup.nav
    #     #
    #     # # 1.5 Blog, Aout Me라는 문구가 내비게이션 바에 있다.
    #     # self.assertIn('Blog', navbar.text)
    #     # self.assertIn('About Me', navbar.text)
    #     self.navbar_test(soup)
    #
    #     # 2.1 메인 영역에 게시물이 하나도 없다면
    #     # (TestCase에서는 새로운 DB를 따로 만들어 사용하므로 비어있다.)
    #     self.assertEqual(Post.objects.count(), 0)
    #
    #     # 2.2 '아직 게시물이 없습니다'라는 문구 출력
    #     main_area = soup.find('div', id='main-area')
    #     self.assertIn('아직 게시물이 없습니다.', main_area.text)
    #
    #     # 3.1 게시물이 2개 이상이라면
    #     # (비어있으므로 게시물 2개를 만들어준다.)
    #     post_001 = Post.objects.create(
    #         title='첫 번째 포스트입니다.',
    #         content='Hello World!!!',
    #         author=self.user_trump,
    #     )
    #     post_002 = Post.objects.create(
    #         title='두 번째 포스트입니다.',
    #         content='Nice to meet you.',
    #         author=self.user_obama,
    #     )
    #     self.assertEqual(Post.objects.count(), 2)
    #
    #     # 3.2 포스트 목록 페이지를 새로고침했을 때
    #     response = self.client.get('/blog/')
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     self.assertEqual(response.status_code, 200)
    #
    #     # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
    #     main_area = soup.find('div', id='main-area')
    #     self.assertIn(post_001.title, main_area.text)
    #     self.assertIn(post_002.title, main_area.text)
    #
    #     # 3.4 ' 아직 게시물이 없습니다' 라는 문구는 더이상 보이지 않는다.
    #     self.assertNotIn('아직 게시물이 없습니다', main_area.text)
    #
    #     # 4 포스트 목록 페이지에 작성자 추가된 것 확인
    #     self.assertIn(self.user_trump.username.upper(), main_area.text)
    #     self.assertIn(self.user_obama.username.upper(), main_area.text)
