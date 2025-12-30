import os
import shutil

def organizar_jsons(pasta_origem):
    # Obtém o caminho absoluto do diretório onde o script está
    diretorio_atual = os.getcwd()
    
    print(f"Buscando arquivos em: {pasta_origem}")
    print(f"Copiando para: {diretorio_atual}\n")

    contador = 0

    # os.walk percorre a pasta raiz, subpastas e arquivos
    for raiz, diretorios, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            # Verifica se a extensão é .json
            if arquivo.lower().endswith('.json'):
                caminho_completo = os.path.join(raiz, arquivo)
                
                # Define o destino (mesmo nome do arquivo na pasta raiz)
                destino = os.path.join(diretorio_atual, arquivo)

                # Tratamento para evitar sobrescrever arquivos com nomes iguais
                if os.path.exists(destino):
                    nome, ext = os.path.splitext(arquivo)
                    destino = os.path.join(diretorio_atual, f"{nome}_copia_{contador}{ext}")

                try:
                    shutil.copy2(caminho_completo, destino)
                    print(f"Copiado: {arquivo}")
                    contador += 1
                except Exception as e:
                    print(f"Erro ao copiar {arquivo}: {e}")

    print(f"\nTarefa concluída! {contador} arquivos copiados.")

    # Substitua pelo caminho da pasta que contém os JSONs
    # Use '.' se quiser que ele busque a partir da pasta atual para baixo
pasta_alvo = "." 

if os.path.exists(pasta_alvo):
    print("Iniciando a organização dos JSONs...\n")
    organizar_jsons(pasta_alvo)
else:
    print("Erro: A pasta de origem especificada não existe.")