import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from accounts.models import User, Faculty
from config.models import SIG, Society  # adjust imports if needed

class Command(BaseCommand):
    help = "Create 10 faculty User and Faculty model instances with dummy data."

    def handle(self, *args, **kwargs):
        sigs = list(SIG.objects.all())
        societies = list(Society.objects.all())

        if not sigs:
            self.stdout.write(
                self.style.ERROR("Please ensure SIGs and Posts exist before running.")
            )
            return
        
        today = date.today()
        created = 0

        for i in range(1, 11):
            first_name = f"Faculty{i}"
            last_name = "Test"
            email = f"faculty{i}@example.com"
            phone_no = f"80000{i:05d}"
            gender = random.choice(["M", "F"])

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_no=phone_no,
                gender=gender,
                password="securepassword"
            )

            sig = random.choice(sigs)
            society = random.choice(societies) if societies else None

            # Each faculty gets valid website/linkedin and a term (2 years)
            Faculty.objects.create(
                user=user,
                sig=sig,
                society=society,
                website=f"https://faculty{i}.example.com",
                linkedin=f"https://linkedin.com/in/faculty{i}",
                term_start=today - timedelta(days=365),
                term_end=today + timedelta(days=365),
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Faculty {user.email} created."))

        self.stdout.write(self.style.SUCCESS(f"Created {created} faculty members."))
