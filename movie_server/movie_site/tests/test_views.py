# will use the django Client to test views... can also use Django Test Factory
from django.test import TestCase, Client
from django.urls import reverse
from ticket_handler.models import Movie, Showing, Ticket
import json


class TestViews(TestCase):

    def setUp(self):
        self.movie = Movie()
        self.movie.title = "I am a title"
        self.movie.image = "http://i-am-a-test-image.com"
        self.movie.runtime_hrs = 2
        self.movie.runtime_mins = 30
        self.movie.rating = "None"
        self.movie.save()

        self.showing = Showing()
        self.showing.date = "2022-05-17"
        self.showing.time = "06:00"
        self.showing.ticket_price = 10.00
        self.showing.seats_available = 10
        self.showing.seats_total = 10
        self.showing.movie = self.movie
        self.showing.save()

        # create a client object
        self.client = Client()
        # get urls for url names
        self.home_url = reverse('home')
        self.showings_url = reverse('showings', args=[self.movie.id])
        self.purchase_url = reverse('purchase', args=[self.showing.id])
        self.register_url = reverse('register')
        self.jspractice_url = reverse('jspractice')

    def test_project_home_GET(self):
        # have client send a get request to the url, save as response
        response = self.client.get(self.home_url)

        # ASSERTIONS
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_project_showings_GET(self):
        response = self.client.get(self.showings_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'showings.html')

    def test_project_purchase_GET(self):
        response = self.client.get(self.purchase_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchase.html')

    def test_project_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_project_jspractice_GET(self):
        response = self.client.get(self.jspractice_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jspractice.html')

    # def test_project_detail_POST_adds_new_expense(self):
    #     # Create a category to post to
    #     Category.objects.create(
    #         project=self.project1,
    #         name='development'
    #     )
    #
    #     # send a POST request to the url with expense parameters
    #     response = self.client.post(self.detail_url, {
    #         'title': 'expense1',
    #         'amount': 1000,
    #         'category': 'development
    #     })
    #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(self.project1.expenses.first(), 'expense1')
    #
    # # check POST request without data
    # def test_project_detail_POST_no_data(self):
    #     response = self.client.post(self.detail_url)
    #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(self.project1.expenses.count(), 0)
    #
    # def test_project_detail_DELETE_deletes_expense(self):
    #     category1 = Category.objects.create(
    #         project=self.project1,
    #         name='development'
    #     )
    #
    #     Expense.objects.create(
    #         project=self.project1,
    #         title='expense1',
    #         amount=1000,
    #         category=category1
    #     )
    #
    #     response = self.client.delete(self.detail_url, json.dumps({
    #         'id': 1
    #     }))
    #
    #     self.assertEquals(response.status_code, 204)
    #     self.assertEquals(self.project1.expenses.count(), 0)
    #
    # def test_project_detail_DELETE_no_id(self):
    #     category1 = Category.objects.create(
    #         project=self.project1,
    #         name='development'
    #     )
    #
    #     Expense.objects.create(
    #         project=self.project1,
    #         title='expense1',
    #         amount=1000,
    #         category=category1
    #     )
    #
    #     # make DELETE request w/o an ID
    #     response = self.client.delete(self.detail_url)
    #
    #     self.assertEquals(response.status_code, 404)
    #     self.assertEquals(self.project1.expenses.count(), 1)
    #
    # def test_project_create_POST(self):
    #     # get the url fo 'add'
    #     url = reverse('add')
    #     # send POST request to 'add' with params to create new project
    #     response = self.client.post(url, {
    #         'name': 'project2',
    #         'budget': 10000,
    #         'categoriesString': 'design, development'
    #     })
    #
    #     # get the new project from the db
    #     project2 = Project.objects.get(id=2)
    #     self.asserEquals(project2.name, 'project2')
    #
    #     # POST request also created 2 new categories - test if they were created -
    #
    #     first_category = Category.objects.get(id=1)
    #     self.assertEquals = (first_category.project, project2)
    #     self.assertEquals = (first_category.name, 'design')
    #
    #     second_category = Category, objects.get(id=2)
    #     self.assertEquals = (second_category.project, project2)
    #     self.assertEquals = (second_category.name, 'development')
