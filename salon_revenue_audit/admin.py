from django.contrib import admin
from .models import SalonRevenueAuditOverview, SalonAuditRepeatedQuestion, HygieneAnnexure, CashVerificationCashCount, CampaignOfferAnnexure, PettyCashAnnexure, VoucherAnnexure, DeletedServiceAnnexure, OtherObservationAnnexure, RectificationBillAnnexure
# Register your models here.
admin.site.register(SalonRevenueAuditOverview)
admin.site.register(SalonAuditRepeatedQuestion)
admin.site.register(HygieneAnnexure)
admin.site.register(CashVerificationCashCount)
admin.site.register(CampaignOfferAnnexure)
admin.site.register(PettyCashAnnexure)
admin.site.register(VoucherAnnexure)
admin.site.register(DeletedServiceAnnexure)
admin.site.register(OtherObservationAnnexure)
admin.site.register(RectificationBillAnnexure)
