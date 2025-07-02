from django.shortcuts import render
from django.http import JsonResponse
#
#import asyncio
from .app.mcp_tools import connect_to_server
from langchain_core.messages import HumanMessage, AIMessage


# Create your views here.


async def chatbot(request):
    if request.method == 'POST':
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

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html')
