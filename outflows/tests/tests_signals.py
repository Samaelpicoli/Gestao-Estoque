from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from outflows.signals import update_product_quantity
from products.models import Product
from suppliers.models import Supplier


class TestsSignalsOutflow(TestCase):
    """Testes para o signal que atualiza a quantidade do produto"""

    def setUp(self):
        """Configuração inicial para os testes de signals."""
        self.brand = Brand.objects.create(name='Microsoft')
        self.category = Category.objects.create(name='Mouse')
        self.product = Product.objects.create(
            title='Mouse Sem Fio',
            brand=self.brand,
            category=self.category,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        self.supplier = Supplier.objects.create(name='Ivan')
        Inflow.objects.create(
            supplier=self.supplier,
            product=self.product,
            quantity=10,
        )

    def test_signal_functionality_directly(self):
        """Testa a funcionalidade do signal diretamente."""
        product = self.product
        initial_quantity = product.quantity

        outflow = Outflow(product=product, quantity=5)
        update_product_quantity(Outflow, outflow, created=True)

        product.refresh_from_db()
        self.assertEqual(product.quantity, initial_quantity - 5)
