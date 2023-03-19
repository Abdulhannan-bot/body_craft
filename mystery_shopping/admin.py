from django.contrib import admin
from .models import MysteryShoppingOverview, MysteryShoppingDetail, MysteryShoppingImages, MonthAudit
# Register your models here.
admin.site.register(MysteryShoppingOverview)
admin.site.register(MysteryShoppingDetail)
admin.site.register(MysteryShoppingImages)
admin.site.register(MonthAudit)
