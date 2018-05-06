# from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User

# from rest_framework.test import APITestCase
# from rest_framework import status
# from rest_framework.authtoken.models import Token

# from user_profiles.models import Client


# class TokenCreationTest(APITestCase):
#     """ Unit test suite to test that the API authorization token is created succesfully
#         and working appropiately.
#     """
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='iupicker', first_name='Simon',
#             last_name='Nomon', email='simon@nomon.com',
#             password='iu_pass_test')
#         self.user_no_group = User.objects.create_user(
#             username='iupicker_false', first_name='Simon2',
#             last_name='Nomon2', email='simon2@nomon.com',
#             password='iu_pass_test_false')
#         self.cliente = Client.objects.create(user=self.user)
#         self.url = reverse('tosp_auth:reset_auth_token')

#     def test_return_authentication_token(self):
#         """ Test that a user with the client group can get its token
#             Test that a client can send a post request with a users credentials and
#             the API will return the user Token for the client to use in further requests.
#         """
#         data = {'username': 'iupicker', 'password': 'iu_pass_test'}
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(Token.objects.all()), 1)

#     def test_incorrect_authentication_credentials(self):
#         """ Test that an existing user can not authenticate with invalid credentials.
#             Test that when a client tries to authenticate a user with invalid credentials
#             he does not recieve a token ang get a 400 http response.
#         """
#         data = {'username': 'iupicker', 'password': 'invalid_password'}
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_incorrect_group_authentication(self):
#         """ Test only certain user groups can authenticate via API
#             Test that other users who have valid credentials but are not
#             part of the Client group can't obtain a Token.
#         """
#         data = {'username': 'iupicker_false', 'password': 'iu_pass_test_false'}
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
