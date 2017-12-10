from django.db import models


from classes.models import ClassModel, RegisterModel


class DateModel(models.Model):

    #오늘 날짜
    today = models.DateField(verbose_name='오늘 날짜')

    # 오늘 출책 시간
    start_time = models.TimeField(verbose_name='출책 시간')

    # 과목은 MTO으로 연결
    register = models.ForeignKey(RegisterModel, on_delete=models.CASCADE, verbose_name='과목')

    def __str__(self):
        return str(self.register) + ' ' + str(self.today)  