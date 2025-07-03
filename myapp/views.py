from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
#
from .app.mcp_tools import connect_to_server
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

        return JsonResponse({
            'message': message, 
            'response': response,
        })
