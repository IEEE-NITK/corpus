import json

from accounts.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "to migrate authors from the json file to the User model"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the json file")

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        with open(json_file, "r") as file:
            data = json.load(file)

            counter = 0
            for item in data.values():
                phone_num = counter + 9999999000
                new_user = User(
                    email=item["email"],
                    phone_no=phone_num,
                    gender="N",
                )
                new_user.save()
                # name_arr = item['name'].split()
                # first_name = name_arr[0]
                # last_name = name_arr[-1]
                # user = User.objects.get(email=item['email'])
                # user.first_name = first_name
                # user.last_name =  last_name
                # user.save()
                counter = counter + 1
                print(f"user number={counter} created")
