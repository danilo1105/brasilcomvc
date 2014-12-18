from django.test import TestCase

from ..context_processors import social_auth_facebook_key


class SocialAuthFacebookKeyTest(TestCase):

    def test_context_processor(self):

        with self.settings(SOCIAL_AUTH_FACEBOOK_KEY='le-key'):
            context = social_auth_facebook_key(None)
            self.assertIn('SOCIAL_AUTH_FACEBOOK_KEY', context)
            self.assertEqual(context['SOCIAL_AUTH_FACEBOOK_KEY'], 'le-key')
