from app import app
import unittest


class FlaskTestCasae(unittest.TestCase):

    # Test must begin with test
    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertTrue(b'You were just logged in!' in response.data)

    # Ensure login behaves correctly given the incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="wrong"),
            follow_redirects=True
        )
        self.assertTrue(b'Invalid credentials. Please try again.'
                        in response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You were just logged out!' in response.data)

    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first' in response.data)

    # Ensure that the logout page requires a user to be logged in.
    def test_logout_route_requires_loggin(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure that posts show up on the main page.
    def test_post_show_up(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertTrue(b"User says" in response.data)

if __name__ == '__main__':
    unittest.main()
