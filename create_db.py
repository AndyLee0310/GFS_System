from website import db, create_app
from website.models import *
from werkzeug.security import generate_password_hash
import os

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

        # 新增使用者
        new_users = [
                        User(email='test@gmail.com', name='測試帳號', password=generate_password_hash('test'), auth='1', state='1', member_id=''),
                        User(email='admin@gmail.com', name='管理員', password=generate_password_hash('admin'), auth='2', state='1', member_id='')
                    ]
        db.session.add_all(new_users)  # 新增多筆資料
        db.session.commit()

        # 新增團員
        # new_members = [
        #                 Member(id='2021010001', id_number='D167890123', first_name='帳號', last_name='測試', name='測試帳號', gender='1', birthday='1995-09-10', email='test@gmail.com', phone='0933-888-999', tel='08-8765-4321', number_of_periods='010', state='0'),
        #                 Member(id='2023000000', id_number='2023000000', last_name='System', first_name='Admin', name='SystemAdmin', gender='1', birthday='2001-02-06', email='admin@gmail.com', phone='20010206', tel='20010206', number_of_periods='0', description='Admin', state='0')
        #             ]
        # db.session.add_all(new_members)  # 新增多筆資料
        # db.session.commit()

        # 新增三項登記
        # new_memberRegistrations = [
        #                             MembershipRegistration(member_id='2021010001', registration_year='2023')
        #                             ]
        # db.session.add_all(new_memberRegistrations)  # 新增多筆資料
        # db.session.commit()

        # 新增階級(升團)
        # new_levels = [
        #                 Level(member_id='2021010001', name='童軍', promotion_date='2023-07-06')
        #             ]
        # db.session.add_all(new_levels)  # 新增多筆資料
        # db.session.commit()

        # 新增進程
        # new_Advancements = [
        #                     Advancement(member_id="2021010001", name="初級", pass_date="2023-07-05")
        #                     ]
        # db.session.add_all(new_Advancements)  # 新增多筆資料
        # db.session.commit()

        # 新增專科章
        # new_proficiencyBadges = [
        #                             ProficiencyBadge(member_id="2021010001", name="社區公民專科章", pass_date="2023-08-21")
        #                         ]
        # db.session.add_all(new_proficiencyBadges)  # 新增多筆資料
        # db.session.commit()

        # 新增活動
        # new_activities = [
        #                     Activity(name='第九屆適性探索祖魯領袖培訓營', start_date='2023-07-21', end_date = '2023-07-23', location = '花蓮縣立國風國中', state='2', participants = '["2021010001"]', staffs='["2023000000"]', allowed='1'),
        #                 ]
        # db.session.add_all(new_activities)  # 新增多筆資料
        # db.session.commit()

        print("Current directory: ", os.getcwd())