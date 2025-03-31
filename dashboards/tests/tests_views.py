import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from dashboards.metrics import (
    get_daily_sales_data,
    get_daily_sales_quantity_data,
    get_graphic_product_brand_metric,
    get_graphic_product_category_metric,
    get_product_metrics,
    get_sales_metrics,
)
from inflows.models import Inflow
from outflows.models import Outflow
from products.models import Product
from suppliers.models import Supplier


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client = Client()

        self.category = Category.objects.create(name='Electronics')
        self.brand = Brand.objects.create(name='Brand A')
        self.supplier = Supplier.objects.create(name='TechLaser')

        self.product1 = Product.objects.create(
            title='Product 1',
            cost_price=100.0,
            selling_price=150.0,
            quantity=10,
            category=self.category,
            brand=self.brand,
        )
        self.product2 = Product.objects.create(
            title='Product 2',
            cost_price=200.0,
            selling_price=300.0,
            quantity=5,
            category=self.category,
            brand=self.brand,
        )

        Inflow.objects.create(
            product=self.product1, supplier=self.supplier, quantity=10
        )
        Inflow.objects.create(
            product=self.product2, supplier=self.supplier, quantity=5
        )
        Outflow.objects.create(product=self.product1, quantity=2)
        Outflow.objects.create(product=self.product2, quantity=1)

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.assertIn('product_metrics', response.context)
        self.assertIn('sales_metrics', response.context)
        self.assertIn('daily_sales_data', response.context)
        self.assertIn('daily_sales_quantity_data', response.context)
        self.assertIn('product_count_by_category', response.context)
        self.assertIn('product_count_by_brand', response.context)

        self.assertEqual(
            response.context['product_metrics'], get_product_metrics()
        )
        self.assertEqual(
            response.context['sales_metrics'], get_sales_metrics()
        )
        self.assertEqual(
            response.context['daily_sales_data'],
            json.dumps(get_daily_sales_data()),
        )
        self.assertEqual(
            response.context['daily_sales_quantity_data'],
            json.dumps(get_daily_sales_quantity_data()),
        )
        self.assertEqual(
            response.context['product_count_by_category'],
            json.dumps(get_graphic_product_category_metric()),
        )
        self.assertEqual(
            response.context['product_count_by_brand'],
            json.dumps(get_graphic_product_brand_metric()),
        )

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(
            response, f'{reverse("login")}?next={reverse("home")}'
        )
