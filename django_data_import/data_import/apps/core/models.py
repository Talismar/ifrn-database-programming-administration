from django.db import models


class Modules(models.Model):
    modelo_modulo = models.CharField(max_length=120)
    potencia_wp_unitaria_modulo = models.FloatField()
    overload_maximo = models.FloatField()
    kwp = models.FloatField()
    marca_modulo = models.CharField(max_length=120)

    def __str__(self):
        return self.modelo_modulo

    class Meta:
        db_table = "modules"


class Accessories(models.Model):
    nome = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "accessories"


class SolarKit(models.Model):
    identificacao_kit = models.CharField(max_length=240, null=True)
    codigo = models.CharField(max_length=32, primary_key=True, unique=True)
    preco = models.FloatField(null=True)
    telhado = models.CharField(max_length=48, null=True)
    tipo_conexao = models.CharField(max_length=48, null=True)
    quant_modulos = models.IntegerField(null=True)
    modulo = models.ForeignKey(Modules, on_delete=models.PROTECT)
    quant_pares_conectores = models.IntegerField(null=True)
    par_conector = models.ForeignKey(
        Accessories,
        on_delete=models.PROTECT,
        related_name="par_conector",
        null=True,
    )
    quant_stringbox = models.IntegerField(null=True)
    stringbox = models.ForeignKey(
        Accessories,
        on_delete=models.PROTECT,
        related_name="stringbox",
        null=True,
    )

    def __str__(self):
        return f"SolarKit - {self.codigo}"

    class Meta:
        db_table = "solar_kit"


class Inverters(models.Model):
    nome = models.CharField(max_length=120, null=True)
    marca = models.CharField(max_length=120, null=True)

    class Meta:
        db_table = "inverters"


class SolarKitInverters(models.Model):
    solar_kit = models.ForeignKey(SolarKit, on_delete=models.PROTECT)
    inversor = models.ForeignKey(Inverters, on_delete=models.PROTECT)
    qtde_inversor = models.IntegerField()

    class Meta:
        db_table = "solar_kit_inverters"


class SolarKitEstructures(models.Model):
    solar_kit = models.ForeignKey(SolarKit, on_delete=models.PROTECT)
    estrutura = models.ForeignKey(Accessories, on_delete=models.PROTECT)
    quant_estrutura = models.IntegerField()

    class Meta:
        db_table = "solar_kit_estructures"


class SolarKitCables(models.Model):
    solar_kit = models.ForeignKey(SolarKit, on_delete=models.PROTECT)
    cabo = models.ForeignKey(Accessories, on_delete=models.PROTECT)
    quant_cabo_em_m = models.FloatField()

    class Meta:
        db_table = "solar_kit_cables"
