from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

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


class TestsMetrics(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.client.login(username='testuser', password='12345')
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

        self.inflow1 = Inflow.objects.create(
            supplier=self.supplier,
            product=self.product1,
            quantity=10,
            created_at=timezone.now(),
        )
        self.inflow2 = Inflow.objects.create(
            supplier=self.supplier,
            product=self.product2,
            quantity=5,
            created_at=timezone.now(),
        )

        self.outflow1 = Outflow.objects.create(
            product=self.product1, quantity=2, created_at=timezone.now()
        )
        self.outflow2 = Outflow.objects.create(
            product=self.product2, quantity=1, created_at=timezone.now()
        )

    def test_get_product_metrics(self):
        metrics = get_product_metrics()
        self.assertEqual(metrics['total_cost_price'], '3.600,00')
        self.assertEqual(metrics['total_selling_price'], '5.400,00')
        self.assertEqual(metrics['total_quantity'], 27)
        self.assertEqual(metrics['total_profit'], '1.800,00')

    def test_get_sales_metrics(self):
        metrics = get_sales_metrics()
        self.assertEqual(metrics['total_sales'], 2)
        self.assertEqual(metrics['total_products_sold'], 3)
        self.assertEqual(metrics['total_sales_value'], '600,00')
        self.assertEqual(metrics['total_sales_profit'], '200,00')

    def test_get_daily_sales_data(self):
        data = get_daily_sales_data()
        today = timezone.now().date()
        self.assertIn(str(today), data['dates'])
        self.assertEqual(len(data['values']), 7)

    def test_get_daily_sales_quantity_data(self):
        data = get_daily_sales_quantity_data()
        today = timezone.now().date()
        self.assertIn(str(today), data['dates'])
        self.assertEqual(len(data['values']), 7)

    def test_get_graphic_product_category_metric(self):
        metrics = get_graphic_product_category_metric()
        self.assertEqual(metrics[self.category.name], 2)

    def test_get_graphic_product_brand_metric(self):
        metrics = get_graphic_product_brand_metric()
        self.assertEqual(metrics[self.brand.name], 2)
