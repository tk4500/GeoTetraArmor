import os
import json

ROOT_DIR = os.path.join(".", "tetra", "modules", "armor")

def adicionar_aspecto(filepath, aspecto_nome):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        alterado = False
        for variant in data.get("variants", []):
            if "aspects" not in variant:
                variant["aspects"] = {}
            
            # Adiciona o aspecto (ex: "heavy": 1)
            if aspecto_nome not in variant["aspects"]:
                variant["aspects"][aspecto_nome] = 1
                alterado = True
        
        if alterado:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Aspecto '{aspecto_nome}' adicionado em: {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"Erro em {filepath}: {e}")

def main():
    if not os.path.exists(ROOT_DIR):
        print("Pasta data/tetra/modules/armor não encontrada.")
        return

    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            
            if file == "heavy.json":
                # Adiciona aspecto 'heavy'
                adicionar_aspecto(full_path, "heavy")
                
            elif file == "light.json":
                # Adiciona aspecto 'light'
                adicionar_aspecto(full_path, "light")
            elif file == "vanilla.json":
                
                adicionar_aspecto(full_path, "vanilla")

if __name__ == "__main__":
    main()