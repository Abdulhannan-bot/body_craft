from django.db import models
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData

# Create your models here.


class CorporateAuditOverview(models.Model):
    added_by = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True, on_delete=models.CASCADE
    )
    shopper_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    start_time = models.TimeField(max_length=200, null=True, blank=True)
    end_time = models.TimeField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    contact_number_reached_for_appointment = models.CharField(
        max_length=200, null=True, blank=True)
    auditor_completed = models.BooleanField(
        default=False, null=True, blank=True)
    admin_reviewed = models.BooleanField(
        default=False, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.shopper_name)


class CorporateAuditDetail(models.Model):
    corporate_audit = models.ForeignKey(
        CorporateAuditOverview, null=True,
        blank=True, on_delete=models.CASCADE
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True,
        on_delete=models.CASCADE)
    sequence = models.CharField(max_length=20, null=True, blank=True)
    compliance_dropdown = models.CharField(
        max_length=500, null=True, blank=True)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    kra = models.CharField(max_length=200, null=True, blank=True)
    checklist = models.CharField(max_length=1000, null=True, blank=True)
    compliance = models.CharField(max_length=200, null=True, blank=True)
    compliance_category = models.CharField(
        max_length=200, null=True, blank=True)
    compliance_category_percentage = models.CharField(
        max_length=20, null=True, blank=True)
    relative_gaps_found = models.CharField(
        max_length=1000, null=True, blank=True)
    remark = models.CharField(max_length=1000, null=True, blank=True)
    staff = models.ForeignKey(
        ExtendedZenotiEmployeesData, null=True, blank=True,
        on_delete=models.CASCADE)
    service_number = models.CharField(max_length=200, null=True, blank=True)
    action_taken_by_outlet_manager = models.CharField(
        max_length=200, null=True, blank=True)
    status_by_om = models.CharField(max_length=200, null=True, blank=True)
    remark_by_om = models.CharField(max_length=1000, null=True, blank=True)
    action_taken_by_management = models.CharField(
        max_length=200, null=True, blank=True)
    remark_by_management = models.CharField(
        max_length=1000, null=True, blank=True)
    expected_dept_intervene = models.CharField(
        max_length=200, null=True, blank=True)
    remark_by_department = models.CharField(
        max_length=1000, null=True, blank=True)
    status_by_department = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.corporate_audit.center.zenoti_data.display_name) + str(self.sequence)
