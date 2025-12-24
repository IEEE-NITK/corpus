from django.test import Client
from django.test import TestCase,override_settings
from django.urls import reverse
from accounts.models import User
from accounts.models import ExecutiveMember
from virtual_expo.models import Report
from virtual_expo.models import ReportMember
from virtual_expo.models import ReportType
from virtual_expo.forms import ReportForm
from config.models import SIG
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from io import BytesIO
import tempfile
import shutil


# New class created as the Thumbnail required to be made needs to be deleted after tests
class MediaTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._temp_media = tempfile.mkdtemp()
        cls.override = override_settings(MEDIA_ROOT=cls._temp_media)
        cls.override.enable()


    @classmethod
    def tearDownClass(cls):
        cls.override.disable()
        shutil.rmtree(cls._temp_media, ignore_errors=True) # ignore_errors = True as tests might fail for wrong reasons
        super().tearDownClass()

def create_dummy_report(title, year, report_type, approved=False):
    return Report.objects.create(
        title=title,
        abstract="This is a dummy abstract.",
        thumbnail=SimpleUploadedFile(
            name="test_thumb.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        ),
        report_type=report_type,
        year=year,
        content="<p>Dummy content</p>",
        approved=approved,
        ready_for_approval=approved,
    )


class NotLoggedInUser(MediaTestCase):
    def setUp(self):
        self.client = Client()

        self.type_yearLong = ReportType.objects.create(name="Year Long")
        self.type_envision = ReportType.objects.create(name="Envision")


        self.sig1 = SIG.objects.create(name="Compsoc")
        self.sig2 = SIG.objects.create(name="Diode")
        self.sig3 = SIG.objects.create(name="Piston")


        self.report1 = create_dummy_report(
            title="AI Project",
            year=2024,
            report_type=self.type_envision,
            approved=True


        )


        self.report2 = create_dummy_report(
            title="Robotics Project",
            year=2024,
            report_type=self.type_yearLong,
            approved=True
        )


        self.report3 = create_dummy_report(
            title="Piston Project",
            year=2024,
            report_type=self.type_envision,
            approved=False
        )


        self.report4 = create_dummy_report(
            title="Another Piston 2",
            year=2023,
            report_type=self.type_yearLong,
            approved=True
        )


        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            phone_no="9876543210",
            gender="M",
            password="testuser@password",
        )


        self.exec = ExecutiveMember.objects.create(
            user=self.user,
            roll_number="000IT456",
            edu_email="test@nitk.edu.in",
            reg_number="123456",
            sig=self.sig1,
            minor_branch="SM",
            ieee_number="123",
            ieee_email="test@ieee.org",
            linkedin="https://linkedin.com/in/testuser",
            github="https://github.com/testuser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )
 
        ReportMember.objects.create(
            report=self.report1,
            member=self.exec
        )

    def test_virtual_expo_home_notLoggedIn(self):
        # the "Go to members dashboard" button is not present
        virtual_expo_home_path = reverse("virtual_expo_home")
        response = self.client.get(virtual_expo_home_path)
        years = list(Report.objects.values_list("year", flat=True).distinct())
        self.assertTemplateUsed(response,"virtual_expo/home.html")
        self.assertEqual(list(response.context["years"]),years)
        self.assertEqual(response.context["exec_member"],False)
        self.assertNotContains(response,"Go to Members Dashboard")
   
    def test_all_reports_visible_NotLoggedIn(self):
        virtual_expo_report_by_year_path = reverse("virtual_expo_reports_by_year",args=[2024])
        response = self.client.get(virtual_expo_report_by_year_path)
        self.assertTemplateUsed(response,"virtual_expo/reports_by_year.html")
        self.assertContains(response,self.report1.title)
        self.assertContains(response,self.report2.title)
        self.assertNotContains(response,self.report3.title) # not approved project report
        self.assertNotContains(response,self.report4.title) # of year 2023

    def test_reports_filter_by_report_type_notLoggedIn(self):
        # filtering the project reports by report type
        path = reverse("virtual_expo_reports_by_year", args=[2024])
        response = self.client.get(path, {
            "report_type": self.type_envision.id,
            "sig": 0
        })


        reports = response.context["reports"]
        for report in reports:
            self.assertEqual(report.report_type, self.type_envision)

    def test_reports_filter_by_sig_notLoggedIn(self):
        path = reverse("virtual_expo_reports_by_year", args=[2024])
        response = self.client.get(path, {
            "report_type": 0,
            "sig": self.sig1.id
        })


        self.assertEqual(response.status_code, 200)


        reports = response.context["reports"]
        self.assertTrue(reports.exists())


        for report in reports:
            self.assertIn(self.sig1, report.sigs())

    def test_report_visible_notLoggedIn(self):
        virtual_expo_report_path = reverse("virtual_expo_report",args=[self.report1.id])
        response = self.client.get(virtual_expo_report_path)
        self.assertTemplateUsed(response,"virtual_expo/report.html")
        self.assertContains(response,self.report1.title) # this is report 1
        self.assertNotContains(response,self.report2.title)
        self.assertNotContains(response,self.report4.title)
        self.assertNotContains(response,self.report3.title)

    def test_report_preview_notLoggedIn(self):
        # report preview can only be seen by logged in users
        preview_path = reverse("virtual_expo_preview_report",args=[self.report1.id])
        response = self.client.get(preview_path,follow=True)
        self.assertRedirects(response,"/")

    def test_dashboard_notLoggedIn(self):
        # members dashboard should not open for non-logged in users
        dashboard_path = reverse("virtual_expo_members_dashboard")
        response = self.client.get(dashboard_path,follow=True)
        self.assertRedirects(response,f"{reverse('accounts_signin')}?next={dashboard_path}")

    def test_new_report_notLoggedIn(self):
        # only memebrs can create reports
        new_report_path = reverse("virtual_expo_members_new_report")
        response = self.client.get(new_report_path,follow=True)
        self.assertRedirects(response,f"{reverse('accounts_signin')}?next={new_report_path}")

    def test_edit_report_notLoggedIn(self):
        # non-members cannot edit reports
        virtual_expo_members_edit_report_path = reverse("virtual_expo_members_edit_report",args=[self.report1.id])
        response = self.client.get(virtual_expo_members_edit_report_path,follow=True)
        self.assertRedirects(response,f"{reverse('accounts_signin')}?next={virtual_expo_members_edit_report_path}")

    def test_add_members_notLoggedIn(self):
        # non-members cannot add members to the reports
        add_members_path = reverse("virtual_expo_members_add_members",args=[self.report1.id])
        response = self.client.get(add_members_path,follow=True)
        self.assertRedirects(response,f"{reverse('accounts_signin')}?next={add_members_path}")

    def test_approver_dashboard_notLoggedIn(self):
        # non-members dont have access to approver-dashboard
        approver_dashboard_path = reverse("virtual_expo_members_approver_dashboard")
        response = self.client.get(approver_dashboard_path,follow=True)
        self.assertRedirects(response,f"{reverse('accounts_signin')}?next={approver_dashboard_path}")

class LoggedInNotExecUser(MediaTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            phone_no="9876543210",
            gender="M",
            password="testuser@password",
        )


        self.type_yearLong = ReportType.objects.create(name="Year Long")
        self.type_envision = ReportType.objects.create(name="Envision")


        # Create some SIGs + Exec Members (optional for filtering tests)
        self.sig2 = SIG.objects.create(name="Diode")
        self.sig3 = SIG.objects.create(name="Piston")

        self.report1 = create_dummy_report(
            title="AI Project",
            year=2024,
            report_type=self.type_envision,
            approved=True


        )
       
        self.report2 = create_dummy_report(
            title="Robotics Project",
            year=2024,
            report_type=self.type_yearLong,
            approved=True
        )

        self.report3 = create_dummy_report(
            title="Piston Project",
            year=2024,
            report_type=self.type_envision,
            approved=False
        )

        # check wether we can log in
        self.assertTrue(self.client.login(username=self.user.email, password="testuser@password"))

    def test_report_preview_LoggedIn_NotExec(self):
        # report preview can only be seen by logged in users
        preview_path = reverse("virtual_expo_preview_report",args=[self.report1.id])
        response = self.client.get(preview_path,follow=True)
        self.assertRedirects(response,"/")
   
    def test_dashboard_LoggedIn_NotExec(self):
        # members dashboard should not open for non-logged in users
        dashboard_path = reverse("virtual_expo_members_dashboard")
        response = self.client.get(dashboard_path,follow=True)
        self.assertRedirects(response,"/")

    def test_new_report_LoggedIn_NotExec(self):
        # only memebrs can create reports
        new_report_path = reverse("virtual_expo_members_new_report")
        response = self.client.get(new_report_path,follow=True)
        self.assertRedirects(response,"/")

    def test_edit_report_LoggedIn_notExec(self):
        # non-members cannot edit reports
        virtual_expo_members_edit_report_path = reverse("virtual_expo_members_edit_report",args=[self.report1.id])
        response = self.client.get(virtual_expo_members_edit_report_path,follow=True)
        self.assertRedirects(response,"/")

    def test_add_members_LoggedIn_notExec(self):
        # non-members cannot add members to the reports
        add_members_path = reverse("virtual_expo_members_edit_report",args=[self.report1.id])
        response = self.client.get(add_members_path,follow=True)
        self.assertRedirects(response,"/")

    def test_approver_dashboard_LoggedIn_notExec(self):
        # non-members dont have access to approver-dashboard
        approver_dashboard_path = reverse("virtual_expo_members_approver_dashboard")
        response = self.client.get(approver_dashboard_path,follow=True)
        self.assertRedirects(response,"/")

class ExecMemberTestCases(MediaTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            phone_no="9876543210",
            gender="M",
            password="testuser@password",
        )
        self.sig1 = SIG.objects.create(name="Compsoc")
        self.exec = ExecutiveMember.objects.create(
            user=self.user,
            roll_number="000IT456",
            edu_email="test@nitk.edu.in",
            reg_number="123456",
            sig=self.sig1,
            minor_branch="SM",
            ieee_number="123",
            ieee_email="test@ieee.org",
            linkedin="https://linkedin.com/in/testuser",
            github="https://github.com/testuser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )

        self.type_yearLong = ReportType.objects.create(name="Year Long")
        self.type_envision = ReportType.objects.create(name="Envision")

        # Create some SIGs + Exec Members (optional for filtering tests)
        self.sig2 = SIG.objects.create(name="Diode")
        self.sig3 = SIG.objects.create(name="Piston")

        self.report1 = create_dummy_report(
            title="AI Project",
            year=2024,
            report_type=self.type_envision,
            approved=True
        )

        self.report2 = create_dummy_report(
            title="Robotics Project",
            year=2024,
            report_type=self.type_yearLong,
            approved=False
        )

        self.report3 = create_dummy_report(
            title="Piston Project",
            year=2024,
            report_type=self.type_envision,
            approved=False
        )

        # user is member of report 2 and 1
        ReportMember.objects.create(
            report=self.report1,
            member=self.exec
        )
        
        ReportMember.objects.create(
            report=self.report2,
            member=self.exec
        )

        # report 3 has to be approved by current user
        self.report3.approver=self.exec
        self.report3.ready_for_approval=True
        self.report3.save()

        self.report4 = create_dummy_report(
            title="Another Piston 2",
            year=2023,
            report_type=self.type_yearLong,
            approved=True
        )
        
        self.assertTrue(self.client.login(username=self.user.email, password="testuser@password"))
   
    def test_edit_report_LoggedIn_ExecMember_POST_report_Approved(self):
        # user is member of report 1 AND it IS approved 
        edit_path = reverse("virtual_expo_members_edit_report",args=[self.report1.id])
        
        original_title = self.report1.title
        original_abstract = self.report1.abstract
        original_content = self.report1.content
        original_thumbnail = self.report1.thumbnail.name
        
        # Making test image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)


        new_thumbnail = SimpleUploadedFile(
            "new_thumbnail.jpg",
            image_io.read(),
            content_type="image/jpeg"
        )

        # POST data dictionary for edit form
        post_data = {
            "title": "AI Project UPDATED",
            "abstract": "Updated abstract",
            "report_type": self.type_envision.id,
            "year": 2024,
            "content": "Updated content",
            "thumbnail": new_thumbnail,
        }


        response = self.client.post(
            edit_path,
            post_data,
            follow=True
        )

        self.assertRedirects(response,reverse("virtual_expo_members_dashboard"))

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "This report is already approved.")

        self.report1.refresh_from_db()

        self.assertEqual(self.report1.title, original_title)
        self.assertEqual(self.report1.abstract, original_abstract)
        self.assertEqual(self.report1.content, original_content)
        self.assertEqual(self.report1.thumbnail.name, original_thumbnail)

        reports_by_year = reverse(
            "virtual_expo_reports_by_year",
            args=[2024]
        )
        response1 = self.client.get(reports_by_year)
        self.assertNotContains(response1, "AI Project UPDATED")
   
    def test_edit_report_LoggedIn_ExecMember_POST_report_notApproved(self):
        # user is member of report 2 AND it is not approved 
        edit_path = reverse("virtual_expo_members_edit_report",args=[self.report2.id])
        
        # Making test image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)


        new_thumbnail = SimpleUploadedFile(
            "new_thumbnail.jpg",
            image_io.read(),
            content_type="image/jpeg"
        )

        # POST data dictionary for edit form
        post_data = {
            "title": "AI Project UPDATED",
            "abstract": "Updated abstract",
            "report_type": self.type_envision.id,
            "year": 2024,
            "content": "Updated content",
            "thumbnail": new_thumbnail,
        }


        response = self.client.post(
            edit_path,
            post_data,
            follow=True
        )

        self.assertRedirects(response,reverse("virtual_expo_members_dashboard"))

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Report updated successfully!")

        self.report2.refresh_from_db()

        self.assertEqual(self.report2.title, post_data["title"])
        self.assertEqual(self.report2.abstract, post_data["abstract"])
        self.assertEqual(self.report2.content, post_data["content"])

    def test_virtual_expo_home_LoggedIn_ExecMember(self):
        virtual_expo_home_path = reverse("virtual_expo_home")
        response = self.client.get(virtual_expo_home_path)
        years = list(Report.objects.values_list("year", flat=True).distinct())
        self.assertTemplateUsed(response,"virtual_expo/home.html")
        self.assertEqual(list(response.context["years"]),years)
        self.assertEqual(response.context["exec_member"],True)
        self.assertContains(response,"Go to Members Dashboard")

    def test_report_preview_LoggedIn_ExecMember_ReportMember(self):
        edit_page = reverse("virtual_expo_members_edit_report",args=[self.report1.id])
        preview_path = reverse("virtual_expo_preview_report",args=[self.report1.id])
        response = self.client.get(preview_path,HTTP_REFERER=edit_page,follow=True)
        self.assertTemplateUsed(response,"virtual_expo/report.html")
        self.assertContains(response,"Preview Mode")
        self.assertContains(response,f'href="{edit_page}"',html=False)

    def test_report_preview_LoggedIn_ExecMember_NotReportMember(self):
        edit_page = reverse("virtual_expo_members_edit_report",args=[self.report2.id])
        preview_path = reverse("virtual_expo_preview_report",args=[self.report2.id])
        response = self.client.get(preview_path,follow=True)
        self.assertTemplateUsed(response,"virtual_expo/report.html")
        self.assertContains(response,"Preview Mode")
        self.assertNotContains(response,f'href="{edit_page}"',html=False)

    def test_dashboard_LoggedIn_ExecMember(self):
        dashboard_path = reverse("virtual_expo_members_dashboard")
        response = self.client.get(dashboard_path)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"virtual_expo/members/dashboard.html")
        self.assertContains(response,self.report1.title)
        self.assertContains(response,self.report2.title)

    def test_new_report_LoggedIn_ExecMember_GET(self):
        # checking if the new report page was rendered or not
        new_report_path = reverse("virtual_expo_members_new_report")
       
        response = self.client.get(new_report_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"virtual_expo/members/new_report.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"],ReportForm)

    def test_new_report_LoggedIn_POST(self):
        new_report_path = reverse("virtual_expo_members_new_report")

        # crating the dummy thmbnail
        image_io = io.BytesIO()
        image = Image.new("RGB", (10, 10), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        thumbnail = SimpleUploadedFile(
            "test.jpg",
            image_io.read(),
            content_type="image/jpeg"
        )

        post_data = {
            "title": "Test Report",
            "abstract": "Test abstract",
            "report_type": self.type_envision.id,
            "year": 2025,
            "content": "Test content",
            "thumbnail": thumbnail,
        }

        response = self.client.post(new_report_path, post_data, follow=True)

        self.assertRedirects(
            response,
            reverse("virtual_expo_members_dashboard")
        )

        report = Report.objects.get(title="Test Report")

        self.assertIsNotNone(report.created_at)

        self.assertTrue(
            ReportMember.objects.filter(
                report=report,
                member=self.exec
            ).exists()
        )

        self.assertTrue(report.thumbnail.name.endswith(".jpg"))

    def test_edit_report_LoggedIn_ExecMember_GET(self):
        virtual_expo_members_edit_report_path = reverse("virtual_expo_members_edit_report",args=[self.report2.id])
        response = self.client.get(virtual_expo_members_edit_report_path,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"virtual_expo/members/edit_report.html")
        self.assertContains(response,self.report2.title)

    def test_add_members_LoggedIn_ExecMember_GET(self):
        # seeing if the add members page is rendered on request
        add_members_path = reverse("virtual_expo_members_add_members",args=[self.report1.id])
        response = self.client.get(add_members_path,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"virtual_expo/members/add_members.html")

    def test_add_members_LoggedIn_POST(self):
        # Creating new usr to be added into project
        user2 = User.objects.create_user(
            first_name="Second",
            last_name="User",
            email="second@gmail.com",
            phone_no="9999999999",
            gender="M",
            password="password123",
        )

        exec2 = ExecutiveMember.objects.create(
            user=user2,
            roll_number="000IT999",
            edu_email="second@nitk.edu.in",
            reg_number="999999",
            sig=self.sig2,
            minor_branch="CS",
            ieee_number="999",
            ieee_email="second@ieee.org",
            linkedin="https://linkedin.com/in/second",
            github="https://github.com/second",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )

        add_members_path = reverse("virtual_expo_members_add_members",args=[self.report1.id],)
        post_data = {"add": "1", "member": exec2.pk}

        response = self.client.post(
            add_members_path,
            post_data,
            follow=True
        )

        self.assertRedirects(
            response,
            add_members_path
        )


        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Member added to project.")


        self.assertTrue(
            ReportMember.objects.filter(
                report=self.report1,
                member=exec2
            ).exists()
        )
   
    def test_add_members_edit_LoggedIn_ExecMember_POST(self):
        user2 = User.objects.create_user(
            first_name="Second",
            last_name="User",
            email="seconduser@gmail.com",
            phone_no="9999999999",
            gender="M",
            password="secondpassword",
        )


        exec2 = ExecutiveMember.objects.create(
            user=user2,
            roll_number="000IT999",
            edu_email="second@nitk.edu.in",
            reg_number="999999",
            sig=self.sig2,
            minor_branch="EE",
            ieee_number="999",
            ieee_email="second@ieee.org",
            linkedin="https://linkedin.com/in/seconduser",
            github="https://github.com/seconduser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )

        ReportMember.objects.create(report=self.report1,member=exec2)

        self.assertTrue(ReportMember.objects.filter(report=self.report1, member=exec2).exists())

        add_members_path = reverse("virtual_expo_members_add_members",args=[self.report1.id])

        response = self.client.post(
            add_members_path,
            {
                "edit": "1",
                "report_id": self.report1.pk,
                "member_id": exec2.pk,
            },
            follow=True
        )

        self.assertRedirects(response, add_members_path)

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Members edited in project.")

        self.assertFalse(
            ReportMember.objects.filter(report=self.report1, member=exec2).exists()
        )

    def test_add_members_cannot_remove_self_LoggedIn_ExecMember_POST(self):
        add_members_path = reverse(
            "virtual_expo_members_add_members",
            args=[self.report1.id]
        )

        response = self.client.post(
            add_members_path,
            {
                "edit": "1",
                "report_id": self.report1.pk,
                "member_id": self.exec.pk,
            },
            follow=True
        )

        self.assertRedirects(response, add_members_path)
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]),
            "You cannot remove yourself from the project."
        )
        self.assertTrue(
            ReportMember.objects.filter(
                report=self.report1,
                member=self.exec
            ).exists()
        )

    def test_approver_dashboard_LoggedIn_ExecMember_GET(self):
        approver_dashboard_path = reverse("virtual_expo_members_approver_dashboard")
        response = self.client.get(approver_dashboard_path,follow=True)
        self.assertTemplateUsed(response,"virtual_expo/members/approver_dashboard.html")
        self.assertContains(response,self.report3.title)
        self.assertEqual(response.status_code,200)

    def test_approver_dashboard_LoggedIn_POST(self):
        approver_dashboard_path = reverse("virtual_expo_members_approver_dashboard")
        response = self.client.post(
            approver_dashboard_path,
            {
                "report_id": self.report3.pk
            },
            follow=True
        )

        self.assertRedirects(response, approver_dashboard_path)

        self.report3.refresh_from_db()

        self.assertTrue(self.report3.approved)
        self.assertIsNotNone(self.report3.approved_at)

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]),"Report marked as approved!")

        self.assertTemplateUsed(response,"virtual_expo/members/approver_dashboard.html")
        self.assertEqual(response.status_code, 200)