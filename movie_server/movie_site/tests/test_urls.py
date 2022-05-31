from django.test import SimpleTestCase
from django.urls import reverse, resolve

# import the views that the urls should resolve to
from ..views import home_view, showings_view, purchase_view, register_request, jspractice


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home_view)

    def test_showings_url_resolves(self):
        url = reverse('showings', args=[1])
        self.assertEquals(resolve(url).func, showings_view)

    def test_purchase_url_resolves(self):
        url = reverse('purchase', args=[1])
        self.assertEquals(resolve(url).func, purchase_view)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_request)

    def test_jspractice_url_resolves(self):
        url = reverse('jspractice')
        self.assertEquals(resolve(url).func, jspractice)