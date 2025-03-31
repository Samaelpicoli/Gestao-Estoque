from django.db.models.signals import post_save
from django.dispatch import receiver

from outflows.models import Outflow


@receiver(post_save, sender=Outflow)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Atualiza a quantidade do produto associado quando uma nova saída é criada.

    Este signal é acionado após a criação de uma nova instância do modelo
    Outflow. Se a instância foi criada e sua quantidade é maior que zero,
    a quantidade do produto associado é decrementada pela quantidade
    da nova saída e o produto é salvo.

    Args:
        sender (Model): O modelo que enviou o sinal.
        instance (Outflow): A instância do modelo Outflow que foi criada.
        created (bool): Indica se a instância foi criada (True)
        ou atualizada (False).
        **kwargs: Argumentos adicionais passados para o signal.
    """
    if created:
        if instance.quantity > 0:
            product = instance.product
            product.quantity -= instance.quantity
            product.save()
