from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
#
import os
from .ai_core.mcp_tools import connect_to_server
from django.utils import timezone
from .models import Chat, Conf
from asgiref.sync import sync_to_async
from django.contrib.sessions.backends.base import UpdateError
from django.contrib import auth
#from langchain_core.messages import HumanMessage, AIMessage


# Create your views here.
class ReactAgentView(View):
    """
    GET → displays the 'chatbot.html' page
    POST → receives the message, talks to the MCP, and returns the JSON
    """

    async def get(self, request):
        return render(request, 'chatbot.html')

    async def post(self, request):
        message = request.POST.get('message', '').strip()
        conf = await Conf.objects.aget(pk=1)
        path = conf.mcp_path
        model = conf.ollama_model
        try:
            response = await connect_to_server(message,path,model)
        except Exception as e:
            return JsonResponse({
                'message': message, 
                'response': f'Failed to use llm or MCP server: {e}',
            })

        if request.session.session_key is None:
            # Browser without cookies → creates everything from scratch
            await sync_to_async(request.session.create)()
        else:
            # Try to save; if the line has already been deleted, create it again.
            try:
                await sync_to_async(request.session.save)()
            except UpdateError:  # line disappeared (clearsessions)
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

class login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('path')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

class logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')
    
class pathconf(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'pathconf.html')
        else:
            return render(request, 'login.html')
    
    def post(self, request):
        mcp_path = request.POST['mcp-path']
        ollama_model = request.POST['ollama-model']

        if mcp_path != '' and ollama_model != '':
            conf = Conf.get_solo()
            conf.mcp_path = mcp_path
            conf.ollama_model = ollama_model
            conf.changed_at = timezone.now()
            conf.save()
            
            change_path = 'mcp-path/ollama-model changed'
            return render(request, 'pathconf.html', {'change_path': change_path})
        else:
            return render(request, 'pathconf.html')