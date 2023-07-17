from pandas import DataFrame, isnull
from ..models import (
    SolarKit,
    Accessories,
    Modules,
    Inverters,
    SolarKitInverters,
    SolarKitCables,
    SolarKitEstructures,
)
from enum import Enum
from typing import TypedDict


class SolarKitDataTypes(TypedDict):
    codigo: str


class BaseEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class SolarKitEnum(BaseEnum):
    identificacao_kit = "Identificação Kit"
    codigo = "Código"
    preco = "Preço"
    telhado = "Telhado"
    tipo_conexao = "Conexão"
    quant_modulos = "Quant. Módulos"
    quant_pares_conectores = "Quant. Pares Conectores"
    quant_stringbox = "Quant. Stringbox"


class ModulesEnum(BaseEnum):
    modelo_modulo = "Modelo Módulo"
    potencia_wp_unitaria_modulo = "Potência Wp Unitária Módulo"
    overload_maximo = "Overload Máximo"
    kwp = "kWp"
    marca_modulo = "Marca do Módulo"


class DataProcessing:
    data = ""

    @staticmethod
    def transform_data(of, to):
        return of if not isnull(of) else to


class DataImportUseCase:
    def __init__(self, dataframe: DataFrame):
        self.df = dataframe

    def inversor_register(self, nome, marca):
        return Inverters.objects.create(nome=nome, marca=marca)

    def run(self):
        for i in range(self.df.shape[0]):
            print(i)
            modules_data = self.get_data_to_create(i, ModulesEnum)
            module = self.get_or_create_module("Modelo Módulo", modules_data)

            accessory_name = self.get_data_by_column(i, "Modelo Par Conector")
            par_conector = self.get_or_create_accessories(accessory_name)

            accessory_name = self.get_data_by_column(i, "Modelo Stringbox")
            stringbox = self.get_or_create_accessories(accessory_name)

            solarkit_data = self.get_data_to_create(i, SolarKitEnum)

            instances_data = self.add_instances_to_create_solarkit(
                [module, par_conector, stringbox]
            )
            solarkit_data.update(instances_data)
            solarkit = self.get_or_create_solarkit(solarkit_data)

            inversores = self.create_inverters(i)
            estruturas = self.create_estructures(i)
            cabos = self.create_cables(i)

            for inversor in inversores:
                SolarKitInverters.objects.create(
                    solar_kit=solarkit, **inversor
                )

            for cabo in cabos:
                SolarKitCables.objects.create(solar_kit=solarkit, **cabo)

            for estrutura in estruturas:
                SolarKitEstructures.objects.create(
                    solar_kit=solarkit, **estrutura
                )

    def create_cables(self, index):
        cabo_vermelho_nome = self.df.loc[index, "Modelo Cabo Vermelho"]
        qtde_cabo_vermelho = self.df.loc[index, "Quant. Cabo Vermelho (m)"]
        cabo_preto_nome = self.df.loc[index, "Modelo Cabo Preto"]
        qtde_cabo_preto = self.df.loc[index, "Quant. Cabo Preto (m)"]
        cabos = []

        if not isnull(cabo_vermelho_nome) and not isnull(qtde_cabo_vermelho):
            cabos.append(
                {
                    "quant_cabo_em_m": qtde_cabo_vermelho,
                    "cabo": self.get_or_create_accessories(cabo_vermelho_nome),
                }
            )

        if not isnull(cabo_preto_nome) and not isnull(qtde_cabo_preto):
            cabos.append(
                {
                    "quant_cabo_em_m": qtde_cabo_preto,
                    "cabo": self.get_or_create_accessories(cabo_preto_nome),
                }
            )

        return cabos

    def create_inverters(self, index):
        inversor1_nome = self.df.loc[index, "Inversor 1"]
        inversor2_nome = self.df.loc[index, "Inversor 2"]
        inversors_marca = self.df.loc[index, "Marca do Inversor"]
        inversor1_qtde = self.df.loc[index, "Qtde. Inversor 1"]
        inversor2_qtde = self.df.loc[index, "Qtde. Inversor 2"]
        inversores = []

        if (
            not isnull(inversor1_nome)
            and not isnull(inversors_marca)
            and not isnull(inversor1_qtde)
        ):
            inversores.append(
                {
                    "qtde_inversor": inversor1_qtde,
                    "inversor": self.inversor_register(
                        inversor1_nome, inversors_marca
                    ),
                }
            )

        if (
            not isnull(inversor2_nome)
            and not isnull(inversors_marca)
            and not isnull(inversor2_qtde)
        ):
            inversores.append(
                {
                    "qtde_inversor": inversor1_qtde,
                    "inversor": self.inversor_register(
                        inversor2_nome, inversors_marca
                    ),
                }
            )

        return inversores

    def create_estructures(self, index):
        estruturas = []

        for j in range(5):
            estrutura_nome = self.df.loc[index, f"Modelo Estrutura {j+1}"]
            qtde_estrutura = self.df.loc[index, f"Quant. Estrutura {j+1}"]

            if not isnull(estrutura_nome) and not isnull(qtde_estrutura):
                estruturas.append(
                    {
                        "quant_estrutura": qtde_estrutura,
                        "estrutura": self.get_or_create_accessories(
                            estrutura_nome
                        ),
                    }
                )

        return estruturas

    def add_instances_to_create_solarkit(
        self, instances: list[SolarKit | Accessories]
    ):
        field_names = ["modulo", "par_conector", "stringbox"]
        return {
            field: instance for field, instance in zip(field_names, instances)
        }

    def get_data_to_create(self, index: int, enum: BaseEnum):
        columns = enum.list()
        ret = {}
        for column in columns:
            if isnull(self.df.loc[index, enum[column].value]):
                ret[column] = 0
            else:
                ret[column] = self.df.loc[index, enum[column].value]

        return ret

    def get_data_by_column(self, index: int, column_name: str):
        return self.df.loc[index, column_name]

    def get_or_create_accessories(self, nome: str):
        defaults = {"nome": nome}
        instance, created = Accessories.objects.get_or_create(
            nome=nome, defaults=defaults
        )
        return instance

    def get_or_create_solarkit(self, data_to_create: SolarKitDataTypes):
        codigo = data_to_create["codigo"]

        instance, created = SolarKit.objects.get_or_create(
            codigo=codigo, defaults=data_to_create
        )
        return instance

    def get_or_create_module(
        self, modelo_modulo: str, data_to_create: dict[str, str]
    ):
        instance, created = Modules.objects.get_or_create(
            modelo_modulo=modelo_modulo, defaults=data_to_create
        )
        return instance
