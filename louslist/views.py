from unittest import result
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from .models import uva_class, uva_dept, users, friendRequest, friendship,comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from autocorrect import Speller
import math


# def index(request):
#     departments = uva_dept.objects.all
#     depts_1 = []
#     depts_2 = []
#     for i in range(len(departments)):
#         if (i % 2 == 0):
#             depts_1.append(departments[i])
#         else:
#             depts_2.append(departments[i])
#     return render(request, 'louslist/index.html', {'dept_1': {depts_1}, 'dept_2': {depts_2}})

class IndexView(generic.ListView):
    template_name = 'louslist/index.html'
    context_object_name = 'dept_list'
    def get_queryset(self):
        return uva_dept.objects.all
    # return HttpResponse("Hello, world. You're at the lous list index.")
    #return render(request, 'louslist/index.html')

def add_class(request, course_number):
    User = request.user
    current_courses = users.objects.filter(username=User.username).all()
    # check if the current course overlaps with any other       
    course_overlaps = False
    same_course = False
    new_course = uva_class.objects.get(course_number=course_number)
    # line added to get rid of errors from classes with no time
    if len(new_course.start_time) < 1 or len(new_course.end_time) < 1:
        return HttpResponseRedirect("/louslist/schedule/")
    for entry in current_courses:
        old_course_number = entry.course
        old_course = uva_class.objects.get(course_number = old_course_number)
        if old_course.description == new_course.description and old_course.component == new_course.component:
            same_course = True
        if new_course.days in old_course.days or old_course.days in new_course.days:
            if compare_times(new_course.start_time, old_course.start_time) == 0 or compare_times(new_course.end_time, old_course.end_time) == 0:
                course_overlaps = True
            elif compare_times(new_course.start_time, old_course.start_time) == 1 and compare_times(new_course.start_time, old_course.end_time) == -1:
                course_overlaps = True
            elif compare_times(new_course.end_time, old_course.start_time) == 1 and compare_times(new_course.end_time, old_course.end_time) == -1:
                course_overlaps = True
            elif compare_times(old_course.start_time, new_course.start_time) == 1 and compare_times(old_course.start_time, new_course.end_time) == -1:
                course_overlaps = True
    if not course_overlaps and not same_course and len(current_courses) < 8:
        users.objects.create(username=User.username, course=course_number)
    return HttpResponseRedirect("/louslist/schedule/")

def compare_times(A, B):    
    # returns 1 if A is later than B, returns -1 if A is earlier than B, returns 0 if they're the same
    A_am_pm = A[-2:]
    B_am_pm = B[-2:]
    A_split = A.split(':')
    B_split = B.split(':')
    A_hour = int(A_split[0])
    if A_hour != 12 and A_am_pm == 'pm': 
        A_hour += 12
    B_hour = int(B_split[0])
    if B_hour != 12 and B_am_pm == 'pm': 
        B_hour += 12
    A_minutes = int(A_split[1][:-2])
    B_minutes = int(B_split[1][:-2])

    if A_hour > B_hour:
        return 1
    if A_hour < B_hour:
        return -1
    if A_minutes > B_minutes:
        return 1
    if A_minutes < B_minutes:
        return -1
    return 0

def delete_class(request, course_number):
    User = request.user
    users.objects.get(username=User.username, course=course_number).delete()
    return HttpResponseRedirect("/louslist/schedule/")

def course_list(request, subject):
    courses = uva_class.objects.filter(subject = subject).all()
    return render(request, 'louslist/detail.html', {'course_list': {courses}})

    
def friend_schedule(request, username):
    if request.user.is_authenticated:
        user_friendships = friendship.objects.filter(friend1=request.user)
        is_friend = False
        for i in user_friendships:
            if i.friend2.username == username:
                is_friend = True
                comments = comment.objects.filter(postee = i.friend2)
        if is_friend == True:
            query = users.objects.filter(username=username).all()
            output = []
            stimes = []
            etimes = []
            times = []
            days = ['Mo', 'Tu', 'We', 'Th', 'Fr']

            for entry in query:
                course = entry.course
                tempcourse = uva_class.objects.get(course_number = course)

                if len(tempcourse.start_time) > 1 and len(tempcourse.end_time) > 1:
                    output.append(tempcourse)
                    stimes.append(scheduleTime(tempcourse.start_time, "start"))
                    etimes.append(scheduleTime(tempcourse.end_time, "end"))

            times.append("0:00")
            for x in range(8,13):
                time1 = str(x) + ":00"
                time2 = str(x) + ":30"
                times.append(time1)
                times.append(time2)
            for x in range(1,10):
                time1 = str(x) + ":00"
                time2 = str(x) + ":30"
                times.append(time1)
                times.append(time2)

            return render(request, 'louslist/friendSchedule.html', {'course_schedule': output, 'starts': stimes, 'ends': etimes, 'times': times, 'days': days, 'username': username, 'comments':comments})

        else:
            return render(request, 'louslist/friendSchedule.html', {"error_message":"You are not friends with this user!"})
    else:
        return render(request, 'louslist/friendSchedule.html')

def search(request):
    # return HttpResponse("Hello, world. You're at the lous list index.")
    # Maybe here pass a variable thats empty to search html and then in submit search pass the actual results.  Then we can use the same template and just display results only when there was a search
    return render(request, 'louslist/search.html')

def submitSearch(request):
    spell = Speller()
    department = request.POST.get('dept')
    description = spell(request.POST.get('description'))
    number = request.POST.get('number')
    day = request.POST.get('day')
    time = request.POST.get('time')


    if (department == '' and description == '' and number == '' and day == '' and time == ''):
        return render(request, 'louslist/search.html', {'error_message': "You didnt enter anything, try again!"})
    result = uva_class.objects
    if (department != ''):
        result = result.filter(subject__iexact=department)
    if (description != ''):
        result = result.filter(description__icontains=description)
    if (number != ''):
        result = result.filter(catalog_number__iexact=number)
    if (day != ''):
        result = result.filter(days__iexact=day)
    if (time != ''):
        result = result.filter(start_time__iexact=time)

    if(len(result)==0):

        return render(request, 'louslist/search.html', {'error_message': "Whoops! Looks like your search didn't match anything in our database.", 'description':description, 'department':department, 'number':number, 'day':day, 'time':time})
    

    context = {'result': {result}, 'description':description, 'department':department, 'number':number, 'day':day, 'time':time}
    return render(request, 'louslist/search.html', context)

def schedule(request):
    if request.user.is_authenticated:
        User = request.user
        context_object_name='course_schedule'
        # username = User.objects.get(username = userID)
        query = users.objects.filter(username=User.username).all()
        output = []
        stimes = []
        etimes = []
        times = []
        days = ['Mo', 'Tu', 'We', 'Th', 'Fr']


        for entry in query:
            course = entry.course
            tempcourse = uva_class.objects.get(course_number = course)

            if len(tempcourse.start_time) > 1 and len(tempcourse.end_time) > 1:
                output.append(tempcourse)
                stimes.append(scheduleTime(tempcourse.start_time, "start"))
                etimes.append(scheduleTime(tempcourse.end_time, "end"))

        times.append("0:00")
        for x in range(8,13):
            time1 = str(x) + ":00"
            time2 = str(x) + ":30"
            times.append(time1)
            times.append(time2)
        for x in range(1,10):
            time1 = str(x) + ":00"
            time2 = str(x) + ":30"
            times.append(time1)
            times.append(time2)

        comments = comment.objects.filter(postee = User)
        return render(request, 'louslist/schedule.html', {'course_schedule': output, 'starts': stimes, 'ends': etimes, 'times': times, 'days': days, 'comments':comments})
    else:
        return render(request, 'louslist/schedule.html')


# function returns time as an int that can be compared to forloop iterator
def scheduleTime(x, state):
    if x[1] == ":":
        # newtime = time as float (3:30 = 3.30)
        newtime = float("0" + x[0] + "." + x[2] + x[3])
        # if time in pm and not 12pm
        if x[4] == "p" and x[1] != "2":
            # add 12 to get 24 hour time
            newtime = newtime + 12
        # multiply by 2 to get 30 minute intervals
        newtime = newtime * 2
        # round to int (calendar can't display a partial 30 minute interval)
        newtime = round(newtime)
        # subtract 14 to match forloop iterator
        newtime = newtime - 14

        # if time ends on the hour, subtract one (otherwise fills up extra cell)
        if (x[2] + x[3]) == "00" and state == "end":
            newtime = newtime - 1

    else:
        newtime = float(x[0] + x[1] + "." + x[3] + x[4])
        if x[5] == "p" and x[1] != "2":
            newtime = newtime + 12
        newtime = newtime * 2
        newtime = round(newtime)
        newtime = newtime - 14

        if (x[3]+x[4] == "00") and state == "end":
            newtime = newtime - 1

    return newtime

def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(username = userID)
    friend_request, created = friendRequest.objects.get_or_create(from_user = from_user, to_user = to_user)
    return HttpResponseRedirect(reverse('louslist:add_friend'))


def accept_friend_request(request, requestID):
    friend_request = friendRequest.objects.get(id=requestID)
    if (friend_request.to_user == request.user):
        friend, created = friendship.objects.get_or_create(friend1 = friend_request.from_user, friend2 = request.user)
        if created:
            friendship.objects.create(friend1 = request.user, friend2 = friend_request.from_user)
            friend_request.delete()
            return HttpResponseRedirect(reverse('louslist:friendPage'))
        else:
            friend_request.delete()
            return HttpResponseRedirect(reverse('louslist:friendPage'))
    else:
        return HttpResponseRedirect(reverse('louslist:friendPage'))

def decline_friend_request(request, requestID):
    friend_request= friendRequest.objects.get(id=requestID)
    if (friend_request.to_user == request.user):
        friend_request.delete()
    return HttpResponseRedirect(reverse('louslist:friendPage'))



def friendPage(request):
    if request.user.is_authenticated:
        friends = friendship.objects.filter(friend1 = request.user)
        requests = friendRequest.objects.filter(to_user = request.user)
        context = {'friend_list': friends, 'friendRequest_list': requests}
        return render(request, 'louslist/friend.html', context)
    else:
        return render(request, 'louslist/friend.html')

def addFriend(request):
    user_list = User.objects.exclude(username = request.user.username) #Get all users other than the current user
    friends = friendship.objects.filter(friend1 = request.user)
    for friend in friends:
        user_list = user_list.exclude(username = friend.friend2.username)
    pending_requests = friendRequest.objects.filter(from_user = request.user)
    for req in pending_requests:
        user_list = user_list.exclude(username = req.to_user.username)
    context = {'user_list':user_list, 'pending_requests':pending_requests}
    return render(request, 'louslist/addFriend.html',context)


def deleteFriend(request, username):
    friend2 = User.objects.get(username=username)
    friendship.objects.get(friend1=request.user, friend2=friend2).delete()
    friendship.objects.get(friend1=friend2, friend2=request.user).delete()
    return HttpResponseRedirect("/louslist/friends/")

def cancelRequest(request, username):
    to_user = User.objects.get(username=username)
    req_to_delete = friendRequest.objects.get(from_user=request.user, to_user=to_user)
    if req_to_delete:
        req_to_delete.delete()
    return HttpResponseRedirect("/louslist/add_friend/")


def submitComment(request, username):
    content = request.POST.get('comment')
    friend2 = User.objects.get(username=username)
    new_comment = comment()
    new_comment.poster = request.user
    new_comment.postee = friend2
    new_comment.content = content
    new_comment.save()
    return HttpResponseRedirect("/friend_schedule/"+username+"/")

def deleteComment(request, username):
    grabbed_id = request.POST.get('id')
    comment_to_delete = comment.objects.get(id=grabbed_id)
    if comment_to_delete.poster == request.user:
        comment_to_delete.delete()
    return HttpResponseRedirect("/friend_schedule/"+username+"/")