import os
import subprocess


diretorio = "/home/kali/JSTargetFuzzer-main/cli/crashes/crashes-30-08/"

extensao = ".js"


caminho_jsc = "/home/kali/JSTargetFuzzer-main/cli/jsc"


arquivo_sucesso = "jsc_sucessos.txt"
arquivo_erro = "jsc_erros.txt"


def executar_comando_jsc_em_arquivos(diretorio, extensao, caminho_jsc):

    with open(arquivo_sucesso, 'a') as log_sucesso, open(arquivo_erro, 'a') as log_erro:

        for arquivo in os.listdir(diretorio):
            if arquivo.endswith(extensao):
                caminho_arquivo = os.path.join(diretorio, arquivo)

                try:
                    resultado = subprocess.run([caminho_jsc, caminho_arquivo], check=True, capture_output=True, text=True)

                    log_sucesso.write(f"Sucesso ao processar {arquivo}\n")
                    log_sucesso.write(f"Saída do comando:\n{resultado.stdout}\n")
                except subprocess.CalledProcessError as e:

                    log_erro.write(f"Erro ao processar {arquivo}: {e.stderr}\n")

executar_comando_jsc_em_arquivos(diretorio, extensao, caminho_jsc)
