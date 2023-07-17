# Generated by Django 4.2.3 on 2023-07-14 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Accessories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=120, null=True)),
            ],
            options={
                "db_table": "accessories",
            },
        ),
        migrations.CreateModel(
            name="Inverters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=120, null=True)),
                ("marca", models.CharField(max_length=120, null=True)),
            ],
            options={
                "db_table": "inverters",
            },
        ),
        migrations.CreateModel(
            name="Modules",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("modelo_modulo", models.CharField(max_length=120)),
                ("potencia_wp_unitaria_modulo", models.FloatField()),
                ("overload_maximo", models.FloatField()),
                ("kwp", models.FloatField()),
                ("marca_modulo", models.CharField(max_length=120)),
            ],
            options={
                "db_table": "modules",
            },
        ),
        migrations.CreateModel(
            name="SolarKit",
            fields=[
                ("identificacao_kit", models.CharField(max_length=240, null=True)),
                (
                    "codigo",
                    models.CharField(
                        max_length=32, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("preco", models.FloatField(null=True)),
                ("telhado", models.CharField(max_length=48, null=True)),
                ("tipo_conexao", models.CharField(max_length=48, null=True)),
                ("quant_modulos", models.IntegerField(null=True)),
                ("quant_pares_conectores", models.IntegerField(null=True)),
                ("quant_stringbox", models.IntegerField(null=True)),
                (
                    "modulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.modules"
                    ),
                ),
                (
                    "par_conector",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="par_conector",
                        to="core.accessories",
                    ),
                ),
                (
                    "stringbox",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="stringbox",
                        to="core.accessories",
                    ),
                ),
            ],
            options={
                "db_table": "solar_kit",
            },
        ),
        migrations.CreateModel(
            name="SolarKitInverters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qtde_inversor", models.IntegerField()),
                (
                    "inversor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.inverters"
                    ),
                ),
                (
                    "solar_kit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.solarkit"
                    ),
                ),
            ],
            options={
                "db_table": "solar_kit_inverters",
            },
        ),
        migrations.CreateModel(
            name="SolarKitEstructures",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quant_estrutura", models.IntegerField()),
                (
                    "estrutura",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.accessories",
                    ),
                ),
                (
                    "solar_kit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.solarkit"
                    ),
                ),
            ],
            options={
                "db_table": "solar_kit_estructures",
            },
        ),
        migrations.CreateModel(
            name="SolarKitCables",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quant_cabo_em_m", models.FloatField()),
                (
                    "cabo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.accessories",
                    ),
                ),
                (
                    "solar_kit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.solarkit"
                    ),
                ),
            ],
            options={
                "db_table": "solar_kit_cables",
            },
        ),
    ]