import os
import fitz  # PyMuPDF
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ContatoForm, ArquivoModelForm
from .models import Arquivo
from .utils import notify_users, notify_sems_users  # Certifique-se de importar as funções corretas
from .forms import UserCreationForm
from django.http import HttpResponse, Http404
import mimetypes

@login_required(login_url='login')
def index(request):
    search_query = request.GET.get('search', '')

    # Carrega todos os arquivos, independentemente do setor
    arquivos = Arquivo.objects.order_by('nome')

    if search_query:
        arquivos = arquivos.filter(codigo__icontains=search_query.lower())

    context = {
        'arquivos': arquivos,
        'search_query': search_query,
    }
    return render(request, 'index.html', context)

@login_required
def contato(request):
    form = ContatoForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')
    context = {'form': form}
    return render(request, 'contato.html', context)

@login_required(login_url='login')
def arquivo(request):
    if request.method == 'POST':
        form = ArquivoModelForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save()
            messages.success(request, 'Arquivo salvo com sucesso.')

            # Envio de notificações
            notify_users(arquivo)

            return redirect('index')  # Redireciona para a página index após o sucesso
        else:
            messages.error(request, 'Erro ao salvar Arquivo.')
    else:
        form = ArquivoModelForm()
    
    context = {'form': form}
    return render(request, 'arquivo.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@staff_member_required
def usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'usuario.html', {'form': form})

def upload_arquivo(request):
    if request.method == 'POST':
        form = ArquivoModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Ou qualquer outra URL desejada
    else:
        form = ArquivoModelForm()
    return render(request, 'upload.html', {'form': form})

def download_arquivo(request, pk):
    arquivo = get_object_or_404(Arquivo, pk=pk)
    file_path = arquivo.arquivopdf.path
    file_extension = arquivo.arquivopdf.url.split('.')[-1]  # Obtém a extensão do arquivo
    file_name = f"{arquivo.nome}.{file_extension}"  # Adiciona um ponto antes da extensão

    mime_type, _ = mimetypes.guess_type(file_path)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except FileNotFoundError:
        raise Http404("Arquivo não encontrado.")