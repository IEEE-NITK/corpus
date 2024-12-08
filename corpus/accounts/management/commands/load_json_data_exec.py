import json

from accounts.models import ExecutiveMember
from accounts.models import User
from config.models import SIG
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "to migrate authors from the json file to the ExecutiveMember model"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the json file")

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        with open(json_file, "r") as file:
            data = json.load(file)

            counter = 0
            for item in data.values():
                edu_email = "noemail" + str(counter) + "@nitk.edu.in"
                roll_number = "111GG" + str(counter)
                reg_number = "1111" + str(counter)
                model_sig = SIG.objects.all()[0]
                user_model_obj = User.objects.get(email=item["email"])
                new_user = ExecutiveMember(
                    sig=model_sig,
                    user=user_model_obj,
                    edu_email=edu_email,
                    roll_number=roll_number,
                    reg_number=reg_number,
                )
                new_user.save()
                counter = counter + 1
                print(f"user number {counter} with email created")
