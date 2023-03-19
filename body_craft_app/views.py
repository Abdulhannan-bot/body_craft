from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, ZenotiCentersData, ZenotiEmployeesData, SecretKeyModel, ExtendedZenotiEmployeesData, AssociatedRoleOptions, WeekOffOptions, EmployeeRoster, ExtendedZenotiCenterData, ExtendedZenotiEmployeesLeaveData, EmployeeScheduler, SectionOption, Position, OperationOption, ErrorLog
from .forms import ExtendedZenotiDataForm, EmployeeRosterForm, ExtendedZenotiCenterDataForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.conf import settings
import requests
import json
import calendar
import time
import csv

# email
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Create your views here.
try:
    api_key = SecretKeyModel.objects.all().first().token
except Exception:
    api_key = ''


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print("user", password, username)
        user = authenticate(request, username=username, password=password)
        # print("us", user)
        if user is not None:
            login(request, user)
            staffProfile = UserProfile.objects.get(user=user)
            usertype = staffProfile.user_type
            if usertype == 'admin':
                return redirect('admin_page')
            elif usertype == 'staff':
                my_zenoti_data = ZenotiEmployeesData.objects.get(
                    user=staffProfile)
                my_zenoti_extended_data = ExtendedZenotiEmployeesData.objects.get(
                    zenoti_data=my_zenoti_data)
                if my_zenoti_extended_data.is_manager:
                    return redirect('roster_dashboard')
                else:
                    messages.info(
                        request, 'You dont have the access to login')
            elif usertype == 'Auditor':
                usertype_name = staffProfile.user_type_name.all()
                for name in usertype_name:
                    if name.user_type == 'Audit Admin':
                        if staffProfile.user_status == 'Active':
                            return redirect('mystery_shopping')
                        else:
                            messages.info(
                                request, 'You dont have the access to login')
                    elif name.user_type == 'Salon Revenue Auditor':
                        if staffProfile.user_status == 'Active':
                            return redirect('revenue_audit_overview')
                        else:
                            messages.info(
                                request, 'You dont have the access to login')
                    elif name.user_type == 'Mystery Shopper':
                        return redirect('mystery_shopping')
                    elif name.user_type == 'Clinic Revenue Auditor':
                        if staffProfile.user_status == 'Active':
                            return redirect('clinic_revenue_audit_overview')
                        else:
                            messages.info(
                                request, 'You dont have the access to login')
                    elif name.user_type == 'Corporate Auditor':
                        if staffProfile.user_status == 'Active':
                            return redirect('corporate_audit_overview')
                        else:
                            messages.info(
                                request, 'You dont have the access to login')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url='user_login')
def admin_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype != 'admin':
        return redirect('/')
    all_centers = ZenotiCentersData.objects.all()
    total_center = all_centers.count()
    all_employees = UserProfile.objects.filter(user_type='staff')
    total_employees = all_employees.count()
    context = {'total_center': total_center,
               'total_employees': total_employees,
               'staffProfile': staffProfile}
    return render(request, "admin_home.html", context)


@login_required(login_url='user_login')
def admin_zenotiUsers_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype != 'admin':
        return redirect('/')
    try:
        selected_center = request.GET.get('select_center')
    except Exception:
        selected_center = None
    try:
        selected_jobtitle = request.GET.get('select_jobtitle')
    except Exception:
        selected_jobtitle = None
    try:
        searched_text = request.GET.get('searched_text')
    except Exception:
        searched_text = None

    print('1', datetime.now())
    # print('query', selected_center, selected_jobtitle, searched_text)
    try:
        searched_center = ZenotiCentersData.objects.get(
            id=int(selected_center))
    except Exception:
        searched_center = None
    try:
        searched_center_extend = ExtendedZenotiCenterData.objects.get(
            zenoti_data=searched_center)
    except Exception:
        searched_center_extend = None
    all_employee_query = ZenotiEmployeesData.objects.all().select_related(
        'user__user').prefetch_related('zenoti_center')
    all_employees = all_employee_query
    all_employees_extend_query = ExtendedZenotiEmployeesData.objects.all(
    ).select_related('zenoti_data').prefetch_related('associated_center__zenoti_data')
    all_employees_extend = all_employees_extend_query
    print('2', datetime.now())
    if searched_center:
        all_employees = all_employees.filter(zenoti_center=searched_center)
        all_employees_extend = all_employees_extend.filter(
            associated_center=searched_center_extend)
    if selected_jobtitle:
        all_employees = all_employees.filter(job_info=selected_jobtitle)
    if searched_text:
        split_text = searched_text.split()
        for text in split_text:
            all_employees = all_employees.filter(
                Q(employee_code__icontains=text) |
                Q(employee_name__icontains=text)
            )
    print('3', datetime.now())
    employee_list = []
    for each_emp in all_employees:
        temp = {}
        temp['employee_code'] = each_emp.employee_code
        temp['name'] = each_emp.employee_name
        temp['username'] = each_emp.user.user.username
        temp['job'] = each_emp.job_info
        temp['gender'] = each_emp.gender
        temp['id'] = each_emp.id
        temp['zenoti_center'] = ''
        temp['assigned_center'] = ''
        for center in each_emp.zenoti_center.all():
            # zenoti_cent.append(center.display_name)
            temp['zenoti_center'] += center.display_name+', '
        # print('00', datetime.now())
        for each_ex_emp in all_employees_extend:
            if each_emp == each_ex_emp.zenoti_data:
                # temp['assigned_center'] = list(each_ex_emp.associated_center.all(
                # ).values_list('zenoti_data__display_name', flat=True))
                for each_cent in each_ex_emp.associated_center.all():
                    # associate_cent.append(each_cent.display_name)
                    temp['assigned_center'] += each_cent.zenoti_data.display_name+', '
        employee_list.append(temp)
    # print('employee', employee_list)
    # print('4', datetime.now())
    page = Paginator(employee_list, 20)
    page_num = request.GET.get('page', 1)
    try:
        staff_page = page.page(page_num)
    except EmptyPage:
        staff_page = page.page(1)
    all_centers = ZenotiCentersData.objects.all()
    all_jobtitle = ZenotiEmployeesData.objects.order_by(
    ).values_list('job_info', flat=True).distinct()
    # print('5', datetime.now())
    # print('jobtitle', all_jobtitle)
    if request.method == "POST":
        # print('start', datetime.now())
        for each_center in all_centers:
            page_number = 1
            while True:
                retry_count = 1
                c_id = each_center.zenoticenterId
                url = f"https://api.zenoti.com/v1/centers/{c_id}/employees?page={page_number}&size=100"
                head = {"Authorization": "apikey "+api_key}
                while True:
                    try:
                        response = requests.request("GET", url, headers=head)
                        break
                    except Exception:
                        time.sleep(5)
                        retry_count = retry_count+1
                        if retry_count > 5:
                            break
                response_got = json.loads(response.text)
                employees_got = response_got.get('employees')
                print(response_got)
                if not employees_got:
                    break
                for employee in employees_got:
                    try:
                        existing_employee_user = User.objects.get(
                            username=employee['personal_info']['user_name'])
                    except Exception:
                        existing_employee_user = None

                    if existing_employee_user is None:
                        new_user = User.objects.create_user(
                            username=employee['personal_info']['user_name'],
                            password=employee['id'],
                            first_name=employee['personal_info']['first_name'],
                            last_name=employee['personal_info']['last_name']
                        )
                        new_userprofile = UserProfile.objects.create(
                            user=new_user,
                            password=employee['id'],
                            user_type='staff'
                        )
                        zenoti_employe_data = ZenotiEmployeesData.objects.create(
                            user=new_userprofile,
                            employee_code=employee['code'],
                            employee_id=employee['id'],
                            employee_name=employee['personal_info']['name'],
                            gender=employee['personal_info']['gender'],
                            job_info=employee['job_info']['name'],
                        )
                        zenoti_employe_data.zenoti_center.add(each_center)
                        ExtendedZenotiEmployeesData.objects.create(
                            zenoti_data=zenoti_employe_data,
                            office_start_time='09:00:00',
                            office_end_time='21:00:00'
                        )
                    else:
                        try:
                            existing_employee = ZenotiEmployeesData.objects.get(
                                employee_id=employee['id'])
                        except Exception:
                            existing_employee = None

                        if existing_employee:
                            existing_employee.employee_code = employee['code']
                            existing_employee.employee_name = employee['personal_info']['name']
                            existing_employee.gender = employee['personal_info']['gender']
                            existing_employee.job_info = employee['job_info']['name']
                            existing_employee.save()
                            if not each_center in existing_employee.zenoti_center.all():
                                existing_employee.zenoti_center.add(
                                    each_center)
                page_number = page_number+1
        print('end', datetime.now())
        return redirect('staffs_list')
    context = {
        # 'all_employees': all_employees,
        'staffProfile': staffProfile,
        #    'all_employees_extend': all_employees_extend,
        'employee_list': staff_page,
        'all_centers': all_centers, 'all_jobtitle': all_jobtitle,
        'selected_center': selected_center,
        'selected_jobtitle': selected_jobtitle,
        'searched_text': searched_text}
    return render(request, "admin_zenotiUser.html", context)


@login_required(login_url='user_login')
def admin_employee_profile_page(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if not usertype == 'admin':
        return redirect('/')
    employee_detail = ZenotiEmployeesData.objects.get(id=pk)
    try:
        extra_employee_detail = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=employee_detail)
    except Exception:
        extra_employee_detail = None

    try:
        employee_leave_detail = ExtendedZenotiEmployeesLeaveData.objects.filter(
            zenoti_data=extra_employee_detail)
    except Exception:
        employee_leave_detail = None
    form = ExtendedZenotiDataForm(
        request.POST or None, instance=extra_employee_detail)
    all_centers = ZenotiCentersData.objects.all()
    all_roles = AssociatedRoleOptions.objects.all()
    all_weekoff = WeekOffOptions.objects.all()
    if request.method == 'POST':
        if 'extra_data_form' in request.POST:
            if form.is_valid():
                password = form.cleaned_data['password']
                print('pass', password)
                user_of_this_profile = employee_detail.user.user
                user_of_this_profile.set_password(password)
                user_of_this_profile.save()
                form.save()
            else:
                print("form invalid: ", form.errors)
        if 'leave_form' in request.POST:
            leave_from = request.POST.get('leave_from')
            leave_to = request.POST.get('leave_to')
            leave_note = request.POST.get('leave_note')
            leave_status = request.POST.get('leave_status')

            ExtendedZenotiEmployeesLeaveData.objects.create(
                zenoti_data=extra_employee_detail,
                leave_from_date=leave_from,
                leave_to_date=leave_to,
                note=leave_note,
                status=leave_status
            )

        if 'leave_form_edit' in request.POST:
            leave_id = request.POST.get('edit_leave_id')
            leave_from = request.POST.get('edit_leave_from')
            leave_to = request.POST.get('edit_leave_to')
            leave_note = request.POST.get('edit_leave_note')
            leave_status = request.POST.get('edit_leave_status')
            try:
                leave_query = ExtendedZenotiEmployeesLeaveData.objects.get(
                    id=int(leave_id))
            except Exception:
                leave_query = None
            leave_query.leave_from_date = leave_from
            leave_query.leave_to_date = leave_to
            leave_query.note = leave_note
            leave_query.status = leave_status
            leave_query.save()
        if 'remove_center' in request.POST:
            today_date = date.today()
            center_id = request.POST.get('remove_centers')
            try:
                center = ExtendedZenotiCenterData.objects.get(
                    id=int(center_id))
            except Exception:
                center = None

            all_schedulers = EmployeeScheduler.objects.filter(
                employee=extra_employee_detail, center=center)

            all_rosters = EmployeeRoster.objects.filter(
                employee=extra_employee_detail, center=center
            )
            print(today_date)
            extra_employee_detail.associated_center.remove(center)
            for scheduler in all_schedulers:
                if scheduler.appoint_date >= today_date:
                    scheduler.delete()

            for roster in all_rosters:
                if roster.appoint_date >= today_date:
                    roster.delete()

        return redirect('body_craft_staff_profile', pk=pk)

    context = {'staffProfile': staffProfile,
               'extra_employee_detail': extra_employee_detail,
               'employee_detail': employee_detail, 'form': form,
               'all_weekoff': all_weekoff, 'all_roles': all_roles,
               'all_centers': all_centers,
               'employee_leave_detail': employee_leave_detail}
    return render(request, "admin_employee_profile.html", context)


@login_required(login_url='user_login')
def admin_zenotiCenter_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if not usertype == 'admin':
        return redirect('/')
    all_center = ZenotiCentersData.objects.all()
    if request.method == "POST":
        url = 'https://api.zenoti.com/v1/centers'
        head = {"Authorization": "apikey "+api_key}
        response = requests.request("GET", url, headers=head)
        response_got = json.loads(response.text)
        # print('response', response_got)
        for center in response_got['centers']:
            # print('each response', center['id'])
            try:
                existing_center = ZenotiCentersData.objects.get(
                    zenoticenterId=center['id'])
            except Exception:
                existing_center = None

            if existing_center is None:
                new_center = ZenotiCentersData.objects.create(
                    zenoticenterId=center['id'],
                    code=center['code'],
                    name=center['name'],
                    display_name=center['display_name'],
                    address_1=center['address_info']['address_1'],
                    address_2=center['address_info']['address_2'],
                    city=center['address_info']['city'],
                    zip_code=center['address_info']['zip_code'],
                    state=center['state']['name'],
                    country=center['country']['name'],
                )
                ExtendedZenotiCenterData.objects.create(
                    zenoti_data=new_center,
                    opening_time='09:00:00',
                    closing_time='22:00:00'
                )
        return redirect('centers_list')
    context = {'all_center': all_center, 'staffProfile': staffProfile}
    return render(request, "admin_zenotiCentre.html", context)


@login_required(login_url='user_login')
def admin_center_profile_page(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if not usertype == 'admin':
        return redirect('/')
    center_detail = ZenotiCentersData.objects.get(id=pk)
    try:
        extended_center_detail = ExtendedZenotiCenterData.objects.get(
            zenoti_data=center_detail)
    except Exception:
        extended_center_detail = None
    form = ExtendedZenotiCenterDataForm(
        request.POST or None, instance=extended_center_detail)

    if request.method == 'POST':
        if 'extra_data_form' in request.POST:
            if form.is_valid():
                form.save()
        return redirect('body_craft_center_profile', pk=pk)
    context = {'center_detail': center_detail,
               'form': form, 'staffProfile': staffProfile}
    return render(request, 'admin_center_profile.html', context)


@login_required(login_url='user_login')
def add_admin(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if not staffProfile.user_type == 'admin':
        return redirect('/')
    admin_user = UserProfile.objects.filter(
        user_type='admin').exclude(user__is_superuser=True)
    if request.method == "POST":
        phone = request.POST.get("phone")
        passcode = request.POST.get("passcode")
        name = request.POST.get("name")
        username = request.POST.get("email")
        try:
            already_user = User.objects.get(username=username)
        except Exception:
            already_user = None
            # print('user', already_user)
        if already_user is None:
            new_user = User.objects.create_user(
                username=username, password=passcode, first_name=name)
            UserProfile.objects.create(
                user=new_user,
                phone=phone,
                email=username,
                password=passcode,
                user_type='admin',
            )
            return redirect('admin_team')
        else:
            messages.info(
                request, 'This Email Id is already exist in our DataBase')
            return redirect('admin_team')
    context = {'admin_user': admin_user, 'staffProfile': staffProfile}
    return render(request, "admin_team.html", context)


@login_required(login_url='user_login')
def staff_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'staff':
        return redirect('roster_dashboard')
    if usertype == 'admin':
        return redirect('admin_page')
    for type_name in staffProfile.user_type_name.all():
        if type_name.user_type == 'Mystery Shopper':
            return redirect('mystery_shopping')
        if type_name.user_type == 'Audit Admin':
            return redirect('mystery_shopping')
        if type_name.user_type == 'Salon Revenue Auditor':
            return redirect('revenue_audit_overview')
        if type_name.user_type == 'Clinic Revenue Auditor':
            return redirect('clinic_revenue_audit_overview')
        if type_name.user_type == 'Corporate Auditor':
            return redirect('corporate_audit_overview')
    context = {'staffProfile': staffProfile}
    return render(request, "staff_home.html", context)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


@login_required(login_url='user_login')
def roster_dashboard_page(request):
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
    if staffProfile.user_type == 'staff' or staffProfile.user_type == 'admin' or staffProfile.roster_access is True:
        pass
    else:
        return redirect('/')
    all_extended_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    zenoti_center_data_ids = all_extended_center.values_list(
        'zenoti_data', flat=True)
    all_centers = ZenotiCentersData.objects.filter(
        id__in=zenoti_center_data_ids)
    # all_centers = ZenotiCentersData.objects.all()
    if staffProfile.user_type == 'staff':
        my_zenoti_data = ZenotiEmployeesData.objects.get(user=staffProfile)
        my_zenoti_extended_data = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=my_zenoti_data)
        my_centers_id = []
        for my_center in my_zenoti_extended_data.associated_center.all():
            my_centers_id.append(my_center.zenoti_data.id)
        all_centers = all_centers.filter(id__in=my_centers_id)
    all_section = SectionOption.objects.all()
    all_roster = EmployeeRoster.objects.all()
    all_roles = AssociatedRoleOptions.objects.all()
    # all_position = Position.objects.all()
    redirect_uri = ''
    selected_center = request.GET.get('selected_center')
    selected_date = request.GET.get('selected_date')
    selected_section = request.GET.get('selected_section')
    # print('section', selected_section)
    if selected_center:
        request.session['selected_center'] = selected_center
    if selected_section:
        # if not selected_section == '0':
        request.session['selected_section'] = selected_section
    # center_id = 1
    q_date = date.today()
    if not selected_date and not selected_center and not selected_section:
        if request.session.get('selected_center'):
            selected_center = request.session.get('selected_center')
        else:
            selected_center = all_centers.first().id
        if request.session.get('selected_section'):
            selected_section = request.session.get('selected_section')
        else:
            selected_section = all_section.first().id
        redirect_uri = f"/roster_dashboard/?selected_center={selected_center}&selected_section={selected_section}&selected_date={q_date}"
        return redirect(redirect_uri)
    if not selected_date:
        selected_date = date.today()
    try:
        searched_center = all_centers.filter(id=int(selected_center)).first()
    except Exception:
        searched_center = all_centers.first()
    try:
        searched_section = all_section.filter(id=int(selected_section)).first()
    except Exception:
        searched_section = all_section.first()
    # print('center', searched_center)
    extend_center_data = ExtendedZenotiCenterData.objects.get(
        zenoti_data=searched_center)
    # roster_form = EmployeeRosterForm(request.POST or None)
    this_center_emp_extend = ExtendedZenotiEmployeesData.objects.filter(
        associated_center=extend_center_data)
    final_employee_list = []
    for emp in this_center_emp_extend:
        temp = {}
        temp['username'] = emp.zenoti_data.employee_name
        temp['id'] = emp.id
        temp['associated_role'] = list(emp.associated_role.all(
        ).values_list('id', flat=True))
        final_employee_list.append(temp)
    # emp_json = serializers.serialize('json', final_employee_list)

    # print(final_employee_list)
    # roster_form.fields['associated_role'].queryset = extend_center_data.position.all()
    # roster_form.fields['employee'].queryset = this_center_emp_extend

    all_roster = all_roster.filter(
        center=extend_center_data, appoint_date=selected_date)
    positions = Position.objects.filter(section=searched_section)
    # print('position', positions)
    if not searched_section.option == 'All':
        all_roster = all_roster.filter(associated_role_id__in=list(
            positions.values_list('id', flat=True)))
    center_role_json = {}
    center_role_list = []
    extend_center_position_data = extend_center_data.position.all()
    if not searched_section.option == 'All':
        extend_center_position_list = []
        for each_position in positions:
            if each_position in extend_center_position_data:
                extend_center_position_list.append(each_position)
    else:
        extend_center_position_list = extend_center_position_data

    # print('all_', extend_center_position_list)

    for role in extend_center_position_list:
        temp = {}
        name = role.name
        id = 'A'+str(role.id)
        center_role_json[name] = id
        temp['name'] = name
        temp['id'] = id
        center_role_list.append(temp)

    # print('role', center_role_list)
    final_roster_list = []
    for roster in all_roster:
        temp = {}
        temp["name"] = roster.employee.zenoti_data.employee_name
        temp["role"] = roster.associated_role.name
        temp['start_time'] = str(roster.office_start_time)
        temp['end_time'] = str(roster.office_end_time)
        temp['roster_pk'] = roster.id
        final_roster_list.append(temp)

    # print('list', final_roster_list)

    all_scheduler = EmployeeScheduler.objects.filter(
        center=extend_center_data, appoint_date=selected_date
    ).order_by('status', 'office_start_time')
    # print('schedler', all_scheduler)
    # print('all_roster', json.dumps(final_roster_list))
    if request.method == 'POST':
        print('submit', request.POST)
        if 'create_one_roster' in request.POST:
            # print('form', roster_form.cleaned_data['employee'])
            from_time = request.POST.get("start_tm")
            to_time = request.POST.get("end_tm")
            employee_id = request.POST.get("filtered_employee")
            kra_id = request.POST.get("select_kar")
            employee = ExtendedZenotiEmployeesData.objects.get(
                id=int(employee_id))
            position = Position.objects.get(id=int(kra_id))
            EmployeeRoster.objects.create(
                center=extend_center_data,
                employee=employee,
                associated_role=position,
                appoint_date=selected_date,
                office_start_time=from_time,
                office_end_time=to_time
            )
            error_sentence = f"One Roster is created for {employee.zenoti_data.employee_name} as {position.name} for {selected_date} at {extend_center_data.zenoti_data.name}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
        if 'future_set' in request.POST:
            from_date = request.POST.get("future_from")
            to_date = request.POST.get("future_to")
            del_check = request.POST.get("del_future")
            # print('fut', type(from_date), to_date, del_check)
            start_date = datetime.strptime(from_date, '%Y-%m-%d')
            end_date = datetime.strptime(to_date, '%Y-%m-%d')
            all_scheduler = EmployeeScheduler.objects.filter(
                center=extend_center_data, appoint_date=selected_date)

            for single_date in daterange(start_date, end_date):
                # print('del', del_check)
                if del_check is not None:
                    EmployeeRoster.objects.filter(
                        center=extend_center_data,
                        appoint_date=single_date).delete()
                # print(single_date.strftime("%Y-%m-%d"))
                for roster in all_roster:
                    # print('loop')
                    EmployeeRoster.objects.create(
                        center=roster.center,
                        employee=roster.employee,
                        associated_role=roster.associated_role,
                        appoint_date=single_date,
                        office_start_time=roster.office_start_time,
                        office_end_time=roster.office_end_time
                    )
                if all_scheduler:
                    exist_scheduler = EmployeeScheduler.objects.filter(
                        center=extend_center_data, appoint_date=single_date)
                    if exist_scheduler:
                        exist_scheduler.delete()
                    for scheduler in all_scheduler:
                        each_scheduler = EmployeeScheduler.objects.create(
                            center=scheduler.center,
                            employee=scheduler.employee,
                            status=scheduler.status,
                            appoint_date=single_date,
                            office_start_time=scheduler.office_start_time,
                            office_end_time=scheduler.office_end_time
                        )
                        for role in scheduler.associated_role.all():
                            each_scheduler.associated_role.add(role)
            error_sentence = f"{extend_center_data.zenoti_data.name} Roster's of {selected_date} copied to future from {from_date} to {to_date}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
        if 'del_roster' in request.POST:
            del_roster_id = request.POST.get('del_id')

            try:
                roster_to_del = EmployeeRoster.objects.get(
                    id=int(del_roster_id))
            except Exception:
                roster_to_del = None
            error_sentence = f"One {roster_to_del.employee.zenoti_data.employee_name}'s Roster deleted for {roster_to_del.associated_role.name} on {roster.appoint_date} at {roster_to_del.center.zenoti_data.name}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
            roster_to_del.delete()

        if 'submit_roster_form' in request.POST:
            from_time = request.POST.get("start_time")
            to_time = request.POST.get("end_time")
            emp_id = request.POST.get("employee_id")
            role_id = request.POST.get("role_id")
            roster_id = request.POST.get('roster_id')

            try:
                emp_roster = EmployeeRoster.objects.get(id=int(roster_id))
            except Exception:
                emp_roster = None

            try:
                emp_role = Position.objects.get(id=int(role_id))
            except Exception:
                emp_role = None

            try:
                employee = ExtendedZenotiEmployeesData.objects.get(
                    id=int(emp_id))
            except Exception:
                employee = None

            emp_roster.employee = employee
            emp_roster.associated_role = emp_role
            emp_roster.office_start_time = from_time
            emp_roster.office_end_time = to_time
            emp_roster.save()

            error_sentence = f"{emp_roster.employee.zenoti_data.employee_name}'s Roster edited for {emp_roster.associated_role.name} on {emp_roster.appoint_date} at {emp_roster.center.zenoti_data.name}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )

        if 'scheduler_create' in request.POST:
            all_employee = ExtendedZenotiEmployeesData.objects.filter(
                associated_center=extend_center_data)
            sel_date = datetime.strptime(
                str(selected_date), '%Y-%m-%d')
            weekday = calendar.day_name[sel_date.weekday()]
            # print('week', weekday)
            for employe in all_employee:
                try:
                    exist_scheduler = EmployeeScheduler.objects.get(
                        center=extend_center_data, appoint_date=selected_date, employee=employe)
                except Exception:
                    exist_scheduler = None
                try:
                    exist_roster = EmployeeRoster.objects.get(
                        center=extend_center_data, appoint_date=selected_date, employe=employe
                    )
                except Exception:
                    exist_roster = None
                if exist_scheduler is None:
                    status = 'Available'
                    # zenoti_emp = ExtendedZenotiEmployeesData.objects.get(
                    #     id=employe.id)
                    emp_leave = ExtendedZenotiEmployeesLeaveData.objects.filter(
                        zenoti_data=employe)
                    for leaves in emp_leave:
                        leave_from_date = datetime.strptime(
                            str(leaves.leave_from_date), '%Y-%m-%d')
                        leave_end_date = datetime.strptime(
                            str(leaves.leave_to_date), '%Y-%m-%d')
                        search_date = datetime.strptime(
                            str(selected_date), '%Y-%m-%d')
                        if search_date in daterange(leave_from_date, leave_end_date):
                            if leaves.status == 'Approved':
                                status = 'Leave Approved'
                            if leaves.status == 'Pending':
                                status = 'Leave Request'
                    if weekday in str(employe.week_off.all()):
                        status = 'Week Off'

                    # print('emp', all_employee)
                    emp_schedulter = EmployeeScheduler.objects.create(
                        center=extend_center_data,
                        employee=employe,
                        status=status,
                        appoint_date=selected_date,
                        office_start_time=employe.office_start_time,
                        office_end_time=employe.office_end_time
                    )
                    for role in employe.associated_role.all():
                        emp_schedulter.associated_role.add(role)
                if status == 'Available':
                    if exist_roster is None:
                        for each_kra in employe.associated_role.all():
                            EmployeeRoster.objects.create(
                                center=extend_center_data,
                                employee=employe,
                                associated_role=each_kra,
                                appoint_date=selected_date,
                                office_start_time=employe.office_start_time,
                                office_end_time=employe.office_end_time
                            )
            error_sentence = f"The Scheduler for {extend_center_data.zenoti_data.name} on {selected_date} has been created."
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )

        if 'refresh_scheduler' in request.POST:
            all_employee = ExtendedZenotiEmployeesData.objects.filter(
                associated_center=extend_center_data)
            sel_date = datetime.strptime(
                str(selected_date), '%Y-%m-%d')
            weekday = calendar.day_name[sel_date.weekday()]
            try:
                all_scheduler = EmployeeScheduler.objects.filter(
                    center=extend_center_data, appoint_date=selected_date)
            except Exception:
                all_scheduler = None

            try:
                all_roster = EmployeeRoster.objects.filter(
                    center=extend_center_data, appoint_date=selected_date)
            except Exception:
                all_roster = None

            if all_scheduler:
                all_scheduler.delete()
            if all_roster:
                all_roster.delete()
            # EmployeeScheduler.objects.filter(
            #     center=extend_center_data, appoint_date=selected_date).delete()
            for each_emp in all_employee:
                try:
                    exist_scheduler = EmployeeScheduler.objects.get(
                        employee=each_emp, appoint_date=selected_date,
                        center=extend_center_data)
                except Exception:
                    exist_scheduler = None

                try:
                    exist_roster = EmployeeRoster.objects.filter(
                        employee=each_emp, appoint_date=selected_date,
                        center=extend_center_data)
                except Exception:
                    exist_roster = None
                status = 'Available'
                if exist_scheduler is None:
                    print('true')
                    emp_leave = ExtendedZenotiEmployeesLeaveData.objects.filter(
                        zenoti_data=each_emp)
                    for leaves in emp_leave:
                        leave_from_date = datetime.strptime(
                            str(leaves.leave_from_date), '%Y-%m-%d')
                        leave_end_date = datetime.strptime(
                            str(leaves.leave_to_date), '%Y-%m-%d')
                        search_date = datetime.strptime(
                            str(selected_date), '%Y-%m-%d')
                        if search_date in daterange(leave_from_date, leave_end_date):
                            if leaves.status == 'Approved':
                                print('approved')
                                status = 'Leave Approved'
                            if leaves.status == 'Pending':
                                print('pending')
                                status = 'Leave Request'
                    if weekday in str(each_emp.week_off.all()):
                        print('weekoff')
                        status = 'Week Off'

                    # print('emp', all_employee)
                    emp_schedulter = EmployeeScheduler.objects.create(
                        center=extend_center_data,
                        employee=each_emp,
                        status=status,
                        appoint_date=selected_date,
                        office_start_time=each_emp.office_start_time,
                        office_end_time=each_emp.office_end_time
                    )
                    for role in each_emp.associated_role.all():
                        emp_schedulter.associated_role.add(role)
                else:
                    leaves = ExtendedZenotiEmployeesLeaveData.objects.filter(
                        zenoti_data=each_emp)
                    print(leaves)
                    for each_leave in leaves:
                        leave_from_date = datetime.strptime(
                            str(each_leave.leave_from_date), '%Y-%m-%d')
                        leave_end_date = datetime.strptime(
                            str(each_leave.leave_to_date), '%Y-%m-%d')
                        compare_date = datetime.strptime(
                            str(selected_date), '%Y-%m-%d')
                        if compare_date in daterange(leave_from_date, leave_end_date):
                            if each_leave.status == 'Approved':
                                exist_scheduler.status = 'Leave Approved'
                                exist_scheduler.save()
                            if each_leave.status == 'Pending':
                                exist_scheduler.status = 'Leave Request'
                                exist_scheduler.save()
                    # if weekday in str(each_emp.week_off.all()):
                    #     status = 'Week Off'
                    # exist_scheduler.status = status
                if status == 'Available':
                    # if exist_roster is None:
                    for each_kra in each_emp.associated_role.all():
                        EmployeeRoster.objects.create(
                            center=extend_center_data,
                            employee=each_emp,
                            associated_role=each_kra,
                            appoint_date=selected_date,
                            office_start_time=each_emp.office_start_time,
                            office_end_time=each_emp.office_end_time
                        )
            error_sentence = f"Scheduler & Roster refreshed at {extend_center_data.zenoti_data.name} for {selected_date}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
        if 'delete_scheduler' in request.POST:
            this_date_scheduler = EmployeeScheduler.objects.filter(
                appoint_date=selected_date, center=extend_center_data)
            this_date_roster = EmployeeRoster.objects.filter(
                appoint_date=selected_date, center=extend_center_data
            )
            if this_date_scheduler:
                this_date_scheduler.delete()
            if this_date_roster:
                this_date_roster.delete()
            error_sentence = f"Scheduler & Roster deleted at {extend_center_data.zenoti_data.name} for {selected_date}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
        if selected_date:
            redirect_uri = f"/roster_dashboard/?selected_center={selected_center}&selected_section={selected_section}&selected_date={selected_date}"
        else:
            redirect_uri = f"/roster_dashboard/?selected_center={selected_center}&selected_section={selected_section}&selected_date={q_date}"
        return redirect(redirect_uri)
    context = {'staffProfile': staffProfile,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_centers': all_centers,
               #    'roster_form': roster_form,
               'all_roster': all_roster,
               #    'all_position': all_position,
               #    'redirect_uri': redirect_uri,
               'center_id': int(selected_center),
               'section_id': int(selected_section),
               'all_scheduler': all_scheduler,
               'all_roles': all_roles, 'roster_list': json.dumps(final_roster_list),
               'center_role_list': json.dumps(center_role_list),
               'center_role_json': json.dumps(center_role_json),
               'all_section': all_section,
               'this_center_emp': this_center_emp_extend,
               'extend_center_data': extend_center_data,
               'emp_json': json.dumps(final_employee_list)}
    return render(request, "employee_roster.html", context)


def roster_missing_report(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        from_date = got_query[0]['from_dt']
        to_date = got_query[0]['to_dt']
        center_id = got_query[0]['center']
        section_id = got_query[0]['section']
        try:
            center = ZenotiCentersData.objects.get(id=int(center_id))
        except Exception:
            center = None
        try:
            extended_center = ExtendedZenotiCenterData.objects.get(
                zenoti_data=center)
        except Exception:
            extended_center = None
        try:
            section = SectionOption.objects.get(id=int(section_id))
        except Exception:
            section = None
        all_role = extended_center.position.all()
        # print('position', positions)
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.strptime(to_date, '%Y-%m-%d')
        # all_role = positions
        rosters = EmployeeRoster.objects.filter(center=extended_center)
        if not section.option == 'All':
            all_role = all_role.filter(section=section)
            rosters = rosters.filter(associated_role_id__in=list(
                all_role.values_list('id', flat=True)))
        final_missing_report = []
        # print('yep')
        if start_date and end_date and extended_center:
            # print('yes')
            for single_date in daterange(start_date, end_date):
                # print('single', single_date)
                for each_role in all_role:
                    # print('role', each_role)
                    role_rosters = rosters.filter(
                        associated_role=each_role, appoint_date=single_date
                    ).order_by('office_start_time')

                    if not role_rosters:
                        final_missing_report.append(
                            '<span class="badge badge-primary" > ' + str(single_date.date()) + '</span> ' +
                            each_role.name + ' is not appointed whole day.'
                        )

                    endtime = None
                    # print('rosterlen', len(role_rosters))
                    for i in range(len(role_rosters)):
                        each_roster = role_rosters[i]
                        weekday = calendar.day_name[single_date.weekday()]
                        try:
                            employezenoti = ExtendedZenotiEmployeesData.objects.get(
                                id=each_roster.employee.id
                            )
                        except Exception:
                            employezenoti = None

                        if weekday in str(employezenoti.week_off.all()):
                            # print('yes weekoff exist')
                            final_missing_report.append(
                                '<span class="badge badge-primary" > ' + str(single_date.date()) + '</span> ' + employezenoti.zenoti_data.employee_name + ' is appointed as ' +
                                each_role.name + ' from ' + str(each_roster.office_start_time.strftime("%I:%M %p")) + ' to ' +
                                str(each_roster.office_end_time.strftime("%I:%M %p")) +
                                ', But the staff has Weekoff'
                            )

                        try:
                            employee_leave = ExtendedZenotiEmployeesLeaveData.objects.filter(
                                zenoti_data=each_roster.employee)
                        except Exception:
                            employee_leave = None

                        for leave in employee_leave:
                            leave_from_date = datetime.strptime(
                                str(leave.leave_from_date), '%Y-%m-%d')
                            leave_end_date = datetime.strptime(
                                str(leave.leave_to_date), '%Y-%m-%d')
                            if single_date in daterange(leave_from_date, leave_end_date):
                                # print('type', single_date)
                                # if single_date == each_date:
                                if leave.status == 'Approved' or leave.status == 'Pending':
                                    final_missing_report.append(
                                        '<span class="badge badge-primary" > '+str(single_date.date()) + '</span> ' + leave.zenoti_data.zenoti_data.employee_name + ' is appointed as ' +
                                        each_role.name + ' But he is on a leave '
                                    )

                        # print('weekday', type(weekday))
                        # print('roster', each_roster)
                        if i == 0:
                            # print('loop1')
                            if each_roster.office_start_time > each_role.start_time:
                                final_missing_report.append(
                                    '<span class="badge badge-primary" > '+str(single_date.date()) + '</span> ' +
                                    each_role.name + ' is not appointed from '
                                    + str(each_role.start_time.strftime("%I:%M %p")) +
                                    ' to ' +
                                    str(each_roster.office_start_time.strftime(
                                        "%I:%M %p"))

                                )
                        elif i == len(role_rosters)-1:
                            if each_roster.office_start_time > endtime:
                                final_missing_report.append(
                                    '<span class="badge badge-primary" > '+str(single_date.date()) + '</span> ' +
                                    each_role.name + ' is not appointed from '
                                    + str(endtime.strftime("%I:%M %p")) +
                                    ' to ' +
                                    str(each_roster.office_start_time.strftime(
                                        "%I:%M %p"))
                                )

                            if each_roster.office_end_time < each_role.end_time:
                                final_missing_report.append(
                                    '<span class="badge badge-primary" > '+str(single_date.date()) + '</span> ' +
                                    each_role.name
                                    + " is not appointed from " +
                                    str(each_roster.office_end_time.strftime("%I:%M %p")) + ' to ' +
                                    str(each_role.end_time.strftime("%I:%M %p"))

                                )
                        else:
                            # print('end', endtime)
                            if each_roster.office_start_time > endtime:
                                final_missing_report.append(
                                    '<span class="badge badge-primary" >'+str(single_date.date()) + '</span> ' +
                                    each_role.name
                                    + ' is not appointed from ' +
                                    str(endtime.strftime("%I:%M %p")) + ' to ' +
                                    str(each_roster.office_start_time.strftime(
                                        "%I:%M %p"))
                                )

                        endtime = each_roster.office_end_time
                        # print('time', endtime.strftime("%I:%M %p"))
        else:
            pass
        # aalimProfile = UserProfile.objects.get(id=int(aalim_id))
        # profile_json = serializers.serialize('json', [aalimProfile])
        # aalim = Alim.objects.filter(user=aalimProfile)
        # aalim_json = serializers.serialize('json', aalim)
        return JsonResponse({"msg": "success",
                             "roster_data": final_missing_report,
                             })
    return render(request, "employee_roster.html")


@login_required(login_url='user_login')
def admin_position_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if not staffProfile.user_type == 'admin':
        return redirect('/')
    all_position = Position.objects.all()
    all_section = SectionOption.objects.all().exclude(option='All')
    all_operation = OperationOption.objects.all()
    if request.method == "POST":
        if 'add_position' in request.POST:
            section = request.POST.get("select_section")
            operation = request.POST.get("select_operation")
            name = request.POST.get("name")
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")
            Position.objects.create(
                name=name,
                section=SectionOption.objects.get(id=int(section)),
                operation=OperationOption.objects.get(id=int(operation)),
                start_time=start,
                end_time=end
            )
        if 'edit_position' in request.POST:
            start = request.POST.get("starttime")
            end = request.POST.get("endtime")
            position_id = request.POST.get("pos_id")
            try:
                position = Position.objects.get(id=int(position_id))
            except Exception:
                position = None
            position.start_time = start
            position.end_time = end
            position.save()
        return redirect('position_page')
    context = {'staffProfile': staffProfile,
               'all_position': all_position,
               'all_section': all_section,
               'all_operation': all_operation}
    return render(request, "admin_position_page.html", context)


def edit_employee_scheduler(request):
    if request.method == "POST":
        user = request.user
        staffProfile = UserProfile.objects.get(user=user)
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        start_time = got_query[0]['from_tm']
        end_time = got_query[0]['to_tm']
        status = got_query[0]['status']
        scheuler_id = got_query[0]['scheduler']
        remark = got_query[0]['remark']
        try:
            scheduler = EmployeeScheduler.objects.get(id=int(scheuler_id))
        except Exception:
            scheduler = None

        try:
            rosters = EmployeeRoster.objects.filter(
                center=scheduler.center, appoint_date=scheduler.appoint_date, employee=scheduler.employee)
        except Exception:
            rosters = None
        if scheduler:
            scheduler.office_start_time = start_time
            scheduler.office_end_time = end_time
            scheduler.status = status
            scheduler.remark = remark
            scheduler.save()

            if status == 'Available':
                if rosters:
                    for eachroster in rosters:
                        eachroster.office_start_time = scheduler.office_start_time
                        eachroster.office_end_time = scheduler.office_end_time
                        eachroster.save()
                else:
                    for each_kra in scheduler.employee.associated_role.all():
                        EmployeeRoster.objects.create(
                            center=scheduler.center,
                            employee=scheduler.employee,
                            associated_role=each_kra,
                            appoint_date=scheduler.appoint_date,
                            office_start_time=scheduler.office_start_time,
                            office_end_time=scheduler.office_end_time,
                        )
            else:
                if rosters:
                    rosters.delete()

            error_sentence = f"Scheduler edited of {scheduler.employee.zenoti_data.employee_name} for {scheduler.appoint_date} at {scheduler.center.zenoti_data.name}"
            ErrorLog.objects.create(
                employee=staffProfile,
                page='roster',
                sentence=error_sentence
            )
            # if status == 'Available':
            #     if rosters is None:
            #         for each_kra in scheduler.employee.associated_role.all():
            #             EmployeeRoster.objects.create(
            #                 center=scheduler.center,
            #                 employee=scheduler.employee,
            #                 associated_role=each_kra,
            #                 appoint_date=scheduler.appoint_date,
            #                 office_start_time=scheduler.employee.office_start_time,
            #                 office_end_time=scheduler.employee.office_end_time
            #             )
            # else:
            #     if rosters:
            #         rosters.delete()
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "employee_roster.html")


def edit_employee_roster(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            roster = EmployeeRoster.objects.get(id=int(got_query))
        except Exception:
            roster = None
        roster_json = serializers.serialize('json', [roster])
        return JsonResponse({"msg": "success",
                             "roster_json": json.loads(roster_json)})
    return render(request, "employee_roster.html")


def edit_position_time(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        print("data", got_query)
        try:
            position = Position.objects.get(id=int(got_query))
        except Exception:
            position = None
        if position:
            json_position = serializers.serialize('json', [position])
            return JsonResponse({"msg": "success", "position_data": json.loads(json_position)})
        else:
            return JsonResponse({"msg": "failed"})
    return render(request, "admin_position_page.html")


def roster_employee_filter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        position_id = got_query[0]['position']
        center_id = got_query[0]['center']
        print("data", got_query)
        try:
            position = Position.objects.get(id=int(position_id))
        except Exception:
            position = None

        try:
            center = ZenotiCentersData.objects.get(id=int(center_id))
        except Exception:
            center = None

        try:
            extend_center = ExtendedZenotiCenterData.objects.get(
                zenoti_data=center)
        except Exception:
            extend_center = None
        print('yes')
        all_employee = ExtendedZenotiEmployeesData.objects.filter(
            associated_center=extend_center, associated_role=position)
        employee_json = []
        for each_emp in all_employee:
            temp = {}
            temp['name'] = each_emp.zenoti_data.user.user.username
            temp['id'] = each_emp.id
        # print(all_employee)
        employee_json = serializers.serialize('json', employee_json)
        return JsonResponse({"msg": "success",
                             "employee_json": json.loads(employee_json)})
    return render(request, "employee_roster.html")

# url = 'http://49.204.73.242/COSEC/initMain.aspx'
# # head = {"Authorization": "apikey "+api_key}
# response = requests.request("GET", url)
# response_got = json.loads(response)
# print('resp', response_got)


# url = 'https://api.zenoti.com/v1/centers/d8ee21a2-c99d-4cb8-9c5a-5bc5da696dd6/employees?page=1&size=100'
# page_url = 'https://api.zenoti.com/v1/centers/{{center_id}}/products?page=1&size=20'
# head = {"Authorization": "apikey "+api_key}
# response = requests.request("GET", url, headers=head)
# response_got = json.loads(response.text)
# print(response_got)
# 1572

def download_csv(request):
    if request.method == 'POST':
        center_id = request.POST.get("center_id")
        start = request.POST.get("csv_from")
        end = request.POST.get("csv_to")
        csv_type = request.POST.get("csv_type")
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')

        try:
            center = ZenotiCentersData.objects.get(id=int(center_id))
        except Exception:
            center = None

        extend_center = ExtendedZenotiCenterData.objects.get(
            zenoti_data=center)
        rosters = EmployeeRoster.objects.filter(
            center=extend_center)
        schedulers = EmployeeScheduler.objects.filter(center=extend_center)
        if csv_type == 'roster':
            csv_headers = [
                'Date', 'Center', 'Employee', 'KRA', 'Start Time', 'End TIme'
            ]
        else:
            csv_headers = [
                'Date', 'Center', 'Employee', 'KRA', 'Start Time', 'End TIme', 'Status'
            ]

        rows = []
        if csv_type == 'roster':
            for single_date in daterange(start_date, end_date):
                filtered_roster = rosters.filter(appoint_date=single_date)
                for each_roster in filtered_roster:
                    rows.append([
                        each_roster.appoint_date,
                        each_roster.center.zenoti_data.name,
                        each_roster.employee.zenoti_data.employee_name,
                        each_roster.associated_role.name,
                        each_roster.office_start_time,
                        each_roster.office_end_time
                    ])
        else:
            for single_date in daterange(start_date, end_date):
                filtered_scheduler = schedulers.filter(
                    appoint_date=single_date)
                for each_scheduler in filtered_scheduler:
                    rows.append([
                        each_scheduler.appoint_date,
                        each_scheduler.center.zenoti_data.name,
                        each_scheduler.employee.zenoti_data.employee_name,
                        each_scheduler.associated_role.name,
                        each_scheduler.office_start_time,
                        each_scheduler.office_end_time,
                        each_scheduler.status
                    ])

        csv_response = HttpResponse(content_type='text/csv')

        if csv_type == 'roster':
            csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                'Roster_report-' + str(datetime.today().date()) + '.csv')
        else:
            csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                'Scheduler_report-' + str(datetime.today().date()) + '.csv')

        writer = csv.writer(csv_response)
        writer.writerow(csv_headers)
        writer.writerows(rows)
        print('response', csv_response)
        return csv_response


@login_required(login_url='user_login')
def report_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if staffProfile.user_type == 'admin' or staffProfile.user_type == 'staff':
        pass
    else:
        return redirect('/')
    context = {'staffProfile': staffProfile}
    return render(request, 'reports.html', context)


@login_required(login_url='user_login')
def roster_report_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if staffProfile.user_type == 'admin' or staffProfile.user_type == 'staff':
        pass
    else:
        return redirect('/')
    all_rosters = EmployeeRoster.objects.all()
    select_center = request.GET.get('select_center')
    select_kra = request.GET.get('select_kra')
    select_from_date = request.GET.get('select_from_date')
    select_to_date = request.GET.get('select_to_date')
    try:
        center = ExtendedZenotiCenterData.objects.get(id=int(select_center))
    except Exception:
        center = None

    try:
        kra = Position.objects.get(id=int(select_kra))
    except Exception:
        kra = None

    if select_center:
        all_rosters = all_rosters.filter(center=center)
    if select_kra:
        all_rosters = all_rosters.filter(associated_role=kra)
    if select_from_date:
        all_rosters = all_rosters.filter(appoint_date__gte=select_from_date)
    if select_to_date:
        all_rosters = all_rosters.filter(appoint_date__lte=select_to_date)

    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_staff = ExtendedZenotiEmployeesData.objects.all()
    all_kra = Position.objects.all()
    if staffProfile.user_type == 'staff':
        # ExtendedZenotiEmployeesData.objects.filter(
        # zenoti_data_id__in=list(all_therapy_emp.values_list('id', flat=True)))
        zenoti_employee = ZenotiEmployeesData.objects.get(user=staffProfile)
        extend_employee_data = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=zenoti_employee)
        all_staff = all_staff.filter(
            associated_center__in=extend_employee_data.associated_center.all()).distinct()
        all_center = extend_employee_data.associated_center.all()
        all_rosters = all_rosters.filter(center__in=all_center)

    page = Paginator(all_rosters, 50)
    page_num = request.GET.get('page', 1)
    try:
        roster_page = page.page(page_num)
    except EmptyPage:
        roster_page = page.page(1)
    if request.method == 'POST':
        print('in')
        csv_headers = [
            'Date', 'Center', 'Employee', 'KRA', 'Start Time', 'End TIme'
        ]
        rows = []
        for each_roster in all_rosters:
            rows.append([
                each_roster.appoint_date,
                each_roster.center.zenoti_data.name,
                each_roster.employee.zenoti_data.employee_name,
                each_roster.associated_role.name,
                each_roster.office_start_time,
                each_roster.office_end_time
            ])
        csv_response = HttpResponse(content_type='text/csv')

        csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            'Roster_report-' + str(datetime.today().date()) + '.csv')

        writer = csv.writer(csv_response)
        writer.writerow(csv_headers)
        writer.writerows(rows)
        print('response', csv_response)
        return csv_response
    context = {'staffProfile': staffProfile,
               'all_rosters': roster_page, 'all_center': all_center,
               'all_kra': all_kra, 'all_staff': all_staff,
               'select_center': select_center, 'select_kra': select_kra,
               'select_from_date': select_from_date,
               'select_to_date': select_to_date}
    return render(request, 'reports_pages/rosters.html', context)


@login_required(login_url='user_login')
def scheduler_report_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if staffProfile.user_type == 'admin' or staffProfile.user_type == 'staff':
        pass
    else:
        return redirect('/')
    all_scheduler = EmployeeScheduler.objects.all()
    select_center = request.GET.get('select_center')
    select_kra = request.GET.get('select_kra')
    select_from_date = request.GET.get('select_from_date')
    select_to_date = request.GET.get('select_to_date')
    try:
        center = ExtendedZenotiCenterData.objects.get(id=int(select_center))
    except Exception:
        center = None

    try:
        kra = Position.objects.get(id=int(select_kra))
    except Exception:
        kra = None

    if select_center:
        all_scheduler = all_scheduler.filter(center=center)
    if select_kra:
        all_scheduler = all_scheduler.filter(associated_role__in=select_kra)
    if select_from_date:
        all_scheduler = all_scheduler.filter(
            appoint_date__gte=select_from_date)
    if select_to_date:
        all_scheduler = all_scheduler.filter(appoint_date__lte=select_to_date)

    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_staff = ExtendedZenotiEmployeesData.objects.all()
    all_kra = Position.objects.all()
    if staffProfile.user_type == 'staff':
        # ExtendedZenotiEmployeesData.objects.filter(
        # zenoti_data_id__in=list(all_therapy_emp.values_list('id', flat=True)))
        zenoti_employee = ZenotiEmployeesData.objects.get(user=staffProfile)
        extend_employee_data = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=zenoti_employee)
        all_staff = all_staff.filter(
            associated_center__in=extend_employee_data.associated_center.all()).distinct()
        all_center = extend_employee_data.associated_center.all()
        all_scheduler = all_scheduler.filter(center__in=all_center)

    page = Paginator(all_scheduler, 50)
    page_num = request.GET.get('page', 1)
    try:
        scheduler_page = page.page(page_num)
    except EmptyPage:
        scheduler_page = page.page(1)

    if request.method == 'POST':
        print('in')
        csv_headers = [
            'Date', 'Center', 'Employee', 'KRA', 'Remark', 'Start Time', 'End TIme', 'Status'
        ]
        rows = []

        for each_scheduler in all_scheduler:
            role_list = []
            for role in each_scheduler.employee.associated_role.all():
                role_list.append(role.name)
            rows.append([
                each_scheduler.appoint_date,
                each_scheduler.center.zenoti_data.name,
                each_scheduler.employee.zenoti_data.employee_name,
                ', '.join(role_list),
                each_scheduler.remark,
                each_scheduler.office_start_time,
                each_scheduler.office_end_time,
                each_scheduler.status
            ])
        csv_response = HttpResponse(content_type='text/csv')

        csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            'Scheduler_report-' + str(datetime.today().date()) + '.csv')

        writer = csv.writer(csv_response)
        writer.writerow(csv_headers)
        writer.writerows(rows)
        print('response', csv_response)
        return csv_response
    context = {'staffProfile': staffProfile,
               'all_scheduler': scheduler_page, 'all_center': all_center,
               'all_kra': all_kra, 'all_staff': all_staff,
               'select_center': select_center, 'select_kra': select_kra,
               'select_from_date': select_from_date,
               'select_to_date': select_to_date}
    return render(request, 'reports_pages/scheduler.html', context)


@login_required(login_url='user_login')
def leave_management_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    print('out', staffProfile.user_type)
    if staffProfile.user_type == 'admin' or staffProfile.user_type == 'staff':
        pass
    else:
        return redirect('/')
    all_leave = ExtendedZenotiEmployeesLeaveData.objects.all()
    all_employee = ExtendedZenotiEmployeesData.objects.all()
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_section = SectionOption.objects.all()
    if staffProfile.user_type == 'staff':
        # ExtendedZenotiEmployeesData.objects.filter(
        # zenoti_data_id__in=list(all_therapy_emp.values_list('id', flat=True)))
        zenoti_employee = ZenotiEmployeesData.objects.get(user=staffProfile)
        extend_employee_data = ExtendedZenotiEmployeesData.objects.get(
            zenoti_data=zenoti_employee)
        all_employee = all_employee.filter(
            associated_center__in=extend_employee_data.associated_center.all()).distinct()
        all_leave = all_leave.filter(zenoti_data__in=all_employee)
        all_center = extend_employee_data.associated_center.all()
    select_empl = request.GET.get('select_empl')
    select_status = request.GET.get('select_status')
    select_section = request.GET.get('select_section')
    select_center = request.GET.get('select_center')
    select_active = request.GET.get('select_active')

    try:
        employee = ExtendedZenotiEmployeesData.objects.get(id=int(select_empl))
    except Exception:
        employee = None
    today_date = date.today()
    if select_active:
        if select_active == 'All':
            all_leave = all_leave
        else:
            all_leave = all_leave.filter(leave_to_date__gte=today_date)
    else:
        all_leave = all_leave.filter(leave_to_date__gte=today_date)
    if select_empl:
        all_leave = all_leave.filter(zenoti_data=employee)
    if select_status:
        all_leave = all_leave.filter(status=select_status)
    if select_section:
        section = SectionOption.objects.get(id=int(select_section))
        if section.option == 'All':
            pass
        else:
            position = Position.objects.filter(section=section)
            position_employees = ExtendedZenotiEmployeesData.objects.filter(
                associated_role__in=list(position.values_list('id', flat=True)))
            all_leave = all_leave.filter(zenoti_data__in=list(
                position_employees.values_list('id', flat=True)))
    if select_center:
        center = ExtendedZenotiCenterData.objects.get(id=int(select_center))
        employees = ExtendedZenotiEmployeesData.objects.filter(
            associated_center__in=[center])
        all_leave = all_leave.filter(zenoti_data__in=list(
            employees.values_list('id', flat=True)))

    all_leave_list = []
    for leave in all_leave:
        center_list = []
        kra_list = []
        section_list = []
        for center in leave.zenoti_data.associated_center.all():
            center_list.append(center.zenoti_data.name)
        for kra in leave.zenoti_data.associated_role.all():
            kra_list.append(kra.name)
            section_list.append(kra.section.option)
        temp = {}
        temp['name'] = leave.zenoti_data.zenoti_data.employee_name
        temp['center'] = ', '.join(center_list)
        temp['from_date'] = leave.leave_from_date
        temp['to_date'] = leave.leave_to_date
        temp['note'] = leave.note
        temp['status'] = leave.status
        temp['id'] = leave.id
        temp['kra'] = ', '.join(kra_list)
        temp['section'] = ', '.join(set(section_list))
        all_leave_list.append(temp)

    page = Paginator(all_leave_list, 50)
    page_num = request.GET.get('page', 1)
    try:
        leave_page = page.page(page_num)
    except EmptyPage:
        leave_page = page.page(1)
    if request.method == "POST":
        if 'create_leave_form' in request.POST:
            employee_id = request.POST.get("select_emp")
            leave_from = request.POST.get("leave_from")
            leave_to = request.POST.get("leave_to")
            leave_note = request.POST.get("leave_note")
            leave_status = request.POST.get("leave_status")
            if not leave_status:
                leave_status = 'Pending'

            try:
                employee = ExtendedZenotiEmployeesData.objects.get(
                    id=int(employee_id))
            except Exception:
                employee = None

            ExtendedZenotiEmployeesLeaveData.objects.create(
                zenoti_data=employee,
                leave_from_date=leave_from,
                leave_to_date=leave_to,
                note=leave_note,
                status=leave_status
            )
            msg_html = render_to_string('email_template/employee_leave_email.html',
                                        {'name': employee.zenoti_data.employee_name, 'from_date': leave_from,
                                         'to_date': leave_to, 'note': leave_note})
            text_content = strip_tags(msg_html)
            all_admin = UserProfile.objects.filter(user_type='admin')
            for admin in all_admin:
                email = EmailMultiAlternatives(
                    # title
                    f'Bodycraft Staff Leave Application',

                    # context
                    text_content,

                    # from email
                    settings.EMAIL_HOST_USER,

                    # to email
                    [admin.email],
                )
                email.attach_alternative(msg_html, "text/html")
                email.send()
        if 'leave_form_edit' in request.POST:
            leave_id = request.POST.get('edit_leave_id')
            employee_id = request.POST.get("edit_select_emp")
            leave_from = request.POST.get("edit_leave_from")
            leave_to = request.POST.get("edit_leave_to")
            leave_note = request.POST.get("edit_leave_note")
            leave_status = request.POST.get("edit_leave_status")

            try:
                leave_data = ExtendedZenotiEmployeesLeaveData.objects.get(
                    id=int(leave_id))
            except Exception:
                leave_data = None
            try:
                employee = ExtendedZenotiEmployeesData.objects.get(
                    id=int(employee_id))
            except Exception:
                employee = None
            leave_data.zenoti_data = employee
            leave_data.leave_from_date = leave_from
            leave_data.leave_to_date = leave_to
            leave_data.note = leave_note
            leave_data.status = leave_status
            leave_data.save()
        if 'del_leave' in request.POST:
            leave_id = request.POST.get('del_pk')
            try:
                leave_data = ExtendedZenotiEmployeesLeaveData.objects.get(
                    id=int(leave_id))
            except Exception:
                leave_data = None
            leave_data.delete()
        if 'download_csv' in request.POST:
            csv_headers = [
                'Employee', 'Center', 'KRA', 'section', 'From Date', 'To Date', 'Note', 'Status'
            ]
            rows = []

            for each_leave in all_leave:
                role_list = []
                center_list = []
                section_list = []
                for role in each_leave.zenoti_data.associated_role.all():
                    role_list.append(role.name)
                    section_list.append(role.section.option)
                for each_center in each_leave.zenoti_data.associated_center.all():
                    center_list.append(each_center.zenoti_data.name)
                rows.append([
                    each_leave.zenoti_data.zenoti_data.employee_name,
                    ', '.join(center_list),
                    ', '.join(role_list),
                    ', '.join(set(section_list)),
                    each_leave.leave_from_date,
                    each_leave.leave_to_date,
                    each_leave.note,
                    each_leave.status
                ])
            csv_response = HttpResponse(content_type='text/csv')

            csv_response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                'leave_report-' + str(datetime.today().date()) + '.csv')

            writer = csv.writer(csv_response)
            writer.writerow(csv_headers)
            writer.writerows(rows)
            print('response', csv_response)
            return csv_response

        return redirect('staff_leave_management')

    context = {'staffProfile': staffProfile,
               'all_leave': leave_page, 'all_employee': all_employee,
               'select_empl': select_empl, 'select_status': select_status,
               'all_center': all_center, 'all_section': all_section,
               'select_section': select_section, 'select_center': select_center,
               'select_active': select_active}
    return render(request, 'leave_management.html', context)


def edit_employee_leave(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            leave_data = ExtendedZenotiEmployeesLeaveData.objects.get(
                id=int(got_query))
        except Exception:
            leave_data = None
        leave_json = serializers.serialize('json', [leave_data])
        return JsonResponse({"msg": "success",
                             "leave_json": json.loads(leave_json)})


def email_missing_report(request):
    tomorrow_date = date.today() + timedelta(days=1)
    all_center = ExtendedZenotiCenterData.objects.filter(
        center_status='Active')
    all_admin = UserProfile.objects.filter(user_type='admin')
    all_role = Position.objects.all()
    final_missing_report = []
    for center in all_center:
        for each_role in all_role:
            # print('role', each_role)
            role_rosters = EmployeeRoster.objects.filter(
                associated_role=each_role, appoint_date=tomorrow_date, center=center
            ).order_by('office_start_time')

            if not role_rosters:
                final_missing_report.append(
                    str(center.zenoti_data.name) + ' - ' +
                    each_role.name + ' is not appointed whole day.'
                )

            endtime = None
            # print('rosterlen', len(role_rosters))
            for i in range(len(role_rosters)):
                each_roster = role_rosters[i]
                weekday = calendar.day_name[tomorrow_date.weekday()]
                try:
                    employezenoti = ExtendedZenotiEmployeesData.objects.get(
                        id=each_roster.employee.id
                    )
                except Exception:
                    employezenoti = None

                if weekday in str(employezenoti.week_off.all()):
                    # print('yes weekoff exist')
                    final_missing_report.append(
                        str(center.zenoti_data.name) + ' - ' + employezenoti.zenoti_data.employee_name + ' is appointed as ' +
                        each_role.name + ' from ' + str(each_roster.office_start_time.strftime("%I:%M %p")) + ' to ' +
                        str(each_roster.office_end_time.strftime("%I:%M %p")) +
                        ', But the staff has Weekoff'
                    )

                try:
                    employee_leave = ExtendedZenotiEmployeesLeaveData.objects.filter(
                        zenoti_data=each_roster.employee)
                except Exception:
                    employee_leave = None

                for leave in employee_leave:
                    leave_from_date = datetime.strptime(
                        str(leave.leave_from_date), '%Y-%m-%d')
                    leave_end_date = datetime.strptime(
                        str(leave.leave_to_date), '%Y-%m-%d')
                    if tomorrow_date in daterange(leave_from_date, leave_end_date):
                        # print('type', single_date)
                        # if single_date == each_date:
                        if leave.status == 'Approved' or leave.status == 'Pending':
                            final_missing_report.append(
                                str(center.zenoti_data.name) + ' - ' + leave.zenoti_data.zenoti_data.employee_name + ' is appointed as ' +
                                each_role.name + ' But he is on a leave '
                            )

                # print('weekday', type(weekday))
                # print('roster', each_roster)
                if i == 0:
                    # print('loop1')
                    if each_roster.office_start_time > each_role.start_time:
                        final_missing_report.append(
                            str(center.zenoti_data.name) + ' - ' +
                            each_role.name + ' is not appointed from '
                            + str(each_role.start_time.strftime("%I:%M %p")) +
                            ' to ' +
                            str(each_roster.office_start_time.strftime(
                                "%I:%M %p"))

                        )
                elif i == len(role_rosters)-1:
                    if each_roster.office_start_time > endtime:
                        final_missing_report.append(
                            str(center.zenoti_data.name) + ' - ' +
                            each_role.name + ' is not appointed from '
                            + str(endtime.strftime("%I:%M %p")) +
                            ' to ' +
                            str(each_roster.office_start_time.strftime(
                                "%I:%M %p"))
                        )

                    if each_roster.office_end_time < each_role.end_time:
                        final_missing_report.append(
                            str(center.zenoti_data.name) + ' - ' +
                            each_role.name
                            + " is not appointed from " +
                            str(each_roster.office_end_time.strftime("%I:%M %p")) + ' to ' +
                            str(each_role.end_time.strftime("%I:%M %p"))

                        )
                else:
                    # print('end', endtime)
                    if each_roster.office_start_time > endtime:
                        final_missing_report.append(
                            str(center.zenoti_data.name) + ' - ' +
                            each_role.name
                            + ' is not appointed from ' +
                            str(endtime.strftime("%I:%M %p")) + ' to ' +
                            str(each_roster.office_start_time.strftime(
                                "%I:%M %p"))
                        )

                endtime = each_roster.office_end_time
                # print('time', endtime.strftime("%I:%M %p"))
            else:
                pass
    print('list: ', final_missing_report)

    msg_html = render_to_string('email_template/daily_missing_report_email.html',
                                {'list': final_missing_report, 'date': tomorrow_date})
    text_content = strip_tags(msg_html)

    for admin in all_admin:
        email = EmailMultiAlternatives(
            # title
            f'Bodycraft Missing Report',

            # context
            text_content,

            # from email
            settings.EMAIL_HOST_USER,

            # to email
            [admin.email],
        )
        email.attach_alternative(msg_html, "text/html")
        email.send()
    return JsonResponse({'Status': 'Email Sent Successfully!!'})


# url = 'https://api.zenoti.com/v1/Centers/051ba6e9-fec8-49d6-94d6-5fd9a7a70a64/collections_report?start_date=2023-02-01&end_date=2023-02-05'
# head = {"Authorization": "apikey "+api_key}
# response = requests.request("GET", url, headers=head)
# response_got = json.loads(response.text)
# print("reposnse", response_got)
def error_log_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if staffProfile.user_type == 'staff' or staffProfile.user_type == 'admin':
        pass
    else:
        return redirect('/')
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
    all_audit_user = UserProfile.objects.filter(
        user_type__in=['staff', 'admin', 'Auditor']).select_related('user')
    all_user_list = []
    for user_list in all_audit_user:
        first_name = user_list.user.first_name or ""
        last_name = user_list.user.last_name or ""
        temp = {}
        temp['id'] = user_list.id
        temp['name'] = first_name + " " + last_name
        all_user_list.append(temp)
    all_error_log = ErrorLog.objects.all().order_by('-id')
    select_user = request.GET.get('select_user')
    search_date = request.GET.get('search_date')
    select_page = request.GET.get('select_page')

    try:
        staff_profile = UserProfile.objects.get(id=int(select_user))
    except Exception:
        staff_profile = None
    if staff_profile:
        all_error_log = all_error_log.filter(employee=staff_profile)
    if search_date:
        all_error_log = all_error_log.filter(date=search_date)
    if select_page:
        all_error_log = all_error_log.filter(page=select_page)
    page = Paginator(all_error_log, 50)
    page_num = request.GET.get('page', 1)
    try:
        error_log_page = page.page(page_num)
    except EmptyPage:
        error_log_page = page.page(1)
    context = {'staffProfile': staffProfile,
               'all_audit_user': all_user_list,
               'is_audit_admin': is_audit_admin,
               'is_mystery_shopper': is_mystery_shopper,
               'is_salon_revenue_auditor': is_salon_revenue_auditor,
               'is_clinic_revenue_auditor': is_clinic_revenue_auditor,
               'is_corporate_auditor': is_corporate_auditor,
               'all_error_log': error_log_page,
               'select_user': select_user,
               'search_date': search_date,
               'select_page': select_page}
    return render(request, 'error_log.html', context)
