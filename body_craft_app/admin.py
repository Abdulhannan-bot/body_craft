from django.contrib import admin
from .models import UserProfile, ZenotiCentersData, ZenotiEmployeesData, SecretKeyModel, ExtendedZenotiEmployeesData, AssociatedRoleOptions, WeekOffOptions, EmployeeRoster, ExtendedZenotiCenterData, ExtendedZenotiEmployeesLeaveData, EmployeeScheduler, OperationOption, SectionOption, Position, UserTypes
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ZenotiCentersData)
admin.site.register(ZenotiEmployeesData)
admin.site.register(SecretKeyModel)
admin.site.register(ExtendedZenotiEmployeesData)
admin.site.register(AssociatedRoleOptions)
admin.site.register(WeekOffOptions)
admin.site.register(EmployeeRoster)
admin.site.register(ExtendedZenotiCenterData)
admin.site.register(ExtendedZenotiEmployeesLeaveData)
admin.site.register(EmployeeScheduler)
admin.site.register(OperationOption)
admin.site.register(SectionOption)
admin.site.register(Position)
admin.site.register(UserTypes)
