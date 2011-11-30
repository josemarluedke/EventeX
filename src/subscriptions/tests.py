from django.test import TestCase
from django.core.urlresolvers import reverse
from subscriptions.models import Subscription
from subscriptions.forms import SubscriptionForm

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.subscription = Subscription.objects.create(
            name="Josemar Luedke",
            cpf="12345678901",
            email="josemarluedke@gmail.com",
            phone="51-00000000"
        )
    
    def test_insert_subscription(self):
        self.assertTrue(self.subscription.pk)

    def test_update_subscription(self):
        self.subscription.name = "Josemar Davi Luedke"
        self.subscription.save()
        self.assertNotEqual(Subscription.DoesNotExist, Subscription.objects.get(name="Josemar Davi Luedke"))

    def test_delete_subscription(self):
        oldPk = self.subscription.pk
        self.subscription.delete()
        self.assertRaises(Subscription.DoesNotExist, Subscription.objects.get, pk=oldPk)



class SubscriptionFormTest(TestCase):
    def test_insert_subscription_form(self):
        form = SubscriptionForm({
            'name': 'Josemar Davi Luedke',
            'cpf': '12345678901',
            'email': 'josemarluedke@mail.com',
            'phone': '51-00000000'
        })
        self.assertTrue(form.is_valid())

    def test_insert_subscription_with_empty_name(self):
        form = SubscriptionForm({
            'name': '',
            'cpf': '12345678901',
            'email': 'josemarluedke@mail.com',
            'phone': '51-00000000'
        })
        self.assertFalse(form.is_valid())

    def test_insert_subscription_with_empty_cpf(self):
        form = SubscriptionForm({
            'name': 'Josemar Davi Luedke',
            'cpf': '',
            'email': 'josemarluedke@mail.com',
            'phone': '51-00000000'
        })
        self.assertFalse(form.is_valid())

    def test_insert_subscription_with_empty_email(self):
        form = SubscriptionForm({
            'name': 'Josemar Davi Luedke',
            'cpf': '12345678901',
            'email': '',
            'phone': '51-00000000'
        })
        self.assertFalse(form.is_valid())

    def test_insert_subscription_with_invalid_email(self):
        form = SubscriptionForm({
            'name': 'Josemar Davi Luedke',
            'cpf': '12345678901',
            'email': 'fulano.castro.mail.com',
            'phone': '51-00000000'
        })
        self.assertFalse(form.is_valid())

    def test_insert_subscription_with_empty_phone(self):
        form = SubscriptionForm({
            'name': 'Josemar Davi Luedke',
            'cpf': '12345678901',
            'email': 'josemarluedke@mail.com',
            'phone': ''
        })
        self.assertTrue(form.is_valid())



class SubscriptionsUrlsTest(TestCase):
    
    def test_url_subscribe(self):
        response = self.client.get(reverse('subscriptions:subscribe'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'subscriptions/new.html')

    def test_url_success(self):
        self.subscription = Subscription.objects.create(
            name="Josemar Luedke",
            cpf="12345678901",
            email="josemarluedke@gmail.com",
            phone="51-00000000"
        )
        
        response = self.client.get(reverse('subscriptions:success', args=[self.subscription.pk]))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'subscriptions/success.html')
        
    def test_url_success_404(self):
        response = self.client.get(reverse('subscriptions:success', args=[1]))
        self.assertEquals(404, response.status_code)
        self.assertTemplateUsed(response, '404.html')
