import os
import json
import copy

# Configurações de Caminho
ROOT_DIR = os.path.join("..", "armor")

# Listas de Materiais
MATERIAIS_VANILLA = [
    "tetra:wood/", "tetra:stone/", "tetra:gem/", "tetra:metal/", "tetra:bone/",
    "tetra:fabric/", "tetra:fibre/", "tetra:skin/", "tetra:scale/"
]
MATERIAIS_LIGHT = [
    "tetra:wood/", "tetra:fabric/", "tetra:fibre/", "tetra:skin/", "tetra:bone/"
]
MATERIAIS_HEAVY = [
    "tetra:stone/", "tetra:metal/", "tetra:scale/", "tetra:gem/"
]

def aplicar_multiplicadores_atributos(attributes_dict, armor_mult, toughness_mult):
    """Percorre o dicionário de atributos e aplica os multiplicadores."""
    if not attributes_dict:
        return

    keys_to_modify = []
    
    # Identificar chaves de armadura e toughness (pode ser minecraft:generic... ou apenas generic...)
    for key in attributes_dict:
        if "armor" in key and "toughness" not in key:
            keys_to_modify.append((key, armor_mult))
        elif "toughness" in key:
            keys_to_modify.append((key, toughness_mult))
            
    # Aplicar modificações
    for key, mult in keys_to_modify:
        original_val = attributes_dict[key]
        attributes_dict[key] = round(original_val * mult, 5) # Arredonda para evitar floats gigantes

def processar_vanilla(full_path_vanilla):
    pasta_atual = os.path.dirname(full_path_vanilla)
    print(f"Lendo: {full_path_vanilla}")
    try:
        with open(full_path_vanilla, 'r', encoding='utf-8') as f:
            data_vanilla = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {full_path_vanilla}: {e}")
        return

    # O arquivo pode ter múltiplos variants, mas geralmente armadura tem 1 principal
    # Vamos iterar sobre todos para garantir
    
    # ==========================================
    # CRIAR VERSÃO LIGHT
    # ==========================================
    data_light = copy.deepcopy(data_vanilla)
    
    for variant in data_light.get("variants", []):
        # 1. Materiais
        variant["materials"] = MATERIAIS_LIGHT
        
        # 2. Key (Renomear vanilla_ para light_)
        if "key" in variant:
            variant["key"] = variant["key"].replace("vanilla", "light")
            
        # 3. Durabilidade (Base 8, Mult 1)
        variant["durability"] = 8
        variant["durabilityMultiplier"] = 1
        
        # 4. Atributos Base (Buffs/Debuffs fixos)
        # Speed +10%, Swim Speed +10%, KB Res -5%
        if "attributes" not in variant:
            variant["attributes"] = {}
        
        variant["attributes"]["**generic.movement_speed"] = 0.10
        variant["attributes"]["**forge:swim_speed"] = 0.10
        variant["attributes"]["**generic.knockback_resistance"] = -0.05
        
        # 5. Math nos atributos extraídos (Extract)
        if "extract" in variant:
            extract = variant["extract"]
            # 75% Armor, 50% Toughness
            aplicar_multiplicadores_atributos(extract.get("primaryAttributes", {}), 0.75, 0.50)
            aplicar_multiplicadores_atributos(extract.get("secondaryAttributes", {}), 0.75, 0.50)
            aplicar_multiplicadores_atributos(extract.get("tertiaryAttributes", {}), 0.75, 0.50)
            extract["durability"] = 1.2
            extract["integrity"] = 4
            extract["magicCapacity"] = 4

        # 6. Modelos/Texturas
        # Mantém Vanilla conforme pedido ("textura do leve vai ser a mesma do vanilla")

    # Salvar Light
    path_light = os.path.join(pasta_atual, "light.json")
    with open(path_light, 'w', encoding='utf-8') as f:
        json.dump(data_light, f, indent=4)
    print(f"Criado: {path_light}")

    # ==========================================
    # CRIAR VERSÃO HEAVY
    # ==========================================
    data_heavy = copy.deepcopy(data_vanilla)
    
    for variant in data_heavy.get("variants", []):
        # 1. Materiais
        variant["materials"] = MATERIAIS_HEAVY
        
        # 2. Key (Renomear vanilla_ para heavy_)
        if "key" in variant:
            variant["key"] = variant["key"].replace("vanilla", "heavy")
            
        # 3. Durabilidade (Base 2, Mult 4)
        variant["durability"] = 2
        variant["durabilityMultiplier"] = 4
        
        # 4. Atributos Base (Buffs/Debuffs fixos)
        # Speed -5%, Gravity +10%, KB Res +5%
        if "attributes" not in variant:
            variant["attributes"] = {}
            
        variant["attributes"]["**generic.movement_speed"] = -0.05
        variant["attributes"]["**generic.knockback_resistance"] = 0.05
        # Gravidade (Forge usa forge:entity_gravity ou similar, verifique se o mod suporta)
        variant["attributes"]["**forge:entity_gravity"] = 0.10 
        
        # 5. Math nos atributos extraídos (Extract)
        if "extract" in variant:
            extract = variant["extract"]
            # 150% Armor, 200% Toughness
            aplicar_multiplicadores_atributos(extract.get("primaryAttributes", {}), 1.50, 2.00)
            aplicar_multiplicadores_atributos(extract.get("secondaryAttributes", {}), 1.50, 2.00)
            aplicar_multiplicadores_atributos(extract.get("tertiaryAttributes", {}), 1.50, 2.00)
            extract["durability"] = 0.15
            extract["integrity"] = 1
            extract["magicCapacity"] = 1
            # 6. Modelos/Texturas (Mudar path vanilla para heavy)
            if "models" in extract:
                for model in extract["models"]:
                    if "location" in model:
                        model["location"] = model["location"].replace("vanilla", "heavy")

    # Salvar Heavy
    path_heavy = os.path.join(pasta_atual, "heavy.json")
    with open(path_heavy, 'w', encoding='utf-8') as f:
        json.dump(data_heavy, f, indent=4)
    print(f"Criado: {path_heavy}")

def main():
    if not os.path.exists(ROOT_DIR):
        print(f"Pasta não encontrada: {ROOT_DIR}")
        print("Certifique-se de rodar o script na pasta raiz do projeto (antes de data/)")
        return

    print("Iniciando geração de módulos Light e Heavy...")
    
    # Caminhar recursivamente pelas pastas
    count = 0
    # os.walk retorna (caminho_da_pasta_atual, subpastas, arquivos)
    for root, dirs, files in os.walk(ROOT_DIR):
        if "vanilla.json" in files:
            full_path = os.path.join(root, "vanilla.json")
            processar_vanilla(full_path)
            count += 1

    if count == 0:
        print("Nenhum arquivo 'vanilla.json' foi encontrado.")
    else:
        print(f"Processo concluído! {count} pastas processadas.")

if __name__ == "__main__":
    main()