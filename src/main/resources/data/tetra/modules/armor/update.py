import os
import json


def deep_merge(origem, atualizacao):
    """
    Mescla dicionários recursivamente.
    Se encontrar uma lista, o comportamento padrão será sobrescrever
    (ajustado abaixo especificamente para o seu caso).
    """
    for chave, valor in atualizacao.items():
        if (
            isinstance(valor, dict)
            and chave in origem
            and isinstance(origem[chave], dict)
        ):
            deep_merge(origem[chave], valor)
        else:
            origem[chave] = valor
    return origem


def processar_tetra_jsons(diretorio_raiz, nome_alvo, dados_novos):
    for raiz, _, arquivos in os.walk(diretorio_raiz):
        if nome_alvo in arquivos:
            caminho = os.path.join(raiz, nome_alvo)

            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = json.load(f)

                # 1. Atualiza o 'improvements' na raiz do JSON
                if "improvements" in dados_novos:
                    conteudo["improvements"] = dados_novos["improvements"]

                # 2. Atualiza o conteúdo dentro de 'variants'
                if "variants" in conteudo and len(conteudo["variants"]) > 0:
                    # Pegamos o primeiro item da lista de variantes do arquivo original
                    variante_original = conteudo["variants"][0]
                    # Pegamos os dados novos que você definiu para a variante
                    novos_dados_variante = dados_novos["variants"][0]

                    # Fazemos o merge profundo apenas dentro dessa variante
                    conteudo["variants"][0] = deep_merge(
                        variante_original, novos_dados_variante
                    )

                # 3. Salva o arquivo atualizado
                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(conteudo, f, indent=4, ensure_ascii=False)

                print(f"✅ Atualizado com sucesso: {caminho}")

            except Exception as e:
                print(f"❌ Erro ao processar {caminho}: {e}")


# --- CONFIGURAÇÃO DOS SEUS PARÂMETROS ---
diretorio_base = "./"  # Coloque o caminho da sua pasta raiz aqui
nome_do_json = "vanilla.json"  # Ou o nome do arquivo que você quer filtrar

parametros_para_injetar = {
    "improvements": ["tetra:armor/shared/", "tetra:shared"],
    "variants": [
        {
            "materials": [
                "tetra:wood/",
                "tetra:stone/",
                "tetra:gem/",
                "tetra:metal/",
                "tetra:bone/",
                "tetra:fabric/",
                "tetra:fibre/",
                "tetra:skin/",
                "tetra:scale/",
            ],
            "durability": 8,  # Note que no seu exemplo você enviou dois valores de durability, o Python pegará o último
            "durabilityMultiplier": 1,
            "integrity": 2,
            "extract": {
                "primaryEffects": {},
                "secondaryEffects": {},
                "tertiaryEffects": {},
                "durability": 0.6,
                "integrity": 2,
                "magicCapacity": 2,
            },
        }
    ],
}

# Execução
processar_tetra_jsons(diretorio_base, nome_do_json, parametros_para_injetar)
