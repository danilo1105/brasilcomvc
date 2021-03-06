from django.contrib.auth import get_user_model
from django.core import mail

from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.test import TestCase

from brasilcomvc.common.views import LoginRequiredMixin

from ..models import Project
from ..views import ProjectApply, ProjectList
from . import ProjectTestMixin


User = get_user_model()


class ProjectListTestCase(TestCase):

    url = reverse('projects:project_list')

    def test_page_opens_successfully(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_list.html')

    def test_check_random_order(self):
        p1 = Project.objects.create(name='project-1', owner=User.objects.create(email='p1@domain.net'))
        p2 = Project.objects.create(name='project-2', owner=User.objects.create(email='p2@domain.net'))

        qs_ids_1 = ProjectList().get_queryset().values_list('id', flat=True)
        qs_ids_2 = ProjectList().get_queryset().values_list('id', flat=True)
        self.assertNotEquals(qs_ids_1, qs_ids_2)



class ProjectDetailsTestCase(ProjectTestMixin, TestCase):

    def setUp(self):
        super(ProjectDetailsTestCase, self).setUp()
        self.url = self.project.get_absolute_url()

    def test_page_opens_successfully(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_details.html')


class ProjectApplyTestCase(ProjectTestMixin, TestCase):

    def setUp(self):
        super(ProjectApplyTestCase, self).setUp()
        self.volunteer = User.objects.create_user(
            'volunteer@example.com', '123', full_name='John Doe')
        self.url = reverse(
            'projects:project_apply', kwargs={'slug': self.project.slug})

    def test_inherits_login_required_mixin(self):
        self.assertTrue(issubclass(ProjectApply, LoginRequiredMixin))

    def test_template_used(self):
        self.client.login(username=self.volunteer.email, password='123')
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, 'projects/project_apply.html')
        self.assertContains(resp, self.project.name)

    def test_volunteer_is_able_to_apply(self):
        self.client.login(username=self.volunteer.email, password='123')
        message = 'wat'
        resp = self.client.post(self.url, {'message': message})
        self.assertRedirects(resp, self.project.get_absolute_url())
        self.assertTrue(self.project.applications.exists())

        # Check emails
        emails_sent = {email.to[0]: email for email in mail.outbox}
        self.assertEqual(
            set(emails_sent),
            set([self.volunteer.email, self.project.owner.email]))
        owner_email = emails_sent[self.project.owner.email]
        self.assertIn(self.volunteer.get_short_name(), owner_email.body)
        self.assertIn(message, owner_email.body)
        volunteer_email = emails_sent[self.volunteer.email]
        self.assertIn(self.project.name, volunteer_email.body)

    def test_volunteer_cant_apply_twice(self):
        self.client.login(username=self.volunteer.email, password='123')
        self.project.applications.create(volunteer=self.volunteer, message='')
        resp = self.client.post(self.url, {'message': 'wat'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.project.applications.count(), 1)
        self.assertFalse(mail.outbox)

    def test_owner_cant_apply(self):
        self.client.login(username=self.project.owner.email, password='123')
        resp = self.client.post(self.url, {'message': 'y u so mad'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(self.project.applications.exists())
        self.assertFalse(mail.outbox)


class ProjectSearchViewTestCase(ProjectTestMixin, TestCase):

    def setUp(self):
        super(ProjectSearchViewTestCase, self).setUp()
        self.sp = Point(x=-46.6333093, y=-23.5505199, srid=4326)
        self.rj = Point(x=-43.1970773, y=-22.9082998, srid=4326)

        # Set a default latlng to the created project
        self.project.latlng = self.sp
        self.project.save()

    def test_search_within_default_range(self):
        resp = self.client.get(reverse('projects:project_search'), data={
            'q': 'some place',
            'lat': self.sp.y,
            'lng': self.sp.x
        })
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(list(resp.context_data['projects']), [self.project])

    def test_search_within_specified_range(self):
        resp = self.client.get(reverse('projects:project_search'), data={
            'q': 'some place',
            'lat': self.rj.y,
            'lng': self.rj.x,
            'radius': 10000,
        })
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(list(resp.context_data['projects']), [self.project])

    def test_search_out_of_range(self):
        self.project.latlng = self.rj
        self.project.save()

        resp = self.client.get(reverse('projects:project_search'), data={
            'q': 'some place',
            'lat': self.sp.y,
            'lng': self.sp.x,
        })
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(list(resp.context_data['projects']), [])

    def test_search_without_params(self):
        resp = self.client.get(reverse('projects:project_search'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(list(resp.context_data['projects']), [])
        self.assertIsNotNone(resp.context_data['form'].errors.get('q'))
        self.assertIsNotNone(resp.context_data['form'].errors.get('lat'))
        self.assertIsNotNone(resp.context_data['form'].errors.get('lng'))
