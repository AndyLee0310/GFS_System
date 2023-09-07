from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from sqlalchemy import *
from ..models import *
from .. import db
import datetime, json, re

management = Blueprint('management', __name__)

# ------------------------- 帳號管理 -------------------------
@management.route('/management/account')
@login_required
def account():
    users = User.query.all()
    members = Member.query.all()
    return render_template('management/account.html', users=users, members=members)

@management.route('/management/account/change_state', methods=['POST'])
def change_tate():
    for field_name, value in request.form.items():
        user_id = value
    user = User.query.filter_by(id=user_id).first()
    if (user.state == "0"):
        user.state = "1"
    elif (user.state == "1"):
        user.state = "0"
    db.session.commit()
    return redirect(url_for('management.account'))

@management.route('/management/account/reset_password', methods=['POST'])
def reset_password():
    for field_name, value in request.form.items():
        email = value
    user = User.query.filter_by(email=email).first()
    user.password = generate_password_hash(email.split("@")[0])

    db.session.commit()
    flash(f'Id: {user.id} 重設密碼成功!', category='success')
    return redirect(url_for('management.account'))

@management.route('/management/account/edit', methods=['POST'])
def edit_account():
    email = request.form.get('email')
    name = request.form.get('name')
    member_id = request.form.get('member_id')
    auth = request.form.get('auth')
    state = request.form.get('state')

    if email == "" or name == "" or auth == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')

    user = User.query.filter_by(email=email).first()
    if user.name != name:
        user.name = name
    if user.member_id != member_id:
        user.member_id = member_id
    if user.auth != auth:
        user.auth = auth
    
    if user.member_id != "":
        member = Member.query.filter_by(id=member_id).first()
        if user.name != member.name:
            user.name = member.name

    db.session.commit()
    flash(f'Id: {user.id} 編輯成功!', category='success')
    return redirect(url_for('management.account'))

@management.route('/management/account/create', methods=['POST'])
def create_account():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    member_id = request.form.get('member_id')
    auth = request.form.get('auth')
    state = "1"

    if email == "" or name == "" or password == "" or auth == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email已存在', category='error')
        print('User already exists!')

    userByMemberId = User.query.filter_by(member_id=member_id).first()
    if userByMemberId:
        flash('團員Id已被連結', category='error')
        print('Member Id has been linked!')
        return redirect(url_for('management.account'))

    new_user = User(email=email, name=name, password=generate_password_hash(password), member_id=member_id, auth=auth, state=state)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('management.account'))

# -----------------------------------------------------------

# ------------------------- 團員管理 -------------------------
@management.route('/management/member')
@login_required
def member():
    members = Member.query.all()
    year_now = datetime.datetime.now().year

    level_array = ['童軍', '行義', '羅浮', '服務員', '團長']
    for member in members:
        levels = Level.query.filter_by(member_id=member.id).all()
        member_level_array = []
        if len(levels) != 0:
            for i in range(0, len(levels), 1):
                if levels[i].name in level_array:
                    member_level_array.append(level_array.index(levels[i].name))
            member.level = level_array[max(member_level_array)]
        else:
            member.level = ""

    return render_template('management/member.html', members=enumerate(members), year_now=year_now)

@management.route('/management/member/edit', methods=['POST'])
def edit_member():
    member_id = request.form.get('member_id')
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    name = request.form.get('name')
    email = request.form.get('email')
    birthday = request.form.get('birthday')
    gender = request.form.get('gender')
    number_of_periods = request.form.get('number_of_periods')
    phone = request.form.get('phone')
    tel = request.form.get('tel')
    description = request.form.get('description')
    state = request.form.get('state')

    if last_name == "" or first_name == "" or name == "" or email == "" or birthday == "" or gender == "" or number_of_periods == "" or phone == "" or tel == "" or state == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.member'))

    member = Member.query.filter_by(id=member_id).first()
    if member.last_name != last_name:
        member.last_name = last_name
    if member.first_name != first_name:
        member.first_name = first_name
    if member.name != name:
        member.name = name
    if member.email != email:
        member.email = email
    if member.birthday != birthday:
        member.birthday = birthday
    if member.number_of_periods != number_of_periods:
        member.number_of_periods = number_of_periods
    if member.gender != gender:
        member.gender = gender
    if member.phone != phone:
        member.phone = phone
    if member.tel != tel:
        member.tel = tel
    if member.description != description:
        member.description = description
    if member.state != state:
        member.state = state

    db.session.commit()
    flash(f'Id: {member.id} 編輯成功!', category='success')
    return redirect(url_for('management.member'))


@management.route('/management/member/create', methods=['POST'])
def create_member():
    id_number = request.form.get('id_number')
    join_year = request.form.get('join_year')
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    name = request.form.get('name')
    email = request.form.get('email')
    birthday = request.form.get('birthday')
    gender = request.form.get('gender')
    number_of_periods = request.form.get('number_of_periods')
    phone = request.form.get('phone')
    tel = request.form.get('tel')
    description = request.form.get('description')
    state = request.form.get('state')

    # 因身分證字號儲存上有安全性問題，輸入可隨意輸入，但不可重複
    if join_year == "" or id_number == "" or first_name == "" or name == "" or email == "" or birthday == "" or gender == "" or number_of_periods == "" or phone == "" or tel == "" or state == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.member'))

    # members = Member.query.filter(and_(Member.id.like(f"{join_year}{int(number_of_periods):03}%"), Member.id_number==id_number)).all()    # 使用身分證字號為第二判斷，來確定是否有重複新增團員
    member = Member.query.filter(and_(Member.id.like(f"{join_year}{int(number_of_periods):03}%"), Member.email==email)).all()
    if member:
        flash('團員已存在', category='error')
        print('Member already exists!')

    member_count = Member.query.filter(Member.id.like(f"{join_year}{int(number_of_periods):03}%")).count()
    member_id = f"{join_year}{int(number_of_periods):03}{member_count + 1:03}"
    new_member = Member(id=member_id, id_number=id_number, first_name=first_name, last_name=last_name, name=name, email=email, birthday=birthday, gender=gender, phone=phone, tel=tel, number_of_periods=number_of_periods, description=description, state=state)

    db.session.add(new_member)
    db.session.commit()
    return redirect(url_for('management.member'))

# -----------------------------------------------------------

# ------------------------- 三項登記 -------------------------
@management.route('/management/member_registration')
@login_required
def member_registration():
    memberRegistrations = MembershipRegistration.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)

    for item in memberRegistrations:
        member = Member.query.filter_by(id=item.member_id).first()
        item.name = member.name

    year_now = datetime.datetime.now().year
    return render_template('management/memberRegistration.html', member_registrations=enumerate(memberRegistrations, start=1), year_now=year_now, members=members)

@management.route('/management/member_registration/create', methods=['POST'])
def create_member_registration():
    member_id = request.form.get('member_id')
    registration_year = request.form.get('registration_year')

    if member_id == "" or registration_year == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')

    memberRegistration = MembershipRegistration.query.filter_by(member_id=member_id, registration_year=registration_year).first()
    if memberRegistration:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.member_registration'))

    new_memberRegistration = MembershipRegistration(member_id=member_id, registration_year=registration_year)
    db.session.add(new_memberRegistration)
    db.session.commit()
    return redirect(url_for('management.member_registration'))

@management.route('/management/member_registration/delete', methods=['POST'])
def delete_member_registration():
    delete_id = request.form.get('delete_id')
    memberRegistration = MembershipRegistration.query.filter_by(id=delete_id).first()
    db.session.delete(memberRegistration)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.member_registration'))

# -----------------------------------------------------------

# ------------------------ 階級(升團) ------------------------
@management.route('/management/level')
@login_required
def level():
    levels = Level.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)
    for item in levels:
        member = Member.query.filter_by(id=item.member_id).first()
        item.member_name = member.name

    return render_template('management/level.html', levels=enumerate(levels, start=1), members=members)

@management.route('/management/level/create', methods=['POST'])
def create_level():
    member_id = request.form.get('member_id')
    promotion_name = request.form.get('promotion_name')
    promotion_date = request.form.get('promotion_date')

    if member_id == "" or promotion_name == "" or promotion_date == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.level'))

    level = Level.query.filter_by(member_id=member_id, name=promotion_name).first()
    if level:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.level'))

    levels = Level.query.filter_by(member_id=member_id).all()
    member_level_array = []
    level_array = ['童軍', '行義', '羅浮', '服務員', '團長']
    for i in range(0, len(levels), 1):
        if levels[i].name in level_array:
            member_level_array.append(level_array.index(levels[i].name))
    new_level_name = level_array.index(promotion_name)
    if len(member_level_array) != 0 and new_level_name > max(member_level_array):
        old_max_level = Level.query.filter_by(member_id=member_id, name=level_array[max(member_level_array)]).first()
        if promotion_date < old_max_level.promotion_date:
            flash('升團日期不可早於原最高階級之升團日期', category='error')
            print('Promotion date cannot be earlier than the promotion date of the original highest rank')
            return redirect(url_for('management.level'))

    new_level = Level(member_id=member_id, name=promotion_name, promotion_date=promotion_date)
    db.session.add(new_level)
    db.session.commit()
    return redirect(url_for('management.level'))

@management.route('/management/level/delete', methods=['POST'])
def delete_level():
    delete_id = request.form.get('delete_id')
    level = Level.query.filter_by(id=delete_id).first()
    db.session.delete(level)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.level'))

# -----------------------------------------------------------

# ------------------------- 進程考驗 -------------------------
@management.route('/management/advancement')
@login_required
def advancement():
    advancements = Advancement.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)
    for item in advancements:
        member = Member.query.filter_by(id=item.member_id).first()
        item.member_name = member.name
    return render_template('management/advancement.html', advancements=enumerate(advancements), members=members)

@management.route('/management/advancement/create', methods=['POST'])
def create_advancement():
    member_id = request.form.get('member_id')
    advancement_name = request.form.get('advancement_name')
    pass_date = request.form.get('pass_date')

    if member_id == "" or advancement_name == "" or pass_date == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.advancement'))
    
    advancement = Advancement.query.filter_by(member_id=member_id, name=advancement_name).first()
    if advancement:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.advancement'))

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
            return redirect(url_for('management.advancement'))


    new_advancement = Advancement(member_id=member_id, name=advancement_name, pass_date=pass_date)
    db.session.add(new_advancement)
    db.session.commit()
    return redirect(url_for('management.advancement'))

@management.route('/management/advancement/delete', methods=['POST'])
def delete_advancement():
    delete_id = request.form.get('delete_id')
    advancement = Advancement.query.filter_by(id=delete_id).first()
    db.session.delete(advancement)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.advancement'))

# -----------------------------------------------------------

# ------------------------ 專科章考驗 ------------------------
@management.route('/management/proficiencyBadge')
@login_required
def proficiencyBadge():
    proficiencyBadges = ProficiencyBadge.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)
    for item in proficiencyBadges:
        member = Member.query.filter_by(id=item.member_id).first()
        item.member_name = member.name
    return render_template('management/proficiencyBadge.html', proficiencyBadges=enumerate(proficiencyBadges), members=members)

@management.route('/management/proficiencyBadge/create', methods=['POST'])
def create_proficiencyBadge():
    member_id = request.form.get('member_id')
    proficiencyBadge_name = request.form.get('proficiencyBadge_name')
    pass_date = request.form.get('pass_date')

    if member_id == "" or proficiencyBadge_name == "" or pass_date == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.proficiencyBadge'))

    proficiencyBadge = ProficiencyBadges.query.filter_by(member_id=member_id, name=proficiencyBadge_name).first()
    if proficiencyBadge:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.proficiencyBadge'))

    new_proficiencyBadge = ProficiencyBadges(member_id=member_id, name=proficiencyBadge_name, pass_date=pass_date)
    db.session.add(new_proficiencyBadge)
    db.session.commit()
    flash('資料新增成功!', category='success')
    return redirect(url_for('management.proficiencyBadge'))

@management.route('/management/proficiencyBadge/delete', methods=['POST'])
def delete_proficiencyBadge():
    delete_id = request.form.get('delete_id')
    proficiencyBadge = ProficiencyBadges.query.filter_by(id=delete_id).first()
    db.session.delete(proficiencyBadge)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.proficiencyBadge'))

# -----------------------------------------------------------

# --------------------------- 活動 ---------------------------
@management.route('/management/activity')
@login_required
def activity():
    activities = Activity.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)
    return render_template('management/activity.html', activities=enumerate(activities, start=1), members=members)

@management.route('/management/activity/create', methods=['POST'])
def create_activity():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    location = request.form.get('location')
    participants = request.form.get('participantList')
    staffs = request.form.get('staffList')
    description = request.form.get('description')
    state = request.form.get('state')
    allowed = "1"

    if re.sub(r'\s*', '', description) == "":
        description = None

    if name == "" or start_date == "" or end_date == "" or location == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.activity'))

    activity = Activity.query.filter_by(name=name).first()
    if activity:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.activity'))

    new_activity = Activity(name=name, start_date=start_date, end_date=end_date, location=location, participants=participants, staffs=staffs, description=description, state=state, allowed=allowed)
    db.session.add(new_activity)
    db.session.commit()
    return redirect(url_for('management.activity'))

@management.route('/management/activity/edit', methods=['POST'])
def edit_activity():
    activity_id = request.form.get('activity_id')
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    location = request.form.get('location')
    participants = request.form.get('participantList')
    staffs = request.form.get('staffList')
    description = request.form.get('description')
    state = request.form.get('state')

    if name == "" or start_date == "" or end_date == "" or location == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.activity'))

    activity = Activity.query.filter_by(id=activity_id).first()
    if activity.name != name:
        activity.name = name
    if activity.start_date != start_date:
        activity.start_date = start_date
    if activity.end_date != end_date:
        activity.end_date = end_date
    if activity.location != location:
        activity.location = location
    if activity.participants != participants:
        activity.participants = participants
    if activity.staffs != staffs:
        activity.staffs = staffs
    if activity.description != description:
        activity.description = description
    if activity.state != state:
        activity.state = state

    db.session.commit()
    flash(f'Id: {activity.id} 編輯成功!', category='success')
    return redirect(url_for('management.activity'))

@management.route('/management/activity/delete', methods=['POST'])
def delete_activity():
    delete_id = request.form.get('delete_id')
    activity = Activity.query.filter_by(id=delete_id).first()
    db.session.delete(activity)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.activity'))

@management.route('/management/activity/allowed', methods=['POST'])
def allowed_activity():
    activity_id = request.form.get('allowed_id')
    print(activity_id)
    activity = Activity.query.filter_by(id=activity_id).first()
    print(activity.allowed)
    if (activity.allowed == "0"):
        activity.allowed = "1"

    db.session.commit()
    flash(f'Id: {activity.id} 審核成功!', category='success')
    return redirect(url_for('management.activity'))

# -----------------------------------------------------------

# --------------------------- 服務 ---------------------------
@management.route('/management/service')
@login_required
def service():
    services = Service.query.all()
    members = Member.query.filter_by(state="0").all()   # 只顯示正式團員(排除退團、休團之團員)
    return render_template('management/service.html', services=enumerate(services, start=1), members=members)

@management.route('/management/service/create', methods=['POST'])
def create_service():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    service_hours = request.form.get('service_hours')
    location = request.form.get('location')
    participants = request.form.get('participantList')

    if name == "" or start_date == "" or end_date == "" or location == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.service'))
    
    service = Service.query.filter_by(name=name).first()
    if service:
        flash('資料已存在', category='error')
        print('Data already exists!')
        return redirect(url_for('management.service'))
    
    new_service = Service(name=name, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, service_hours=service_hours, location=location, participants=participants)
    db.session.add(new_service)
    db.session.commit()
    return redirect(url_for('management.service'))

@management.route('/management/service/edit', methods=['POST'])
def edit_service():
    id = request.form.get('service_id')
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    service_hours = request.form.get('service_hours')
    location = request.form.get('location')
    participants = request.form.get('participantList')

    if name == "" or start_date == "" or end_date == "" or location == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')
        return redirect(url_for('management.service'))
    
    service = Service.query.filter_by(id=id).first()
    if service.name != name:
        service.name = name
    if service.start_date != start_date:
        service.start_date = start_date
    if service.end_date != end_date:
        service.end_date = end_date
    if service.start_time != start_time:
        service.start_time = start_time
    if service.end_time != end_time:
        service.end_time = end_time
    if service.service_hours != service_hours:
        service.service_hours = service_hours
    if service.location != location:
        service.location = location
    if service.participants != participants:
        service.participants = participants
    
    db.session.commit()
    flash(f'Id: {service.id} 編輯成功!', category='success')
    return redirect(url_for('management.service'))

@management.route('/management/service/delete', methods=['POST'])
def delete_service():
    delete_id = request.form.get('delete_id')
    service = Service.query.filter_by(id=delete_id).first()
    db.session.delete(service)
    db.session.commit()
    flash('資料刪除成功!', category='success')
    return redirect(url_for('management.service'))
# -----------------------------------------------------------

# --------------------------- API ---------------------------
def member_encoder(obj):
    if isinstance(obj, Member):
        return {
            "id" : obj.id,
            "id_number" : obj.id_number,
            "first_name" : obj.first_name,
            "last_name" : obj.last_name,
            "name" : obj.name,
            "gender" : obj.gender,
            "birthday" : obj.birthday,
            "email" : obj.email,
            "phone" : obj.phone,
            "tel" : obj.tel,
            "number_of_periods" : obj.number_of_periods,
            "description" : obj.description,
            "state" : obj.state
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# 透過團員Id取得團員資料
@management.route('/management/member', methods=['POST'])
def get_member_by_member_id():
    data = request.json
    member_id = data.get('member_id', '')
    member = Member.query.filter_by(id=member_id).first()
    member_json = json.loads(json.dumps(member, default=member_encoder,indent=4, ensure_ascii=False))
    return member_json

# 檢查團員Id是否已被連結
@management.route('/management/user/checkLinkStatus', methods=['POST'])
def check_link_status():
    data = request.json
    member_id = data.get('member_id', '')
    user = User.query.filter_by(member_id=member_id).first()
    if user:
        return json.loads(json.dumps({'checkResult' : True}))
    return json.loads(json.dumps({'checkResult' : False}))

def activity_encoder(obj):
    if isinstance(obj, Activity):
        return {
            "id": obj.id,
            "name": obj.name,
            "start_date": obj.start_date,
            "end_date": obj.end_date,
            "location": obj.location,
            "participants": obj.participants,
            "staffs": obj.staffs,
            "file_path": obj.file_path,
            "description": obj.description,
            "state": obj.state,
            "allowed": obj.allowed
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# 透過活動Id取得活動資料
@management.route('/management/activity', methods=['POST'])
def get_activity_by_id():
    data = request.json
    activity_id = data.get('activity_id', '')
    activity = Activity.query.filter_by(id=activity_id).first()
    activity_json = json.loads(json.dumps(activity, default=activity_encoder, indent=4, ensure_ascii=False))
    return activity_json

def service_encoder(obj):
    if isinstance(obj, Service):
        return {
            "id": obj.id,
            "name": obj.name,
            "start_date": obj.start_date,
            "start_time": obj.start_time,
            "end_date": obj.end_date,
            "end_time": obj.end_time,
            "service_hours": obj.service_hours,
            "location": obj.location,
            "participants": obj.participants
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# 透過服務Id取得服務資料
@management.route('/management/service', methods=['POST'])
def get_service_by_id():
    data = request.json
    service_id = data.get('service_id', '')
    service = Service.query.filter_by(id=service_id).first()
    service_json = json.loads(json.dumps(service, default=service_encoder, indent=4, ensure_ascii=False))
    return service_json