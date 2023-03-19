from django.db import models
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData

# Create your models here.


class ClinicRevenueAuditOverview(models.Model):
    added_by = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    center = models.ForeignKey(
        ExtendedZenotiCenterData, null=True, blank=True, on_delete=models.CASCADE
    )
    date = models.DateField(null=True, blank=True)
    auditor_name = models.CharField(max_length=200, null=True, blank=True)
    audit_period_from = models.DateField(null=True, blank=True)
    audit_period_to = models.DateField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    total_discount_cases_as_per_zenoti = models.CharField(
        max_length=500, null=True, blank=True)
    total_approvals_verified = models.CharField(
        max_length=500, null=True, blank=True)
    dicount_cases_remark = models.CharField(
        max_length=500, null=True, blank=True)
    total_membership_redemption_as_per_zenoti = models.CharField(
        max_length=500, null=True, blank=True)
    membership_redemption_remark = models.CharField(
        max_length=500, null=True, blank=True)
    rectification_tracker_maintained = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_rectification_bill_as_per_zenoti = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_issues_as_per_zenoti_rectification = models.CharField(
        max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.auditor_name) + ' - ' + str(self.center.zenoti_data.name) + ' - ' + str(self.date)


class ClinicAuditRepeatedQuestion(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, related_name='clinic_revenue_audit', null=True, blank=True, on_delete=models.CASCADE
    )
    checklist = models.CharField(max_length=500, null=True, blank=True)
    responsible_kra = models.CharField(max_length=200, null=True, blank=True)
    person_responsible = models.ForeignKey(
        ExtendedZenotiEmployeesData, null=True, blank=True, on_delete=models.CASCADE
    )
    relative_gap_found = models.CharField(
        max_length=500, blank=True, null=True)
    compliance = models.CharField(max_length=200, blank=True, null=True)
    compliance_category = models.CharField(
        max_length=200, null=True, blank=True)
    compliance_category_percentage = models.CharField(
        max_length=20, null=True, blank=True)
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
    tab_name = models.CharField(max_length=200, null=True, blank=True)
    question_series = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class ClinicHygieneCheckAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    sample_dates = models.CharField(max_length=100, null=True, blank=True)
    total_guest = models.CharField(max_length=500, null=True, blank=True)
    sample_size_for_audit = models.CharField(
        max_length=500, null=True, blank=True)
    invoice_date = models.CharField(max_length=500, null=True, blank=True)
    invoice_number = models.CharField(max_length=500, null=True, blank=True)
    client_name = models.CharField(max_length=500, null=True, blank=True)
    category_of_sample = models.CharField(
        max_length=500, null=True, blank=True)
    quantity_of_injectable_as_per_bill = models.CharField(
        max_length=500, null=True, blank=True)
    quantity_of_injectable_as_per_consent_form = models.CharField(
        max_length=500, null=True, blank=True)
    quantity_of_injectable_as_per_treatment_record = models.CharField(
        max_length=500, null=True, blank=True)
    consumable_bill_quantity_matching_as_per_treatment_record = models.CharField(
        max_length=500, null=True, blank=True)
    reception_copy = models.CharField(max_length=200, null=True, blank=True)
    security_copy = models.CharField(max_length=200, null=True, blank=True)
    security_sheet = models.CharField(max_length=200, null=True, blank=True)
    feedback_updated = models.CharField(max_length=200, null=True, blank=True)
    job_card_attached = models.CharField(max_length=200, null=True, blank=True)
    job_card_matches_invoice = models.CharField(
        max_length=200, null=True, blank=True)
    client_profile_form = models.CharField(
        max_length=200, null=True, blank=True)
    disclaimer_form = models.CharField(
        max_length=200, null=True, blank=True)
    consent_form = models.CharField(
        max_length=200, null=True, blank=True)
    client_signature_matching_all_docs = models.CharField(
        max_length=200, null=True, blank=True)
    treatment_record_entry = models.CharField(
        max_length=200, null=True, blank=True)
    customer_signature_treatment_record = models.CharField(
        max_length=200, null=True, blank=True)
    doctor_signature_treatment_record = models.CharField(
        max_length=200, null=True, blank=True)
    redemption_of_all_service_under_right_package = models.CharField(
        max_length=200, null=True, blank=True)
    consultant_signature = models.CharField(
        max_length=200, null=True, blank=True)
    evidence = models.FileField(upload_to='media', null=True, blank=True)
    remark = models.CharField(
        max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class ClinicDeletedServiceAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    no_of_services_deleted = models.CharField(
        max_length=200, null=True, blank=True)
    deleted_without_proper_justification = models.CharField(
        max_length=200, null=True, blank=True)
    remark = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class ClinicRectificationBillAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    bill_no = models.CharField(max_length=200, null=True, blank=True)
    issue_no = models.CharField(max_length=200, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class ClinicOtherObservationAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    observation_area = models.CharField(max_length=200, null=True, blank=True)
    audit_findings = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class ClinicNotRedeemedAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        ClinicRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    date_as_per_record = models.CharField(
        max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    client_name = models.CharField(max_length=200, null=True, blank=True)
    category_of_sample = models.CharField(
        max_length=200, null=True, blank=True)
    quantity_of_not_redeemed = models.CharField(
        max_length=200, null=True, blank=True)
    evidence = models.FileField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)
