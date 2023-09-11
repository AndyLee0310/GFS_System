from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..controllers.controller import create_system_record
from sqlalchemy import *
from ..models import *
import json

user = Blueprint('user', __name__)

# --------------------------- 帳號 ---------------------------
@user.route('/user/account')
@login_required
def account_info():
    return render_template('/user/account.html')

# -------------------------------------------------------------

# -------------------------- 個人資料 --------------------------
@user.route('/user/profile')
@login_required
def profile():
    member_info = Member.query.filter_by(id=current_user.member_id).first()
    return render_template('/user/profile.html', member_info=member_info)

@user.route('/user/profile/edit', methods=['POST'])
def profile_edit():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    gender = data.get('gender')
    birthday = data.get('birthday')
    phone = data.get('phone')
    tel = data.get('tel')

    # if email == "" or name == "" or gender == "" or birthday == "" or phone == "" or tel == "":
    #     flash('請填寫所有欄位', category='error')
    #     return redirect(url_for('user.profile'))

    member = Member.query.filter_by(id=current_user.member_id).first()
    if member.email != email:
        member.email = email
    if member.name != name:
        member.name = name
    if member.gender != gender:
        member.gender = gender
    if member.birthday != birthday:
        member.birthday = birthday
    if member.phone != phone:
        member.phone = phone
    if member.tel != tel:
        member.tel = tel

    db.session.commit()
    member_info = Member.query.filter_by(id=current_user.member_id).first()
    return render_template('/user/profile.html', member_info=member_info)

@user.route('/user/resetPassword', methods=['POST'])
def reset_password():
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')
    print(old_password, new_password, confirm_password)
    user = User.query.filter_by(id=current_user.id).first()
    
    if not check_password_hash(current_user.password, old_password):
        flash('舊密碼錯誤', category='error')
        return redirect(url_for('user.profile'))
    if new_password != confirm_password:
        flash('新密碼與確認密碼不符', category='error')
        return redirect(url_for('user.profile'))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('重設密碼成功!', category='success')
    return redirect(url_for('user.profile'))

# -------------------------------------------------------------

# -------------------------- 三項登記 --------------------------
@user.route('/user/memberRegistration')
@login_required
def member_registration():
    membershipRegistrations = MembershipRegistration.query.filter_by(member_id=current_user.member_id).all()
    return render_template('/user/memberRegistration.html', membershipRegistrations=enumerate(membershipRegistrations))

# -------------------------------------------------------------

# ------------------------- 階級(升團) -------------------------
@user.route('/user/level')
@login_required
def level():
    levels = Level.query.filter_by(member_id=current_user.member_id).all()
    return render_template('/user/level.html', levels=enumerate(levels))

# -------------------------------------------------------------

# -------------------------- 進程考驗 --------------------------
@user.route('/user/advancement')
@login_required
def advancement():
    advancements = Advancement.query.filter_by(member_id=current_user.member_id).all()
    return render_template('/user/advancement.html', advancements=enumerate(advancements))

@user.route('/user/advancement/create', methods=['POST'])
def create_advancement():
    try:
        member_id = request.form.get('member_id')
        advancement_name = request.form.get('advancement_name')
        pass_date = request.form.get('pass_date')

        if member_id == "" or advancement_name == "" or pass_date == "":
            flash('請填寫所有欄位', category='error')
            print('Please fill in all fields')
            return redirect(url_for('user.advancement'))
        
        advancement = Advancement.query.filter_by(member_id=member_id, name=advancement_name).first()
        if advancement:
            flash('資料已存在', category='error')
            print('Data already exists')
            return redirect(url_for('user.advancement'))

        advancements = Advancement.query.filter_by(member_id=member_id).all()
        member_advancement_array = []
        advancement_array = ['初級', '中級', '高級', '獅級', '長城', '國花', '見習羅浮', '授銜羅浮', '服務羅浮']
        for i in range(0, len(advancements), 1):
            if advancements[i].name in advancement_array:
                member_advancement_array.append(advancement_array.index(advancements[i].name))
        new_advancement_name = advancement_array.index(advancement_name)
        if len(member_advancement_array) != 0 and new_advancement_name > max(member_advancement_array):
            old_max_advancement = Advancement.query.filter_by(member_id=member_id, name=advancement_array[max(member_advancement_array)]).first()
            if pass_date < old_max_advancement.pass_date:
                flash('新進程考驗不可早於原最高進程考驗之通過日期', category='error')
                print('The new progress test cannot be earlier than the pass date of the original highest progress test')
                return redirect(url_for('user.advancement'))

        new_advancement = Advancement(member_id=member_id, name=advancement_name, pass_date=pass_date)
        db.session.add(new_advancement)
        db.session.commit()
        create_system_record(f"user.advancement:新增 member id:{member_id} 的進程考驗")
        flash('新增成功!', category='success')
    except Exception as e:
        print(e)
        flash('新增失敗!', category='error')
    return redirect(url_for('user.advancement'))

# -------------------------------------------------------------

# ------------------------- 專科章考驗 -------------------------
@user.route('/user/proficiencyBadge')
@login_required
def proficiencyBadge():
    proficiencyBadges = ProficiencyBadge.query.filter_by(member_id=current_user.member_id).all()
    return render_template('/user/proficiencyBadge.html', proficiencyBadges=enumerate(proficiencyBadges))

@user.route('/user/proficiencyBadge/create', methods=['POST'])
def create_proficiencyBadge():
    try:
        member_id = request.form.get('member_id')
        proficiencyBadge_name = request.form.get('proficiencyBadge_name')
        pass_date = request.form.get('pass_date')

        if member_id == "" or proficiencyBadge_name == "" or pass_date == "":
            flash('請填寫所有欄位', category='error')
            print('Please fill in all fields')
            return redirect(url_for('user.proficiencyBadge'))
        
        proficiencyBadge = ProficiencyBadge.query.filter_by(member_id=member_id, name=proficiencyBadge_name).first()
        if proficiencyBadge:
            flash('資料已存在', category='error')
            print('Data already exists')
            return redirect(url_for('user.proficiencyBadge'))
        
        new_proficiencyBadge = ProficiencyBadge(member_id=member_id, name=proficiencyBadge_name, pass_date=pass_date)
        db.session.add(new_proficiencyBadge)
        db.session.commit()
        create_system_record(f"user.proficiencyBadge:新增 member id:{member_id} 的專科章考驗")
        flash('新增成功!', category='success')
    except Exception as e:
        print(e)
        flash('新增失敗!', category='error')
    return redirect(url_for('user.proficiencyBadge'))

# -------------------------------------------------------------

# -------------------------- 活動紀錄 --------------------------
@user.route('/user/activity')
@login_required
def activity():
    activities = []
    activities_participant = Activity.query.filter(Activity.participants.like(f"%{current_user.member_id}%")).all()
    activities_staff = Activity.query.filter(Activity.staffs.like(f"%{current_user.member_id}%")).all()
    for i in activities_participant:
        i.identity = "參加人員"
        activities.append(i)
    for i in activities_staff:
        i.identity = "服務人員"
        activities.append(i)
    return render_template('/user/activity.html', activities=enumerate(activities))

def get_member(name, number_of_periods):
    if name != "" and number_of_periods == "":
        member = Member.query.filter_by(name=name).first()
    elif name == "" and number_of_periods != "":
        member = Member.query.filter_by(number_of_periods=number_of_periods).first()
    elif name != "" and number_of_periods != "":
        member = Member.query.filter_by(name=name, number_of_periods=number_of_periods).first()

    if member:
        return member.id
    else:
        return f"{name}_{number_of_periods}"

def find_duplicate_and_leave_one_at_list(find_list):
    unique_set = set()
    result_list = []

    for item in find_list:
        if item not in unique_set:
            unique_set.add(item)
            result_list.append(item)
    return result_list


@user.route('/user/activity/create', methods=['POST'])
def create_activity():
    try:
        name = request.form.get('name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        location = request.form.get('location')
        participants = request.form.get('participantList')
        staffs = request.form.get('staffList')
        description = request.form.get('description')
        state = request.form.get('state')
        allowed = "0"

        if name == "" or start_date == "" or end_date == "" or location == "" or state == "":
            flash('請填寫所有欄位', category='error')
            print('Please fill in all fields')
            return redirect(url_for('user.activity'))

        activity = Activity.query.filter_by(name=name, start_date=start_date, end_date=end_date).first()
        if activity:
            flash('資料已存在，若畫面無顯示則向詢問團長', category='error')
            print('Data already exists')
            return redirect(url_for('user.activity'))

        array_participant = []
        if participants != "":
            json_participants = json.loads(participants)
            for i in range(0, len(json_participants), 1):
                array_participant.append(get_member(json_participants[i]['name'], json_participants[i]['num']))
            array_participant = find_duplicate_and_leave_one_at_list(array_participant)
        if array_participant != []:
            string_participant = str(array_participant)
        else:
            string_participant = ""

        array_staff = []
        if staffs != "":
            json_staffs = json.loads(staffs)
            for i in range(0, len(json_staffs), 1):
                array_staff.append(get_member(json_staffs[i]['name'], json_staffs[i]['num']))
            array_staff = find_duplicate_and_leave_one_at_list(array_staff)
            print(array_staff)
        if array_staff != []:
            string_staff = str(array_staff)
        else:
            string_staff = ""

        new_activity = Activity(name=name, start_date=start_date, end_date=end_date, location=location, participants=string_participant, staffs=string_staff, description=description, state=state, allowed=allowed)
        db.session.add(new_activity)
        db.session.commit()
        create_system_record(f"user.activity:新增活動 {name}")
        flash('新增成功!請等待團長審核!', category='success')
    except Exception as e:
        print(e)
        flash('新增失敗!', category='error')
    return redirect(url_for('user.activity'))

# -------------------------------------------------------------

# -------------------------- 服務紀錄 --------------------------
@user.route('/user/service')
@login_required
def service():
    services = Service.query.filter(Service.participants.like(f"%{current_user.member_id}%")).all()
    return render_template('/user/service.html', services=enumerate(services))

@user.route('/user/service/create', methods=['POST'])
def create_service():
    try:
        name = request.form.get('name')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')
        service_hours = request.form.get('service_hours')
        location = request.form.get('location')
        participants = request.form.get('participantList')
        description = request.form.get('description')
        allowed = "0"
        allDayCheckbox = request.form.get('allDayCheckbox')
        print(allDayCheckbox)
        if name == "" or start_date == ""  or end_date == "" or service_hours == "" or location == "":
            flash('請填寫所有欄位', category='error')
            print('Please fill in all fields')
            return redirect(url_for('user.service'))
        if allDayCheckbox == None:
            if start_time == "" or end_time == "":
                flash('請填寫所有欄位', category='error')
                print('Please fill in all fields')
                return redirect(url_for('user.service'))

        service = Service.query.filter_by(name=name, start_date=start_date, end_date=end_date).first()
        if service:
            flash('資料已存在，若畫面無顯示則向詢問團長', category='error')
            print('Data already exists')
            return redirect(url_for('user.service'))

        array_participant = []
        if participants != "":
            json_participants = json.loads(participants)
            for i in range(0, len(json_participants), 1):
                array_participant.append(get_member(json_participants[i]['name'], json_participants[i]['num']))
            array_participant = find_duplicate_and_leave_one_at_list(array_participant)
        if array_participant != []:
            string_participant = str(array_participant)
        else:
            string_participant = ""
        
        new_service = Service(name=name, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, service_hours=service_hours, location=location, participants=string_participant, description=description, allowed=allowed)
        db.session.add(new_service)
        db.session.commit()
        create_system_record(f"user.service:新增服務 {name}")
        flash('新增成功!請等待團長審核!', category='success')
    except Exception as e:
        print(e)
        flash('新增失敗!', category='error')
    return redirect(url_for('user.service'))
# -------------------------------------------------------------
