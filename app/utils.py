from django.core.mail import send_mail
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import requests
import time
from django.contrib.auth.models import User
from .models import UserProfile

USER_DATABASE_FILENAME = 'usuarios.db'

urls = {
    "NR-1": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1",
    "NR-2": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-2-nr-2",
    "NR-3": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-3-nr-3",
    "NR-4": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-4-nr-4",
    "NR-5": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-5-nr-5",
    "NR-6": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-6-nr-6",
    "NR-7": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-7-nr-7",
    "NR-8": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-8-nr-8",
    "NR-9": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-9-nr-9",
    "NR-10": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10",
    "NR-11": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-11-nr-11",
    "NR-12": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-12-nr-12",
    "NR-13": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-13-nr-13",
    "NR-14": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-14-nr-14",
    "NR-15": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-15-nr-15",
    "NR-16": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-16-nr-16",
    "NR-17": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-17-nr-17",
    "NR-18": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-18-nr-18",
    "NR-19": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-19-nr-19",
    "NR-20": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-20-nr-20",
    "NR-21": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-21-nr-21",
    "NR-22": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-22-nr-22",
    "NR-23": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-23-nr-23",
    "NR-24": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-24-nr-24",
    "NR-25": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-25-nr-25",
    "NR-26": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-26-nr-26",
    "NR-27": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-27-nr-27",
    "NR-28": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-28-nr-28",
    "NR-29": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-29-nr-29",
    "NR-30": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-30-nr-30",
    "NR-31": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-31-nr-31",
    "NR-32": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-32-nr-32",
    "NR-33": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-33-nr-33",
    "NR-34": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-34-nr-34",
    "NR-35": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-35-nr-35",
    "NR-36": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-36-nr-36",
    "NR-37": "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/ctpp-nrs/norma-regulamentadora-no-37-nr-37",
    "NR-38": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-38-nr-38",
}


# Função para enviar email
def send_email(to_email, subject, message):
    try:
        validate_email(to_email)
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Acessando EMAIL_HOST_USER das configurações do Django
            [to_email],
            fail_silently=False,
            html_message=message,
        )
        print(f"Email enviado para {to_email}")
    except EmailNotValidError as e:
        print(f"Email inválido: {to_email}")
    except Exception as e:
        print(f"Erro ao enviar email para {to_email}: {e}")

def notify_users(sender, instance, **kwargs):
    arquivo = instance
    subject = f"Atualização do Arquivo: {arquivo.nome}"
    message = f"O arquivo {arquivo.nome} foi atualizado para a versão {arquivo.versao}."

    from .models import UserProfile
    # Lista para coletar todos os usuários a serem notificados
    users_to_notify = set()

    for opcao in instance.opcao:
        users = UserProfile.objects.filter(setor__icontains=opcao)
        users_to_notify.update(users)

    for user in users_to_notify:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.user.email],
            fail_silently=False,
        )
        
def notify_sems_users(sender, instance, **kwargs):
    arquivo = instance
    subject = f"Atualização do Arquivo: {arquivo.nome}"
    message = f"O arquivo {arquivo.nome} foi atualizado para a versão {arquivo.versao}."

    from .models import UserProfile
    users = UserProfile.objects.filter(setor__icontains="SESMT")

    for user in users:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.user.email],
            fail_silently=False,
        )


# Função para obter o conteúdo da página
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
        return None

# Função para extrair a data de modificação da página
def extract_update_time(content):
    soup = BeautifulSoup(content, 'html.parser')
    update_span = soup.select_one('span.documentModified > span.value')
    if update_span:
        date_str = update_span.text.strip().split(' ')[0]  # Extrai apenas a data
        return datetime.strptime(date_str, "%d/%m/%Y")
    else:
        return None

# Função para verificar atualizações
def check_for_updates(urls, last_checked_times):
    updates = []
    for nr, url in urls.items():
        content = get_page_content(url)
        if content:
            current_update_time = extract_update_time(content)
            if current_update_time and (nr not in last_checked_times or current_update_time > last_checked_times[nr]):
                updates.append((nr, current_update_time))
                last_checked_times[nr] = current_update_time
    return updates

def notify_updates(updates):
    for nr, update_time in updates:
        # Formatar a mensagem de notificação
        subject = f"Atualização da Norma Regulamentadora {nr}"
        message = f"A Norma Regulamentadora {nr} foi atualizada em {update_time.strftime('%d/%m/%Y')}."
        
        # Notificar usuários do setor SESMT
        notify_sems_users(nr, update_time.strftime('%d/%m/%Y'))

# Função principal para monitorar e notificar
def monitor_and_notify(urls, check_interval=3600):
    last_checked_times = {}
    
    while True:
        updates = check_for_updates(urls, last_checked_times)
        if updates:
            notify_updates(updates)
        
        # Aguardar o intervalo de tempo antes de verificar novamente
        time.sleep(check_interval)

if __name__ == "__main__":
    monitor_and_notify(urls)

# Função para notificar todos os usuários do SESMT
def notify_sems_users(file_title, new_version):
    notify_users(file_title, new_version, "SESMT")