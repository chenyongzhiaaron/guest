from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

# Create your tests here.
from sign.models import Event, Guest


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name='相亲会', status=True, limit=2000, address='深圳', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='rose', phone='18828762234', email='rose@mail.com', sign=False)

    def test_event_model(self):
        result = Event.objects.get(id='1')
        self.assertEqual(result.address, '深圳')
        self.assertEqual(result.name, '相亲会')
        self.assertTrue(result.status)

    def test_guest_model(self):
        result = Guest.objects.get(phone='18828762234')
        self.assertEqual(result.realname, 'rose')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    def test_index_page_render_index_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginActionTest(TestCase):
    # 测试登录函数
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        # 用户名密码为空
        test_data = {'username': '', 'password': ''}
        response = self.c.post('/login_action', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)
    def test_login_action_username_password_error(self):
        # 用户名密码错误
        test_data ={'username': 'abc', 'password': "123"}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        # 登录成功
        test_data = {'username': 'admin', 'password': "admin123456"}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)
        # self.assertIn()

class EventManageTest(TestCase):
    # 发布会管理
    def setUp(self):
        Event.objects.create(id=2, name='见面会', limit=2000, status=True, address='北京', start_time=(2017, 8, 9, 2, 0, 0))
        self.c = Client()

    def test_event_manage_success(self):
        # 测试 见面会
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('见面会', response.content)
        self.assertIn('北京', response.content)

    def test_event_manage_search_success(self):
        # 测试发布会搜索
        response = self.c.post('/search_name/', {'name': '见面会'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('见面会', response.content)
        self.assertIn('北京', response.content)

class GuestManageTest(TestCase):
    # 嘉宾管理
    def setUp(self):
        Event.objects.create(id=1, name='xiaomi5', limit=2000, address='beijing', status=1, start_time=(2017, 8, 9, 12, 0, 0))
        Guest.objects.create(realname='rose', phone=18127813600, email='rose@mail.com', sign=0, event_id=1)
        self.c = Client()

    def test_event_manage_success(self):
        response = self.c.post('/guest_manage')
        self.assertEqual(response.status_code, 200)
        self.assertIn('rose', response.content)
        self.assertIn('18127813600', response.content)

    def test_guest_manage_search_success(self):
        # 测试嘉宾搜索 ‘rose’
        response = self.c.post('/search_phone/', {'phone': '18127813600'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('rose', response.content)
        self.assertIn('18127813600', response.content)

class SignIndexActionTest(TestCase):
    # 发布会签到
    def setUp(self):
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen', status=1, start_time='2017-6-10 12:30:00')
        Guest.objects.create(realname="alen", phone=18611001100, email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname="una", phone=18611001101, email='una@mail.com', sign=1, event_id=2)
        self.c = Client()

    def test__sign_index_action_phone_null(self):
        # 手机号为空
        response = self.c.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone error!', response.content)

    def test_sign_index_action_phone_or_event_id_erroe(self):
        # 手机号或发布会ID 错误
        response = self.c.post('/sign_index_action/2/', {'phone': '18611001100'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('event id or phone error!', response.content)

    def test_sign_index_action_user_sing_has(self):
        response = self.c.post('/sign_index_action/2/', {'phone': '18611001101'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("user has sign in", response.content)

    def test_sign_index_action_user_sign_success(self):
        response = self.c.post('/sign_index_action/1/', '18611001100')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sign in success', response.content)
