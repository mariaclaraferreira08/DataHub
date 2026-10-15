from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import Categoria, Dataset
from .forms import CategoriaForm, DatasetForm


# =====================================================
# HOME
# =====================================================

def home(request):
    quantidade_categorias = Categoria.objects.count()
    quantidade_datasets = Dataset.objects.count()

    datasets_recentes = Dataset.objects.order_by("-id")[:5]

    contexto = {
        "quantidade_categorias": quantidade_categorias,
        "quantidade_datasets": quantidade_datasets,
        "datasets_recentes": datasets_recentes,
    }

    return render(
        request,
        "catalogo/home.html",
        contexto,
    )


# =====================================================
# CATEGORIAS
# =====================================================

def categoria_lista(request):
    categorias = Categoria.objects.all().order_by("nome")

    return render(
        request,
        "catalogo/categorias/lista.html",
        {
            "categorias": categorias,
        },
    )


def categoria_criar(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("categoria_lista")

    else:
        form = CategoriaForm()

    return render(
        request,
        "catalogo/categorias/formulario.html",
        {
            "form": form,
            "titulo": "Nova Categoria",
        },
    )


def categoria_editar(request, id):
    categoria = get_object_or_404(
        Categoria,
        id=id,
    )

    if request.method == "POST":
        form = CategoriaForm(
            request.POST,
            instance=categoria,
        )

        if form.is_valid():
            form.save()
            return redirect("categoria_lista")

    else:
        form = CategoriaForm(
            instance=categoria
        )

    return render(
        request,
        "catalogo/categorias/formulario.html",
        {
            "form": form,
            "titulo": "Editar Categoria",
        },
    )


def categoria_excluir(request, id):
    categoria = get_object_or_404(
        Categoria,
        id=id,
    )

    if request.method == "POST":
        categoria.delete()
        return redirect("categoria_lista")

    return render(
        request,
        "catalogo/categorias/excluir.html",
        {
            "categoria": categoria,
        },
    )


# =====================================================
# DATASETS
# =====================================================

def dataset_lista(request):
    datasets = Dataset.objects.select_related(
        "categoria"
    ).all()

    busca = request.GET.get(
        "busca",
        ""
    ).strip()

    categoria = request.GET.get(
        "categoria",
        ""
    )

    formato = request.GET.get(
        "formato",
        ""
    )

    if busca:
        datasets = datasets.filter(
            nome__icontains=busca
        )

    if categoria:
        datasets = datasets.filter(
            categoria_id=categoria
        )

    if formato:
        datasets = datasets.filter(
            formato=formato
        )

    datasets = datasets.order_by("nome")

    categorias = Categoria.objects.all().order_by(
        "nome"
    )

    contexto = {
        "datasets": datasets,
        "categorias": categorias,
        "formatos": Dataset.FORMATOS,

        "busca": busca,
        "categoria_selecionada": categoria,
        "formato_selecionado": formato,
    }

    return render(
        request,
        "catalogo/datasets/lista.html",
        contexto,
    )


def dataset_criar(request):
    if request.method == "POST":
        form = DatasetForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()
            return redirect("dataset_lista")

    else:
        form = DatasetForm()

    return render(
        request,
        "catalogo/datasets/formulario.html",
        {
            "form": form,
            "titulo": "Novo Dataset",
        },
    )


def dataset_editar(request, id):
    dataset = get_object_or_404(
        Dataset,
        id=id,
    )

    if request.method == "POST":
        form = DatasetForm(
            request.POST,
            request.FILES,
            instance=dataset,
        )

        if form.is_valid():
            form.save()
            return redirect("dataset_lista")

    else:
        form = DatasetForm(
            instance=dataset
        )

    return render(
        request,
        "catalogo/datasets/formulario.html",
        {
            "form": form,
            "titulo": "Editar Dataset",
            "dataset": dataset,
        },
    )


def dataset_excluir(request, id):
    dataset = get_object_or_404(
        Dataset,
        id=id,
    )

    if request.method == "POST":
        dataset.delete()
        return redirect("dataset_lista")

    return render(
        request,
        "catalogo/datasets/excluir.html",
        {
            "dataset": dataset,
        },
    )