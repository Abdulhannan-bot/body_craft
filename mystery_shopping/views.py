from django.shortcuts import render, redirect, HttpResponse
from body_craft_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from .models import MysteryShoppingOverview, MysteryShoppingDetail, MysteryShoppingImages, MonthAudit
from body_craft_app.models import ExtendedZenotiEmployeesData, ExtendedZenotiCenterData, ZenotiEmployeesData, UserTypes
from .forms import MysteryShoppingForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from urllib.request import urlopen
import json
import csv
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


@login_required(login_url='user_login')
def audit_users(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    if staffProfile.user_type == 'admin' or is_audit_admin:
        pass
    else:
        return redirect('/')
    audit_user = UserProfile.objects.filter(
        user_type='Auditor')
    all_audit_type = UserTypes.objects.all()
    if request.method == "POST":
        if 'new_audit_user' in request.POST:
            phone = request.POST.get("phone")
            passcode = request.POST.get("passcode")
            name = request.POST.get("name")
            username = request.POST.get("email")
            usertype = request.POST.getlist("user_type")
            is_roster = request.POST.get("is_roster")
            if is_roster == 'on':
                is_roster = True
            else:
                is_roster = False
            try:
                already_user = User.objects.get(username=username)
            except Exception:
                already_user = None
                # print('user', already_user)
            if already_user is None:
                new_user = User.objects.create_user(
                    username=username, password=passcode, first_name=name)
                new_userprofile = UserProfile.objects.create(
                    user=new_user,
                    phone=phone,
                    email=username,
                    password=passcode,
                    user_type='Auditor',
                    user_status='Active',
                    roster_access=is_roster
                )
                selected_user_type = UserTypes.objects.filter(id__in=usertype)
                print(selected_user_type)
                new_userprofile.user_type_name.set(selected_user_type)
                return redirect('audit_users')
            else:
                messages.info(
                    request, 'This Email Id is already exist in our DataBase')
        if 'edit_audit_user' in request.POST:
            user_id = request.POST.get('audit_user_id')
            name = request.POST.get('edit_name')
            phone = request.POST.get('edit_phone')
            email = request.POST.get('edit_email')
            user_type = request.POST.getlist('edit_user_type')
            user_status = request.POST.get('edit_user_status')
            edit_is_roster = request.POST.get("edit_is_roster")
            passcode = request.POST.get('edit_passcode')
            print('status', user_status)
            try:
                audit_user = UserProfile.objects.get(id=int(user_id))
            except Exception:
                audit_user = None

            if edit_is_roster == 'on':
                edit_is_roster = True
            else:
                edit_is_roster = False
            selected_user_type = UserTypes.objects.filter(id__in=user_type)
            audit_user.phone = phone
            audit_user.email = email
            audit_user.user_status = user_status
            audit_user.roster_access = edit_is_roster
            audit_user.password = passcode
            audit_user.user_type_name.set(selected_user_type)
            audit_user.save()

            main_user = audit_user.user
            main_user.first_name = name
            main_user.set_password(passcode)
            main_user.save()
            return redirect('audit_users')
    context = {'audit_user': audit_user,
               'staffProfile': staffProfile,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_audit_type': all_audit_type}
    return render(request, "mystery_shopping/audit_user_page.html", context)


def edit_audit_user_modal_popup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            audit_user = UserProfile.objects.get(
                id=int(got_query))
        except Exception:
            audit_user = None
        user_json = serializers.serialize('json', [audit_user])
        return JsonResponse({"msg": "success",
                            "user_json": json.loads(user_json), 'user_name': audit_user.user.first_name})
    return render(request, "mystery_shopping/mystery_shopping_tabs_page.html")


@login_required(login_url='user_login')
def mystery_shopping_overview(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()

    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    # all_employee = ExtendedZenotiEmployeesData.objects.all()
    all_mystery = MysteryShoppingOverview.objects.all().order_by('-id')
    all_months = MonthAudit.objects.all()
    all_mystery_detail = MysteryShoppingDetail.objects.filter(
        audit_status__in=['Completed', 'Action Required', 'Action Taken'])
    all_mystery_image = MysteryShoppingImages.objects.all()
    all_therapy_ext_emp = ExtendedZenotiEmployeesData.objects.all()
    mystery_form = MysteryShoppingForm(request.POST or None)
    if is_mystery_shopper:
        all_mystery = MysteryShoppingOverview.objects.filter(
            added_by=staffProfile)
        all_mystery_detail = all_mystery_detail.filter(
            mystery_shopping__in=all_mystery)
        all_mystery_image = all_mystery_image.filter(
            mystery_shopping__in=all_mystery
        )

    if staffProfile.user_type == 'staff':
        zenoti_data = ZenotiEmployeesData.objects.get(user=staffProfile)
        extended_zenoti_data = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=zenoti_data)
        all_center = extended_zenoti_data.associated_center.all()
        # print('print', all_mystery.first().admin_reviewed)
        all_reviewed_mystery = all_mystery.filter(admin_reviewed=True)
        # print('.....', all_reviewed_mystery)
        all_mystery_detail = all_mystery_detail.filter(
            mystery_shopping__in=all_reviewed_mystery, center__in=all_center)
        all_mystery_image = all_mystery_image.filter(
            mystery_shopping__in=all_reviewed_mystery)
        # print('////', all_mystery_detail)
    selected_center_ids = request.GET.getlist('select_center')
    # searched_from_date = request.GET.get('searched_from_date')
    select_audit_status = request.GET.get('select_audit_status')
    searched_month = request.GET.get('select_month')
    searched_text = request.GET.get('searched_text')
    searched_compliance = request.GET.getlist('searched_compliance')
    searched_kra = request.GET.get('searched_kra')
    searched_dept = request.GET.get('searched_dept')
    searched_om = request.GET.get('searched_om')
    unique_kra_fieled = MysteryShoppingDetail.objects.order_by(
    ).values_list('kra', flat=True).distinct()
    unique_process_fieled = MysteryShoppingDetail.objects.order_by(
    ).values_list('process', flat=True).distinct()
    try:
        selected_center = ExtendedZenotiCenterData.objects.filter(
            id__in=selected_center_ids)
    except Exception:
        selected_center = None

    try:
        selected_month = MonthAudit.objects.get(id=int(searched_month))
    except Exception:
        selected_month = None

    if selected_center:
        all_mystery = all_mystery.filter(center__in=selected_center)
        all_mystery_detail = all_mystery_detail.filter(
            center__in=selected_center)
        all_mystery_image = all_mystery_image.filter(
            center__in=selected_center)

    if select_audit_status:
        all_mystery_detail = all_mystery_detail.filter(
            audit_status=select_audit_status)

    if selected_month:
        all_mystery = all_mystery.filter(
            month_of_audit=selected_month)
        all_mystery_detail = all_mystery_detail.filter(
            mystery_shopping__in=all_mystery)
        all_mystery_image = all_mystery_image.filter(
            mystery_shopping__in=all_mystery)

    if searched_compliance:
        all_mystery_detail = all_mystery_detail.filter(
            compliance_category__in=searched_compliance)

    if searched_kra:
        all_mystery_detail = all_mystery_detail.filter(kra=searched_kra)

    if searched_om:
        all_mystery_detail = all_mystery_detail.filter(
            status_by_om=searched_om
        )
    if searched_dept:
        all_mystery_detail = all_mystery_detail .filter(
            status_by_department=searched_dept
        )
    mystery_overview_query = []
    for overview in all_mystery:
        all_not_blank_question = MysteryShoppingDetail.objects.filter(
            mystery_shopping=overview).exclude(audit_status='')
        total_completed = all_not_blank_question.filter(
            audit_status='Completed')
        total_pending = all_not_blank_question.filter(audit_status='Pending')
        total_action_required = all_not_blank_question.filter(
            audit_status='Action Required')
        total_action_taken = all_not_blank_question.filter(
            audit_status='Action Taken')
        try:
            month_audit = overview.month_of_audit.month
        except Exception:
            month_audit = None
        temp = {}
        temp['id'] = overview.id
        temp['added_by'] = overview.added_by.user.first_name
        temp['added_on'] = overview.added_on
        temp['shopper_name'] = overview.shopper_name
        temp['month_audit'] = month_audit
        temp['date'] = overview.date
        temp['start_time'] = overview.start_time
        temp['end_time'] = overview.end_time
        temp['center'] = overview.center.zenoti_data.name
        temp['total_question'] = all_not_blank_question.count()
        temp['total_completed_question'] = total_completed.count()
        temp['total_pending_question'] = total_pending.count()
        temp['total_action_required_question'] = total_action_required.count()
        temp['total_action_taken_question'] = total_action_taken.count()
        try:
            s1 = overview.service_availed_1
        except Exception:
            s1 = ''
        if s1 is None:
            s1 = ''
        try:
            s2 = overview.service_availed_2
        except Exception:
            s2 = ''
        if s2 is None:
            s2 = ''
        try:
            s3 = overview.service_availed_3
        except Exception:
            s3 = ''
        if s3 is None:
            s3 = ''
        temp['service_availed'] = (s1 + '\n' + s2 + '\n' + s3).strip()
        temp['cost_of_service'] = overview.cost_of_service
        temp['invoice_number'] = overview.invoice_number
        temp['admin_reviewed'] = overview.admin_reviewed
        temp['auditor_completed'] = overview.auditor_completed
        # this_overview_detail = MysteryShoppingDetail.objects.filter(
        #     mystery_shopping=overview)
        # total_question = this_overview_detail.count()
        # print("total_que", total_question)
        # total_question_done = 0
        # question_count = 0
        # for detail in this_overview_detail:
        #     # if not detail.compliance == 'NA':
        #     if (detail.compliance and detail.staff) or detail.compliance == 'NA':
        #         print('inside', detail.compliance,
        #               detail.staff, question_count)
        #         total_question_done += 1
        #         question_count += 1
        #     else:
        #         print('outside', detail.checklist, detail.compliance,
        #               detail.staff, question_count)
        #         question_count += 1
        # print('total', question_count)
        # get_percentage = (total_question_done / total_question) * 100
        # # print('per', get_percentage)
        # temp['percentage'] = "{:.2f}".format(get_percentage)
        mystery_overview_query.append(temp)
    # print('print', mystery_overview_query)

    # list pagination
    page = Paginator(mystery_overview_query, 20)
    list_page_num = request.GET.get('page', 1)
    try:
        list_page = page.page(list_page_num)
    except EmptyPage:
        list_page = page.page(1)

    list_start_index = (int(list_page_num) - 1) * page.per_page + 1
    list_end_index = min(list_start_index + page.per_page - 1, page.count)

    # detail pagination
    page_2 = Paginator(all_mystery_detail, 50)
    detail_page_num = request.GET.get('page_2', 1)
    try:
        detail_page = page_2.page(detail_page_num)
    except EmptyPage:
        detail_page = page_2.page(1)
    detail_start_index = (int(detail_page_num) - 1) * page_2.per_page + 1
    detail_end_index = min(detail_start_index +
                           page_2.per_page - 1, page_2.count)

    page_3 = Paginator(all_mystery_image, 20)
    image_page_num = request.GET.get('page_3', 1)
    try:
        image_page = page_3.page(image_page_num)
    except EmptyPage:
        image_page = page_3.page(1)

    if request.method == 'POST':
        data_json = open("mistery_data.txt", "r")
        mystery_detail_data = json.loads(data_json.read())
        # print('data', type(mystery_detail_data))
        # print('each', mystery_detail_data[0])
        if 'mystery_form' in request.POST:
            if mystery_form.is_valid():
                new_mystery = mystery_form.save(commit=False)
                service_agent_id_1 = request.POST.get('add_service_agent_1')
                service_agent_id_2 = request.POST.get('add_service_agent_2')
                service_agent_id_3 = request.POST.get('add_service_agent_3')
                # add_admin_review = False
                # add_auditor_completed = False
                # if request.POST.get('add_admin_review') == 'on':
                #     add_admin_review = True
                # if request.POST.get('add_auditor_completed') == 'on':
                #     add_auditor_completed = True
                # print(add_admin_review, add_auditor_completed)
                try:
                    agent_1 = ExtendedZenotiEmployeesData.objects.get(
                        id=int(service_agent_id_1))
                except Exception:
                    agent_1 = None
                try:
                    agent_2 = ExtendedZenotiEmployeesData.objects.get(
                        id=int(service_agent_id_2))
                except Exception:
                    agent_2 = None
                try:
                    agent_3 = ExtendedZenotiEmployeesData.objects.get(
                        id=int(service_agent_id_3))
                except Exception:
                    agent_3 = None
                new_mystery.added_by = staffProfile
                new_mystery.service_agent_1 = agent_1
                new_mystery.service_agent_2 = agent_2
                new_mystery.service_agent_3 = agent_3
                # new_mystery.admin_reviewed = add_admin_review
                # new_mystery.auditor_completed = add_auditor_completed
                new_mystery.save()
                for overview in mystery_detail_data:
                    # print(type(overview['service_number']))
                    if overview['service_number'] == "1":
                        service_responsible = new_mystery.service_agent_1
                    elif overview['service_number'] == "2":
                        service_responsible = new_mystery.service_agent_2
                    elif overview['service_number'] == "3":
                        service_responsible = new_mystery.service_agent_3
                    else:
                        service_responsible = None
                    # status = 'Pending'
                    if (overview['service_number'] == '1' and new_mystery.service_availed_1 and new_mystery.service_agent_1) or (overview['service_number'] == '2' and new_mystery.service_availed_2 and new_mystery.service_agent_2) or (overview['service_number'] == '3' and new_mystery.service_availed_3 and new_mystery.service_agent_3) or (overview['service_number'] == ''):
                        audit_status = 'Pending'
                    else:
                        audit_status = ''
                    # print('ser', service_responsible)
                    MysteryShoppingDetail.objects.create(
                        mystery_shopping=new_mystery,
                        center=new_mystery.center,
                        staff=service_responsible,
                        month_of_audit=new_mystery.month_of_audit,
                        date=new_mystery.date,
                        sequence=overview['sequence'],
                        client_journey=overview['client_journey'],
                        kra=overview['kra'],
                        process=overview['process'],
                        checklist=overview['checklist'],
                        relative_gaps_found=overview['relative_gaps_found'],
                        compliance_dropdown=overview['dropdown'],
                        service_number=overview['service_number'],
                        service_availed_1=new_mystery.service_availed_1,
                        service_availed_2=new_mystery.service_availed_2,
                        service_availed_3=new_mystery.service_availed_3,
                        audit_status=audit_status
                    )
        if 'del_mystery' in request.POST:
            del_mystery_id = request.POST.get('del_id')
            try:
                mystery_shopping = MysteryShoppingOverview.objects.get(
                    id=int(del_mystery_id))
            except Exception:
                mystery_shopping = None

            mystery_shopping.delete()
        if 'edit_mystery' in request.POST:
            mystery_id = request.POST.get('mystery_pk')
            center_id = request.POST.get('edit_center')
            shopper_name = request.POST.get('edit_shopper_name')
            phone = request.POST.get('edit_phone')
            email = request.POST.get('edit_email')
            gender = request.POST.get('edit_gender')
            start_time = request.POST.get('edit_start')
            end_time = request.POST.get('edit_end')
            month_id = request.POST.get('edit_month')
            date = request.POST.get('edit_date')
            cost_of_service = request.POST.get('edit_cost_of_service')
            invoice_number = request.POST.get('edit_invoice_number')
            admin_reviewed = request.POST.get('edit_admin_review')
            auditor_completed = request.POST.get('edit_auditor_completed')
            paid_in_cash = request.POST.get('edit_paid_cash')
            payment_mode = request.POST.get('edit_payment_mode')
            amount_redeemed = request.POST.get('edit_amount_redeemed')
            number_reached = request.POST.get('edit_number_reached')
            service_availed_1 = request.POST.get('edit_service_av_1')
            service_agent_id_1 = request.POST.get('edit_service_ag_1')
            service_availed_2 = request.POST.get('edit_service_av_2')
            service_agent_id_2 = request.POST.get('edit_service_ag_2')
            service_availed_3 = request.POST.get('edit_service_av_3')
            service_agent_id_3 = request.POST.get('edit_service_ag_3')

            print('edit', request.POST.get('edit_admin_review'),
                  request.POST.get('edit_auditor_completed'))
            print('timing', start_time, end_time)
            if start_time == '':
                starting_time = None
            else:
                starting_time = start_time
            if end_time == '':
                ending_time = None
            else:
                ending_time = end_time
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
                mystery = MysteryShoppingOverview.objects.get(
                    id=int(mystery_id))
            except Exception:
                mystery = None

            try:
                center = ExtendedZenotiCenterData.objects.get(
                    id=int(center_id))
            except Exception:
                center = None

            try:
                mystery_detail = MysteryShoppingDetail.objects.filter(
                    mystery_shopping=mystery)
            except Exception:
                mystery_detail = None

            try:
                month_query = MonthAudit.objects.get(id=int(month_id))
            except Exception:
                month_query = None

            try:
                agent_1 = ExtendedZenotiEmployeesData.objects.get(
                    id=int(service_agent_id_1))
            except Exception:
                agent_1 = None
            try:
                agent_2 = ExtendedZenotiEmployeesData.objects.get(
                    id=int(service_agent_id_2))
            except Exception:
                agent_2 = None
            try:
                agent_3 = ExtendedZenotiEmployeesData.objects.get(
                    id=int(service_agent_id_3))
            except Exception:
                agent_3 = None

            mystery.center = center
            mystery.shopper_name = shopper_name
            mystery.mobile = phone
            mystery.email = email
            mystery.gender = gender
            mystery.start_time = starting_time
            mystery.end_time = ending_time
            mystery.month_of_audit = month_query
            mystery.date = date
            mystery.cost_of_service = cost_of_service
            mystery.invoice_number = invoice_number
            mystery.admin_reviewed = add_admin_review
            mystery.auditor_completed = add_auditor_completed
            mystery.paid_in_cash = paid_in_cash
            mystery.payment_mode = payment_mode
            mystery.amount_redeemed = amount_redeemed
            mystery.contact_number_reached_for_appointment = number_reached
            mystery.service_availed_1 = service_availed_1
            mystery.service_agent_1 = agent_1
            mystery.service_availed_2 = service_availed_2
            mystery.service_agent_2 = agent_2
            mystery.service_availed_3 = service_availed_3
            mystery.service_agent_3 = agent_3
            mystery.save()

            for each_detail in mystery_detail:
                each_detail.center = center
                each_detail.date = date
                each_detail.month_of_audit = month_query
                each_detail.service_availed_1 = service_availed_1
                each_detail.service_availed_2 = service_availed_2
                each_detail.service_availed_3 = service_availed_3
                if each_detail.service_number == '1':
                    each_detail.staff = mystery.service_agent_1
                if each_detail.service_number == '2':
                    each_detail.staff = mystery.service_agent_2
                if each_detail.service_number == '3':
                    each_detail.staff = mystery.service_agent_3
                if (each_detail.service_number == '1' and mystery.service_availed_1 and mystery.service_agent_1) or (each_detail.service_number == '2' and mystery.service_availed_2 and mystery.service_agent_2) or (each_detail.service_number == '3' and mystery.service_availed_3 and mystery.service_agent_3) and not each_detail.audit_status:
                    each_detail.audit_status = 'Pending'

                if ((each_detail.service_number == '1' and (not mystery.service_availed_1 or not mystery.service_agent_1)) or (each_detail.service_number == '2' and (not mystery.service_availed_2 or not mystery.service_agent_2)) or (each_detail.service_number == '3' and (not mystery.service_availed_3 or not mystery.service_agent_3))) and each_detail.audit_status:
                    each_detail.audit_status = ''
                each_detail.save()

        if 'mystery_csv' in request.POST:
            csv_headers = [
                'Mystery ID', 'Checklist ID', 'Series No', 'Center', 'Month of Audit', 'Client Journey', 'KRA', 'Process', 'Checklist', 'Compliance', 'Compliance Category', 'Compliance Category Percentage', 'Relative Gaps Found', 'User Responsible', 'Service Availed', 'Remark By Auditor', 'Action Taken By Outlet Manager', 'Status By Om', 'Remark By OM', 'Action Taken By Management', 'Remark By Management', 'Expected Dept/Personnel to Intervene', 'Remark By Department', 'Status By Department'
            ]
            rows = []

            for each_detail in all_mystery_detail:
                service_availed = ''
                if each_detail.service_number == '1':
                    service_availed = each_detail.service_availed_1
                elif each_detail.service_number == '2':
                    service_availed = each_detail.service_availed_2
                elif each_detail.service_number == '3':
                    service_availed = each_detail.service_availed_3
                else:
                    service_availed = each_detail.service_availed_1, each_detail.service_availed_2, each_detail.service_availed_3
                try:
                    user_responsible = each_detail.staff.zenoti_data.employee_name
                except Exception:
                    user_responsible = ''

                try:
                    month_audit = each_detail.mystery_shopping.month_of_audit.month
                except Exception:
                    month_audit = ''
                rows.append([
                    each_detail.mystery_shopping.id,
                    each_detail.id,
                    each_detail.service_number,
                    each_detail.center.zenoti_data.name,
                    month_audit,
                    each_detail.client_journey,
                    each_detail.kra,
                    each_detail.process,
                    each_detail.checklist,
                    each_detail.compliance,
                    each_detail.compliance_category,
                    each_detail.compliance_category_percentage,
                    each_detail.relative_gaps_found,
                    user_responsible,
                    service_availed,
                    each_detail.remark,
                    each_detail.action_taken_by_outlet_manager,
                    each_detail.status_by_om,
                    each_detail.remark_by_om,
                    each_detail.action_taken_by_management,
                    each_detail.remark_by_management,
                    each_detail.expected_dept_intervene,
                    each_detail.remark_by_department,
                    each_detail.status_by_department
                ])
            csv_response = HttpResponse(content_type='text/csv')

            csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                'mystery_shopping_atr-' + str(datetime.today().date()) + '.csv')
            writer = csv.writer(csv_response)
            writer.writerow(csv_headers)
            writer.writerows(rows)
            print('response', csv_response)
            return csv_response
        if 'mystery_overview_csv' in request.POST:
            csv_headers = [
                'ID', 'Added By', 'Center', 'Shopper Name', 'Mobile', 'Email', 'Gender', 'Month of Audit', 'Date', 'Start time', 'End time', 'Cost of Service', 'Invoice Number', 'Paid in Cash', 'Amount Redeemed', 'Contact Reached for Apointment', 'Service Availed 1', 'Service Agent 1', 'Service Availed 2', 'Service Agent 2', 'Service Availed 3', 'service Agent 3', 'Auditor Completed', 'Admin Reviewed'
            ]
            rows = []
            for each_mystery in all_mystery:
                try:
                    added_by = each_mystery.added_by.user.first_name
                except Exception:
                    added_by = ''
                try:
                    month_audit = each_mystery.month_of_audit.month
                except Exception:
                    month_audit = ''

                try:
                    service_agent_1 = each_mystery.service_agent_1.zenoti_data.employee_name
                except Exception:
                    service_agent_1 = ''
                try:
                    service_agent_2 = each_mystery.service_agent_2.zenoti_data.employee_name
                except Exception:
                    service_agent_2 = ''
                try:
                    service_agent_3 = each_mystery.service_agent_3.zenoti_data.employee_name
                except Exception:
                    service_agent_3 = ''
                rows.append([
                    each_mystery.id,
                    added_by,
                    each_mystery.center.zenoti_data.name,
                    each_mystery.shopper_name,
                    each_mystery.mobile,
                    each_mystery.email,
                    each_mystery.gender,
                    month_audit,
                    each_mystery.date,
                    each_mystery.start_time,
                    each_mystery.end_time,
                    each_mystery.cost_of_service,
                    each_mystery.invoice_number,
                    each_mystery.paid_in_cash,
                    each_mystery.amount_redeemed,
                    each_mystery.contact_number_reached_for_appointment,
                    each_mystery.service_availed_1,
                    service_agent_1,
                    each_mystery.service_availed_2,
                    service_agent_2,
                    each_mystery.service_availed_3,
                    service_agent_3,
                    each_mystery.auditor_completed,
                    each_mystery.admin_reviewed
                ])
            csv_response = HttpResponse(content_type='text/csv')

            csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                'mystery_shopping_list-' + str(datetime.today().date()) + '.csv')
            writer = csv.writer(csv_response)
            writer.writerow(csv_headers)
            writer.writerows(rows)
            print('response', csv_response)
            return csv_response

        return redirect('mystery_shopping')
    context = {'all_mystery': list_page,
               'staffProfile': staffProfile,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'mystery_form': mystery_form,
               'all_center': all_center,
               'all_mystery_detail': detail_page,
               'all_mystery_image': image_page,
               #    'all_employee': all_employee,
               'selected_center_id': selected_center_ids,
               'list_start_index': list_start_index,
               'list_end_index': list_end_index,
               'list_total': page.count,
               'detail_start_index': detail_start_index,
               'detail_end_index': detail_end_index,
               'detail_total': page_2.count,
               #    'searched_from_date': searched_from_date,
               #    'searched_to_date': searched_to_date,
               'select_audit_status': select_audit_status,
               'searched_month': searched_month,
               'searched_text': searched_text,
               'searched_compliance': searched_compliance,
               'unique_kra_filed': unique_kra_fieled,
               'unique_process_fieled': unique_process_fieled,
               'searched_kra': searched_kra,
               'searched_dept': searched_dept,
               'searched_om': searched_om,
               'all_months': all_months,
               'compliance_category_percentage': compliance_category_percentage,
               'all_therapy_ext_emp': all_therapy_ext_emp}
    return render(request, "mystery_shopping/mystery_shopping_tabs_page.html", context)


@login_required(login_url='user_login')
def mystery_shopping_detail(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    is_audit_admin = staffProfile.user_type_name.filter(
        user_type='Audit Admin').exists()
    is_mystery_shopper = staffProfile.user_type_name.filter(
        user_type='Mystery Shopper').exists()
    is_salon_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Salon Revenue Auditor').exists()
    is_clinic_revenue_auditor = staffProfile.user_type_name.filter(
        user_type='Clinic Revenue Auditor').exists()
    is_corporate_auditor = staffProfile.user_type_name.filter(
        user_type='Corporate Auditor').exists()
    try:
        mystery_shopping = MysteryShoppingOverview.objects.get(id=int(pk))
    except Exception:
        mystery_shopping = None
    all_images_list = MysteryShoppingImages.objects.filter(
        mystery_shopping=mystery_shopping)
    all_employee = ExtendedZenotiEmployeesData.objects.filter(
        associated_center=mystery_shopping.center)
    all_mystery_detail = MysteryShoppingDetail.objects.filter(
        ~Q(kra='Service Agent'), mystery_shopping=mystery_shopping,)
    all_service_agent_mystery_detail_1 = MysteryShoppingDetail.objects.filter(
        mystery_shopping=mystery_shopping, kra='Service Agent', service_number='1')
    all_service_agent_mystery_detail_2 = MysteryShoppingDetail.objects.filter(
        mystery_shopping=mystery_shopping, kra='Service Agent', service_number='2')
    all_service_agent_mystery_detail_3 = MysteryShoppingDetail.objects.filter(
        mystery_shopping=mystery_shopping, kra='Service Agent', service_number='3')
    # all_therapy_emp = ZenotiEmployeesData.objects.filter(job_info='Therapist')
    all_therapy_ext_emp = ExtendedZenotiEmployeesData.objects.all()
    if request.method == 'POST':
        if 'image_submit' in request.POST:
            description = request.POST.get('desc')
            image = request.FILES["selected_img"]
            MysteryShoppingImages.objects.create(
                mystery_shopping=mystery_shopping,
                center=mystery_shopping.center,
                date=mystery_shopping.date,
                description=description,
                image=image
            )
            print(image)
        if 'image_delete' in request.POST:
            img_id = request.POST.get('img_id')
            try:
                mystery_image = MysteryShoppingImages.objects.get(
                    id=int(img_id))
            except Exception:
                mystery_image = None
            mystery_image.delete()

        return redirect('mystery_shopping_detail', pk=pk)

    context = {'all_mystery_detail': all_mystery_detail,
               'staffProfile': staffProfile,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_employee': all_employee,
               'total_length': all_mystery_detail.count(),
               'total_service_agent_length': all_service_agent_mystery_detail_1.count(),
               'mystery_shopping': mystery_shopping,
               'all_service_agent_mystery_detail_1': all_service_agent_mystery_detail_1,
               'all_service_agent_mystery_detail_2': all_service_agent_mystery_detail_2,
               'all_service_agent_mystery_detail_3': all_service_agent_mystery_detail_3,
               'all_images_list': all_images_list,
               'all_therapy_ext_emp': all_therapy_ext_emp}
    return render(request, "mystery_shopping/mystery_shopping_profile.html", context)


def edit_mystery_shopping_profile(request):
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
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        print('get_query', got_query)
        if got_query:
            for query in got_query:
                mystery_shopping_detail = MysteryShoppingDetail.objects.get(
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
                if (query['compliance'] and employee) or (query['compliance'] == 'NA'):
                    mystery_shopping_detail.audit_status = 'Completed'
                mystery_shopping_detail.save()
                # print(query)
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    context = {}
    return render(request, "mystery_shopping/mystery_shopping_profile.html", context)


def edit_mystery_shopping(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            mystery_shopping = MysteryShoppingOverview.objects.get(
                id=int(got_query))
        except Exception:
            mystery_shopping = None

        mystery_json = serializers.serialize('json', [mystery_shopping])
        return JsonResponse({"msg": "success",
                            "mystery_json": json.loads(mystery_json)})
    return render(request, "mystery_shopping/mystery_shopping_tabs_page.html")


def edit_mystery_extra_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print(got_query)
        mystery_id = got_query[0]['mystery_id']
        got_value = got_query[0]['mystery_value']
        got_name = got_query[0]['name']

        try:
            mystery_query = MysteryShoppingDetail.objects.get(
                id=int(mystery_id))
        except Exception:
            mystery_query = None
        if mystery_query:
            if got_name == 'audit_status':
                mystery_query.audit_status = got_value
                mystery_query.save()
            if got_name == 'comment_auditor':
                mystery_query.comment_for_auditor = got_value
                mystery_query.save()
            if got_name == 'action_outlet':
                mystery_query.action_taken_by_outlet_manager = got_value
                mystery_query.save()
            if got_name == 'status_om':
                mystery_query.status_by_om = got_value
                mystery_query.save()
            if got_name == 'remark_om':
                mystery_query.remark_by_om = got_value
                mystery_query.save()
            if got_name == 'action_management':
                mystery_query.action_taken_by_management = got_value
                mystery_query.save()
            if got_name == 'remark_management':
                mystery_query.remark_by_management = got_value
                mystery_query.save()
            if got_name == 'expected_intervene':
                mystery_query.expected_dept_intervene = got_value
                mystery_query.save()
            if got_name == 'remark_department':
                mystery_query.remark_by_department = got_value
                mystery_query.save()
            if got_name == 'status_department':
                mystery_query.status_by_department = got_value
                mystery_query.save()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "mystery_shopping/mystery_shopping_tabs_page.html")


def edit_mystery_audit_status_dropdown(request):
    data = json.loads(request.body)
    got_id = data['data_id']
    got_status = data['status']
    if got_id:
        try:
            mystery_detail_query = MysteryShoppingDetail.objects.get(
                id=int(got_id))
        except Exception:
            mystery_detail_query = None

        mystery_detail_query.audit_status = got_status
        mystery_detail_query.save()
        return JsonResponse({"msg": "success"})
    else:
        return JsonResponse({"msg": "failed"})


def user_search_list(request):
    search_query = request.GET.get('search_query', '')
    print('search', search_query)
    user_query = ExtendedZenotiEmployeesData.objects.filter(
        Q(zenoti_data__employee_name__icontains=search_query))
    final_data = []
    for obj in user_query:
        temp = {}
        temp['id'] = obj.id
        temp['name'] = obj.zenoti_data.employee_name
        final_data.append(temp)
    return JsonResponse(final_data, safe=False)
# def add_service_agent_to_mystery_shopping(request, pk):
#     mystery_shopping = MysteryShoppingOverview.objects.get(id=pk)
#     mystery_detail = MysteryShoppingDetail.objects.filter(
#         mystery_shopping=mystery_shopping)
#     data_json = open("mistery_data.txt", "r")
#     mystery_detail_data = json.loads(data_json.read())
#     for overview in mystery_detail_data:
#         if overview['kra'] == 'Service Agent':
#             if overview['service_number'] == "1":
#                 service_responsible = mystery_shopping.service_agent_1
#             elif overview['service_number'] == "2":
#                 service_responsible = mystery_shopping.service_agent_2
#             elif overview['service_number'] == "3":
#                 service_responsible = mystery_shopping.service_agent_3
#             else:
#                 service_responsible = None

#             MysteryShoppingDetail.objects.create(
#                 mystery_shopping=mystery_shopping,
#                 center=mystery_shopping.center,
#                 staff=service_responsible,
#                 date=mystery_shopping.date,
#                 sequence=overview['sequence'],
#                 client_journey=overview['client_journey'],
#                 kra=overview['kra'],
#                 process=overview['process'],
#                 checklist=overview['checklist'],
#                 relative_gaps_found=overview['relative_gaps_found'],
#                 compliance_dropdown=overview['dropdown'],
#                 service_number=overview['service_number']
#             )
#             print('yes')

#     context = {}
#     return HttpResponse('Done')
