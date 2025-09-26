import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, ExecutiveMember
from config.models import SIG


class Command(BaseCommand):
    help = "Create dummy Users and ExecutiveMembers with even gender/SIG distribution."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of dummy members to create (default=50)",
        )

    def handle(self, *args, **options):
        sigs = list(SIG.objects.all())
        if not sigs:
            self.stdout.write(
                self.style.ERROR("⚠️ No SIGs found. Please create SIGs first.")
            )
            return

        departments = [dept[0] for dept in ExecutiveMember.NITK_DEPARTMENTS]
        reg_prefixes = ['221', '231', '241']

        total_members = options["count"]
        sig_count = len(sigs)

        for i in range(1, total_members + 1):
            # Alternate gender between M/F
            prefix = random.choice(reg_prefixes)
            dept_code = random.choice(departments)
            unique_suffix = f"{i:03d}"
            reg_number = f"{prefix}{dept_code}{unique_suffix}"
            gender = "M" if i % 2 == 1 else "F"

            # Round-robin SIG assignment
            sig = sigs[(i - 1) % sig_count]

            # ---- Create USER ----
            first_name = f"User{i}"
            last_name = "Test"
            email = f"user{i}@example.com"
            phone_no = f"900000{i:04d}"

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_no=phone_no,
                gender=gender,
                password="password123",
            )

            # ---- OPTIONAL FIELDS (hide + GitHub/LinkedIn) ----
            hide_github = random.choice([True, False])
            hide_linkedin = random.choice([True, False])

            github_username = None if hide_github else f"githubuser{i}"
            linkedin_url = (
                None if hide_linkedin else f"https://www.linkedin.com/in/user{i}"
            )

            # ---- Create ExecutiveMember ----
            ExecutiveMember.objects.create(
                user=user,
                sig=sig,
                edu_email=f"user{i}@nitk.edu.in",
                roll_number=f"21{i:04d}",
                reg_number=reg_number,
                minor_branch=random.choice(departments),
                ieee_number=f"IEEE{i:05d}",
                ieee_email=f"ieee{i}@ieee.org",
                github=github_username,
                linkedin=linkedin_url,
                hide_github=hide_github,
                hide_linkedin=hide_linkedin,
                is_nep=random.choice([True, False]),
                date_joined=timezone.now(),
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Created {user.first_name} {user.last_name} ({gender}) "
                    f"in SIG [{sig.name}] | GitHub Hidden? {hide_github} | LinkedIn Hidden? {hide_linkedin}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Successfully created {total_members} dummy users and executive members!"
            )
        )
