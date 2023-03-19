from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from body_craft_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CorporateAuditOverview, CorporateAuditDetail
from body_craft_app.models import ExtendedZenotiEmployeesData, ExtendedZenotiCenterData, ZenotiEmployeesData
from .forms import CorporateAuditForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from urllib.request import urlopen
import json
from django.http import JsonResponse
from django.core import serializers
# Create your views here.

compliance_category_percentage = {
    "RNR": 100,
    "Benchmark KRA": 50,
    "CPI": 0,
    "PIP": 0,
    "Education": 0
}

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


@login_required(login_url='user_login')
def corporate_audit_overview(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    if staffProfile.user_type == 'admin' or is_corporate_auditor:
        pass
    else:
        return redirect('/')
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_employee = ExtendedZenotiEmployeesData.objects.all()
    all_corporate = CorporateAuditOverview.objects.all()
    all_corporate_detail = CorporateAuditDetail.objects.all()
    if is_corporate_auditor:
        all_corporate = CorporateAuditOverview.objects.filter(
            added_by=staffProfile)
        all_corporate_detail = all_corporate_detail.filter(
            corporate_audit__in=all_corporate)
    all_therapy_ext_emp = ExtendedZenotiEmployeesData.objects.all()
    corporate_form = CorporateAuditForm(request.POST or None)
    selected_center_id = request.GET.get('select_center')
    searched_from_date = request.GET.get('searched_from_date')
    searched_to_date = request.GET.get('searched_to_date')
    searched_text = request.GET.get('searched_text')
    searched_compliance = request.GET.getlist('searched_compliance')
    searched_kra = request.GET.get('searched_kra')
    searched_dept = request.GET.get('searched_dept')
    searched_om = request.GET.get('searched_om')
    unique_kra_fieled = CorporateAuditDetail.objects.order_by(
    ).values_list('kra', flat=True).distinct()
    try:
        selected_center = ExtendedZenotiCenterData.objects.get(
            id=int(selected_center_id))
    except Exception:
        selected_center = None

    if selected_center:
        all_corporate = all_corporate.filter(center=selected_center)
        all_corporate_detail = all_corporate_detail.filter(
            center=selected_center)

    if searched_from_date:
        all_corporate = all_corporate.filter(date__gte=searched_from_date)

    if searched_to_date:
        all_corporate = all_corporate.filter(date__lte=searched_to_date)

    if searched_compliance:
        all_corporate_detail = all_corporate_detail.filter(
            compliance_category__in=searched_compliance)

    if searched_kra:
        all_corporate_detail = all_corporate_detail.filter(kra=searched_kra)

    if searched_om:
        all_corporate_detail = all_corporate_detail.filter(
            status_by_om=searched_om
        )
    if searched_dept:
        all_corporate_detail = all_corporate_detail.filter(
            status_by_department=searched_dept
        )
    corporate_overview_query = []
    for overview in all_corporate:
        temp = {}
        temp['id'] = overview.id
        temp['added_by'] = overview.added_by.user.first_name
        temp['added_on'] = overview.added_on
        temp['shopper_name'] = overview.shopper_name
        temp['date'] = overview.date
        temp['start_time'] = overview.start_time
        temp['end_time'] = overview.end_time
        temp['center'] = overview.center.zenoti_data.name
        temp['invoice_number'] = overview.invoice_number
        temp['admin_reviewed'] = overview.admin_reviewed
        temp['auditor_completed'] = overview.auditor_completed
        this_overview_detail = CorporateAuditDetail.objects.filter(
            corporate_audit=overview)
        # total_question = this_overview_detail.count()
        # total_question_done = 0
        # for detail in this_overview_detail:
        #     if not detail.compliance == 'NA':
        #         if detail.compliance and detail.staff:
        #             total_question_done += 1
        # get_percentage = (total_question_done / total_question) * 100
        # print('per', get_percentage)
        # temp['percentage'] = "{:.2f}".format(get_percentage)
        temp['percentage'] = 50
        corporate_overview_query.append(temp)
    # print('print', mystery_overview_query)

    # list pagination
    page = Paginator(corporate_overview_query, 20)
    list_page_num = request.GET.get('page', 1)
    try:
        list_page = page.page(list_page_num)
    except EmptyPage:
        list_page = page.page(1)

    # detail pagination
    page_2 = Paginator(all_corporate_detail, 50)
    detail_page_num = request.GET.get('page_2', 1)
    try:
        detail_page = page_2.page(detail_page_num)
    except EmptyPage:
        detail_page = page_2.page(1)

    if request.method == 'POST':
        data_json = open("corporate_audit.txt", "r")
        corporate_detail_data = json.loads(data_json.read())
        if 'corporate_form' in request.POST:
            if corporate_form.is_valid():
                new_mystery = corporate_form.save(commit=False)
                new_mystery.added_by = staffProfile
                new_mystery.save()
                for overview in corporate_detail_data:
                    # print('ser', service_responsible)
                    CorporateAuditDetail.objects.create(
                        corporate_audit=new_mystery,
                        center=new_mystery.center,
                        date=new_mystery.date,
                        sequence=overview['Sequence'],
                        kra=overview['Protocol'],
                        checklist=overview['Audit Checklist'],
                        relative_gaps_found=overview['Audit Methodology'],
                        compliance_dropdown=overview['dropdown'],
                    )
        if 'del_corporate' in request.POST:
            del_corporate_id = request.POST.get('del_id')
            try:
                corporate_audit = CorporateAuditOverview.objects.get(
                    id=int(del_corporate_id))
            except Exception:
                corporate_audit = None
            corporate_audit.delete()
        if 'edit_corporate' in request.POST:
            print('data', request.POST)
            corporate_id = request.POST.get('mystery_pk')
            center_id = request.POST.get('edit_center')
            shopper_name = request.POST.get('edit_shopper_name')
            phone = request.POST.get('edit_phone')
            email = request.POST.get('edit_email')
            gender = request.POST.get('edit_gender')
            start_time = request.POST.get('edit_start')
            end_time = request.POST.get('edit_end')
            date = request.POST.get('edit_date')
            cost_of_service = request.POST.get('edit_cost_of_service')
            invoice_number = request.POST.get('edit_invoice_number')
            admin_reviewed = request.POST.get('edit_admin_review')
            auditor_completed = request.POST.get('edit_auditor_completed')
            paid_in_cash = request.POST.get('edit_paid_cash')
            payment_mode = request.POST.get('edit_payment_mode')
            amount_redeemed = request.POST.get('edit_amount_redeemed')
            number_reached = request.POST.get('edit_number_reached')

            print('edit', request.POST.get('edit_admin_review'),
                  request.POST.get('edit_auditor_completed'))
            if admin_reviewed == 'on':
                add_admin_review = True
            else:
                add_admin_review = False

            if auditor_completed == 'on':
                add_auditor_completed = True
            else:
                add_auditor_completed = False
            # print('id', mystery_id, center_id)

            try:
                corporate = CorporateAuditOverview.objects.get(
                    id=int(corporate_id))
            except Exception:
                corporate = None

            try:
                center = ExtendedZenotiCenterData.objects.get(
                    id=int(center_id))
            except Exception:
                center = None

            try:
                corporate_detail = CorporateAuditDetail.objects.filter(
                    corporate_audit=corporate)
            except Exception:
                corporate_detail = None

            corporate.center = center
            corporate.shopper_name = shopper_name
            corporate.mobile = phone
            corporate.email = email
            corporate.gender = gender
            corporate.start_time = start_time
            corporate.end_time = end_time
            corporate.date = date
            corporate.cost_of_service = cost_of_service
            corporate.invoice_number = invoice_number
            corporate.admin_reviewed = add_admin_review
            corporate.auditor_completed = add_auditor_completed
            corporate.paid_in_cash = paid_in_cash
            corporate.payment_mode = payment_mode
            corporate.amount_redeemed = amount_redeemed
            corporate.contact_number_reached_for_appointment = number_reached
            corporate.save()
            for each_detail in corporate_detail:
                each_detail.center = center
                each_detail.date = date
                each_detail.save()
        return redirect('corporate_audit_overview')
    context = {'all_corporate': list_page,
               'staffProfile': staffProfile,
               'is_corporate_auditor': is_corporate_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'corporate_form': corporate_form,
               'all_center': all_center,
               'all_corporate_detail': detail_page,
               'all_employee': all_employee,
               'selected_center_id': selected_center_id,
               'searched_from_date': searched_from_date,
               'searched_to_date': searched_to_date,
               'searched_text': searched_text,
               'searched_compliance': searched_compliance,
               'unique_kra_filed': unique_kra_fieled,
               'searched_kra': searched_kra,
               'searched_dept': searched_dept,
               'searched_om': searched_om,
               'compliance_category_percentage': compliance_category_percentage,
               'all_therapy_ext_emp': all_therapy_ext_emp}
    return render(request, "corporate_audit/overview_tab.html", context)


def edit_corporate_audit_overview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            corporate_audit = CorporateAuditOverview.objects.get(
                id=int(got_query))
        except Exception:
            corporate_audit = None

        corporate_json = serializers.serialize('json', [corporate_audit])
        return JsonResponse({"msg": "success",
                            "mystery_json": json.loads(corporate_json)})
    return render(request, "corporate_audit/overview_tab.html")


@login_required(login_url='user_login')
def corporate_audit_detail(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    try:
        corporate_audit = CorporateAuditOverview.objects.get(id=int(pk))
    except Exception:
        corporate_audit = None
    all_employee = ExtendedZenotiEmployeesData.objects.filter(
        associated_center=corporate_audit.center)
    all_corporate_detail = CorporateAuditDetail.objects.filter(
        corporate_audit=corporate_audit)
    context = {'all_corporate_detail': all_corporate_detail,
               'staffProfile': staffProfile,
               'is_corporate_auditor': is_corporate_auditor,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'all_employee': all_employee,
               'total_length': all_corporate_detail.count(),
               'corporate_audit': corporate_audit}
    return render(request, "corporate_audit/profile_tab.html", context)


def edit_corporate_audit_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        print('get_query', got_query)
        if got_query:
            for query in got_query:
                mystery_shopping_detail = CorporateAuditDetail.objects.get(
                    id=int(query['id']))
                try:
                    employee = ExtendedZenotiEmployeesData.objects.get(
                        id=int(query['staff']))
                except Exception:
                    employee = None
                compliance_value = query['compliance']
                mystery_shopping_detail.compliance = query['compliance']
                mystery_shopping_detail.remark = query['remark']
                mystery_shopping_detail.staff = employee
                try:
                    mystery_shopping_detail.compliance_category = compliance_category_value[
                        compliance_value]
                except Exception:
                    mystery_shopping_detail.compliance_category = ''
                try:
                    mystery_shopping_detail.compliance_category_percentage = compliance_category_percentage[compliance_category_value[
                        compliance_value]]
                except Exception:
                    mystery_shopping_detail.compliance_category_percentage = ''
                mystery_shopping_detail.save()
                # print(query)
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    context = {}
    return render(request, "corporate_audit/profile_tab.html.html", context)


def edit_corporate_extra_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        print(got_query)
        mystery_id = got_query[0]['mystery_id']
        action_outlet = got_query[0]['action_outlet']
        status_om = got_query[0]['status_om']
        remark_om = got_query[0]['remark_om']
        action_management = got_query[0]['action_management']
        remark_management = got_query[0]['remark_management']
        expected_intervene = got_query[0]['except_intervene']
        remark_department = got_query[0]['remark_department']
        status_department = got_query[0]['status_department']

        try:
            mystery = CorporateAuditDetail.objects.get(id=int(mystery_id))
        except Exception:
            mystery = None
        if mystery:
            mystery.action_taken_by_outlet_manager = action_outlet
            mystery.status_by_om = status_om
            mystery.remark_by_om = remark_om
            mystery.action_taken_by_management = action_management
            mystery.remark_by_management = remark_management
            mystery.expected_dept_intervene = expected_intervene
            mystery.remark_by_department = remark_department
            mystery.status_by_department = status_department
            mystery.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "corporate_audit/overview_tab.html.html")
