from django.urls import path
from django.shortcuts import redirect, render
from .views import index, contato, arquivo, login_view, logout_view, usuario, upload_arquivo, download_arquivo, health_check
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserCreationForm

urlpatterns = [
    path('', index, name='index'),  # Certifique-se de que esta URL exista e tenha o nome 'index'
    path('contato/', contato, name='contato'),
    path('arquivo/', arquivo, name='arquivo'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('usuario/',usuario, name='usuario'),
    path('upload/', upload_arquivo, name='upload_arquivo'),
    path('download/<int:pk>/', download_arquivo, name='download_arquivo'),
    path('health/', health_check, name='health_check')
]

# Verifica se o usuário é superusuário
def is_superuser(user):
    return user.is_superuser

# Restrinja o acesso apenas a superusuários
@user_passes_test(is_superuser)
@login_required
def usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirecione para uma página de sua escolha após a criação do usuário
    else:
        form = UserCreationForm()
    return render(request, 'usuario.html', {'form': form})