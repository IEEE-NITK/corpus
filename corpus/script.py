import os
import django
from faker import Faker
import random
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corpus.settings")
django.setup()

from accounts.models import ExecutiveMember, User
from config.models import SIG
from virtual_expo.models import Report, ReportType, ReportMember
from blog.models import Post, Tag

fake = Faker()

def clear_all_data():
    print("Clearing all existing data...")
    ReportMember.objects.all().delete()
    Report.objects.all().delete()
    ReportType.objects.all().delete()
    ExecutiveMember.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    SIG.objects.all().delete()
    Post.objects.all().delete()
    Tag.objects.all().delete()
    print("All data cleared successfully!")

def generate_fake_data_virtualExpo():
    print("\nCreating SIGs...")
    sig_names = ["CompSoc", "Diode", "Piston","Inter-SIG"]
    sigs = []
    for name in sig_names:
        sig = SIG.objects.create(name=name)
        sigs.append(sig)
        print(f"Created SIG: {name}")

    print("\nCreating Executive Members...")
    for i in range(10):
        email = fake.email()
        user = User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            phone_no=f"{''.join(random.choices('0123456789', k=10))}",
            gender=random.choice(['M', 'F'])
        )
        
        roll_num = f"21{random.choice(['CS', 'EC', 'EE'])}{str(i+1).zfill(3)}"
        reg_num = f"21{random.choice(['CS', 'EC', 'EE'])}0{str(i+1).zfill(2)}"
        
        member = ExecutiveMember.objects.create(
            user=user,
            sig=random.choice(sigs),
            edu_email=f"{roll_num.lower()}@nitk.edu.in",
            roll_number=roll_num,
            reg_number=reg_num,
            minor_branch=random.choice([dept[0] for dept in ExecutiveMember.NITK_DEPARTMENTS]),
            ieee_number=f"{''.join(random.choices('0123456789', k=8))}",
            ieee_email=f"{user.first_name.lower()}.ieee@ieee.org",
            linkedin=f"https://linkedin.com/in/{user.first_name.lower()}-{user.last_name.lower()}",
            github=f"{user.first_name.lower()}{user.last_name.lower()}",
            is_nep=random.choice([True, False]),
            date_joined=timezone.now()
        )
        print(f"Created ExecutiveMember: {member}")

    print("\nCreating Report Types...")
    report_type_names = [
        "Research Paper", "Project Report", "Technical Article", 
        "Case Study", "Tutorial", "Workshop Summary",
        "Experiment Results", "Innovation Brief"
    ]
    for name in report_type_names:
        report_type = ReportType.objects.create(name=name)
        print(f"Created ReportType: {report_type.name}")

    print("\nCreating Reports...")
    technical_terms = ["AI", "Machine Learning", "IoT", "Blockchain", "Cloud Computing", 
                      "Neural Networks", "Data Analysis", "Robotics", "Cybersecurity",
                      "Edge Computing", "5G", "Quantum Computing"]
    
    for _ in range(30):
        created_at = timezone.now() - timezone.timedelta(days=random.randint(0, 1825))
        approved_at = created_at + timezone.timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None
        
        title = f"{random.choice(technical_terms)}: {fake.sentence(nb_words=5)}"
        
        report = Report.objects.create(
            title=title,
            abstract=fake.paragraph(nb_sentences=random.randint(10, 15)),
            thumbnail="https://cdn.britannica.com/70/234870-050-D4D024BB/Orange-colored-cat-yawns-displaying-teeth.jpg",
            report_type=random.choice(ReportType.objects.all()),
            year=2024,
            content="\n\n".join([fake.paragraph(nb_sentences=8) for _ in range(5)]),
            ready_for_approval=random.choice([True, False]),
            approved=random.choice([True, False]),
            created_at=created_at,
            approved_at=approved_at,
        )
        print(f"Created Report: {report.title}")

        members = random.sample(list(ExecutiveMember.objects.all()), k=random.randint(2, 3))
        for member in members:
            report_member = ReportMember.objects.create(report=report, member=member)
            print(f"Created ReportMember: {report_member}")
            
def generate_fake_data_blog():
    print("\nCreating Tags...")
    tag_names = ["CompSoc", "Diode", "Piston"]
    tags = []
    
    for name in tag_names:
        tag = Tag.objects.create(tag_name=name)
        tags.append(tag)
        print(f"Created Tag: {tag.tag_name}")

    print("\nCreating Posts...")
    
    executive_members = ExecutiveMember.objects.all()
    
    for _ in range(20):
        title = fake.sentence(nb_words=6)
        description = fake.sentence(nb_words=10)
        slug = fake.slug()
        text = fake.paragraph(nb_sentences=25)
        
        author = random.choice(executive_members)
        
        post = Post.objects.create(
            title=title,
            description=description,
            slug=slug,
            text=text,
            author=author,
            author_github=f"https://github.com/{fake.user_name()}",
            created_date=timezone.now(),
            published_date=timezone.now() - timezone.timedelta(days=random.randint(0, 30)),
        )
        print(f"Created Post: {post.title}")
        
        assigned_tags = random.sample(tags, random.randint(1, 3))
        post.blog_tag.set(assigned_tags)
        post.save()

if __name__ == "__main__":
    clear_all_data()
    generate_fake_data_virtualExpo()
    generate_fake_data_blog()