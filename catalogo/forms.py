from django import forms

from .models import Categoria, Dataset


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            "nome",
            "descricao",
        ]

        labels = {
            "nome": "Nome",
            "descricao": "Descrição",
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome da categoria",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descrição da categoria",
                }
            ),
        }


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = [
            "nome",
            "descricao",
            "formato",
            "origem",
            "categoria",
            "data_atualizacao",
            "arquivo",
        ]

        labels = {
            "nome": "Nome",
            "descricao": "Descrição",
            "formato": "Formato",
            "origem": "Origem",
            "categoria": "Categoria",
            "data_atualizacao": "Data de atualização",
            "arquivo": "Arquivo",
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome do dataset",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descrição do dataset",
                }
            ),
            "formato": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "origem": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Origem dos dados",
                }
            ),
            "categoria": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "data_atualizacao": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "arquivo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        formato = cleaned_data.get("formato")
        arquivo = cleaned_data.get("arquivo")

        if not arquivo:
            return cleaned_data

        nome_arquivo = arquivo.name.lower()

        extensoes_permitidas = {
            "CSV": [".csv"],
            "JSON": [".json"],
            "XLSX": [".xlsx"],
            "XLS": [".xls"],
            "SQL": [".sql"],
            "TXT": [".txt"],
            "XML": [".xml"],
            "PARQUET": [".parquet"],
            "AVRO": [".avro"],
            "TSV": [".tsv"],
            "YAML": [".yaml", ".yml"],
        }

        if formato == "OUTRO":
            return cleaned_data

        extensoes_validas = extensoes_permitidas.get(formato, [])

        arquivo_valido = any(
            nome_arquivo.endswith(extensao)
            for extensao in extensoes_validas
        )

        if not arquivo_valido:
            raise forms.ValidationError(
                f"O arquivo enviado não corresponde ao formato "
                f"selecionado ({formato})."
            )

        return cleaned_data