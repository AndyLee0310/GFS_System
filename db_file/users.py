from website.models import *
from werkzeug.security import generate_password_hash

new_users = [
    User(
        id="0",
        email="user_email",
        password=generate_password_hash("member_password"),
        name="user_name",
        auth="3",
        state="1"
    ),
    User(
        email="user_email",
        password=generate_password_hash("member_password"),
        name="user_name",
        auth="2",
        state="1",
        member_id="user_linked_member_id"
    )
]