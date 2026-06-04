from django.db import models
from django.db.models import CharField

class DropdownItem:
    def get_key(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

class User(DropdownItem, models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    loginId = models.EmailField()
    password = models.CharField(max_length=20)
    confirmPassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobileNumber = models.CharField(max_length=50, default='')
    roleId = models.IntegerField(null=True, blank=True)
    roleName = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'scrd_User'

class BankNote(models.Model):
    bankName = models.CharField(max_length=100)
    principal = models.FloatField()
    interestRate = models.FloatField()
    dueDate = models.DateField()

    class Meta:
        db_table = 'scrd_banknote'

class BloodBank(models.Model):
    bloodGroup = models.CharField(max_length=100)
    unitsAvailable = models.IntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'scrd_bankblood'

class RateLimit(models.Model):
    rateLimitCode = models.CharField(max_length=100)
    apiName = models.CharField(max_length=100)
    limitPerMinute = models.IntegerField()
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_ratelimit"

class BranchManager(models.Model):
    managerName = CharField(max_length=100)
    branchName = CharField(max_length=100)
    contactNumber = CharField(max_length=100)

    class Meta:
        db_table = "scrd_branch"

class Channel (models.Model):
    channelCode = CharField(max_length=100)
    channelName = CharField(max_length=100)
    type = CharField(max_length=100)
    status = CharField(max_length=100)

    class Meta:
        db_table = "scrd_channel"

class Attempt(models.Model):
    attemptCode = CharField(max_length=100)
    userName = CharField(max_length=100)
    attemptTime = models.DateField()
    status = CharField(max_length=100)

    class Meta:
        db_table = "scrd_attempt"

class Broadcast(models.Model):
    broadcastCode = CharField(max_length=100)
    broadMessage = CharField(max_length=100)
    sentBy = CharField(max_length=100)
    status = CharField(max_length=100)

    class Meta:
        db_table = "scrd_broadcast"

class BatchProcessing(models.Model):
    batchCode = models.CharField(max_length=100)
    batchName = models.CharField(max_length=100)
    totalRecords = models.IntegerField()
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_batchprocessing"

class spaceMission(models.Model):
    missionName = models.CharField(max_length=100)
    launchVehicle  = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    missionStatus = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_mission"

class StudentManagment(DropdownItem,models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(max_length=20)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_studentmanag"

class Mobile(models.Model):
    brand_name  = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    ram = models.IntegerField()
    price = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_mobile"

class Appointment(models.Model):
    patient_name  = models.CharField(max_length=100)
    appointment_date = models.DateField(max_length=20)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "scrd_patientappointment"

















