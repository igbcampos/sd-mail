from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import requests
import os

base_url = os.environ.get('BASE_URL')

def token_valido(request):
    auth_token = request.session.get('auth_token')
    response = requests.get(base_url+'/me', headers={"x-access-tokens": auth_token})

    if 'message' in response.json().keys() and response.json()['message'] == 'token is invalid':
        return False

    return True

def is_authenticated(request):
    user = {}
    
    user['auth_token'] = request.session.get('auth_token')
    user['name'] = request.session.get('name')
    user['email'] = request.session.get('email')

    return user

class Login(View):
    def get(self, request):
        print(base_url)
        if is_authenticated(request)['auth_token']:
            return redirect('/')
        else:
            return render(request, 'core/login.html', {})
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = requests.post(base_url+'/login', auth=(email, password))

        if response.status_code == 200:
            request.session['auth_token'] = response.json()['token']

            response = requests.get(base_url+'/me', headers={"x-access-tokens": response.json()['token']})

            request.session['name'] = response.json()['name']
            request.session['email'] = response.json()['email']

            return redirect('/')
        else:
            contexto = {'email': email, 'mensagem': 'Usuário ou senha inválidos. Por favor, tente novamente.'}
            return render(request, 'core/login.html', contexto)

class Register(View):
    def get(self, request):
        if is_authenticated(request)['auth_token']:
            return redirect('/')
        else:
            return render(request, 'core/register.html', {})
    
    def post(self, request):
        contexto = {
            'name':  request.POST.get('name'),
            'email':  request.POST.get('email'),
            'password':  request.POST.get('password'),
        }
        
        response = requests.post(base_url+'/register', json=contexto)
        response = response.json()

        if response['message'] == 'registered successfully':
            messages.success(request, 'Usuário registrado com sucesso.')
            return redirect('/login')
        elif response['message'] == 'email address not available':
            contexto['mensagem'] = 'Endereço de e-mail não disponível. Por favor, tente outro.'
            return render(request, 'core/register.html', contexto)
        else:
            contexto['mensagem'] = 'Não foi possível fazer o seu registro. Por favor, tente novamente.'
            return render(request, 'core/register.html', contexto)

def logout(request):
    if is_authenticated(request)['auth_token']:
        del request.session['auth_token']
        del request.session['name']
        del request.session['email']
    
    return redirect('/')

def emails_received(request):
    user = is_authenticated(request)

    if user['auth_token'] and token_valido(request):
        response = requests.get(base_url+'/emails/received', headers={"x-access-tokens": user['auth_token']})
        
        return render(request, 'core/emails_received.html', {'user': user, 'emails': response.json()})
    else:
        return redirect('/login')

def send_email(request):
    user = is_authenticated(request)

    if user['auth_token'] and token_valido(request):
        email = {
            "receiver": request.POST.get('receiver'), 
            "subject": request.POST.get('subject'), 
            "body": request.POST.get('body')
        }

        response = requests.post(base_url+'/emails', json=email, headers={"x-access-tokens": user['auth_token']})
        response = response.json()
    
        if response['message'] == 'receiver not found':
            messages.error(request, 'Destinatário não encontrado.')
        elif response['message'] == 'email sent':
            messages.success(request, 'E-mail enviado com sucesso.')
        else:
            messages.error(request, 'O e-mail não foi enviado. Por favor, tente novamente.')

        return redirect('/')
    else:
        return redirect('/login')

def emails_sent(request):
    user = is_authenticated(request)

    if user['auth_token'] and token_valido(request):
        response = requests.get(base_url+'/emails/sent', headers={"x-access-tokens": user['auth_token']})

        print(response.json())

        return render(request, 'core/emails_sent.html', {'user': user, 'emails': response.json()})
    else:
        return redirect('/login')

def delete(request):
    user = is_authenticated(request)
    id = request.GET.get('id')
    source = request.GET.get('source')

    if user['auth_token'] and token_valido(request):
        response = requests.delete(base_url+'/emails/delete?id={}&source={}'.format(id, source), headers={"x-access-tokens": user['auth_token']})
        
        response = response.json()

        if response['message'] == 'email successfully deleted':
            messages.success(request, 'E-mail deletado com sucesso.')
        else:
            messages.error(request, 'O e-mail não foi deletado. Por favor, tente novamente')

        return redirect('/')
    else:
        return redirect('/login')
    
def reply_email(request):
    user = is_authenticated(request)

    if user['auth_token'] and token_valido(request):
        email = {
            "email_id": request.POST.get('email_id'), 
            "body": request.POST.get('body')
        }

        response = requests.post(base_url+'/emails/reply', json=email, headers={"x-access-tokens": user['auth_token']})
        response = response.json()
    
        if response['message'] == 'email not found':
            messages.error(request, 'E-mail não encontrado.')
        elif response['message'] == 'email replied':
            messages.success(request, 'E-mail respondido com sucesso.')
        else:
            messages.error(request, 'O e-mail não foi respondido. Por favor, tente novamente.')

        return redirect('/')
    else:
        return redirect('/login')

def forward_email(request):
    user = is_authenticated(request)

    if user['auth_token'] and token_valido(request):
        email = {
            "receiver": request.POST.get('receiver'), 
            "email_id": request.POST.get('email_id')
        }

        response = requests.post(base_url+'/emails/forward', json=email, headers={"x-access-tokens": user['auth_token']})
        response = response.json()
    
        if response['message'] == 'receiver not found':
            messages.error(request, 'Destinatário não encontrado.')
        elif response['message'] == 'email forwarded':
            messages.success(request, 'E-mail encaminhado com sucesso.')
        else:
            messages.error(request, 'O e-mail não foi encaminhado. Por favor, tente novamente.')

        return redirect('/')
    else:
        return redirect('/login')