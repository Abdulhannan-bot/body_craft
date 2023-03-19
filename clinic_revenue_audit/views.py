from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from body_craft_app.models import UserProfile, ExtendedZenotiCenterData, ExtendedZenotiEmployeesData, Position, OperationOption
from .models import ClinicRevenueAuditOverview, ClinicOtherObservationAnnexure, ClinicAuditRepeatedQuestion, ClinicDeletedServiceAnnexure, ClinicHygieneCheckAnnexure, ClinicRectificationBillAnnexure, ClinicNotRedeemedAnnexure
from django.core.paginator import Paginator, EmptyPage
import json
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime

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
all_clinic_checklist_list = [
    ["Discount Cases", "AE/Billing", "Discount Cases", "1"],
    ["Membership Redemptions", "AE/Billing", "Membership Redemptions", "2"],
    ["Consumables bill quantity matching as per treatment record & consent form (TR, Stickers v/s bill)",
     "OPS", "Hygiene Check", "3"],
    ["Reception copy", "AE/Billing", "Hygiene Check", "4"],
    ["Security copy", "AE/Billing", "Hygiene Check", "6"],
    ["Security Sheet", "AE/Billing", "Hygiene Check", "7"],
    ["Feedback updated", "AE/Billing", "Hygiene Check", "8"],
    ["Job card attached", "AE/Billing", "Hygiene Check", "9"],
    ["Job card matches with Invoice", "AE/Billing", "Hygiene Check", "10"],
    ["360 degree/Client Profile Form", "OPS", "Hygiene Check", "11"],
    ["360 degree/Client Profile Form", "Doctor", "Hygiene Check", "12"],
    ["Disclaimer Form", "OPS", "Hygiene Check", "13"],
    ["Disclaimer Form", "Doctor", "Hygiene Check", "14"],
    ["Consent Form", "OPS", "Hygiene Check", "15"],
    ["Consent Form", "Doctor", "Hygiene Check", "16"],
    ["Client signature matching with all other documents",
        "OPS", "Hygiene Check", "17"],
    ["Client signature matching with all other documents",
        "Doctor", "Hygiene Check", "18"],
    ["Treatment Record entry", "OPS", "Hygiene Check", "19"],
    ["Treatment Record entry", "Doctor", "Hygiene Check", "20"],
    ["Treatment Record entry", "Aesthetician", "Hygiene Check", "21"],
    ["Customer signature in treatment record", "OPS",
     "Hygiene Check", "22"],
    ["Doctors signature in treatment record", "OPS", "Hygiene Check", "23"],
    ["Doctors signature in treatment record", "Doctor", "Hygiene Check", "24"],
    ["Redemption of all service under right package",
     "AE", "Hygiene Check", "25"],
    ["Redemption of all service under right package",
        "Aesthetician", "Hygiene Check", "26"],
    ["Redemption of all service under right package", "Doctor",
     "Hygiene Check", "27"],
    ["Consultant signature", "Doctor", "Hygiene Check", "28"],
    ["Consultant signature", "Aesthetician", "Hygiene Check", "29"],
    ["Not redeemed", "Doctor", "Not redeemed", "30"],
    ["Not redeemed", "OPS", "Not redeemed", "31"],
    ["Not redeemed", "Consultant", "Not redeemed", "32"],
    ["Not redeemed", "Aesthetician", "Not redeemed", "33"],
    ["Not redeemed", "OM", "Not redeemed", "34"],
    ["Deleted Services", "OPS", "Deleted Services", "35"],
    ["Deleted Services", "Consultant", "Deleted Services", "36"],
    ["Rectification bill's", "Doctor", "Rectification bill", "37"],
    ["Rectification bill's", "Aesthetician", "Rectification bill", "38"],
    ["Rectification bill's", "Consultant", "Rectification bill", "39"],
    ["Other Observation", "OM", "Other Observation", "40"],
]


@login_required(login_url='user_login')
def clinic_revenue_audit_overview(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    if is_clinic_revenue_auditor or staffProfile.user_type == 'admin':
        pass
    else:
        return redirect('/')
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_revenue_audit = ClinicRevenueAuditOverview.objects.all()
    all_revenue_audit_detail = ClinicAuditRepeatedQuestion.objects.all()
    if is_clinic_revenue_auditor:
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
        if 'add_clinic_revenue_audit' in request.POST:
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
            new_audit = ClinicRevenueAuditOverview.objects.create(
                added_by=staffProfile,
                center=center,
                auditor_name=auditor_name,
                audit_period_from=from_audit_period,
                audit_period_to=to_audit_period,
                date=audit_date
            )
            for each_checklist in all_clinic_checklist_list:
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
                ClinicAuditRepeatedQuestion.objects.create(
                    revenue_audit=new_audit,
                    checklist=each_checklist[0],
                    responsible_kra=each_checklist[1],
                    person_responsible=person_responsible,
                    tab_name=each_checklist[2],
                    question_series=each_checklist[3]
                )
            ClinicHygieneCheckAnnexure.objects.create(
                revenue_audit=new_audit
            )
            ClinicNotRedeemedAnnexure.objects.create(
                revenue_audit=new_audit
            )
            ClinicDeletedServiceAnnexure.objects.create(
                revenue_audit=new_audit
            )
            ClinicRectificationBillAnnexure.objects.create(
                revenue_audit=new_audit
            )
            ClinicOtherObservationAnnexure.objects.create(
                revenue_audit=new_audit
            )
        if 'del_audit' in request.POST:
            del_audit_id = request.POST.get('del_id')
            try:
                audit_overview = ClinicRevenueAuditOverview.objects.get(
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
                audit = ClinicRevenueAuditOverview.objects.get(
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
        return redirect('clinic_revenue_audit_overview')

    context = {'all_center': all_center,
               'all_revenue_audit': list_page,
               'staffProfile': staffProfile,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_revenue_audit_detail': detail_page,
               'selected_center_id': selected_center_id,
               'searched_from_date': searched_from_date,
               'searched_to_date': searched_to_date,
               'searched_dept': searched_dept, 'searched_om': searched_om,
               'searched_compliance': searched_compliance}
    return render(request, "clinic_revenue_audit/clinic_audit_main_tabs.html", context)
# Create your views here.


def edit_clinic_revenue_audit_overview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            audit_overview = ClinicRevenueAuditOverview.objects.get(
                id=int(got_query))
        except Exception:
            audit_overview = None

        audit_json = serializers.serialize('json', [audit_overview])
        return JsonResponse({"msg": "success",
                            "mystery_json": json.loads(audit_json)})
    return render(request, "clinic_revenue_audit/clinic_audit_main_tabs.html")


def edit_clinic_audit_extra_data(request):
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
            audit_query = ClinicAuditRepeatedQuestion.objects.get(
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


@login_required(login_url='user_login')
def clinic_revenue_audit_profile_page(request, pk):
    user = request.user
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    staffProfile = UserProfile.objects.get(user=user)
    revenue_audit = ClinicRevenueAuditOverview.objects.get(id=int(pk))
    all_employee = ExtendedZenotiEmployeesData.objects.filter(
        associated_center=revenue_audit.center)
    all_discount_cases_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Discount Cases')
    all_membership_redemption_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Membership Redemptions'
    )
    all_hygiene_check_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Hygiene Check'
    )
    all_hygiene_annexure = ClinicHygieneCheckAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_not_redeemed_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Not redeemed'
    )
    all_not_redeemed_annexure = ClinicNotRedeemedAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_deleted_services_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Deleted Services'
    )
    all_deleted_service_annexure = ClinicDeletedServiceAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_rectification_bill_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Rectification bill'
    )
    all_rectification_bill_annexure = ClinicRectificationBillAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_other_observation_checklist = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit, tab_name='Other Observation'
    )
    all_other_observation_annexure = ClinicOtherObservationAnnexure.objects.filter(
        revenue_audit=revenue_audit
    )
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_repeated_question = ClinicAuditRepeatedQuestion.objects.filter(
        revenue_audit=revenue_audit
    )
    if request.method == 'POST':
        if 'create_one_hygiene_annexure_row' in request.POST:
            ClinicHygieneCheckAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'hygiene_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                ClinicHygieneCheckAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'hygiene_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = ClinicHygieneCheckAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
            all_annexure_query = ClinicHygieneCheckAnnexure.objects.filter(
                revenue_audit=revenue_audit
            )
            all_checklist_query = ClinicAuditRepeatedQuestion.objects.filter(
                revenue_audit=revenue_audit, tab_name='Hygiene Check'
            )
            if not all_annexure_query:
                for each_checklist in all_checklist_query:
                    each_checklist.compliance = ''
                    each_checklist.compliance_category = ''
                    each_checklist.compliance_category_percentage = ''
                    each_checklist.save()
        if 'create_one_clinic_not_redeemed_annexure_row' in request.POST:
            ClinicNotRedeemedAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'clinic_not_redeemed_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                ClinicNotRedeemedAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'not_redeemed_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = ClinicNotRedeemedAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
            all_annexure_query = ClinicNotRedeemedAnnexure.objects.filter(
                revenue_audit=revenue_audit
            )
            all_checklist_query = ClinicAuditRepeatedQuestion.objects.filter(
                revenue_audit=revenue_audit, tab_name='Not redeemed'
            )
            if not all_annexure_query:
                for each_checklist in all_checklist_query:
                    each_checklist.compliance = ''
                    each_checklist.compliance_category = ''
                    each_checklist.compliance_category_percentage = ''
                    each_checklist.save()
        if 'create_one_deleted_service_annexure_row' in request.POST:
            ClinicDeletedServiceAnnexure.objects.create(
                revenue_audit=revenue_audit
            )
        if 'deleted_service_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                ClinicDeletedServiceAnnexure.objects.create(
                    revenue_audit=revenue_audit
                )
        if 'deleted_service_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = ClinicDeletedServiceAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
            all_annexure_query = ClinicDeletedServiceAnnexure.objects.filter(
                revenue_audit=revenue_audit
            )
            all_checklist_query = ClinicAuditRepeatedQuestion.objects.filter(
                revenue_audit=revenue_audit, tab_name='Deleted Services'
            )
            if not all_annexure_query:
                for each_checklist in all_checklist_query:
                    each_checklist.compliance = ''
                    each_checklist.compliance_category = ''
                    each_checklist.compliance_category_percentage = ''
                    each_checklist.save()
        if 'create_one_clinic_rectification_annexure_row' in request.POST:
            ClinicRectificationBillAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'clinic_rectification_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                ClinicRectificationBillAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'clinic_rectification_bill_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = ClinicRectificationBillAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
            # all_annexure_query = ClinicRectificationBillAnnexure.objects.filter(
            #     revenue_audit=revenue_audit
            # )
            # all_checklist_query = ClinicAuditRepeatedQuestion.objects.filter(
            #     revenue_audit=revenue_audit, tab_name='Rectification bill'
            # )
            # if not all_annexure_query:
            #     for each_checklist in all_checklist_query:
            #         each_checklist.compliance = ''
            #         each_checklist.compliance_category = ''
            #         each_checklist.compliance_category_percentage = ''
            #         each_checklist.save()
        if 'create_one_clinic_observation_annexure_row' in request.POST:
            ClinicOtherObservationAnnexure.objects.create(
                revenue_audit=revenue_audit)
        if 'clinic_observation_annexure_multiple_row' in request.POST:
            rows = request.POST.get('annexure_row')
            for i in range(int(rows)):
                ClinicOtherObservationAnnexure.objects.create(
                    revenue_audit=revenue_audit)
        if 'observation_annexure_del_row' in request.POST:
            del_id = request.POST.get('del_id')
            try:
                annexure_query = ClinicOtherObservationAnnexure.objects.get(
                    id=int(del_id))
            except Exception:
                annexure_query = None
            annexure_query.delete()
            all_annexure_query = ClinicOtherObservationAnnexure.objects.filter(
                revenue_audit=revenue_audit
            )
            all_checklist_query = ClinicAuditRepeatedQuestion.objects.filter(
                revenue_audit=revenue_audit, tab_name='Other Observation'
            )
            if not all_annexure_query:
                for each_checklist in all_checklist_query:
                    each_checklist.compliance = ''
                    each_checklist.compliance_category = ''
                    each_checklist.compliance_category_percentage = ''
                    each_checklist.save()
        return redirect('clinic_revenue_audit_profile', pk=pk)
    context = {'all_center': all_center,
               'staffProfile': staffProfile,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_discount_cases': all_discount_cases_checklist,
               'all_membership_redemption': all_membership_redemption_checklist,
               'all_hygiene_check_checklist': all_hygiene_check_checklist,
               'all_hygiene_annexure': all_hygiene_annexure,
               'all_deleted_services_checklist': all_deleted_services_checklist,
               'all_rectification_bill_checklist': all_rectification_bill_checklist,
               'all_other_observation_checklist': all_other_observation_checklist,
               'all_deleted_service_annexure': all_deleted_service_annexure,
               'all_rectification_bill_annexure': all_rectification_bill_annexure,
               'all_other_observation_annexure': all_other_observation_annexure,
               'all_not_redeemed_checklist': all_not_redeemed_checklist,
               'all_not_redeemed_annexure': all_not_redeemed_annexure,
               'all_repeated_question': all_repeated_question,
               'all_employee': all_employee,
               'revenue_audit': revenue_audit}
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html", context)


def edit_audit_discount_cases(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['discountchecklist_check_list']
        unique_question_data = data['discountchecklist_unique_question']
        if unique_question_data:
            try:
                clinic_audit = ClinicRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                clinic_audit = None
            clinic_audit.total_discount_cases_as_per_zenoti = unique_question_data[
                0]['as_zenoti']
            clinic_audit.total_approvals_verified = unique_question_data[0]['verified']
            clinic_audit.dicount_cases_remark = unique_question_data[0]['remark']
            clinic_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = ClinicAuditRepeatedQuestion.objects.get(
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
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_audit_membership_redemption(request):
    if request.method == "POST":
        data = json.loads(request.body)
        repeated_question_data = data['membershipchecklist_check_list']
        unique_question_data = data['membershipchecklist_unique_question']
        if unique_question_data:
            try:
                clinic_audit = ClinicRevenueAuditOverview.objects.get(
                    id=int(unique_question_data[0]['id']))
            except Exception:
                clinic_audit = None
            clinic_audit.total_membership_redemption_as_per_zenoti = unique_question_data[
                0]['as_zenoti']
            clinic_audit.membership_redemption_remark = unique_question_data[0]['remark']
            clinic_audit.save()
        if repeated_question_data:
            for question in repeated_question_data:
                try:
                    repeated_question_query = ClinicAuditRepeatedQuestion.objects.get(
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
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_audit_clinic_hygiene_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_hygiene_checklist = data['hygine_checklist']
        got_hygiene_annexure = data['hygiene_annexure_list']
        if got_hygiene_checklist:
            for checklist in got_hygiene_checklist:
                try:
                    clinic_repeated_query = ClinicAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    clinic_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                clinic_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                clinic_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    clinic_repeated_query.compliance_category = 'RNR'
                    clinic_repeated_query.compliance_category_percentage = 100
                elif checklist['compliance'] == 'Partially Followed':
                    clinic_repeated_query.compliance_category = 'Benchmark KRA'
                    clinic_repeated_query.compliance_category_percentage = 50
                else:
                    clinic_repeated_query.compliance_category = 'PIP'
                    clinic_repeated_query.compliance_category_percentage = 0
                clinic_repeated_query.save()
        if got_hygiene_annexure:
            print('annexure', got_hygiene_annexure)
            for annexure in got_hygiene_annexure:
                print('2', annexure)
                try:
                    hygiene_annexure_query = ClinicHygieneCheckAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    hygiene_annexure_query = None

                hygiene_annexure_query.sample_dates = annexure['sample_date']
                hygiene_annexure_query.total_guest = annexure['total_guest']
                hygiene_annexure_query.sample_size_for_audit = annexure['sample_size']
                hygiene_annexure_query.invoice_date = annexure['invoice_date']
                hygiene_annexure_query.invoice_number = annexure['invoice_number']
                hygiene_annexure_query.client_name = annexure['client_name']
                hygiene_annexure_query.category_of_sample = annexure['category_of_sample']
                hygiene_annexure_query.quantity_of_injectable_as_per_bill = annexure[
                    'injectable_bill']
                hygiene_annexure_query.quantity_of_injectable_as_per_consent_form = annexure[
                    'injectable_consent']
                hygiene_annexure_query.quantity_of_injectable_as_per_treatment_record = annexure[
                    'injectable_treatment']
                hygiene_annexure_query.consumable_bill_quantity_matching_as_per_treatment_record = annexure[
                    'consumable_bill']
                hygiene_annexure_query.reception_copy = annexure['reception_copy']
                hygiene_annexure_query.security_copy = annexure['security_copy']
                hygiene_annexure_query.security_sheet = annexure['security_sheet']
                hygiene_annexure_query.feedback_updated = annexure['feedback_updated']
                hygiene_annexure_query.job_card_attached = annexure['job_card_attached']
                hygiene_annexure_query.job_card_matches_invoice = annexure['job_card_matches']
                hygiene_annexure_query.client_profile_form = annexure['client_form']
                hygiene_annexure_query.disclaimer_form = annexure['disclaimer_form']
                hygiene_annexure_query.consent_form = annexure['consent_form']
                hygiene_annexure_query.client_signature_matching_all_docs = annexure[
                    'client_signature']
                hygiene_annexure_query.treatment_record_entry = annexure['treatment_entry']
                hygiene_annexure_query.customer_signature_treatment_record = annexure[
                    'customer_signature']
                hygiene_annexure_query.doctor_signature_treatment_record = annexure[
                    'doctor_signature']
                hygiene_annexure_query.redemption_of_all_service_under_right_package = annexure[
                    'redemption_services']
                hygiene_annexure_query.consultant_signature = annexure['consultant_signature']
                hygiene_annexure_query.evidence = annexure['evidence']
                hygiene_annexure_query.remark = annexure['remark']
                hygiene_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_clinic_audit_deleted_service(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_deltedservice_checklist = data['deleted_service_check_list']
        got_deletedservice_annexure = data['deleted_service_annexure']
        if got_deltedservice_checklist:
            for checklist in got_deltedservice_checklist:
                try:
                    clinic_repeated_query = ClinicAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    clinic_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                clinic_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                clinic_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    clinic_repeated_query.compliance_category = 'RNR'
                    clinic_repeated_query.compliance_category_percentage = 100
                else:
                    clinic_repeated_query.compliance_category = 'PIP'
                    clinic_repeated_query.compliance_category_percentage = 0
                clinic_repeated_query.save()
        if got_deletedservice_annexure:
            print('annexure', got_deletedservice_annexure)
            for annexure in got_deletedservice_annexure:
                print('2', annexure)
                try:
                    ds_annexure_query = ClinicDeletedServiceAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    ds_annexure_query = None

                ds_annexure_query.name = annexure['name']
                ds_annexure_query.designation = annexure['designation']
                ds_annexure_query.no_of_services_deleted = annexure['delted_service']
                ds_annexure_query.deleted_without_proper_justification = annexure[
                    'deleted_service_without_justification']
                ds_annexure_query.remark = annexure['remark']
                ds_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_clinic_audit_rectification_bill(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_rectification_checklist = data['rectification_bill_check_list']
        got_rectification_annexure = data['rectification_annexure_list']
        got_rectification_unique_question = data[
            'rectification_bill_unique_question']
        if got_rectification_checklist:
            for checklist in got_rectification_checklist:
                try:
                    clinic_repeated_query = ClinicAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    clinic_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                clinic_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                clinic_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    clinic_repeated_query.compliance_category = 'RNR'
                    clinic_repeated_query.compliance_category_percentage = 100
                else:
                    clinic_repeated_query.compliance_category = 'PIP'
                    clinic_repeated_query.compliance_category_percentage = 0
                clinic_repeated_query.save()
        if got_rectification_annexure:
            for annexure in got_rectification_annexure:
                print('2', annexure)
                try:
                    rectification_annexure_query = ClinicRectificationBillAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    rectification_annexure_query = None

                rectification_annexure_query.bill_no = annexure['bill']
                rectification_annexure_query.issue_no = annexure['issue']
                rectification_annexure_query.remark = annexure['remark']
                rectification_annexure_query.save()
        if got_rectification_unique_question:
            print('unique', got_rectification_unique_question)
            try:
                clinic_audit = ClinicRevenueAuditOverview.objects.get(
                    id=int(got_rectification_unique_question[0]['id']))
            except Exception:
                clinic_audit = None
            clinic_audit.rectification_tracker_maintained = got_rectification_unique_question[0][
                'tracker_updated']
            clinic_audit.no_of_rectification_bill_as_per_zenoti = got_rectification_unique_question[0][
                'no_of_rect_bill']
            clinic_audit.no_of_issues_as_per_zenoti_rectification = got_rectification_unique_question[0][
                'no_of_rect_issues']
            clinic_audit.save()

        return JsonResponse({"msg": "success"})
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_clinic_audit_other_observation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_observation_checklist = data['observation_check_list']
        got_observation_annexure = data['observation_annexure']
        if got_observation_checklist:
            for checklist in got_observation_checklist:
                try:
                    salon_repeated_query = ClinicAuditRepeatedQuestion.objects.get(
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
                    observation_annexure_query = ClinicOtherObservationAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    observation_annexure_query = None

                observation_annexure_query.observation_area = annexure['area']
                observation_annexure_query.audit_findings = annexure['audit_finding']
                observation_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")


def edit_clinic_audit_not_redeemed(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # got_file = data
        # print('file', got_file.files)
        got_notredeemed_checklist = data['not_redeemed_check_list']
        got_notredeemed_annexure = data['not_redeemed_annexure']
        if got_notredeemed_checklist:
            for checklist in got_notredeemed_checklist:
                try:
                    clinic_repeated_query = ClinicAuditRepeatedQuestion.objects.get(
                        id=int(checklist['id']))
                except Exception:
                    clinic_repeated_query = None
                try:
                    user_response = ExtendedZenotiEmployeesData.objects.get(
                        id=int(checklist['person_responsible']))
                except Exception:
                    user_response = None
                clinic_repeated_query.person_responsible = user_response
                # salon_repeated_query.relative_gap_found = checklist['relative_gap']
                clinic_repeated_query.compliance = checklist['compliance']
                if checklist['compliance'] == 'Followed':
                    clinic_repeated_query.compliance_category = 'RNR'
                    clinic_repeated_query.compliance_category_percentage = 100
                else:
                    clinic_repeated_query.compliance_category = 'PIP'
                    clinic_repeated_query.compliance_category_percentage = 0
                clinic_repeated_query.save()
        if got_notredeemed_annexure:
            print('annexure', got_notredeemed_annexure)
            for annexure in got_notredeemed_annexure:
                # print(type(annexure['evidence']))
                print('2', annexure)
                try:
                    notredeemed_annexure_query = ClinicNotRedeemedAnnexure.objects.get(
                        id=int(annexure['id']))
                except Exception:
                    notredeemed_annexure_query = None

                notredeemed_annexure_query.date_as_per_record = annexure['date_record']
                notredeemed_annexure_query.phone_number = annexure['phone']
                notredeemed_annexure_query.client_name = annexure['name']
                notredeemed_annexure_query.category_of_sample = annexure['category_sample']
                notredeemed_annexure_query.quantity_of_not_redeemed = annexure['quantity']
                notredeemed_annexure_query.evidence = None
                notredeemed_annexure_query.save()
        return JsonResponse({"msg": "success"})
    return render(request, "clinic_revenue_audit/clinic_audit_profile_tabs.html")
