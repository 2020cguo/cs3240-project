from django.test import TestCase
from .models import uva_class, uva_dept, friendRequest,friendship
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import client


# class DummyTestCase(TestCase):
#     def setUp(self):
#         x = 1
#         y = 2
    
#     def test_dummy_test_case(self):
#         self.assertEqual(1, 2)

# class DummyTestCase(TestCase):
#     def test_dummy_test_case(self):
#         self.assertEqual(1, 1)

class UVAClassTestCase(TestCase):
    def setUp(self):
        self.test_class = uva_class()
        self.test_class.instructor_name = 'Fake Professor'

    def test_uva_class_instantiation(self): 
        self.assertEqual('Fake Professor', self.test_class.instructor_name)
    
    def test_uva_class_empty_fields(self):
        self.assertEqual('',self.test_class.days)

class AddingUVAClassTestCase(TestCase):
    def setUp(self):
        self.test_class = uva_class()
        self.test_class.instructor_name = 'Fake Professor'
        self.test_class.instructor_email = ' '
        self.test_class.course_number = 0
        self.test_class.semester_code = 0
        self.test_class.course_section = ' '
        self.test_class.subject = ' '
        self.test_class.catalog_number = ' '
        self.test_class.description = ' '
        self.test_class.units = ' '
        self.test_class.component = ' '
        self.test_class.class_capacity = 0
        self.test_class.wait_list = 0
        self.test_class.wait_cap = 0
        self.test_class.enrollment_available = 0
        self.test_class.enrollment_total = 0
        self.test_class.topic = ' '
        self.test_class.days = ' '
        self.test_class.start_time = ' '
        self.test_class.end_time = ' '
        self.test_class.facility_description = ' '
        self.test_class.save()

    def test_uva_class_in_database(self):
        my_class = uva_class.objects.filter(instructor_name='Fake Professor')
        self.assertEqual(self.test_class,my_class.first())

    def tearDown(self):
        self.test_class.delete()

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@virginia.edu',
            username = 'testuser',
            password = 'password'
        )
        self.client.force_login(self.user)
        self.response = self.client.get('')
    def test_valid_response(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_correct_index(self):
        self.assertContains(self.response,'Welcome, testuser')

class UserNotLoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@virginia.edu',
            username = 'testuser',
            password = 'password'
        )
        self.response = self.client.get('')

    def test_valid_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_index(self):
        self.assertContains(self.response,'Please login to proceed to site')

class DepartmentDisplayTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@virginia.edu',
            username = 'testuser',
            password = 'password'
        )
        self.client.force_login(self.user)
        self.response = self.client.get('')
    
    def test_dept_present(self):
        for dept in uva_dept.objects.all():
            self.assertContains(self.response,dept)


# class SearchTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email = 'test@virginia.edu',
#             username = 'testuser',
#             password = 'password'
#         )
#         self.client.force_login(self.user)
#         self.response = self.client.get('submitSearch/',{'dept':'CS', 'description':'Advanced Software Development Techniques',
#         'number':'3240'})
#     def test_class_search(self):
#         self.assertContains(self.response,'001-LEC (15991)')

class FriendRequestTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(  
            email = 'test1@virginia.edu',
            username = 'testuser1',
            password = 'password'
        )
        self.user2 = User.objects.create_user(  
            email = 'test2@virginia.edu',
            username = 'testuser2',
            password = 'password'
        )
        self.client.force_login(self.user1)
        self.client.force_login(self.user2)
        self.test_request = friendRequest(from_user=self.user1,to_user=self.user2)
        self.test_request.save()

    def test_request_present(self):
        my_request = friendRequest.objects.filter(from_user=self.user1)
        my_request2 = friendRequest.objects.filter(to_user=self.user2)
        self.assertEqual(self.test_request,my_request.first())
        self.assertEqual(self.test_request,my_request2.first())

    def tearDown(self):
        self.test_request.delete()
        self.user1.delete()
        self.user2.delete()

class FriendshipTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(  
            email = 'test1@virginia.edu',
            username = 'testuser1',
            password = 'password'
        )
        self.user2 = User.objects.create_user(  
            email = 'test2@virginia.edu',
            username = 'testuser2',
            password = 'password'
        )
        self.client.force_login(self.user1)
        self.client.force_login(self.user2)    
        self.test_friendship = friendship(friend1=self.user1, friend2=self.user2)
        self.test_friendship.save()
    def test_request_present(self):
        my_friendship = friendship.objects.filter(friend1=self.user1)
        self.assertEqual(self.test_friendship,my_friendship.first())

    def tearDown(self):
        self.test_friendship.delete()
        self.user1.delete()
        self.user2.delete()        
    