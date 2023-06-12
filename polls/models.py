from django.db import models

# Create your models here.
class Maincar(models.Model):
    manuf = models.TextField(db_column='Manuf', blank=True, null=True)  # Field name made lowercase.
    model = models.TextField(db_column='Model', blank=True, null=True)  # Field name made lowercase.
    cc = models.TextField(db_column='CC', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(blank=True, null=True)
    otc = models.IntegerField(db_column='OTC', blank=True, null=True)  # Field name made lowercase.
    cartype = models.TextField(db_column='CarType', blank=True, null=True)  # Field name made lowercase.
    manufkor = models.TextField(db_column='ManufKor', blank=True, null=True)  # Field name made lowercase.
    modekor = models.TextField(db_column='ModeKor', blank=True, null=True)  # Field name made lowercase.
    badge = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maincar'


class ParamsTrans(models.Model):
    korname = models.TextField(db_column='KorName', blank=True, null=True)  # Field name made lowercase.
    runame = models.TextField(db_column='RuName', blank=True, null=True)  # Field name made lowercase.
    korgroup = models.TextField(db_column='KorGroup', blank=True, null=True)  # Field name made lowercase.
    rugroup = models.TextField(db_column='RuGroup', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'params_trans'

class CarFuel(models.Model):
    korfuel = models.TextField(blank=True, null=True)
    rufuel = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_fuel'


class CarTransmission(models.Model):
    kortrans = models.TextField(blank=True, null=True)
    rutrans = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_transmission'


class Colors(models.Model):
    korcolor = models.TextField(blank=True, null=True)
    rucolor = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colors'        