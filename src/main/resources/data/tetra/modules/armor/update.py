import os
import json

def atualizar_jsons(diretorio_raiz, nome_arquivo_alvo, novos_dados):
    # Percorre pastas, subpastas e arquivos
    for raiz, diretorios, arquivos in os.walk(diretorio_raiz):
        for arquivo in arquivos:
            if arquivo == nome_arquivo_alvo:
                caminho_completo = os.path.join(raiz, arquivo)
                
                try:
                    # 1. Abre e lê o conteúdo atual
                    with open(caminho_completo, 'r', encoding='utf-8') as f:
                        dados_originais = json.load(f)
                    
                    # 2. Atualiza com os novos parâmetros
                    # O .update() faz o merge: altera o que existe e cria o que falta
                    dados_originais.update(novos_dados)
                    
                    # 3. Salva de volta no arquivo
                    with open(caminho_completo, 'w', encoding='utf-8') as f:
                        json.dump(dados_originais, f, indent=4, ensure_ascii=False)
                    
                    print(f"✅ Atualizado: {caminho_completo}")
                
                except Exception as e:
                    print(f"❌ Erro ao processar {caminho_completo}: {e}")

# --- CONFIGURAÇÃO ---
diretorio_base = './'  # Pasta onde começar a busca
arquivo_para_buscar = 'heavy.json' # Nome exato do arquivo

# Parâmetros que você quer inserir ou mudar
parametros_para_injetar = {
    "improvements": [
    "tetra:armor/shared/",
    "tetra:shared"
  ],"variants": [
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
        "tetra:scale/"
      ],
      "durability": 4,
      "durabilityMultiplier": 2,
      "integrity": 1,"attributes": {
        "**generic.movement_speed": -0.05
      },
        "primaryEffects": {},
        "secondaryEffects": {},
        "tertiaryEffects": {},
        "durability": 0.3,
        "integrity": 1,
        "magicCapacity": 1,
    }
  ]
}

# Executa a função
atualizar_jsons(diretorio_base, arquivo_para_buscar, parametros_para_injetar)