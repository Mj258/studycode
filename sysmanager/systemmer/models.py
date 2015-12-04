from django.db import models

# Create your models here.
class User(models.Model):

    # ADMINCHOICES =(True,u'是'；
    #         False,u'不是')

    name= models.CharField(max_length=50)
    email= models.EmailField()
    password= models.CharField(max_length=100)
    is_active= models.IntegerField()
    is_admin= models.CharField()
    is_suppor= models.IntegerField()

    class Meta:
        managed= False


class Auto(object):
    pass
