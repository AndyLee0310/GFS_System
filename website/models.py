from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True) # email唯一性
    password = db.Column(db.String(150)) # 密碼
    name = db.Column(db.String(150)) # 姓名 - 與團員資料做連結以後，以團員姓名為主
    auth = db.Column(db.String[10]) # 權限(0:訪客、1:一般會員、2:管理員、3:系統管理員)
    state = db.Column(db.String(150)) # 帳號狀態(1:正常、0:停權)
    member_id = db.Column(db.String(50), db.ForeignKey('member.id')) # 團員id - 若有連結團員資料，則為團員id

class Member(db.Model):
    id = db.Column(db.String(50), primary_key=True) # 團員id (年份+屆數+流水號) ex: 2013007001 (2013年第7屆第1號)
    id_number = db.Column(db.String(150), unique=True) # 身分證字號唯一性 - 先創建但資安問題待解決
    first_name = db.Column(db.String(150)) # 名字
    last_name = db.Column(db.String(150)) # 姓氏
    name = db.Column(db.String(150)) # 姓名(姓氏+名字) - 先創建以防未來有需要
    gender = db.Column(db.String(5)) # 性別(1:男、0:女)
    birthday = db.Column(db.String(150)) # 生日
    email = db.Column(db.String(255), unique=True) # email唯一性 - 聯絡用，可與帳號的email不同
    phone = db.Column(db.String(150)) # 手機號碼
    tel = db.Column(db.String(150)) # 家裡電話
    number_of_periods = db.Column(db.String(255)) # 屆數/期數
    description = db.Column(db.Text()) # 備註 - 用於團長管理團員時的紀錄，而不是給團員看的
    state = db.Column(db.String(150)) # 狀態(0:正式、1:退團、2:休團)

# 三項登記
class MembershipRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) # 團員id
    registration_year = db.Column(db.String(150)) # 登記年份

# 階級(升團)
class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) # 團員id
    name = db.Column(db.String(255)) # 階級名稱(ex:童軍、行義、羅浮、服務員、團長等) - 需思考是否需要正規化
    promotion_date = db.Column(db.String(255)) # 升團日期(童軍的升團日期即加入日期)

# 進程考驗 - 團員可自己新增，不須經過管理員/團長審核
class Advancement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) # 團員id
    name = db.Column(db.String(255)) # 進程名稱(ex:初級、中級、高級、獅級、長城、國花、見習、授銜、服務) - 需思考是否需要正規化
    pass_date = db.Column(db.String(255)) # 通過日期
    file_path = db.Column(db.Text()) # 檔案路徑(證書/證明)

# 專科章 - 團員可自己新增，不須經過管理員/團長審核
class ProficiencyBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) # 團員id
    name = db.Column(db.String(255)) # 專科章名稱
    pass_date = db.Column(db.String(255)) # 通過日期
    file_path = db.Column(db.Text()) # 檔案路徑(證書/證明)

# 活動 - 純紀錄活動，不考慮服務時數
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text()) # 活動名稱
    start_date = db.Column(db.String(255)) # 開始日期
    end_date = db.Column(db.String(255)) # 結束日期
    location = db.Column(db.Text()) # 地點
    participants = db.Column(db.Text()) # 參加人員
    staffs = db.Column(db.Text()) # 服務人員
    file_path = db.Column(db.Text()) # 檔案路徑(活動企劃書檔案)
    description = db.Column(db.Text()) # 備註(例如:取消原因、活動內容、活動照片連結、活動相關資訊連結等)
    state = db.Column(db.String(150))   # 狀態(0:取消(停辦)、1:待舉辦、2:已舉辦)
    allowed = db.Column(db.String(150)) # 是否允許登入該活動(0:不允許、1:允許) - 意旨:若團員自己新增活動資料，則預設為不允許，需由管理員/團長審核後才能允許

# 服務 - 先以多人情況下的服務紀錄為主，未來再考慮特殊情況(例如:早退、中間請假、中間加入等)
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text()) # 服務名稱
    start_date = db.Column(db.String(255)) # 開始日期
    start_time = db.Column(db.String(255)) # 開始時間
    end_date = db.Column(db.String(255)) # 結束日期
    end_time = db.Column(db.String(255)) # 結束時間
    service_hours = db.Column(db.String(255)) # 服務時數
    location = db.Column(db.Text()) # 地點
    participants = db.Column(db.Text()) # 參加人員(意旨:參加服務的人員)
    description = db.Column(db.Text()) # 備註(例如:服務內容、服務照片連結、服務相關資訊連結等)
    file_path = db.Column(db.Text()) # 檔案路徑(服務紀錄檔案)
    allowed = db.Column(db.String(150)) # 是否允許登入該活動(0:不允許、1:允許) - 意旨:若團員自己新增活動資料，則預設為不允許，需由管理員/團長審核後才能允許

# 紀錄
class SystemRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 使用者id
    description = db.Column(db.Text()) # 紀錄操作內容
    record_date = db.Column(db.String(255)) # 紀錄日期
    record_time = db.Column(db.String(255)) # 紀錄時間

# 紀錄錯誤訊息 - 用於除錯，先創建以防未來有需要
class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text()) # 錯誤訊息
    error_date = db.Column(db.String(255)) # 錯誤日期
    error_time = db.Column(db.String(255)) # 錯誤時間
