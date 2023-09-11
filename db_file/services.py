from website.models import *

new_services = [
                Service(
                        name="service_name",
                        start_date="service_start_date",
                        end_date="service_end_date",
                        service_hours="service_hours",
                        location="service_location",
                        participants="['member_id', 'member_id', 'member_id', 'member_id', 'member_id']",
                        allowed="0"
                )
        ]