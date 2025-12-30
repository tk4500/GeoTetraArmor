import os
import json

# ==========================================
# CONFIGURAÇÃO GERAL
# ==========================================
ROOT_DIR = "." # Pasta raiz onde os arquivos serão gerados
MOD_ID = "tetra" # Seu ID de mod/datapack

# Estrutura de Pastas de Saída
PATH_IMPROVEMENTS = os.path.join(ROOT_DIR, "tetra", "improvements", "armor")
PATH_SCHEMATICS = os.path.join(ROOT_DIR, "tetra", "schematics", "armor", "honing")

# ==========================================
# DEFINIÇÃO DOS HONINGS
# ==========================================
# Lista de dicionários definindo cada honing
# types: ["light", "heavy", "vanilla", "all"]
# slots: ["chest", "legs", "feet", "head", "any"]
HONING_CONFIG = [
    # --- GERAL ---
    {
        "name": "reinforce_armor",
        "types": ["all"], "slots": ["any"],
        "attribute": "generic.armor", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "reinforce_toughness",
        "types": ["all"], "slots": ["any"],
        "attribute": "generic.armor_toughness", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "reinforce_durability",
        "types": ["all"], "slots": ["any"],
        "special_field": "durabilityMultiplier", "value_per_level": 0.1, # +10% por nivel
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "gild_capacity",
        "types": ["all"], "slots": ["any"],
        "special_field": "magicCapacity", "value_per_level": 10,
        "integrity_cost": 0, "max_levels": 5 # Geralmente Gild não custa integridade, ele ADICIONA capacidade
    },

    # --- LEVE ---
    {
        "name": "light_attack_speed",
        "types": ["light"], "slots": ["chest"],
        "attribute": "generic.attack_speed", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "light_flying_speed",
        "types": ["light"], "slots": ["legs"],
        "attribute": "generic.flying_speed", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "light_step_height",
        "types": ["light"], "slots": ["feet"],
        "attribute": "forge:step_height_addition", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 3 # Step height não precisa de muitos niveis
    },

    # --- NORMAL (VANILLA) ---
    {
        "name": "vanilla_health",
        "types": ["vanilla"], "slots": ["any"],
        "attribute": "generic.max_health", "value_per_level": 2.0, # 1 Coração
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "vanilla_luck",
        "types": ["vanilla"], "slots": ["any"],
        "attribute": "generic.luck", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5
    },

    # --- PESADA ---
    {
        "name": "heavy_damage",
        "types": ["heavy"], "slots": ["chest"],
        "attribute": "generic.attack_damage", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "heavy_knockback",
        "types": ["heavy"], "slots": ["legs"],
        "attribute": "generic.knockback_resistance", "value_per_level": 0.1,
        "integrity_cost": 1, "max_levels": 5
    },
    {
        "name": "heavy_gravity",
        "types": ["heavy"], "slots": ["feet"],
        "attribute": "forge:entity_gravity", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5
    }
]

# Mapeamento de Slots para nomes de módulos Tetra (simplificado)
SLOT_MAPPING = {
    "chest": ["chest/base", "chest/left", "chest/right"],
    "legs": ["legs/belt", "legs/left", "legs/right"],
    "feet": ["feet/left", "feet/right"],
    "head": ["head/base"],
    "any": [
        "chest/base", "chest/left", "chest/right", 
        "feet/left", "feet/right", 
        "head/base", 
        "legs/belt", "legs/left", "legs/right"
    ]
}

def criar_improvement(data):
    """Cria o arquivo JSON de Improvement contendo todos os níveis."""
    filename = f"{data['name']}.json"
    filepath = os.path.join(PATH_IMPROVEMENTS, filename)
    
    improvements = []
    
    for level in range(1, data['max_levels'] + 1):
        entry = {
            "key": f"{MOD_ID}:{data['name']}",
            "level": level,
            "group": data['name'],
            "integrity": -data['integrity_cost']
        }
        
        # Define se é atributo ou campo especial
        val = round(data['value_per_level'] * level, 4)
        
        if "attribute" in data:
            entry["attributes"] = {
                data['attribute']: val
            }
        elif "special_field" in data:
            entry[data['special_field']] = val
            
        improvements.append(entry)
        
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(improvements, f, indent=4)
    print(f"Improvement criado: {filepath}")

def criar_schematics(data):
    """Cria um arquivo Schematic para CADA nível do honing."""
    
    # Definir quais slots esse schematic aceita
    target_slots = []
    if data['slots'][0] == "any":
        target_slots = SLOT_MAPPING["any"]
    else:
        for slot_key in data['slots']:
            target_slots.extend(SLOT_MAPPING.get(slot_key, []))
            
    # Loop por níveis
    for level in range(1, data['max_levels'] + 1):
        filename = f"{data['name']}_{level}.json"
        filepath = os.path.join(PATH_SCHEMATICS, filename)
        
        # Definir Requerimentos
        requirements = []
        
        # 1. Requerimento de Hone (Nível anterior ou Hone disponível)
        if level == 1:
            requirements.append({
                "type": "tetra:not",
                "requirement": {
                    "type": "tetra:improvement",
                    "improvement": f"{MOD_ID}:{data['name']}"
                }
            })
        else:
            requirements.append({
                "type": "tetra:improvement",
                "improvement": f"{MOD_ID}:{data['name']}",
                "level": level - 1
            })
            
        # 2. Requerimento de Tipo (Light/Heavy/Vanilla)
        # Nota: Tetra não tem "type: variant_category", então verificamos se a variant string contém o nome
        # Isso assume que suas variants se chamam "heavy_...", "light_...", "vanilla_..."
        type_reqs = []
        for t in data['types']:
            if t == "all":
                continue
            
            # Aqui usamos regex simples no schematic requirement se o Tetra suportar, 
            # mas o Tetra padrão usa "variant". Como não sabemos o slot exato na hora de gerar 
            # o requirement genérico para "any", isso fica complexo.
            # SOLUÇÃO: Usar "tetra:variant_contains" se existisse, mas vamos usar "tetra:or" com as possibilidades
            # OU assumir que o nome da variante começa com o tipo.
            pass # Vamos tratar isso na estrutura principal
            
        # Estrutura do Schematic
        schematic = {
            "replace": true_if_exists(filepath), # Tenta manter replace true se arquivo ja existe
            "slots": target_slots,
            "materialSlotCount": 0,
            "hone": True,
            "rarity": "hone",
            "displayType": "major",
            "glyph": {
                "textureLocation": "geotetraarmor:textures/gui/gui_gta.png",
                "textureX": 0, # Placeholder, idealmente mudar por tipo
                "textureY": 0
            },
            "outcomes": [
                {
                    "improvements": {
                        f"{MOD_ID}:{data['name']}": level
                    }
                }
            ]
        }
        
        # Montar a lógica de requerimento final
        # Se for especifico (ex: heavy), precisamos injetar um requiremento de variante
        # Como o Tetra schematics "requirement" é global para o schematic, e "slots" é uma lista,
        # se tivermos slots diferentes, a validação de variant é chata.
        # Mas como seus módulos seguem padrão "heavy_chest_base", podemos tentar filtrar.
        
        # Simples: Se não for ALL, adicionamos requerimento de improvement nulo mas com nome sugestivo?
        # Não, o melhor jeito no Tetra para filtrar Variant em Honing é garantir que o schematic
        # só apareça para aquele item. 
        # Infelizmente o Tetra vanilla json não tem "variant_contains".
        # O que faremos: Deixamos o schematic "aberto" nos slots, mas se você quiser ser RIGIDO,
        # teria que criar um schematic por slot por tipo.
        # VAMOS SIMPLIFICAR: O schematic checa o improvement anterior. 
        # Para o Nivel 1, vamos adicionar um "translation" key customizada para indicar que é Heavy.
        
        schematic["requirement"] = {
            "type": "tetra:and",
            "requirements": requirements
        }
        
        # Adiciona requirement de Variant se não for ALL
        # Isso é TRUQUE: O Tetra permite requirements aninhados.
        # Se for Heavy, exigimos que o item tenha uma propriedade Heavy? 
        # Infelizmente sem um "tag" na variant é dificil filtrar 100% via JSON puro sem listar todas as variants.
        # VOU LISTAR AS VARIANTS NO REQUIREMENT SE FOR ESPECIFICO.
        
        if "all" not in data['types']:
            variant_reqs = []
            target_type = data['types'][0] # heavy, light, vanilla
            
            # Gera lista de todas as variants possiveis para esse tipo e slots
            for slot in target_slots:
                # Ex: heavy_chest_base/
                clean_slot = slot.replace("/", "_")
                variant_name = f"{target_type}_{clean_slot}/"
                
                variant_reqs.append({
                    "type": "tetra:module",
                    "module": slot,
                    "variant": variant_name
                })
            
            # Adiciona um OR gigante: O item tem que ser (Heavy Chest Base OR Heavy Chest Left OR ...)
            if variant_reqs:
                requirements.append({
                    "type": "tetra:or",
                    "requirements": variant_reqs
                })

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(schematic, f, indent=4)
    
    print(f"Schematics criados para {data['name']} (1-{data['max_levels']})")

def true_if_exists(path):
    return True # Sempre replace true para garantir update

def main():
    print("Iniciando geração de Honings...")
    
    if not os.path.exists(PATH_IMPROVEMENTS):
        os.makedirs(PATH_IMPROVEMENTS)
    if not os.path.exists(PATH_SCHEMATICS):
        os.makedirs(PATH_SCHEMATICS)

    for honing in HONING_CONFIG:
        criar_improvement(honing)
        criar_schematics(honing)

    print("Concluído!")

if __name__ == "__main__":
    main()