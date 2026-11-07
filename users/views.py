from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "As senhas não conferem!")
            return render(request, 'users/signup.html')

        try:
            validate_password(pass1)
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)
            return redirect('users:signup')

        # Verifica usuário existente
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso!')
            return redirect('users:signup')

        # Verifica email existente
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado!')
            return redirect('users:signup')

        myuser = User.objects.create_user(username=username, email=email, password=pass1, is_active = False)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        # messages.success(request, 'Sua conta foi criada com sucesso!')
        messages.info(request, 'Conta criada! Verifique seu email para ativar sua conta.')

        # Gerar identificador e token de ativação
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = default_token_generator.make_token(myuser)

        # Montar o link completo de ativação
        activation_link = request.build_absolute_uri(
            reverse('users:activate', kwargs = {'uidb64': uid, 'token': token}))

        # Preparar o e-mail
        subject = 'Ative sua conta no DataHub'

        message = f"""
        Olá, {myuser.first_name}!
        Sua conta no DataHub foi criada.
        Para ativar sua conta, acesse o link abaixo:
        {activation_link}

        Se você não realizou esse cadastro, ignore este e-mail.
        """

        # Enviar e-mail
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [myuser.email],
            fail_silently=False
        )

        return redirect('users:signin')
    return render(request, 'users/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        # Autenticar usuário
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha incorretos.")
            return redirect('users:signin')

    return render(request, 'users/signin.html')

def signout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Você saiu da sua conta. Esperamos vê-lo novamente em breve!')
        return redirect('users:index')

    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Ativar a conta
        user.is_active = True
        user.save(update_fields=['is_active'])

        # Autenticar o usuário
        login(request, user)
        messages.success(
            request,
            'E-mail verificado! Sua conta está ativa. Bem-vindo ao DataHub!')
        return redirect('home')

    messages.error(request, 'O link de verificação é inválido ou expirou.')
    return redirect('users:signin')