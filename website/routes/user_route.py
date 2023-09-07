from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import *
from ..models import *

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

# -------------------------------------------------------------

# ------------------------- 專科章考驗 -------------------------
@user.route('/user/proficiencyBadge')
@login_required
def proficiencyBadge():
    proficiencyBadges = ProficiencyBadge.query.filter_by(member_id=current_user.member_id).all()
    return render_template('/user/proficiencyBadge.html', proficiencyBadges=enumerate(proficiencyBadges))

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

# -------------------------------------------------------------

# -------------------------- 服務紀錄 --------------------------
@user.route('/user/service')
@login_required
def service():
    services = Service.query.filter(Service.participants.like(f"%{current_user.member_id}%")).all()
    return render_template('/user/service.html', services=enumerate(services))

# -------------------------------------------------------------
