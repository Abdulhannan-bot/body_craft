from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserTypes(models.Model):
    user_type = models.CharField(max_length=100)
    # unique_id = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user_type)


class UserProfile(models.Model):
    USERTYPE = (
        ('staff', 'staff'),
        ('admin', 'admin'),
        ('Auditor', 'Auditor'),
        ('Audit Admin', 'Audit Admin'),
        ('Mystery Shopper', 'Mystery Shopper'),
        ('Salon Revenue Auditor', 'Salon Revenue Auditor'),
        ('Clinic Revenue Auditor', 'Clinic Revenue Auditor'),
        ('Corporate Auditor', 'Corporate Auditor')
    )
    USERSTATUS = (
        ('Active', 'Active'),
        ('InActive', 'InActive')
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.CharField(max_length=100, blank=True, choices=USERTYPE)
    user_type_name = models.ManyToManyField(UserTypes)
    user_status = models.CharField(
        max_length=200, null=True, blank=True, choices=USERSTATUS)
    roster_access = models.BooleanField(default=False, null=True, blank=True)
    date_of_joining = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class SecretKeyModel(models.Model):
    token = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.token)

# this center data is what we are getting from zenoti


class ZenotiCentersData(models.Model):
    zenoticenterId = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    address_1 = models.CharField(max_length=500, null=True, blank=True)
    address_2 = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.name) + '-' + str(self.code)


# this employee data is what we are getting from zenoti
class ZenotiEmployeesData(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    # zenoticenterId = models.CharField(max_length=100, null=True, blank=True)
    employee_code = models.CharField(max_length=100, null=True, blank=True)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=500, null=True, blank=True)
    job_info = models.CharField(max_length=500, null=True, blank=True)
    zenoti_center = models.ManyToManyField(
        ZenotiCentersData, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class AssociatedRoleOptions(models.Model):
    option = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.option)


class WeekOffOptions(models.Model):
    option = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.option)


class SectionOption(models.Model):
    option = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.option)


class OperationOption(models.Model):
    option = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.option)


class Position(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    section = models.ForeignKey(
        SectionOption, null=True, blank=True, on_delete=models.CASCADE
    )
    operation = models.ForeignKey(
        OperationOption, null=True, blank=True, on_delete=models.CASCADE
    )
    start_time = models.TimeField(max_length=100, null=True, blank=True)
    end_time = models.TimeField(max_length=100, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ExtendedZenotiCenterData(models.Model):
    CENTRESTATUS = (
        ('Active', 'Active'),
        ('InActive', 'InActive')
    )
    zenoti_data = models.OneToOneField(
        ZenotiCentersData, null=True, blank=True, on_delete=models.CASCADE
    )
    opening_time = models.TimeField(max_length=100, null=True, blank=True)
    closing_time = models.TimeField(max_length=100, null=True, blank=True)
    closed_on = models.ManyToManyField(WeekOffOptions, blank=True)
    position = models.ManyToManyField(Position, blank=True)
    center_status = models.CharField(
        max_length=200, null=True, blank=True, default='Active', choices=CENTRESTATUS)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.zenoti_data.name)


class ExtendedZenotiEmployeesData(models.Model):
    zenoti_data = models.ForeignKey(
        ZenotiEmployeesData, null=True, blank=True, on_delete=models.CASCADE
    )
    associated_center = models.ManyToManyField(
        ExtendedZenotiCenterData, blank=True)
    associated_role = models.ManyToManyField(
        Position, blank=True)
    office_start_time = models.TimeField(max_length=100, null=True, blank=True)
    office_end_time = models.TimeField(max_length=100, null=True, blank=True)
    week_off = models.ManyToManyField(WeekOffOptions, blank=True)
    is_manager = models.BooleanField(default=False, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.zenoti_data.user)


class ExtendedZenotiEmployeesLeaveData(models.Model):
    LEAVESTATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )
    zenoti_data = models.ForeignKey(
        ExtendedZenotiEmployeesData, null=True, blank=True, on_delete=models.CASCADE
    )
    leave_from_date = models.DateField(null=True, blank=True)
    leave_to_date = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=LEAVESTATUS)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.zenoti_data.zenoti_data.user)


class EmployeeRoster(models.Model):
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True, on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        ExtendedZenotiEmployeesData, blank=True, null=True, on_delete=models.CASCADE)
    associated_role = models.ForeignKey(
        Position, blank=True, null=True, on_delete=models.CASCADE)
    appoint_date = models.DateField(auto_now_add=False, null=True, blank=True)
    office_start_time = models.TimeField(max_length=100, null=True, blank=True)
    office_end_time = models.TimeField(max_length=100, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.employee) + '-' + str(self.appoint_date)


class ErrorLog(models.Model):
    employee = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    page = models.CharField(max_length=200, null=True, blank=True)
    sentence = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.employee) + '-' + str(self.added_date)


class EmployeeScheduler(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Week Off', 'Week Off'),
        ('Leave Request', 'Leave Request'),
        ('Leave Approved', 'Leave Approved'),
        ('Unplanned Leave', 'Unplanned Leave'),
        ('Training/Meeting', 'Training/Meeting'),
        ('Floating Resource', 'Floating Resource'),
        ('Internal Transfer', 'Internal Transfer'),
        ('Exit', 'Exit'),
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True, on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        ExtendedZenotiEmployeesData, blank=True, null=True, on_delete=models.CASCADE)
    associated_role = models.ManyToManyField(
        Position, blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS)
    remark = models.CharField(
        max_length=500, null=True, blank=True)
    appoint_date = models.DateField(auto_now_add=False, null=True, blank=True)
    office_start_time = models.TimeField(max_length=100, null=True, blank=True)
    office_end_time = models.TimeField(max_length=100, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.employee) + '-' + str(self.appoint_date)
