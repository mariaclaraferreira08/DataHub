from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Dataset(models.Model):
    FORMATOS = [
        ("CSV", "CSV"),
        ("JSON", "JSON"),
        ("XLSX", "Excel (.xlsx)"),
        ("XLS", "Excel (.xls)"),
        ("SQL", "SQL"),
        ("TXT", "Texto (.txt)"),
        ("XML", "XML"),
        ("PARQUET", "Parquet"),
        ("AVRO", "Avro"),
        ("TSV", "TSV"),
        ("YAML", "YAML"),
        ("OUTRO", "Outro"),
    ]

    nome = models.CharField(max_length=150)

    descricao = models.TextField(
        blank=True
    )

    formato = models.CharField(
        max_length=20,
        choices=FORMATOS,
    )

    origem = models.CharField(
        max_length=150
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="datasets",
    )

    data_atualizacao = models.DateField(
        null=True,
        blank=True,
    )

    arquivo = models.FileField(
        upload_to="datasets/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nome