from django import forms
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from .models import Arquivo, UserProfile

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    assunto = forms.CharField(label='Assunto', max_length=120)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject='E-mail enviado pelo sistema django2',
            body=conteudo,
            from_email='contato@seudominio.com.br',
            to=['contato@seudominio.com.br',],
            headers={'Reply-To': email}
        )
        mail.send()


class ArquivoModelForm(forms.ModelForm):

    class Meta:
        model = Arquivo
        fields = ['nome', 'codigo', 'versao', 'arquivopdf', 'opcao', 'disponivel_para_download', 'tipo']


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    sorted_opcoes = sorted(UserProfile.OPCOES, key=lambda x: x[1])

    setor = forms.MultipleChoiceField(
        choices=sorted_opcoes,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Verifica se o perfil já existe
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.setor = self.cleaned_data['setor']
            profile.save()
        return user
