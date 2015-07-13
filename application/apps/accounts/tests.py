# coding=utf-8
import random
import string
from django.template import Template, Context
from application import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from application.apps.accounts.forms import SignupForm
from functions import old_pw_crypt
import models

def create_users(num=None):
    if not num:
        num = 10

    for i in range(num):
        email = '%s@returngreat.com' % ''.join([random.choice(string.ascii_lowercase) for x in range(40)])
        form = SignupForm(data={
            'first_name': 'Firstname_%s' % random.choice(string.ascii_uppercase),
            'last_name': 'Lastname_%s' % random.choice(string.ascii_uppercase),
            'phone': '07%s' % ''.join([random.choice(string.digits) for x in range(8)]),
            'email': email,
            'email_confirm': email,
            'business_name': ''.join([random.choice(string.ascii_letters) for x in range(20)]),
            'country': 'Sweden',
            'address': '%s 22' % ''.join([random.choice(string.ascii_letters) for x in range(20)]),
            'addres_zipcode': ''.join([random.choice(string.digits) for x in range(5)]),
            'address_city': ''.join([random.choice(string.ascii_letters) for x in range(15)]),
            'password': ''.join([random.choice(string.ascii_letters) for x in range(15)]),
            'terms': True
        })

        if form.is_valid():
            form.save()

class AccountTests(TestCase):
    def test_create_user(self):
        """
        Test create user
        """

        u = User()
        u.username = "test@test.se"
        u.email = "test@test.se"
        u.password = "asdf"
        u.save()

        db_user = User.objects.get(pk=1)
        db_user_profile = db_user.get_userprofile()

        self.failUnless(u.email == db_user.email)
        self.failUnless(db_user_profile)

    def test_create_business_profile(self):
        """
        Test #2 create business profile
        """

        u = User()
        u.username = "test@test.se"
        u.email = "test@test.se"
        u.password = "asdf"
        u.save()

        db_user = User.objects.get(pk=1)
        user_profile = db_user.get_userprofile()
        db_user_profile = models.UserProfile.objects.get(pk=user_profile.pk)

        business_profile = models.BusinessProfile(business_name="Test business", creator=db_user_profile)
        business_profile.save()

        db_user_profile.business_profiles.add(business_profile)
        db_user_profile.save()

        db_user = User.objects.get(pk=1)

        """ Check for exception if not active user profile, should throw exception """
        try:
            db_business_profile = db_user.get_business_profile()
        except ObjectDoesNotExist:
            pass
        else:
            self.fail()

        db_user_profile = db_user.get_userprofile()

        """ Does has_active_business_profile work? """
        self.failUnless(db_user_profile.has_active_business_profile() == False)

        """ Test to see if has any business profiles """
        self.failUnless(db_user_profile.has_business_profile() == True)

        """ Test number of business profiles """
        self.failUnless(db_user_profile.get_business_profiles().count() == 1)

        """ Add active profile """
        db_user_profile.active_profile = business_profile
        db_user_profile.save()

        db_user = User.objects.get(pk=1)

        """ Check for exception if not active user profile again, should not throw exception """
        try:
            db_business_profile = db_user.get_business_profile()
        except ObjectDoesNotExist:
            self.fail()

        """ Does has_active_business_profile work? (again) """
        self.failUnless(type(db_business_profile) == models.BusinessProfile)

        self.failUnless(db_user.get_userprofile().has_active_business_profile() == True)

        db_user = User.objects.get(pk=1)
        db_business_profile = db_user.get_business_profile()

        """ Test for the same business name """
        self.failUnless(db_business_profile.business_name == business_profile.business_name)

    def test_signup_form(self):
        """ Test signup """
        form_url = reverse('accounts:signup')
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'email': 'test@test.se',
            'email_confirm': 'test@test.se',
            'password': '123456',
            'first_name': 'TestF åäö',
            'last_name': 'asdf',
            'phone': '08-0123456',
            'business_name': 'Testföretag AB',
            'country': 'Sweden',
            'address': 'TestA Åäö 12345',
            'address_zipcode': '12345',
            'address_city': 'TestC Åäö',
        }
        response = self.client.post(form_url, post_data)
        self.assertEqual(response.has_header('location'), True)

        response = self.client.get('/')
        user = response.context['user']

        self.assertEqual(user.is_authenticated(), True)
        self.assertEqual(user.email, post_data['email'])

        # make sure it can also fail
        self.client.logout()
        self.client.get(form_url)

        post_data['email'] = 'notthesame@email.com'

        response = self.client.post(form_url, post_data)
        self.assertEqual(response.has_header('location'), False)

        response = self.client.get('/')
        user = response.context['user']

        self.assertEqual(user.is_authenticated(), False)

    def test_old_pw_crypt(self):
        """ Test old pw crypt function """
        pw = "Qwerty01"
        nonce = "d591d28621d98abe08124e4f42783943"
        end_hash = "789bedc01376ba0cbc1e5011b4f7d7e41981f1691808b663c877f43bad4a502b4cc1820a3d722e147f4dfdd9c78b61634dd33fc7517a595287fb6a3d46719f27"

        test_hash = old_pw_crypt(pw, nonce)
        #print test_hash

        self.failUnless(test_hash == end_hash)

    def test_change_language(self):
        for lang_code in settings.LANGUAGES:
            client = Client()
            client.get('/accounts/change_language/%s' % lang_code[0])

            self.failUnless(client.session['django_language'] == lang_code[0])

    def test_check_old_password(self):
        """ Test login with old password """

        email = "test@test.se"
        password = "testABC$$!!12345"
        nonce = "450f3b902c1eeff97c97669339dd7c8a"

        user = User(username=email, email=email, password="pbkdf2_sha256$10000$0$0=")
        user.save()

        models.OldPassword(user=user, old_password=old_pw_crypt(password, nonce), old_nonce=nonce).save()

        user = User.objects.get(username=email)

        try:
            old_password = models.OldPassword.objects.get(user=user)
        except:
            self.fail()

        """ Test simple db workings """
        self.failUnless(old_password.old_password == old_pw_crypt(password, old_password.old_nonce))

        auth_user = authenticate(username=email, password=password)

        """ Test for real! """
        self.failUnless(type(auth_user) == User)

        self.failUnless(auth_user.email == user.email)

    def test_login_view(self):
        client = Client()

        response = client.get(reverse('accounts:login'))
        self.failUnless(response.status_code == 200)

        User.objects.create_user('testuser@test.se', email='testuser@test.se', password='testpassword')

        kwargs = {
            'email': 'testuser@test.se',
            'password': 'testpassword'
        }
        response = client.post(reverse('accounts:login'), data=kwargs)
        self.assertEqual(response.has_header('location'), True)

        response = client.get('/')
        user = response.context['user']
        self.failUnless(user.is_authenticated())
        self.assertEqual(kwargs['email'], user.email)

    def test_flag_tag(self):
        flags = getattr(settings, 'FLAGS')
        flags_root = getattr(settings, 'FLAGS_ROOT')
        t = Template("""
            {% load accounts_extras %}
            {% flag LANGUAGE_CODE %}
        """)

        for lang in getattr(settings, 'LANGUAGES'):
            c = Context({'LANGUAGE_CODE': lang[0]})
            rendered = t.render(c)
            self.assertIn(flags_root, rendered)
