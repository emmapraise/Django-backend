from .test_setup import TestSetUp

class TestViews(TestSetUp):

    def test_user_can_register(self):
        res = self.client.post(self.register_url)
        res.status_code == 400