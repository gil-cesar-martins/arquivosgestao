from django.db import models
from stdimage.models import StdImageField
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save, pre_save 
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Arquivo(Base):
    OPCOES = sorted([
        ("EDITOR SESMT", "EDITOR SESMT"),
        ("RECRUTAMENTO", "RECRUTAMENTO"),
        ("ALMOXARIFADO", "ALMOXARIFADO"),
        ("OFICINA", "OFICINA"),
        ("CONTROLE", "CONTROLE"),
        ("CONSERVAÇÃO", "CONSERVAÇÃO"),
        ("SUPRIMENTOS", "SUPRIMENTOS"),
        ("FISCAL", "FISCAL"),
        ("MARKETING", "MARKETING"),
        ("COMERCIAL", "COMERCIAL"),
        ("SESMT", "SESMT"),
        ("COMPRAS", "COMPRAS"),
        ("FINANCEIRO", "FINANCEIRO"),
        ("ENGENHARIA", "ENGENHARIA"),
        ("CONTROLADORIA", "CONTROLADORIA"),
        ("DPOB", "DPOB"),
        ("DIREÇÃO", "DIREÇÃO"),
        ("DEPARTAMENTO PESSOAL", "DEPARTAMENTO PESSOAL"),
        ("OBRAS", "OBRAS"),
        ("QUALIDADE", "QUALIDADE"),
        ("TODOS", "TODOS"),
    ])
    
    TIPOS = [("Interno", "Interno"), ("Externo", "Externo")]
    
    nome = models.CharField('Arquivo', max_length=100)
    codigo = models.CharField('Codigo', max_length=100, default='000')
    versao = models.CharField('Versao', max_length=50, default='000')
    opcao = MultiSelectField('Opções', choices=OPCOES, max_length=300, default='000')
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)
    arquivopdf = models.FileField('Arquivo PDF', upload_to='pdfs/', null=True, blank=True)
    tipo = MultiSelectField('Tipo', choices=TIPOS, max_length=300, default='000')
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    disponivel_para_download = models.BooleanField(default=False)  # Novo campo
    tipo = models.CharField(max_length=50, choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('word', 'Word')], default='pdf')  # Novo campo para tipo de arquivo
    
    def __str__(self):
        return self.nome

def Arquivo_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.nome)

pre_save.connect(Arquivo_pre_save, sender=Arquivo)

def notify_users(arquivo):
    subject = f"Atualização do Arquivo: {arquivo.nome}"
    message = f"O arquivo {arquivo.nome} foi atualizado para a versão {arquivo.versao}."
    
    # Obter todos os usuários do setor correspondente
    from .models import UserProfile
    for opcao in arquivo.opcao:
        users = UserProfile.objects.filter(setor__icontains=opcao)
        for user in users:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.user.email],
                fail_silently=False,
            )

# Signal para notificar os usuários após salvar um novo arquivo ou atualizar um existente
def arquivo_post_save(sender, instance, created, **kwargs):
    if created:
        notify_users(instance)

post_save.connect(arquivo_post_save, sender=Arquivo)

class UserProfile(models.Model):
    OPCOES = sorted([
        ("EDITOR SESMT", "EDITOR SESMT"),
        ("RECRUTAMENTO", "RECRUTAMENTO"),
        ("ALMOXARIFADO", "ALMOXARIFADO"),
        ("OFICINA", "OFICINA"),
        ("CONTROLE", "CONTROLE"),
        ("CONSERVAÇÃO", "CONSERVAÇÃO"),
        ("SUPRIMENTOS", "SUPRIMENTOS"),
        ("FISCAL", "FISCAL"),
        ("MARKETING", "MARKETING"),
        ("COMERCIAL", "COMERCIAL"),
        ("SESMT", "SESMT"),
        ("COMPRAS", "COMPRAS"),
        ("FINANCEIRO", "FINANCEIRO"),
        ("ENGENHARIA", "ENGENHARIA"),
        ("CONTROLADORIA", "CONTROLADORIA"),
        ("DPOB", "DPOB"),
        ("DIREÇÃO", "DIREÇÃO"),
        ("DEPARTAMENTO PESSOAL", "DEPARTAMENTO PESSOAL"),
        ("OBRAS", "OBRAS"),
        ("QUALIDADE", "QUALIDADE"),
        ("TODOS", "TODOS"),
    ])
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    setor = MultiSelectField(choices=OPCOES, max_length=300, default='TODOS')

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)