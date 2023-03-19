from django.contrib import admin
from .models import ClinicAuditRepeatedQuestion, ClinicDeletedServiceAnnexure, ClinicHygieneCheckAnnexure, ClinicNotRedeemedAnnexure, ClinicOtherObservationAnnexure, ClinicRectificationBillAnnexure, ClinicRevenueAuditOverview
# Register your models here.
admin.site.register(ClinicAuditRepeatedQuestion)
admin.site.register(ClinicDeletedServiceAnnexure)
admin.site.register(ClinicHygieneCheckAnnexure)
admin.site.register(ClinicNotRedeemedAnnexure)
admin.site.register(ClinicOtherObservationAnnexure)
admin.site.register(ClinicRectificationBillAnnexure)
admin.site.register(ClinicRevenueAuditOverview)
