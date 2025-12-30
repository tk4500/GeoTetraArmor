import math
import os
import json

# ==========================================
# CONFIGURAÇÃO GERAL
# ==========================================
ROOT_DIR = "." # Pasta raiz onde os arquivos serão gerados
MOD_ID = "tetra" # Seu ID de mod/datapack

# Estrutura de Pastas de Saída
PATH_IMPROVEMENTS = os.path.join(ROOT_DIR, "tetra", "improvements", "armor", "shared")
PATH_SCHEMATICS = os.path.join(ROOT_DIR, "tetra", "schematics", "armor", "shared")

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
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 1
    },
    {
        "name": "reinforce_toughness",
        "types": ["all"], "slots": ["any"],
        "attribute": "generic.armor_toughness", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 1
    },
    {
        "name": "reinforce_durability",
        "types": ["all"], "slots": ["any"],
        "special_field": "durabilityMultiplier", "value_per_level": 0.1, # +10% por nivel
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 1
    },
    {
        "name": "gild_capacity",
        "types": ["all"], "slots": ["any"],
        "special_field": "magicCapacity", "value_per_level": 10,
        "integrity_cost": 0, "max_levels": 5, "integrity_per_level": 0.5 # Geralmente Gild não custa integridade, ele ADICIONA capacidade
    },

    # --- LEVE ---
    {
        "name": "light_attack_speed",
        "types": ["light"], "slots": ["chest"],
        "attribute": "generic.attack_speed", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 1
    },
    {
        "name": "light_flying_speed",
        "types": ["light"], "slots": ["legs"],
        "attribute": "generic.flying_speed", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 1
    },
    {
        "name": "light_step_height",
        "types": ["light"], "slots": ["feet"],
        "attribute": "forge:step_height", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 3 , "integrity_per_level": 1
    },

    # --- NORMAL (VANILLA) ---
    {
        "name": "vanilla_health",
        "types": ["vanilla"], "slots": ["any"],
        "attribute": "generic.max_health", "value_per_level": 2.0, # 1 Coração
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 0.5
    },
    {
        "name": "vanilla_luck",
        "types": ["vanilla"], "slots": ["any"],
        "attribute": "generic.luck", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 0.5
    },

    # --- PESADA ---
    {
        "name": "heavy_damage",
        "types": ["heavy"], "slots": ["chest"],
        "attribute": "generic.attack_damage", "value_per_level": 0.5,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 0.5
    },
    {
        "name": "heavy_knockback",
        "types": ["heavy"], "slots": ["legs"],
        "attribute": "generic.knockback_resistance", "value_per_level": 0.1,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 0.5
    },
    {
        "name": "heavy_gravity",
        "types": ["heavy"], "slots": ["feet"],
        "attribute": "forge:entity_gravity", "value_per_level": 0.05,
        "integrity_cost": 1, "max_levels": 5, "integrity_per_level": 0.5
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
    filename = f"{data['name']}.json"
    filepath = os.path.join(PATH_IMPROVEMENTS, filename)
    
    improvements = []
    
    for level in range(1, data['max_levels'] + 1):
        entry = {
            "key": f"{MOD_ID}:{data['name']}",
            "level": level,
            "group": data['name'],
            "integrity": -data['integrity_cost'] - math.floor(data['integrity_per_level'] * (level))
        }
        
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
    print(f"Improvement: {filename}")

def criar_schematics(data):
    # Define slots
    target_slots = []
    if data['slots'][0] == "any":
        target_slots = SLOT_MAPPING["any"]
    else:
        for slot_key in data['slots']:
            target_slots.extend(SLOT_MAPPING.get(slot_key, []))
            
    for level in range(1, data['max_levels'] + 1):
        filename = f"{data['name']}_{level}.json"
        filepath = os.path.join(PATH_SCHEMATICS, filename)
        
        # -------------------------------------------------
        # LÓGICA DE REQUERIMENTOS (CORRIGIDA)
        # -------------------------------------------------
        main_requirements = []
        
        # 1. Progressão de Nível (Not Nivel 1 OR Tem Nivel Anterior)
        if level == 1:
            main_requirements.append({
                "type": "tetra:not",
                "requirement": {
                    "type": "tetra:improvement",
                    "improvement": f"{MOD_ID}:{data['name']}"
                }
            })
        else:
            main_requirements.append({
                "type": "tetra:improvement",
                "improvement": f"{MOD_ID}:{data['name']}",
                "level": level - 1
            })
            
        # 2. Filtro de Tipo (Aspecto)
        # Aqui usamos o tetra:aspect que é muito mais limpo
        for t in data['types']:
            if t == "heavy":
                main_requirements.append({
                    "type": "tetra:aspect",
                    "aspect": "heavy"
                })
            elif t == "light":
                main_requirements.append({
                    "type": "tetra:aspect",
                    "aspect": "light"
                })
            elif t == "vanilla":
                main_requirements.append({
                    "type": "tetra:aspect",
                    "aspect": "vanilla"
                })

        schematic = {
            "replace": True,
            "slots": target_slots,
            "materialSlotCount": 0,
            "hone": True,
            "rarity": "hone",
            "displayType": "major",
            "glyph": {
                "textureLocation": "geotetraarmor:textures/gui/gui_gta.png",
                "textureX": 0,
                "textureY": 0
            },
            "requirement": {
                "type": "tetra:and",
                "requirements": main_requirements
            },
            "outcomes": [
                {
                    "improvements": {
                        f"{MOD_ID}:{data['name']}": level
                    }
                }
            ]
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(schematic, f, indent=4)
    
    print(f"Schematics: {data['name']}")

def main():
    if not os.path.exists(PATH_IMPROVEMENTS): os.makedirs(PATH_IMPROVEMENTS)
    if not os.path.exists(PATH_SCHEMATICS): os.makedirs(PATH_SCHEMATICS)

    for honing in HONING_CONFIG:
        criar_improvement(honing)
        criar_schematics(honing)

if __name__ == "__main__":
    main()