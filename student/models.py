from django.db import models
from django.conf import settings

# Create your models here.


STATUS_CHOICES = (
    ('a', 'Attend'),
    ('n', 'Absance'),
    ('l', 'Late'),
)


class StudentModel(models.Model):
    name = models.CharField(max_length=20)
    student_id = models.IntegerField(unique=True)
    year = models.IntegerField(default=1)

    def __str__(self):
        return self.name + '-' + str(self.student_id)

class StudentInstance(models.Model):
    student = models.ForeignKey('StudentModel', on_delete=models.CASCADE)
    date = models.ForeignKey('attendance.DateModel', on_delete=models.CASCADE)
    
    #출석 정보
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')

    # 오늘 출책 시간
    attend_time = models.TimeField(verbose_name='출책 시간')

    team_no = models.IntegerField(blank=True, null=True, verbose_name="팀 번호")

    def __str__(self):
        return self.student.name + '-' + str(self.student.student_id)
    