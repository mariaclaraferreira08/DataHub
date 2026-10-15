from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "categorias/",
        views.categoria_lista,
        name="categoria_lista",
    ),
    path(
        "categorias/nova/",
        views.categoria_criar,
        name="categoria_criar",
    ),
    path(
        "categorias/<int:id>/editar/",
        views.categoria_editar,
        name="categoria_editar",
    ),
    path(
        "categorias/<int:id>/excluir/",
        views.categoria_excluir,
        name="categoria_excluir",
    ),

    path(
        "datasets/",
        views.dataset_lista,
        name="dataset_lista",
    ),
    path(
        "datasets/novo/",
        views.dataset_criar,
        name="dataset_criar",
    ),
    path(
        "datasets/<int:id>/editar/",
        views.dataset_editar,
        name="dataset_editar",
    ),
    path(
        "datasets/<int:id>/excluir/",
        views.dataset_excluir,
        name="dataset_excluir",
    ),
]