
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'users/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = (request.POST.get('email') or '').strip()
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "As senhas não conferem!")
            return redirect('users:signup')

        try:
            validate_password(pass1)
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)
            return redirect('users:signup')

        # Verifica usuário existente
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Este nome de usuário já está em uso!'
            )
            return redirect('users:signup')

        # Verifica e-mail existente, ignorando maiúsculas e minúsculas
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                'Este e-mail já está cadastrado!'
            )
            return redirect('users:signup')

        # Cria a conta já ativa
        myuser = User.objects.create_user(
            username=username,
            email=email,
            password=pass1,
            is_active=True
        )

        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(
            request,
            'Sua conta foi criada com sucesso! Faça login para continuar.'
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
        messages.success(
            request,
            'Você saiu da sua conta. Esperamos vê-lo novamente em breve!'
        )
        return redirect('users:index')

    return redirect('home')
