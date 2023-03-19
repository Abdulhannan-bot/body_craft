from django.db import models
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData

# Create your models here.


class MonthAudit(models.Model):
    month = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.month)


class MysteryShoppingOverview(models.Model):
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
    month_of_audit = models.ForeignKey(MonthAudit,
                                       null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    cost_of_service = models.CharField(max_length=200, null=True, blank=True)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    paid_in_cash = models.CharField(max_length=500, null=True, blank=True)
    payment_mode = models.CharField(max_length=200, null=True, blank=True)
    amount_redeemed = models.CharField(max_length=200, null=True, blank=True)
    contact_number_reached_for_appointment = models.CharField(
        max_length=200, null=True, blank=True)
    auditor_completed = models.BooleanField(
        default=False, null=True, blank=True)
    admin_reviewed = models.BooleanField(
        default=False, null=True, blank=True)
    service_availed_1 = models.CharField(max_length=500, null=True, blank=True)
    service_agent_1 = models.ForeignKey(
        ExtendedZenotiEmployeesData, null=True, blank=True, on_delete=models.CASCADE
    )
    service_availed_2 = models.CharField(max_length=500, null=True, blank=True)
    service_agent_2 = models.ForeignKey(
        ExtendedZenotiEmployeesData, related_name='service_agent_2', null=True, blank=True, on_delete=models.CASCADE
    )
    service_availed_3 = models.CharField(max_length=500, null=True, blank=True)
    service_agent_3 = models.ForeignKey(
        ExtendedZenotiEmployeesData, related_name='service_agent_3', null=True, blank=True, on_delete=models.CASCADE
    )
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.shopper_name)


class MysteryShoppingDetail(models.Model):
    mystery_shopping = models.ForeignKey(
        MysteryShoppingOverview, null=True,
        blank=True, on_delete=models.CASCADE
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True,
        on_delete=models.CASCADE)
    sequence = models.CharField(max_length=20, null=True, blank=True)
    compliance_dropdown = models.CharField(
        max_length=500, null=True, blank=True)
    month_of_audit = models.ForeignKey(MonthAudit,
                                       null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    client_journey = models.CharField(max_length=200, null=True, blank=True)
    kra = models.CharField(max_length=200, null=True, blank=True)
    process = models.CharField(max_length=200, null=True, blank=True)
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
    service_availed_1 = models.CharField(max_length=200, null=True, blank=True)
    service_availed_2 = models.CharField(max_length=200, null=True, blank=True)
    service_availed_3 = models.CharField(max_length=200, null=True, blank=True)
    audit_status = models.CharField(max_length=200, null=True, blank=True)
    comment_for_auditor = models.CharField(
        max_length=500, null=True, blank=True)
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
        return str(self.mystery_shopping.center.zenoti_data.display_name) + str(self.sequence)


class MysteryShoppingImages(models.Model):
    mystery_shopping = models.ForeignKey(
        MysteryShoppingOverview, null=True,
        blank=True, on_delete=models.CASCADE
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True,
        on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.FileField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return str(self.center.zenoti_data.display_name) + ' - ' + str(self.date)
