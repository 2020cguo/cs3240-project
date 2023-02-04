from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class uva_class(models.Model):
        instructor_name = models.CharField(max_length=200)
        instructor_email = models.CharField(max_length=200)
        course_number = models.IntegerField()
        semester_code = models.IntegerField()
        course_section = models.CharField(max_length=200)
        subject = models.CharField(max_length=200)
        catalog_number = models.CharField(max_length=200)
        description = models.CharField(max_length=200)
        units = models.CharField(max_length=200)
        component = models.CharField(max_length=200)
        class_capacity = models.IntegerField()
        wait_list = models.IntegerField()
        wait_cap = models.IntegerField()
        enrollment_total = models.IntegerField()
        enrollment_available = models.IntegerField()
        topic = models.CharField(max_length=200)
        days = models.CharField(max_length=200)
        start_time = models.CharField(max_length=200)
        end_time = models.CharField(max_length=200)
        facility_description = models.CharField(max_length=200)
        def __str__(self):
            return self.description

class uva_dept(models.Model):
    subject = models.CharField(max_length = 10)
    def __str__(self):
        return self.subject

class users(models.Model):
    username = models.CharField(max_length=100)  
    course = models.IntegerField(default=0)   # contains course numbers of the courses they've added

class friendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = 'from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name = 'to_user', on_delete=models.CASCADE)

class friendship(models.Model):
    friend1 = models.ForeignKey(User, related_name = 'friend_1', on_delete=models.CASCADE)
    friend2 = models.ForeignKey(User, related_name = 'friend_2', on_delete=models.CASCADE)

class comment(models.Model):
    poster = models.ForeignKey(User, related_name = 'poster', on_delete=models.CASCADE)
    postee = models.ForeignKey(User, related_name = 'postee', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
