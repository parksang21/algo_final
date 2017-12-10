from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_POST

# import DBs
from student.models import StudentModel, StudentInstance
from classes.models import RegisterModel
from attendance.models import DateModel

from project.addition import lonlatCalculator

#attend/{{class_id}}/load/ url redirecting
def detour(request, class_hash):
    return render(request, 'attendance/temp_first.html',{'class_hash':class_hash})

# attend/check url POST 요청 처리, GET 방식으로 들어오는 것은 거부
@require_POST
def checkattend(request):
    print('\n\nSuccess redirecting....\nFirst authentication is done\n')

    class_hash = request.POST['class_hash']
    print('hash input ---------- %s' % class_hash)

    class_info = get_object_or_404(RegisterModel, class_hash=class_hash)
    print('[Success] ----------- %s  /  pk : %s' % (class_info, class_info.pk))

    return render(request, 'attendance/test.html', {'class_info':class_info})


# attend/success url POST 요청처리, GET 방식으로 들어오는 것은 거부
@require_POST
def success(request):
    print('\n\nThird authentication is done\n')

    # 학생 정보 받기
    student_id = request.POST['student_id'] or 0
    print('student_id [%s] ---------- attemps to attend' % student_id)

    # 학생 정보와 매칭되는 학생 Data 찾기
    student_info = get_object_or_404(StudentModel, student_id=student_id)
    print('[Success] ---------- [%s]' % student_info)

    # 수업 정보 만들기
    class_pk = request.POST['class_pk']
    class_info = get_object_or_404(RegisterModel, pk=class_pk)
    print('[Success] ---------- [%s]' % class_info)

    # 등록한 학생인지 검사
    if (student_info in class_info.student.all()):
        print('Register Conformed')
        
        print(request.POST['lat'], request.POST['lon'])
        input_lon = float(request.POST['lon'])
        input_lat = float(request.POST['lat'])
        class_lat, class_lon  = map(lambda x: float(x), class_info.lnglat.split(','))
        print('사용자의 위도(%lf) 경도(%lf) 값 호출 성공' % (input_lat, input_lon))
        print('[%s]의 위도(%lf) 경도(%lf) 값 호출 성공' % (class_info, class_lat, class_lon))

        distance = lonlatCalculator(class_lat, class_lon, input_lat, input_lon)
        print('사용자와 강의실의 거리 ---------- [%f]' % distance)

        current_date =  timezone.localtime().strftime('%Y-%m-%d')
        current_time = timezone.localtime().strftime('%H:%M:%S')

        try:
            new_date = get_object_or_404(DateModel, today=current_date, register=class_pk)
        except:
            new_date = DateModel(register=class_info, today=current_date, start_time=current_time)          
            new_date.save()

        new_student = StudentInstance(status='l', student=student_info, date=new_date, attend_time=current_time)
        new_student.save()
        return render(request, 'attendance/success.html', {"student" : student_info})
    else:
        print('student [%s] has not registered [%s]' %(student_info, class_info))
        err_message = '해당 과목 수강자가 아닙니다.'
        return render(request, 'attendance/error.html', {'err' : err_message})