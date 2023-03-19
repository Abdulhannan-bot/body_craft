from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData, Position, OperationOption, SecretKeyModel
from .models import SalonRevenueAuditOverview, SalonAuditRepeatedQuestion, HygieneAnnexure, DeletedServiceAnnexure, RectificationBillAnnexure, CampaignOfferAnnexure, OtherObservationAnnexure, VoucherAnnexure, PettyCashAnnexure, CashVerificationCashCount, SalonCyberSecurityAnnexure
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
import json
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, timedelta, date
import requests
import calendar
import random
# Create your views here.
compliance_category_value = {
    "Followed": "RNR",
    "Partially followed": "Benchmark KRA",
    "Couldn't follow": "CPI",
    "Not aware": "Education",
    "Not followed": "PIP",
    "1": "PIP",
    "2": "PIP",
    "3": "PIP",
    "4": "Benchmark KRA",
    "5": "RNR",
    "Like": "RNR",
    "Partially Like": "Benchmark KRA",
    "Dislike": "PIP",
    "Yes": "RNR",
    "No": "PIP",
    "May be": "Benchmark KRA",
    "NA": "NA"
}

compliance_category_percentage = {
    "RNR": 100,
    "Benchmark KRA": 50,
    "CPI": 0,
    "PIP": 0,
    "Education": 0
}
all_checklist_list = [
    ["Physical cash verification", "AE/Billing", "Cash Verification", "1"],
    ["Physical card verification", "AE/Billing", "Cash Verification", "2"],
    ["Custom verification", "AE/Billing", "Cash Verification", "3"],
    ["Was the cash draw locked during the audit?",
        "AE/Billing", "Cash Verification", "4"],
    ["Reception copy", "AE/Billing", "Hygiene Check", "5"],
    ["Security copy", "AE/Billing", "Hygiene Check", "6"],
    ["Security Sheet", "AE/Billing", "Hygiene Check", "7"],
    ["Feedback updated", "AE/Billing", "Hygiene Check", "8"],
    ["Was the rating above 4 for all categories",
        "AE/Billing", "Hygiene Check", "9"],
    ["If No, was the IM created", "AE/Billing", "Hygiene Check", "10"],
    ["Job card attached", "AE/Billing", "Hygiene Check", "11"],
    ["Job card matches with Invoice", "AE/Billing", "Hygiene Check", "12"],
    ["SA signature", "AE/Billing", "Hygiene Check", "13"],
    ["Open bills", "AE/Billing", "Open bills", "14"],
    ["Pushed Appointments", "OM", "Pushed Appointments", "15"],
    ["Block Outs", "OM", "Block Outs", "16"],
    ["Deleted Services", "OM", "Deleted Services", "17"],
    ["Opening Balance", "AE/Billing", "Opening Balance", "18"],
    ["Petty Cash", "AE/Billing", "Petty Cash", "19"],
    ["Rectification bill's", "AE/Billing", "Rectification bill's", "20"],
    ["Other Observation", "OM", "Other Observation", "21"],
    ["DCR", "AE/Billing", "DCR", "22"],
    ["OTP Overrides", "OM", "OTP Overrides", "23"],
    ["Nearby Vouchers", "AE/Billing", "Nearby Vouchers", "24"],
    ["Campaigns & Offers", "AE/Billing", "Campaigns & Offers", "25"],
    ["Cyber Security Controls", "OM", "Cyber Security Controls", "26"]
]

try:
    api_key = SecretKeyModel.objects.all().first().token
except Exception:
    api_key = ''


@login_required(login_url='user_login')
def revenue_audit_overview(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    if is_salon_revenue_auditor or staffProfile.user_type == 'admin':
        pass
    else:
        return redirect('/')
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_revenue_audit = SalonRevenueAuditOverview.objects.all()
    all_revenue_audit_detail = SalonAuditRepeatedQuestion.objects.all()
    if is_salon_revenue_auditor:
        all_revenue_audit = all_revenue_audit.filter(added_by=staffProfile)
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            revenue_audit__in=all_revenue_audit)
    selected_center_id = request.GET.get('select_center')
    searched_from_date = request.GET.get('searched_from_date')
    searched_to_date = request.GET.get('searched_to_date')
    # searched_text = request.GET.get('searched_text')
    searched_compliance = request.GET.getlist('searched_compliance')
    searched_dept = request.GET.get('searched_dept')
    searched_om = request.GET.get('searched_om')
    print(searched_compliance)
    try:
        selected_center = ExtendedZenotiCenterData.objects.get(
            id=int(selected_center_id))
    except Exception:
        selected_center = None
    if selected_center:
        all_revenue_audit = all_revenue_audit.filter(center=selected_center)
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            revenue_audit__in=all_revenue_audit)
    if searched_from_date:
        all_revenue_audit = all_revenue_audit.filter(
            audit_period_from__gte=searched_from_date)
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            revenue_audit__in=all_revenue_audit)

    if searched_to_date:
        all_revenue_audit = all_revenue_audit.filter(
            audit_period_to__lte=searched_to_date)
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            revenue_audit__in=all_revenue_audit)
    if searched_compliance:
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            compliance_category__in=searched_compliance
        )

    if searched_dept:
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            status_by_department=searched_dept)
    if searched_om:
        all_revenue_audit_detail = all_revenue_audit_detail.filter(
            status_by_om=searched_om)
    # list page
    page = Paginator(all_revenue_audit, 20)
    list_page_num = request.GET.get('page', 1)
    try:
        list_page = page.page(list_page_num)
    except EmptyPage:
        list_page = page.page(1)

    # detail pagination
    page_2 = Paginator(all_revenue_audit_detail, 50)
    detail_page_num = request.GET.get('page_2', 1)
    try:
        detail_page = page_2.page(detail_page_num)
    except EmptyPage:
        detail_page = page_2.page(1)

    if request.method == 'POST':
        if 'add_revenue_audit' in request.POST:
            auditor_name = request.POST.get('add_auditor_name')
            audit_date = request.POST.get('add_audit_date')
            audit_outlet = request.POST.get('add_outlet')
            from_audit_period = request.POST.get('from_audit_date')
            to_audit_period = request.POST.get('to_audit_date')
            try:
                center = ExtendedZenotiCenterData.objects.get(
                    id=int(audit_outlet))
            except Exception:
                center = None
            new_audit = SalonRevenueAuditOverview.objects.create(
                added_by=staffProfile,
                center=center,
                auditor_name=auditor_name,
                audit_period_from=from_audit_period,
                audit_period_to=to_audit_period,
                date=audit_date
            )
            for each_checklist in all_checklist_list:
                protocol = OperationOption.objects.filter(
                    option=each_checklist[1]).first()
                position = Position.objects.filter(operation=protocol).first()
                # print('position', position)
                try:
                    person_responsible = ExtendedZenotiEmployeesData.objects.filter(
                        associated_center=center, associated_role=position).first()
                except Exception:
                    person_responsible = None
                print('each', each_checklist)
                SalonAuditRepeatedQuestion.objects.create(
                    revenue_audit=new_audit,
                    checklist=each_checklist[0],
                    responsible_kra=each_checklist[1],
                    person_responsible=person_responsible,
                    tab_name=each_checklist[2],
                    checklist_series=each_checklist[3]
                )
            # HygieneAnnexure.objects.create(
            #     revenue_audit=new_audit
            # )
            CashVerificationCashCount.objects.create(
                revenue_audit=new_audit
            )
        if 'del_audit' in request.POST:
            del_audit_id = request.POST.get('del_id')
            try:
                audit_overview = SalonRevenueAuditOverview.objects.get(
                    id=int(del_audit_id))
            except Exception:
                audit_overview = None

            audit_overview.delete()
        if 'edit_revenue_audit' in request.POST:
            audit_id = request.POST.get('audit_pk')
            center_id = request.POST.get('edit_outlet')
            auditor_name = request.POST.get('edit_auditor_name')
            audit_date = request.POST.get('edit_audit_date')
            from_audit_period = request.POST.get('edit_from_date')
            to_audit_period = request.POST.get('edit_to_date')

            try:
                audit = SalonRevenueAuditOverview.objects.get(
                    id=int(audit_id))
            except Exception:
                audit = None

            try:
                center = ExtendedZenotiCenterData.objects.get(
                    id=int(center_id))
            except Exception:
                center = None

            audit.date = audit_date
            audit.center = center
            audit.audit_period_from = from_audit_period
            audit.audit_period_to = to_audit_period
            audit.auditor_name = auditor_name
            audit.save()
        return redirect('revenue_audit_overview')
    context = {'all_center': all_center,
               'all_revenue_audit': list_page,
               'staffProfile': staffProfile,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_revenue_audit_detail': detail_page,
               'selected_center_id': selected_center_id,
               'searched_from_date': searched_from_date,
               'searched_to_date': searched_to_date,
               'searched_dept': searched_dept, 'searched_om': searched_om,
               'searched_compliance': searched_compliance}
    return render(request, "revenue_audit/revenue_audit_overview_tabs.html", context)


@login_required(login_url='user_login')
def revenue_audit_profile_page(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    revenue_audit = SalonRevenueAuditOverview.objects.get(id=int(pk))
    all_employee = ExtendedZenotiEmployeesData.objects.filter(
        associated_center=revenue_audit.center)
    all_cashverification_one = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Cash Verification', checklist_series__in=['1', '2', '3'])
    all_cashverification_two = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Cash Verification', checklist_series='4'
    )
    try:
        all_cashverification_cash_count = CashVerificationCashCount.objects.get(
            revenue_audit=revenue_audit
        )
    except Exception:
        all_cashverification_cash_count = None
    all_hygiene_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Hygiene Check'
    )
    all_hygiene_annexure = HygieneAnnexure.objects.filter(
        revenue_audit=revenue_audit
    ).order_by('sample_dates')
    # annexure pagination
    page = Paginator(all_hygiene_annexure, 15)
    hygiene_page_num = request.GET.get('hygiene_page', 1)
    try:
        hygiene_page = page.page(hygiene_page_num)
    except EmptyPage:
        hygiene_page = page.page(1)

    all_open_bill_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Open Bills')
    all_blackout_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Block Outs'
    )
    all_pushed_appointment = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Pushed Appointments'
    )
    all_deleted_services = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Deleted Services'
    )
    all_deleted_service_annexure = DeletedServiceAnnexure.objects.filter(
        revenue_audit=revenue_audit)
    all_opening_balance_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Opening Balance'
    )
    all_rectification_bil = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name="Rectification bill's"
    )
    all_rectification_annexure = RectificationBillAnnexure.objects.filter(
        revenue_audit=revenue_audit)
    all_dcr_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='DCR')
    all_otp_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='OTP Overrides'
    )
    all_campaign_offer_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Campaigns & Offers'
    )
    all_campaign_annexure = CampaignOfferAnnexure.objects.filter(
        revenue_audit=revenue_audit)
    all_other_observation_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Other Observation'
    )
    all_other_observation_annexure = OtherObservationAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_nearby_voucher_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Nearby Vouchers'
    )
    all_nearby_voucher_annexure = VoucherAnnexure.objects.filter(
        revenue_audit=revenue_audit)
    all_petty_cash_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Petty Cash'
    )
    all_petty_cash_annexure = PettyCashAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_cyber_security_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Cyber Security Controls'
    )
    all_cyber_security_annexure = SalonCyberSecurityAnnexure.objects.filter(
        revenue_audit=revenue_audit)
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_salon_checklist = SalonAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit)
    if request.method == 'POST':
        if 'create_one_hygiene_annexure_row' in request.POST:
            HygieneAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'hygiene_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                HygieneAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'hygiene_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = HygieneAnnexure.objects.get(id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_deleted_service_annexure_row' in request.POST:
            DeletedServiceAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'deleted_service_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                DeletedServiceAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'deleted_service_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = DeletedServiceAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_rectification_annexure_row' in request.POST:
            RectificationBillAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'rectification_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                RectificationBillAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'rectification_bill_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = RectificationBillAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_campaign_annexure_row' in request.POST:
            CampaignOfferAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'campaign_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                CampaignOfferAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'campaign_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = CampaignOfferAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_observation_annexure_row' in request.POST:
            OtherObservationAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'observation_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                OtherObservationAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'observation_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = OtherObservationAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_voucher_annexure_row' in request.POST:
            VoucherAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'voucher_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                VoucherAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'voucher_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = VoucherAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_pettycash_annexure_row' in request.POST:
            PettyCashAnnexure.objects.create(revenue_audit=revenue_audit)
        if 'pettycash_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                PettyCashAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'pettycash_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = PettyCashAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'create_one_cyber_security_annexure_row' in request.POST:
            SalonCyberSecurityAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'cyber_security_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                SalonCyberSecurityAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'cyber_security_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = SalonCyberSecurityAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
        if 'fetch_zenoti_data_hygiene_salon' in request.POST:
            print('zenoti data')
            print(str(revenue_audit.audit_period_from))
            start_date = date(revenue_audit.audit_period_from.year,
                              revenue_audit.audit_period_from.month, revenue_audit.audit_period_from.day)
            print('start date', start_date)
            end_date = date(revenue_audit.audit_period_to.year,
                            revenue_audit.audit_period_to.month, revenue_audit.audit_period_to.day)
            date_range = []
            current_date = start_date
            while current_date <= end_date:
                next_date = current_date + timedelta(days=5)
                if next_date > end_date:
                    next_date = end_date
                date_range.append((current_date, next_date))
                current_date = next_date + timedelta(days=1)

            print('date range', date_range)
            collections = []
            # date_count = {}
            for each_range in date_range:
                center_id = revenue_audit.center.zenoti_data.zenoticenterId
                url = f'https://api.zenoti.com/v1/Centers/{center_id}/collections_report?start_date={each_range[0]}&end_date={each_range[1]}'
                print('url', url)
                head = {"Authorization": "apikey "+api_key}
                response = requests.request("GET", url, headers=head)
                response_got = json.loads(response.text)
                print('got', len(response_got))
                collections_report = response_got['collections_report']
                for collection in collections_report:
                    invoice_no = collection['invoice_no']
                    net_amount = collection['net_amount']
                    closed_date = collection['closed_date'][0:10]
                    date_key = 'a_'+closed_date.replace("-", "")
                    days = datetime.strptime(closed_date, "%Y-%m-%d").date()
                    weekday = calendar.day_name[days.weekday()]
                    collections.append(
                        [invoice_no, net_amount, closed_date, weekday, date_key])
            print("reposnse", len(collections))
            # print("date_count", date_count)
            date_counts = Counter([collection[4]
                                  for collection in collections])
            print('date_count', date_counts)

            # print('collection', collections)
            weekend_collections = []
            for each_collection in collections:
                if each_collection[3] in ['Friday', 'Sunday', 'Saturday']:
                    weekend_collections.append(each_collection)
            weekend_date_counts = Counter([weekend_date[4]
                                           for weekend_date in weekend_collections])
            print("weekend collection", weekend_date_counts)

            weekday_collections = []
            for weekday in collections:
                if weekday[3] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                    weekday_collections.append(weekday)
            weekday_date_counts = Counter([weekday_date[4]
                                           for weekday_date in weekday_collections])
            print("weekday collection", weekday_date_counts)

            total_weekday = len(weekday_collections)
            total_weekend = len(weekend_collections)

            weekend_75 = round(0.75*total_weekend)
            weekday_25 = round(0.25*total_weekday)

            weekday_sample = random.sample(weekday_collections, weekday_25)
            weekend_sample = random.sample(weekend_collections, weekend_75)
            final_sample = weekday_sample + weekend_sample
            print('final sample', final_sample)

            final_sample_counts = Counter([final_sample_cont[4]
                                           for final_sample_cont in final_sample])

            final_collections = []
            for sample in final_sample:
                invoice_number = sample[0]
                final_date_key = sample[4]
                total_guest = date_counts[final_date_key]
                sample_audit_size = final_sample_counts[final_date_key]
                closed_date = sample[2]
                final_collections.append(
                    [closed_date, total_guest, sample_audit_size, invoice_number])

            print('final_collection', final_collections)
            for final in final_collections:
                HygieneAnnexure.objects.create(
                    revenue_audit=revenue_audit,
                    sample_dates=final[0],
                    total_guest=final[1],
                    sample_size_for_audit=final[2],
                    invoice_number=final[3]
                )

        return redirect('revenue_audit_profile', pk=pk)
    context = {'all_center': all_center,
               'staffProfile': staffProfile,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_cashverification_one': all_cashverification_one,
               'all_cashverification_two': all_cashverification_two,
               'all_cashverification_cash_count': all_cashverification_cash_count,
               'all_hygiene_checklist': all_hygiene_checklist,
               'all_hygiene_annexure': hygiene_page,
               'all_blackout_checklist': all_blackout_checklist,
               'all_open_bill_checklist': all_open_bill_checklist,
               'all_pushed_appointment': all_pushed_appointment,
               'all_deleted_services': all_deleted_services,
               'all_deleted_service_annexure': all_deleted_service_annexure,
               'all_opening_balance_checklist': all_opening_balance_checklist,
               'all_rectification_bil': all_rectification_bil,
               'all_rectification_annexure': all_rectification_annexure,
               'all_dcr_checklist': all_dcr_checklist,
               'all_otp_checklist': all_otp_checklist,
               'all_campaign_offer_checklist': all_campaign_offer_checklist,
               'all_campaign_annexure': all_campaign_annexure,
               'all_other_observation_checklist': all_other_observation_checklist,
               'all_other_observation_annexure': all_other_observation_annexure,
               'all_nearby_voucher_checklist': all_nearby_voucher_checklist,
               'all_nearby_voucher_annexure': all_nearby_voucher_annexure,
               'all_petty_cash_checklist': all_petty_cash_checklist,
               'all_petty_cash_annexure': all_petty_cash_annexure,
               'all_cyber_security_checklist': all_cyber_security_checklist,
               'all_cyber_security_annexure': all_cyber_security_annexure,
               'all_salon_checklist': all_salon_checklist,
               'all_employee': all_employee,
               'revenue_audit': revenue_audit}
    return render(request, "revenue_audit/audit_profile.html", context)


def edit_revenue_audit_overview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            audit_overview = SalonRevenueAuditOverview.objects.get(
                id=int(got_query))
        except Exception:
            audit_overview = None

        audit_json = serializers.serialize('json', [audit_overview])
        return JsonResponse({"msg": "success",
                            "mystery_json": json.loads(audit_json)})
    return render(request, "revenue_audit/revenue_audit_overview_tabs.html")


def edit_audit_cashverification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        salon_audit_extend_data = data['salon_audit']
        got_cash_one = data['one_data_obj']
        got_cash_two = data['two_data_obj']
        got_cash_count = data['cash_count_obj']
        print(got_cash_one, got_cash_two, salon_audit_extend_data)
        if salon_audit_extend_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(salon_audit_extend_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.physical_cash_as_per_zenoti = salon_audit_extend_data[0]['cash_as_zenoti']
            salon_audit.physical_cash_as_per_counter = salon_audit_extend_data[
                0]['cash_dashboard']
            salon_audit.physical_cash_reconciliation = salon_audit_extend_data[
                0]['cash_reconciliation']
            salon_audit.physical_cash_remark = salon_audit_extend_data[0]['remark_1']
            salon_audit.physcial_card_as_per_zenoti = salon_audit_extend_data[0]['card_as_zenoti']
            salon_audit.physcial_card_as_per_counter = salon_audit_extend_data[
                0]['card_dashboard']
            salon_audit.physcial_card_reconciliation = salon_audit_extend_data[
                0]['card_reconciliation']
            salon_audit.physical_card_remark = salon_audit_extend_data[0]['remark_2']
            salon_audit.custom_verification_as_per_zenoti = salon_audit_extend_data[
                0]['custom_as_zenoti']
            salon_audit.custom_verification_as_per_counter = salon_audit_extend_data[
                0]['custom_dashboard']
            salon_audit.custom_verification_reconciliation = salon_audit_extend_data[
                0]['custom_reconciliation']
            salon_audit.custom_verification_remark = salon_audit_extend_data[0]['remark_3']
            salon_audit.save()
        if got_cash_one:
            for one in got_cash_one:
                try:
                    cash_one_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(one['id']))
                except Exception:
                    cash_one_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(one['person_responsible']))
                except Exception:
                    person = None
                cash_one_query.person_responsible = person
                # cash_one_query.relative_gap_found = one['relative_gap']
                cash_one_query.compliance = one['compliance']
                if one['compliance'] == 'Followed':
                    cash_one_query.compliance_category = 'RNR'
                    cash_one_query.compliance_category_percentage = 100
                else:
                    cash_one_query.compliance_category = 'PIP'
                    cash_one_query.compliance_category_percentage = 0
                cash_one_query.save()
        if got_cash_two:
            cash_two_query = SalonAuditRepeatedQuestion.objects.get(
                id=int(got_cash_two[0]['id']))
            try:
                person = ExtendedZenotiEmployeesData.objects.get(
                    id=int(got_cash_two[0]['person_responsible']))
            except Exception:
                person = None
            cash_two_query.person_responsible = person
            # cash_two_query.relative_gap_found = got_cash_two[0]['relative_gap']
            cash_two_query.compliance = got_cash_two[0]['compliance']
            if got_cash_two[0]['compliance'] == 'Followed':
                cash_two_query.compliance_category = 'RNR'
                cash_two_query.compliance_category_percentage = 100
            else:
                cash_two_query.compliance_category = 'PIP'
                cash_two_query.compliance_category_percentage = 0
            cash_two_query.save()
        if got_cash_count:
            try:
                cash_count_query = CashVerificationCashCount.objects.get(
                    id=int(got_cash_count[0]['id']))
            except Exception:
                cash_count_query = None
            cash_count_query.count_2000 = got_cash_count[0]['count_2000']
            cash_count_query.count_500 = got_cash_count[0]['count_500']
            cash_count_query.count_200 = got_cash_count[0]['count_200']
            cash_count_query.count_100 = got_cash_count[0]['count_100']
            cash_count_query.count_50 = got_cash_count[0]['count_50']
            cash_count_query.count_20 = got_cash_count[0]['count_20']
            cash_count_query.count_10 = got_cash_count[0]['count_10']
            cash_count_query.count_5 = got_cash_count[0]['count_5']
            cash_count_query.count_2 = got_cash_count[0]['count_2']
            cash_count_query.count_1 = got_cash_count[0]['count_1']
            cash_count_query.count_50p = got_cash_count[0]['count_50p']
            cash_count_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/cashverification_tab.html")


def edit_audit_hygiene_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_id = data['id']
        print('id', got_id)
        try:
            revenue_audit = SalonRevenueAuditOverview.objects.get(
                id=int(got_id))
        except Exception:
            revenue_audit = None
        print(revenue_audit, 'reven')
        if revenue_audit:
            all_salon_hygiene = HygieneAnnexure.objects.filter(
                revenue_audit=revenue_audit)
            reception_copy = 0
            security_copy = 0
            security_sheet = 0
            feedback_updated = 0
            was_the_rating_above_4 = 0
            was_im_created = 0
            job_card_attached = 0
            job_card_matches = 0
            sa_signature = 0
            for hygiene in all_salon_hygiene:
                if hygiene.reception_copy == 'No':
                    reception_copy += 1
                if hygiene.security_copy == 'No':
                    security_copy += 1
                if hygiene.security_sheet == 'No':
                    security_sheet += 1
                if hygiene.feedback_updated == 'No':
                    feedback_updated += 1
                if hygiene.was_the_rating_above_4 == 'No' or hygiene.was_the_rating_above_4 == 'NA':
                    was_the_rating_above_4 += 1
                if hygiene.if_no_was_the_im_created == 'No' or hygiene.if_no_was_the_im_created == 'NA':
                    was_im_created += 1
                if hygiene.job_card_attached == 'No':
                    job_card_attached += 1
                if hygiene.job_card_matches_invoice == 'No' or hygiene.job_card_matches_invoice == 'NM':
                    job_card_matches += 1
                if hygiene.sa_signature == 'No':
                    sa_signature += 1
            all_checklist_list = SalonAuditRepeatedQuestion.objects.filter(
                revenue_audit=revenue_audit)

            checklist_1 = all_checklist_list.filter(
                checklist_series='5').first()
            checklist_2 = all_checklist_list.filter(
                checklist_series='6').first()
            checklist_3 = all_checklist_list.filter(
                checklist_series='7').first()
            checklist_4 = all_checklist_list.filter(
                checklist_series='8').first()
            checklist_5 = all_checklist_list.filter(
                checklist_series='9').first()
            checklist_6 = all_checklist_list.filter(
                checklist_series='10').first()
            checklist_7 = all_checklist_list.filter(
                checklist_series='11').first()
            checklist_8 = all_checklist_list.filter(
                checklist_series='12').first()
            checklist_9 = all_checklist_list.filter(
                checklist_series='13').first()
            # print(checklist_1.checklist, checklist_2.checklist, checklist_3.checklist, checklist_4.checklist,
            #       checklist_5.checklist, checklist_6.checklist, checklist_7.checklist, checklist_8.checklist, checklist_9.checklist)
            # print('number', reception_copy, security_copy, security_sheet,
            #       feedback_updated, was_the_rating_above_4, job_card_attached, job_card_matches, was_im_created, sa_signature)
            if reception_copy == 0:
                checklist_1.compliance = 'Followed'
                checklist_1.compliance_category = 'RNR'
                checklist_1.compliance_category_percentage = 100
                checklist_1.save()
            else:
                checklist_1.compliance == 'Not Followed'
                checklist_1.compliance_category = 'PIP'
                checklist_1.compliance_category_percentage = 0
                checklist_1.save()

            if security_copy == 0:
                checklist_2.compliance = 'Followed'
                checklist_2.compliance_category = 'RNR'
                checklist_2.compliance_category_percentage = 100
                checklist_2.save()
            else:
                checklist_2.compliance = 'Not Followed'
                checklist_2.compliance_category = 'PIP'
                checklist_2.compliance_category_percentage = 0
                checklist_2.save()

            if security_sheet == 0:
                checklist_3.compliance = 'Followed'
                checklist_3.compliance_category = 'RNR'
                checklist_3.compliance_category_percentage = 100
                checklist_3.save()
            else:
                checklist_3.compliance = 'Not Followed'
                checklist_3.compliance_category = 'PIP'
                checklist_3.compliance_category_percentage = 0
                checklist_3.save()

            if feedback_updated == 0:
                checklist_4.compliance = 'Followed'
                checklist_4.compliance_category = 'RNR'
                checklist_4.compliance_category_percentage = 100
                checklist_4.save()
            else:
                checklist_4.compliance = 'Not Followed'
                checklist_4.compliance_category = 'PIP'
                checklist_4.compliance_category_percentage = 0
                checklist_4.save()

            if was_the_rating_above_4 == 0:
                checklist_5.compliance = 'Followed'
                checklist_5.compliance_category = 'RNR'
                checklist_5.compliance_category_percentage = 100
                checklist_5.save()
            else:
                checklist_5.compliance = 'Not Followed'
                checklist_5.compliance_category = 'PIP'
                checklist_5.compliance_category_percentage = 0
                checklist_5.save()

            if was_im_created == 0:
                checklist_6.compliance = 'Followed'
                checklist_6.compliance_category = 'RNR'
                checklist_6.compliance_category_percentage = 100
                checklist_6.save()
            else:
                checklist_6.compliance = 'Not Followed'
                checklist_6.compliance_category = 'PIP'
                checklist_6.compliance_category_percentage = 0
                checklist_6.save()

            if job_card_attached == 0:
                checklist_7.compliance = 'Followed'
                checklist_7.compliance_category = 'RNR'
                checklist_7.compliance_category_percentage = 100
                checklist_7.save()
            else:
                checklist_7.compliance = 'Not Followed'
                checklist_7.compliance_category = 'PIP'
                checklist_7.compliance_category_percentage = 0
                checklist_7.save()

            if job_card_matches == 0:
                checklist_8.compliance = 'Followed'
                checklist_8.compliance_category = 'RNR'
                checklist_8.compliance_category_percentage = 100
                checklist_8.save()
            else:
                checklist_8.compliance = 'Not Followed'
                checklist_8.compliance_category = 'PIP'
                checklist_8.compliance_category_percentage = 0
                checklist_8.save()

            if sa_signature == 0:
                checklist_9.compliance = 'Followed'
                checklist_9.compliance_category = 'RNR'
                checklist_9.compliance_category_percentage = 100
                checklist_9.save()
            else:
                checklist_9.compliance = 'Not Followed'
                checklist_9.compliance_category = 'PIP'
                checklist_9.compliance_category_percentage = 0
                checklist_9.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "reveue_audit/audit_tabs/hygiene_check_tab.html")


def add_hygiene_check_from_sheet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_list = data['sheet_data']
        revenue_audit_id = data['salon_overview_id']
        print('list', got_list, 'idd:', revenue_audit_id)
        try:
            salon_revenue_Audit = SalonRevenueAuditOverview.objects.get(
                id=int(revenue_audit_id))
        except Exception:
            salon_revenue_Audit = None

        if salon_revenue_Audit:
            for each_list in got_list:
                HygieneAnnexure.objects.create(
                    revenue_audit=salon_revenue_Audit,
                    invoice_number=each_list[0],
                    sample_dates=each_list[1],
                    total_guest=each_list[2],
                    sample_size_for_audit=each_list[3]
                )
                print("list ", each_list)
            return JsonResponse({"msg": "success"})


def edit_salon_audit_extra_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        print(got_query)
        mystery_id = got_query[0]['audit_id']
        action_outlet = got_query[0]['action_outlet']
        status_om = got_query[0]['status_om']
        remark_om = got_query[0]['remark_om']
        action_management = got_query[0]['action_management']
        remark_management = got_query[0]['remark_management']
        expected_intervene = got_query[0]['except_intervene']
        remark_department = got_query[0]['remark_department']
        status_department = got_query[0]['status_department']

        try:
            audit_query = SalonAuditRepeatedQuestion.objects.get(
                id=int(mystery_id))
        except Exception:
            audit_query = None
        if audit_query:
            audit_query.action_taken_by_outlet_manager = action_outlet
            audit_query.status_by_om = status_om
            audit_query.remark_by_om = remark_om
            audit_query.action_taken_by_management = action_management
            audit_query.remark_by_management = remark_management
            audit_query.expected_dept_intervene = expected_intervene
            audit_query.remark_by_department = remark_department
            audit_query.status_by_department = status_department
            audit_query.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "revenue_audit/revenue_audit_overview_tabs.html")


def edit_audit_openbill(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['openbill_check_list']
        unique_question_data = data['openbill_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.open_bill_audit_row_one = unique_question_data[0]['audit_period_1']
            salon_audit.no_of_open_bill_row_one = unique_question_data[0]['no_of_bills_1']
            salon_audit.no_of_clients_on_floor_row_one = unique_question_data[0]['no_of_client_1']
            salon_audit.open_bill_remark_row_one = unique_question_data[0]['bill_remark_1']
            salon_audit.open_bill_audit_row_two = unique_question_data[0]['audit_period_2']
            salon_audit.no_of_open_bill_row_two = unique_question_data[0]['no_of_bills_2']
            salon_audit.no_of_clients_on_floor_row_two = unique_question_data[0]['no_of_client_2']
            salon_audit.open_bill_remark_row_two = unique_question_data[0]['bill_remark_2']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/open_bill_tab.html")


def edit_audit_pushedappointment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['pushappointment_check_list']
        unique_question_data = data['pushappointment_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.pushed_appointment_audit_period_row_one = unique_question_data[0][
                'audit_period_1']
            salon_audit.no_of_appointment_as_per_zenoti_row_one = unique_question_data[
                0]['no_of_appointment_1']
            salon_audit.pushed_appointment_remark_row_one = unique_question_data[0]['remark_1']
            salon_audit.pushed_appointment_audit_period_row_two = unique_question_data[
                0]['audit_period_2']
            salon_audit.no_of_appointment_as_per_zenoti_row_two = unique_question_data[
                0]['no_of_appointment_2']
            salon_audit.pushed_appointment_remark_row_two = unique_question_data[0]['remark_2']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/pushed_appointment_tab.html")


def edit_audit_blockout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['blockout_check_list']
        unique_question_data = data['blockout_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.no_of_blockout_notes_active = unique_question_data[0]['no_of_active']
            salon_audit.no_of_blockout_notes_deleted = unique_question_data[0]['no_of_deleted']
            salon_audit.blockout_remark = unique_question_data[0]['remark']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/block_out_tab.html")


def edit_audit_deleted_service(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_deltedservice_checklist = data['deleted_service_check_list']
        got_deletedservice_annexure = data['deleted_service_annexure']
        if got_deltedservice_checklist:
            for checklist in got_deltedservice_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_deletedservice_annexure:
            print('annexure', got_deletedservice_annexure)
            for annexure in got_deletedservice_annexure:
                print('2', annexure)
                try:
                    ds_annexure_query = DeletedServiceAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    ds_annexure_query = None

                ds_annexure_query.name = annexure['name']
                ds_annexure_query.designation = annexure['designation']
                ds_annexure_query.no_of_services_deleted = annexure['delted_service']
                ds_annexure_query.deleted_without_justification = annexure[
                    'deleted_service_without_justification']
                ds_annexure_query.remarks = annexure['remark']
                ds_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def edit_audit_opening_balance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['openingbalance_check_list']
        unique_question_data = data['openingbalance_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.ob_as_per_statement = unique_question_data[0]['statement']
            salon_audit.ob_as_per_pv = unique_question_data[0]['pv']
            salon_audit.ob_remark = unique_question_data[0]['remark']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/opening_balance_tab.html")


def edit_audit_rectification_bill(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_rectification_checklist = data['rectification_bill_check_list']
        got_rectification_annexure = data['rectification_annexure_list']
        got_rectification_unique_question = data[
            'rectification_bill_unique_question']
        if got_rectification_checklist:
            for checklist in got_rectification_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_rectification_annexure:
            for annexure in got_rectification_annexure:
                print('2', annexure)
                try:
                    ds_annexure_query = RectificationBillAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    ds_annexure_query = None

                ds_annexure_query.bill_no = annexure['bill']
                ds_annexure_query.issue_no = annexure['issue']
                ds_annexure_query.remark = annexure['remark']
                ds_annexure_query.save()
        if got_rectification_unique_question:
            print('unique', got_rectification_unique_question)
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(got_rectification_unique_question[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.rectification_tracker_updated = got_rectification_unique_question[0][
                'tracker_updated']
            salon_audit.no_of_rectification_bill_as_per_zenoti = got_rectification_unique_question[0][
                'no_of_rect_bill']
            salon_audit.no_of_issues_as_per_zenoti_for_rectification_bill = got_rectification_unique_question[0][
                'no_of_rect_issues']
            salon_audit.save()

        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def edit_audit_dcr(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['dcr_check_list']
        unique_question_data = data['dcr_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.dcr_updated = unique_question_data[0]['update']
            salon_audit.dcr_cash_deposited = unique_question_data[0]['deposit']
            salon_audit.dcr_remark = unique_question_data[0]['remark']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/opening_balance_tab.html")


def edit_audit_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['otp_check_list']
        unique_question_data = data['otp_unique_question']
        if unique_question_data:
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.no_of_otp_overrides_as_per_zenoti = unique_question_data[
                0]['otp_override']
            salon_audit.om_approved_otp_overrides = unique_question_data[0]['om_approved']
            salon_audit.otp_override_remark = unique_question_data[0]['remark']
            salon_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(question['id']))
                except Exception:
                    repeated_question_query = None
                try:
                    person = ExtendedZenotiEmployeesData.objects.get(
                        id=int(question['person_responsible']))
                except Exception:
                    person = None
                repeated_question_query.person_responsible = person
                # repeated_question_query.relative_gap_found = question['relative_gap']
                repeated_question_query.compliance = question['compliance']
                if question['compliance'] == 'Followed':
                    repeated_question_query.compliance_category = 'RNR'
                    repeated_question_query.compliance_category_percentage = 100
                else:
                    repeated_question_query.compliance_category = 'PIP'
                    repeated_question_query.compliance_category_percentage = 0
                repeated_question_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/opening_balance_tab.html")


def edit_audit_campaign_offer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_campaign_checklist = data['campaign_offers_check_list']
        got_campaign_annexure = data['campaign_offers_annexure_list']
        got_campaign_unique_question = data[
            'campaign_offers_unique_question']
        if got_campaign_checklist:
            for checklist in got_campaign_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_campaign_annexure:
            for annexure in got_campaign_annexure:
                print('2', annexure)
                try:
                    campaign_annexure_query = CampaignOfferAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    campaign_annexure_query = None

                campaign_annexure_query.date_of_request = annexure['request_date']
                campaign_annexure_query.date_of_redemption = annexure['redemption_date']
                campaign_annexure_query.client_name = annexure['client_name']
                campaign_annexure_query.invoice_number = annexure['invoice_number']
                campaign_annexure_query.guest_code = annexure['guest_code']
                campaign_annexure_query.voucher_value = annexure['voucher_value']
                campaign_annexure_query.remark = annexure['remark']
                campaign_annexure_query.save()
        if got_campaign_unique_question:
            print('unique', got_campaign_unique_question)
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(got_campaign_unique_question[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.total_no_of_membership_redeemed_for_campaign = got_campaign_unique_question[0][
                'membership']
            salon_audit.save()

        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def edit_audit_observation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_observation_checklist = data['observation_check_list']
        got_observation_annexure = data['observation_annexure']
        if got_observation_checklist:
            for checklist in got_observation_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_observation_annexure:
            print('annexure', got_observation_annexure)
            for annexure in got_observation_annexure:
                print('2', annexure)
                try:
                    observation_annexure_query = OtherObservationAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    observation_annexure_query = None

                observation_annexure_query.observation_area = annexure['area']
                observation_annexure_query.audit_findings = annexure['audit_finding']
                observation_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def edit_audit_nearby_voucher(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_voucher_checklist = data['voucher_check_list']
        got_voucher_annexure = data['voucher_annexure_list']
        got_voucher_unique_question = data[
            'voucher_unique_question']
        if got_voucher_checklist:
            for checklist in got_voucher_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_voucher_annexure:
            for annexure in got_voucher_annexure:
                print('2', annexure)
                try:
                    voucher_annexure_query = VoucherAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    voucher_annexure_query = None

                voucher_annexure_query.date_of_request = annexure['date_request']
                voucher_annexure_query.date_of_redemption = annexure['date_redemption']
                voucher_annexure_query.client_name = annexure['name']
                voucher_annexure_query.invoice_number = annexure['invoice_number']
                voucher_annexure_query.guest_code = annexure['guest_code']
                voucher_annexure_query.voucher_value = annexure['value']
                voucher_annexure_query.remark = annexure['remark']
                voucher_annexure_query.save()
        if got_voucher_unique_question:
            print('unique', got_voucher_unique_question)
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(got_voucher_unique_question[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.total_no_of_nearby_transaction_in_zenoti = got_voucher_unique_question[0][
                'transaction']
            salon_audit.total_no_of_audit_sample = got_voucher_unique_question[0][
                'audit_sample']
            salon_audit.remarks_with_voucher_number = got_voucher_unique_question[0][
                'voucher_number']
            salon_audit.without_voucher_number = got_voucher_unique_question[0][
                'without_voucher_number']
            salon_audit.save()

        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def edit_audit_pettycash(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_pettycash_checklist = data['pettycash_check_list']
        got_pettycash_annexure = data['pettycash_annexure_list']
        got_pettycash_unique_question = data[
            'pettycash_unique_question']
        if got_pettycash_checklist:
            for checklist in got_pettycash_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_pettycash_annexure:
            for annexure in got_pettycash_annexure:
                print('2', annexure)
                try:
                    pettycash_annexure_query = PettyCashAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    pettycash_annexure_query = None

                pettycash_annexure_query.voucher_number = annexure['voucher_number']
                pettycash_annexure_query.om_signature_available = annexure['om_signature']
                pettycash_annexure_query.reflecting_in_zenoti = annexure['reflecting']
                pettycash_annexure_query.supporting_document = annexure['supporting_document']
                pettycash_annexure_query.authenticity = annexure['authenticity']
                pettycash_annexure_query.remark = annexure['remark']
                pettycash_annexure_query.save()
        if got_pettycash_unique_question:
            print('unique', got_pettycash_unique_question)
            try:
                salon_audit = SalonRevenueAuditOverview.objects.get(
                    id=int(got_pettycash_unique_question[0]['id']))
            except Exception:
                salon_audit = None
            salon_audit.petty_cash_date = got_pettycash_unique_question[0][
                'date']
            salon_audit.closing_balance_as_per_zenoti = got_pettycash_unique_question[0][
                'closing_balance']
            salon_audit.cash_in_hand = got_pettycash_unique_question[0][
                'cash']
            salon_audit.balance_in_happy_card = got_pettycash_unique_question[0][
                'happy_card']
            salon_audit.petty_cash_remark = got_pettycash_unique_question[0][
                'remark']
            salon_audit.physical_voucher_available = got_pettycash_unique_question[0][
                'physical_voucher']
            salon_audit.audit_sample_size = got_pettycash_unique_question[0][
                'sample_size']
            salon_audit.no_of_voucher_updated_on_zenoti = got_pettycash_unique_question[
                0]['voucher_updated']
            salon_audit.save()

        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/deleted_service_tab.html")


def delete_multiple_salon_hygiene_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_list = data['id_list']
        print('list', got_list)
        for del_id in got_list:
            try:
                annexure_query = HygieneAnnexure.objects.get(id=int(del_id))
            except Exception:
                annexure_query = None
            if annexure_query:
                annexure_query.delete()
        return JsonResponse({"msg": "success"})


def save_salon_hygiene_annexure(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_id = data['annexure_id']
        got_value = data['value']
        got_name = data['name']
        print('list', got_id, got_value, got_name)
        if got_id:
            try:
                annexure_query = HygieneAnnexure.objects.get(id=int(got_id))
            except Exception:
                annexure_query = None
            if got_name == 'invoice_number':
                annexure_query.invoice_number = got_value
                annexure_query.save()
            if got_name == 'sample_date':
                annexure_query.sample_dates = got_value
                annexure_query.save()
            if got_name == 'total_guest':
                annexure_query.total_guest = got_value
                annexure_query.save()
            if got_name == 'sample_size':
                annexure_query.sample_size_for_audit = got_value
                annexure_query.save()
            if got_name == 'reception_copy':
                annexure_query.reception_copy = got_value
                annexure_query.save()
            elif got_name == 'security_copy':
                annexure_query.security_copy = got_value
                annexure_query.save()
            elif got_name == 'security_sheet':
                annexure_query.security_sheet = got_value
                annexure_query.save()
            elif got_name == 'feedback_updated':
                annexure_query.feedback_updated = got_value
                annexure_query.save()
            elif got_name == 'rating_above_4':
                annexure_query.was_the_rating_above_4 = got_value
                annexure_query.save()
            elif got_name == 'im_created':
                annexure_query.if_no_was_the_im_created = got_value
                annexure_query.save()
            elif got_name == 'job_card_attached':
                annexure_query.job_card_attached = got_value
                annexure_query.save()
            elif got_name == 'job_card_matches':
                annexure_query.job_card_matches_invoice = got_value
                annexure_query.save()
            elif got_name == 'sa_signature':
                annexure_query.sa_signature = got_value
                annexure_query.save()
            elif got_name == 'remark_annexure':
                annexure_query.remark = got_value
                annexure_query.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})


@csrf_exempt
def save_salon_hygiene_annexure_file(request):
    if request.method == "POST":
        got_file = request.FILES['file']
        got_id = request.POST.get('annexure_id')
        print('print', got_file, 'body')
        print('post:', request.POST.get(
            'annexure_id'))
        # print(request.body.get('annexure_id'))

        if got_id:
            try:
                annexure_query = HygieneAnnexure.objects.get(id=int(got_id))
            except Exception:
                annexure_query = None
            annexure_query.evidence = got_file
            annexure_query.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})


def edit_audit_cyber_security(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_cyber_checklist = data['cyber_check_list']
        got_cyber_annexure = data['cyber_annexure']
        if got_cyber_checklist:
            for checklist in got_cyber_checklist:
                try:
                    salon_repeated_query = SalonAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    salon_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                salon_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                salon_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    salon_repeated_query.compliance_category = 'RNR'
                    salon_repeated_query.compliance_category_percentage = 100
                else:
                    salon_repeated_query.compliance_category = 'PIP'
                    salon_repeated_query.compliance_category_percentage = 0
                salon_repeated_query.save()
        if got_cyber_annexure:
            print('annexure', got_cyber_annexure)
            for annexure in got_cyber_annexure:
                print('2', annexure)
                try:
                    observation_annexure_query = SalonCyberSecurityAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    observation_annexure_query = None
                observation_annexure_query.area = annexure['area']
                observation_annexure_query.sub_area = annexure['sub_area']
                observation_annexure_query.zenoti_login_id = annexure['zenoti_login']
                observation_annexure_query.used_by = annexure['used_by']
                observation_annexure_query.compliance = annexure['compliance']
                observation_annexure_query.remark = annexure['remark']
                observation_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "reveue_audit/audit_tabs/cyber_security_tab.html")
