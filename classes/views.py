from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse

import json
import re

from classes.models import RegisterModel
from attendance.models import DateModel

# Create your views here.

@login_required
def today_class(request, id):
    print('%s request the page' % request.user)

    user = get_object_or_404(User, pk=id)
    if(user == request.user):
        print("user is verified")
        class_list = RegisterModel.objects.filter(prof=user)
        print(class_list)
        return render(request, 'classes/class_manage.html', {"class_list":class_list})
    else:
        return render(request, 'error.html', {'err':"unauthorized user"})

@login_required
def class_detail(request, id):
    class_choice = get_object_or_404(RegisterModel, pk=id)
    current_date =  timezone.localtime().strftime('%Y-%m-%d')

    date_list = DateModel.objects.filter(register=class_choice)
    print(date_list)

    if(request.user == class_choice.prof):
        return render(request, 'classes/class_detail.html',{'class': class_choice,'currenttime':current_date, 'date_model':date_list})
    else:
        return render(request, 'error.html', {'err':"unauthorized user"})

@login_required
def date_detail(request, c_id, id):
    print('%s---- 수업의 date id[%s]가 넘어왔습니다.' % (c_id, id))

    class_choice = get_object_or_404(RegisterModel, pk=c_id)

    if(request.user == class_choice.prof):
        print('%s authorized' % str(request.user))

        date = get_object_or_404(DateModel, id=id)
        print("%s ----------- loaded" % date)

        student_list = date.studentinstance_set.all()

        print(student_list)

        context = {'date':date, 'students':student_list}

        if request.method == 'POST':
            input_time = request.POST.get('standtime', None)
            input_time = "%s:%s" % (input_time, '59')
            print('%s ---------- input time' % input_time)
            
            context['time'] = input_time

            parse = ""
            
            for x in input_time.split(":"):
                parse += x
            parse = int(parse)

            for student in student_list:
                st = ""
                for y in str(student.attend_time).split(':'):
                    st += y

                st = int(st)
                if st < parse:
                    student.status = 'a'
                else:
                    student.status = 'l'
                student.save()
        
        template = 'classes/date_detail.html'
    else:
        template = 'error.html'
        context = {'err': 'unauthorized user'}

    return render(request, template, context)

@require_POST
def refresh(request):
    id = request.POST.get('pk', None)
    st_list = request.POST.get('st_list', None)
    p = re.compile(r'\d{10}')
    st_list = p.findall(st_list)

    date = get_object_or_404(DateModel, id=id)
    student_list = date.studentinstance_set.all()

    new_students_name = []
    new_students_time = []
    
    for student in student_list:
        if str(student.student.student_id) not in st_list:
            new_students_name.append(str(student.student.name) + '-' + str(student.student.student_id))
            new_students_time.append(str(student.attend_time))

    context = {'student_name':new_students_name, 'attend_time': new_students_time}
    return HttpResponse(json.dumps(context), content_type="application/json")

def date_option(request, c_id, id):
    class_info = get_object_or_404(RegisterModel, pk=c_id)
    if(request.user == class_info.prof):
        date = get_object_or_404(DateModel, pk=id)

        return render(request, 'classes/class_option.html', {'class':class_info, 'date':date})
    else:
        return render(request, 'error.html', {'err': 'unexpected user request'})

def teamBuild(request,c_id, id):
    class_info = get_object_or_404(RegisterModel, pk=c_id)

    if(request.user == class_info.prof):
        print("%s is verified" % request.user)

        date = get_object_or_404(DateModel, pk=id)

        student_list = date.studentinstance_set.all()

        if request.method == "POST":
            member_number = int(request.POST.get('team-number', 3))
            for i in range(0, len(student_list)):
                student_list[i].team_no = i // member_number + 1

        template="classes/class_team.html"
        context = {'date':date, 'students':student_list}
    else:
        template="error.html"
        context = {'err':'permission denied'}
    return render(request, template, context)