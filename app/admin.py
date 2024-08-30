from django.contrib import admin

from .models import Arquivo

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

admin.site.site_header = "GESTÃO DE ARQUIVOS"
admin.site.site_title = "GESTÃO DE ARQUIVOS"
admin.site.index_title = "Bem-vindo ao sistema de gestão de arquivos"

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'versao', 'opcao', 'slug', 'criado', 'modificado', 'ativo','tipo', 'disponivel_para_download')
    list_editable = ('disponivel_para_download','tipo')
    search_fields = ('nome', 'codigo', 'versao')
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'user'
    fields = ['setor']

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_setor')
    list_select_related = ('userprofile',)
    inlines = (UserProfileInline,)

    def get_setor(self, instance):
        return ', '.join(instance.userprofile.setor)
    get_setor.short_description = 'Setor'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Se o usuário é novo
            UserProfile.objects.get_or_create(user=obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)