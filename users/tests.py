from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
DADOS = {
    "username": "ana",
    "fname": "Ana",
    "lname": "Silva",
    "email": "ana@exemplo.com",
    "pass1": "SenhaForte123!",
    "pass2": "SenhaForte123!",
}


class CadastroTests(TestCase):

    def test_cadastro_cria_usuaria_ativa_e_vai_para_login(self):
        resposta = self.client.post(
            reverse("users:signup"),
            DADOS
        )

        self.assertRedirects(
            resposta,
            reverse("users:signin")
        )

        usuaria = User.objects.get(username="ana")
        self.assertTrue(usuaria.is_active)
        self.assertTrue(usuaria.check_password(DADOS["pass1"]))

    def test_email_repetido_nao_cria_conta(self):
        User.objects.create_user(
            username="bia",
            email="ana@exemplo.com",
            password="SenhaForte123!"
        )

        resposta = self.client.post(
            reverse("users:signup"),
            DADOS,
            follow=True
        )

        self.assertFalse(
            User.objects.filter(username="ana").exists()
        )
        self.assertContains(
            resposta,
            "Este e-mail já está cadastrado!"
        )

    def test_email_com_maiusculas_conta_como_repetido(self):
        User.objects.create_user(
            username="bia",
            email="ana@exemplo.com",
            password="SenhaForte123!"
        )

        dados = {
            **DADOS,
            "email": "Ana@Exemplo.com"
        }

        resposta = self.client.post(
            reverse("users:signup"),
            dados,
            follow=True
        )

        self.assertFalse(
            User.objects.filter(username="ana").exists()
        )
        self.assertContains(
            resposta,
            "Este e-mail já está cadastrado!"
        )

    def test_usuaria_cadastrada_consegue_entrar(self):
        self.client.post(
            reverse("users:signup"),
            DADOS
        )

        resposta = self.client.post(
            reverse("users:signin"),
            {
                "username": "ana",
                "pass1": "SenhaForte123!"
            }
        )

        self.assertRedirects(
            resposta,
            reverse("home"),
            fetch_redirect_response=False
        )

        usuaria = User.objects.get(username="ana")
        self.assertTrue(
            usuaria.is_authenticated
            if hasattr(usuaria, "is_authenticated")
            else usuaria.is_active
        )
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            usuaria.pk
        )
