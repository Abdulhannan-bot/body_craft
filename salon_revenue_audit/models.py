from django.db import models
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData

# Create your models here.


class SalonRevenueAuditOverview(models.Model):
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
    physical_cash_as_per_zenoti = models.CharField(max_length=100,
                                                   null=True, blank=True)
    physical_cash_as_per_counter = models.CharField(max_length=100,
                                                    null=True, blank=True)
    physical_cash_reconciliation = models.CharField(max_length=100,
                                                    null=True, blank=True)
    physical_cash_remark = models.CharField(
        max_length=500, null=True, blank=True)
    physcial_card_as_per_zenoti = models.CharField(max_length=100,
                                                   null=True, blank=True)
    physcial_card_as_per_counter = models.CharField(max_length=100,
                                                    null=True, blank=True)
    physcial_card_reconciliation = models.CharField(max_length=100,
                                                    null=True, blank=True)
    physical_card_remark = models.CharField(
        max_length=500, null=True, blank=True)
    custom_verification_as_per_zenoti = models.CharField(max_length=100,
                                                         null=True, blank=True)
    custom_verification_as_per_counter = models.CharField(max_length=100,
                                                          null=True, blank=True)
    custom_verification_reconciliation = models.CharField(max_length=100,
                                                          null=True, blank=True)
    custom_verification_remark = models.CharField(
        max_length=500, null=True, blank=True)
    open_bill_audit_row_one = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_open_bill_row_one = models.CharField(
        max_length=100, null=True, blank=True)
    no_of_clients_on_floor_row_one = models.CharField(
        max_length=100, null=True, blank=True)
    open_bill_remark_row_one = models.CharField(
        max_length=500, null=True, blank=True)
    open_bill_audit_row_two = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_open_bill_row_two = models.CharField(
        max_length=100, null=True, blank=True)
    no_of_clients_on_floor_row_two = models.CharField(
        max_length=100, null=True, blank=True)
    open_bill_remark_row_two = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_appointment_as_per_zenoti_row_one = models.CharField(max_length=100,
                                                               null=True, blank=True)
    pushed_appointment_remark_row_one = models.CharField(
        max_length=500, null=True, blank=True)
    pushed_appointment_audit_period_row_one = models.CharField(
        max_length=500, null=True, blank=True)
    pushed_appointment_audit_period_row_two = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_appointment_as_per_zenoti_row_two = models.CharField(max_length=100,
                                                               null=True, blank=True)
    pushed_appointment_remark_row_two = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_blockout_notes_active = models.CharField(
        max_length=100, null=True, blank=True)
    no_of_blockout_notes_deleted = models.CharField(
        max_length=100, null=True, blank=True)
    blockout_remark = models.CharField(
        max_length=500, null=True, blank=True)
    ob_as_per_statement = models.CharField(
        max_length=100, null=True, blank=True)
    ob_as_per_pv = models.CharField(max_length=100, null=True, blank=True)
    ob_remark = models.CharField(
        max_length=500, null=True, blank=True)
    petty_cash_date = models.CharField(max_length=100, null=True, blank=True)
    closing_balance_as_per_zenoti = models.CharField(
        max_length=100, null=True, blank=True)
    cash_in_hand = models.CharField(max_length=100, null=True, blank=True)
    balance_in_happy_card = models.CharField(
        max_length=100, null=True, blank=True)
    petty_cash_remark = models.CharField(
        max_length=500, null=True, blank=True)
    physical_voucher_available = models.CharField(
        max_length=100, null=True, blank=True)
    audit_sample_size = models.CharField(max_length=100, null=True, blank=True)
    no_of_voucher_updated_on_zenoti = models.CharField(max_length=100,
                                                       null=True, blank=True)
    rectification_tracker_updated = models.CharField(
        max_length=100, null=True, blank=True)
    no_of_rectification_bill_as_per_zenoti = models.CharField(max_length=100,
                                                              null=True, blank=True)
    no_of_issues_as_per_zenoti_for_rectification_bill = models.CharField(max_length=100,
                                                                         null=True, blank=True)
    dcr_updated = models.CharField(max_length=100, null=True, blank=True)
    dcr_cash_deposited = models.CharField(
        max_length=100, null=True, blank=True)
    dcr_remark = models.CharField(
        max_length=500, null=True, blank=True)
    no_of_otp_overrides_as_per_zenoti = models.CharField(max_length=100,
                                                         null=True, blank=True)
    om_approved_otp_overrides = models.CharField(max_length=100,
                                                 null=True, blank=True)
    otp_override_remark = models.CharField(
        max_length=500, null=True, blank=True)
    total_no_of_nearby_transaction_in_zenoti = models.CharField(max_length=100,
                                                                null=True, blank=True)
    total_no_of_audit_sample = models.CharField(max_length=100,
                                                null=True, blank=True)
    remarks_with_voucher_number = models.CharField(
        max_length=100, null=True, blank=True)
    without_voucher_number = models.CharField(
        max_length=100, null=True, blank=True)
    total_no_of_membership_redeemed_for_campaign = models.CharField(max_length=100,
                                                                    null=True, blank=True)

    def __str__(self):
        return str(self.auditor_name) + ' - ' + str(self.center.zenoti_data.name) + ' - ' + str(self.date)


class SalonAuditRepeatedQuestion(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, related_name='salon_revenue_audit', null=True, blank=True, on_delete=models.CASCADE
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
    tab_name = models.CharField(
        max_length=200, null=True, blank=True)
    checklist_series = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class HygieneAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    sample_dates = models.CharField(max_length=200, null=True, blank=True)
    total_guest = models.CharField(max_length=500, null=True, blank=True)
    sample_size_for_audit = models.CharField(
        max_length=500, null=True, blank=True)
    invoice_number = models.CharField(max_length=500, null=True, blank=True)
    reception_copy = models.CharField(max_length=200, null=True, blank=True)
    security_copy = models.CharField(max_length=200, null=True, blank=True)
    security_sheet = models.CharField(max_length=200, null=True, blank=True)
    feedback_updated = models.CharField(max_length=200, null=True, blank=True)
    was_the_rating_above_4 = models.CharField(
        max_length=200, null=True, blank=True)
    if_no_was_the_im_created = models.CharField(
        max_length=200, null=True, blank=True)
    job_card_attached = models.CharField(max_length=200, null=True, blank=True)
    job_card_matches_invoice = models.CharField(
        max_length=200, null=True, blank=True)
    sa_signature = models.CharField(
        max_length=200, null=True, blank=True)
    remark = models.CharField(
        max_length=500, null=True, blank=True)
    evidence = models.FileField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class DeletedServiceAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=500, null=True, blank=True)
    designation = models.CharField(max_length=500, null=True, blank=True)
    no_of_services_deleted = models.CharField(
        max_length=500, null=True, blank=True)
    deleted_without_justification = models.CharField(
        max_length=500, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class RectificationBillAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    bill_no = models.CharField(max_length=500, null=True, blank=True)
    issue_no = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class CampaignOfferAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    date_of_request = models.CharField(max_length=500, null=True, blank=True)
    date_of_redemption = models.CharField(
        max_length=500, null=True, blank=True)
    client_name = models.CharField(max_length=500, null=True, blank=True)
    invoice_number = models.CharField(max_length=500, null=True, blank=True)
    guest_code = models.CharField(max_length=500, null=True, blank=True)
    voucher_value = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class OtherObservationAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    observation_area = models.CharField(max_length=500, null=True, blank=True)
    audit_findings = models.CharField(
        max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class VoucherAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    date_of_request = models.CharField(max_length=500, null=True, blank=True)
    date_of_redemption = models.CharField(
        max_length=500, null=True, blank=True)
    client_name = models.CharField(max_length=500, null=True, blank=True)
    invoice_number = models.CharField(max_length=500, null=True, blank=True)
    guest_code = models.CharField(max_length=500, null=True, blank=True)
    voucher_value = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class PettyCashAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    voucher_number = models.CharField(max_length=500, null=True, blank=True)
    om_signature_available = models.CharField(
        max_length=500, null=True, blank=True)
    reflecting_in_zenoti = models.CharField(
        max_length=500, null=True, blank=True)
    supporting_document = models.CharField(
        max_length=500, null=True, blank=True)
    authenticity = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class CashVerificationCashCount(models.Model):
    revenue_audit = models.OneToOneField(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    count_2000 = models.CharField(max_length=50, null=True, blank=True)
    count_500 = models.CharField(max_length=50, null=True, blank=True)
    count_200 = models.CharField(max_length=50, null=True, blank=True)
    count_100 = models.CharField(max_length=50, null=True, blank=True)
    count_50 = models.CharField(max_length=50, null=True, blank=True)
    count_20 = models.CharField(max_length=50, null=True, blank=True)
    count_10 = models.CharField(max_length=50, null=True, blank=True)
    count_5 = models.CharField(max_length=50, null=True, blank=True)
    count_2 = models.CharField(max_length=50, null=True, blank=True)
    count_1 = models.CharField(max_length=50, null=True, blank=True)
    count_50p = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)


class SalonCyberSecurityAnnexure(models.Model):
    revenue_audit = models.ForeignKey(
        SalonRevenueAuditOverview, null=True, blank=True, on_delete=models.CASCADE
    )
    area = models.CharField(max_length=500, null=True, blank=True)
    sub_area = models.CharField(
        max_length=500, null=True, blank=True)
    zenoti_login_id = models.CharField(
        max_length=500, null=True, blank=True)
    used_by = models.CharField(
        max_length=500, null=True, blank=True)
    evidence = models.FileField(upload_to='media', null=True, blank=True)
    compliance = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.revenue_audit)
