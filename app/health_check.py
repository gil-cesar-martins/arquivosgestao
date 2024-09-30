from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError

def health_check(request):
    """
    View para verificação de integridade.
    """
    try:
        conn = connections['default']
        conn.cursor().execute("SELECT 1")
    except OperationalError:
        return HttpResponse("Erro na conexão com o banco de dados", status=500)

    # ... outras verificações que você queira adicionar ...

    return HttpResponse("OK")