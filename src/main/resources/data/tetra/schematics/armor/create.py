import os
import json
import copy

# Configurações de Caminho
# O script vai procurar a partir desta pasta para dentro
ROOT_DIR = "."

# Listas de Materiais
MATERIAIS_ALL = [
    "tetra:wood/", "tetra:stone/", "tetra:gem/", "tetra:metal/", "tetra:bone/",
    "tetra:fabric/", "tetra:fibre/", "tetra:skin/", "tetra:scale/"
]
MATERIAIS_LIGHT = [
    "tetra:wood/", "tetra:fabric/", "tetra:fibre/", "tetra:skin/", "tetra:bone/"
]
MATERIAIS_HEAVY = [
    "tetra:stone/", "tetra:metal/", "tetra:scale/", "tetra:gem/"
]

def processar_schematic_vanilla(full_path_vanilla):
    pasta_atual = os.path.dirname(full_path_vanilla)
    print(f"Processando: {full_path_vanilla}")
    
    try:
        with open(full_path_vanilla, 'r', encoding='utf-8') as f:
            data_vanilla = json.load(f)
    except Exception as e:
        print(f"ERRO ao ler {full_path_vanilla}: {e}")
        return

    # Informações base para o requirement (assumindo que o slot 0 é o alvo)
    #target_slot = data_vanilla.get("slots", [""])[0]
    
    # Tentar pegar a variant vanilla do primeiro outcome para usar no requirement
    vanilla_variant_key = ""
    if "outcomes" in data_vanilla and len(data_vanilla["outcomes"]) > 0:
        vanilla_variant_key = data_vanilla["outcomes"][0].get("moduleVariant", "")

    # ==========================================
    # ATUALIZAR O PRÓPRIO VANILLA
    # ==========================================
    # Regra: countFactor em 3, todos os materiais
    data_vanilla["applicableMaterials"] = MATERIAIS_ALL
    
    for outcome in data_vanilla.get("outcomes", []):
        outcome["countFactor"] = 3
        outcome["materials"] = MATERIAIS_ALL
        # Nota: Não mudamos offset no vanilla, mantemos o original

    # Salvar as alterações no Vanilla
    with open(full_path_vanilla, 'w', encoding='utf-8') as f:
        json.dump(data_vanilla, f, indent=4)
    print(f" -> Atualizado Vanilla: {full_path_vanilla}")

    # ==========================================
    # CRIAR VERSÃO LIGHT
    # ==========================================
    data_light = copy.deepcopy(data_vanilla)
    
    # 1. Materiais
    data_light["applicableMaterials"] = MATERIAIS_LIGHT
    
    # 2. Requirement (Só permite se for vanilla)
    #if target_slot and vanilla_variant_key:
    #    data_light["requirement"] = {
    #        "type": "tetra:module",
    #        "module": target_slot,
    #        "variant": vanilla_variant_key
    #    }
    
    for outcome in data_light.get("outcomes", []):
        outcome["materials"] = MATERIAIS_LIGHT
        outcome["countFactor"] = 3
        
        # Substituir chaves de vanilla para light
        if "moduleKey" in outcome:
            outcome["moduleKey"] = outcome["moduleKey"].replace("vanilla", "light")
        if "moduleVariant" in outcome:
            outcome["moduleVariant"] = outcome["moduleVariant"].replace("vanilla", "light")
            
        # Regra: baixar countOffset em 1
        current_count_offset = outcome.get("countOffset", 0)
        outcome["countOffset"] = current_count_offset - 1
        

    # Salvar Light
    path_light = os.path.join(pasta_atual, "light.json")
    with open(path_light, 'w', encoding='utf-8') as f:
        json.dump(data_light, f, indent=4)
    print(f" -> Criado Light: {path_light}")

    # ==========================================
    # CRIAR VERSÃO HEAVY
    # ==========================================
    data_heavy = copy.deepcopy(data_vanilla) # Copia do vanilla já atualizado (countFactor 3)
    
    # 1. Materiais
    data_heavy["applicableMaterials"] = MATERIAIS_HEAVY
    
    # 2. Requirement
    #if target_slot and vanilla_variant_key:
    #    data_heavy["requirement"] = {
    #        "type": "tetra:module",
    #        "module": target_slot,
    #        "variant": vanilla_variant_key
    #    }
        
    for outcome in data_heavy.get("outcomes", []):
        outcome["materials"] = MATERIAIS_HEAVY
        outcome["countFactor"] = 3
        
        # Substituir chaves
        if "moduleKey" in outcome:
            outcome["moduleKey"] = outcome["moduleKey"].replace("vanilla", "heavy")
        if "moduleVariant" in outcome:
            outcome["moduleVariant"] = outcome["moduleVariant"].replace("vanilla", "heavy")
            
        # Regra: aumentar countOffset em 2
        current_count_offset = outcome.get("countOffset", 0)
        outcome["countOffset"] = current_count_offset + 2
        
        # Regra: aumentar toolOffset em 1
        current_tool_offset = outcome.get("toolOffset", 0)
        outcome["toolOffset"] = current_tool_offset + 1

    # Salvar Heavy
    path_heavy = os.path.join(pasta_atual, "heavy.json")
    with open(path_heavy, 'w', encoding='utf-8') as f:
        json.dump(data_heavy, f, indent=4)
    print(f" -> Criado Heavy: {path_heavy}")


def main():
    if not os.path.exists(ROOT_DIR):
        print(f"ERRO: Pasta raiz não encontrada: {ROOT_DIR}")
        print("Verifique se você está executando o script na pasta correta.")
        return

    print(f"Iniciando varredura de Schematics em: {ROOT_DIR}")
    
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file == "vanilla.json":
                full_path = os.path.join(root, file)
                processar_schematic_vanilla(full_path)
                count += 1

    if count == 0:
        print("Nenhum arquivo 'vanilla.json' foi encontrado nas pastas de schematics.")
    else:
        print(f"Concluído! {count} schematics processados.")

if __name__ == "__main__":
    main()