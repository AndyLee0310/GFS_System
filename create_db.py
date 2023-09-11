from website import db, create_app
from website.models import *
import os

if __name__ == '__main__':
    app = create_app()

    if os.path.exists('./instance/db.sqlite'):
        os.remove('./instance/db.sqlite')

    with app.app_context():
        db.create_all()

        # 新增使用者
        from db_file.users import new_users
        db.session.add_all(new_users)  # 新增多筆資料
        db.session.commit()

        # 新增團員
        from db_file.members import new_members
        db.session.add_all(new_members)  # 新增多筆資料
        db.session.commit()

        # 新增三項登記
        from db_file.memberRegistrations import new_memberRegistrations
        db.session.add_all(new_memberRegistrations)  # 新增多筆資料
        db.session.commit()

        # 新增階級(升團)
        from db_file.levels import new_levels
        db.session.add_all(new_levels)  # 新增多筆資料
        db.session.commit()

        # 新增進程
        from db_file.advancements import new_Advancements
        db.session.add_all(new_Advancements)  # 新增多筆資料
        db.session.commit()

        # 新增專科章
        from db_file.proficiencyBadges import new_proficiencyBadges
        db.session.add_all(new_proficiencyBadges)  # 新增多筆資料
        db.session.commit()

        # 新增活動
        from db_file.activities import new_activities
        db.session.add_all(new_activities)  # 新增多筆資料
        db.session.commit()

        # 新增服務
        from db_file.services import new_services
        db.session.add_all(new_services)  # 新增多筆資料
        db.session.commit()

        print("Current directory: ", os.getcwd())