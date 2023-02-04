import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'group_a_07.settings')
import django
django.setup()
from louslist.models import uva_class, uva_dept
import requests
import re

def update_dept_database():
    uva_dept.objects.all().delete()
    dept_names_api = 'http://luthers-list.herokuapp.com/api/deptlist/?format=json'
    dept_names = requests.get(dept_names_api)
    names_json = dept_names.json()
    for dept in names_json:
        new_dept = uva_dept()
        new_dept.subject = dept['subject']
        new_dept.save()

def update_class_database():
    ##should probably add something at the top of this to clear the uva_class table before rebuilding it\
    uva_class.objects.all().delete()
    dept_names_api = 'http://luthers-list.herokuapp.com/api/deptlist/?format=json'
    dept_names = requests.get(dept_names_api)
    names_json = dept_names.json()
    for i in names_json:
        new_link = 'http://luthers-list.herokuapp.com/api/dept/'+i['subject']+'?format=json'
        classes = requests.get(new_link)
        classes_json = classes.json()
        for j in classes_json:
            ## This is where we are accessing every class, creating a uva_class object(a row in the database uva_class table), and then saving it to the db
            ## probably want to put this in a try catch?
            new_instance = uva_class()##uva_class will be our model name
            new_instance.instructor_name = j['instructor']['name']
            new_instance.instructor_email = j['instructor']['email']
            new_instance.course_number = j['course_number']
            new_instance.semester_code = j['semester_code']
            new_instance.course_section = j['course_section']
            new_instance.subject = j['subject']
            new_instance.catalog_number = j['catalog_number']
            new_instance.description = j['description']
            new_instance.units = j['units']
            new_instance.component = j['component']
            new_instance.class_capacity = j['class_capacity']
            new_instance.wait_list = j['wait_list']
            new_instance.wait_cap = j['wait_cap']
            new_instance.enrollment_total = j['enrollment_total']
            new_instance.enrollment_available = j['enrollment_available']
            new_instance.topic = j['topic']
            if len(j['meetings']) != 0:
                new_instance.days = j['meetings'][0]['days']

                start_time = j['meetings'][0]['start_time']
                x = re.search("(\d{2})\.(\d{2})\.",start_time)
                if (x):
                    start_hour = int(x.group(1))
                    start_minute = x.group(2)
                    start_morning = "am"
                    if (start_hour >12):
                        start_hour = start_hour - 12
                        start_morning = "pm"
                    if (start_hour == 12):
                        start_morning = "pm"
                    new_instance.start_time = str(start_hour) + ":" + str(start_minute)+ start_morning
                else:
                    new_instance.start_time = ""
                end_time = j['meetings'][0]['end_time']
                y = re.search("(\d{2})\.(\d{2})\.",end_time)
                if (y):
                    end_hour = int(y.group(1))
                    end_minute = y.group(2)
                    end_morning = "am"
                    if (end_hour >12):
                        end_hour = end_hour - 12
                        end_morning = "pm"
                    if (end_hour == 12):
                        end_morning = "pm"
                    new_instance.end_time = str(end_hour) + ":" + str(end_minute)+ end_morning
                else:
                    new_instance.end_time = ""
                new_instance.facility_description = j['meetings'][0]['facility_description']
            else:
                new_instance.days = '-'
                new_instance.start_time = ''
                new_instance.end_time = ''
                new_instance.facility_description = '-'
            new_instance.save()

#uva_class.objects.all().delete()
update_class_database()
# update_dept_database()