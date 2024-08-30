from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Arquivo
from .utils import notify_users, notify_sems_users


@receiver(post_save, sender=Arquivo)
def enviar_notificacao_arquivo(sender, instance, created, **kwargs):
    # Notifica os usuários dos setores especificados na opção
    for opcao in instance.opcao:
        notify_users(sender, instance, opcao=opcao, **kwargs)

    # Notifica os usuários do setor SESMT, se necessário
    if "SESMT" in instance.opcao:
        notify_sems_users(sender, instance, **kwargs)