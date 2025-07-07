from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
#
from .app.mcp_tools import connect_to_server
from django.utils import timezone
from .models import Chat
from asgiref.sync import sync_to_async
from django.contrib.sessions.backends.base import UpdateError
#from langchain_core.messages import HumanMessage, AIMessage


# Create your views here.
class ReactAgentView(View):
    """
    GET  → exibe a página 'chatbot.html'
    POST → recebe a mensagem, fala com o MCP e devolve o JSON
    """

    async def get(self, request):
        return render(request, 'chatbot.html')

    async def post(self, request):
        message = request.POST.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'mensagem vazia'}, status=400)

        try:
            response = await connect_to_server(message)
        except Exception as e:
            return JsonResponse(
                {'error': f'Falha ao falar com MCP: {e}'},
                status=502
            )

        if request.session.session_key is None:
            # Navegador sem cookie → cria tudo do zero
            await sync_to_async(request.session.create)()
        else:
            # Tenta salvar; se a linha já foi apagada, cria de novo
            try:
                await sync_to_async(request.session.save)()
            except UpdateError:  # linha sumiu (clearsessions)
                await sync_to_async(request.session.create)()

        await Chat.objects.acreate(
            session_id=request.session.session_key,
            message=message,
            response=response,
            created_at=timezone.now()
        )
        
        return JsonResponse({
            'message': message, 
            'response': response,
        })
