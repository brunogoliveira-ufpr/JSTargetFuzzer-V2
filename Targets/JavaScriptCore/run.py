import os
import subprocess

# Diretório onde estão os patches
patches_dir = "/home/kali/JSTargetFuzzer-main/Targets/JavaScriptCore/Patches"
patch_files = ["webkit.patch"]

# Navegar para o diretório WebKit
os.chdir("/home/kali/webkit")

# Função para aplicar um patch


def apply_patch(patch):
    try:
        result = subprocess.run(
            ["git", "apply", patch], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Patch {patch} aplicado com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"Falha ao aplicar o patch {patch}: {e.stderr.decode()}")
        # Saída manual de aplicação de patch
        with open(patch, 'r') as f:
            print(f.read())
        exit(1)


# Aplicar cada patch individualmente
for patch in patch_files:
    patch_path = os.path.join(patches_dir, patch)
    apply_patch(patch_path)

# Executar o script de compilação
try:
    subprocess.run(["./fuzzbuild.sh"], check=True)
    print("Compilação concluída com sucesso")
except subprocess.CalledProcessError as e:
    print(f"Falha na compilação: {e.stderr.decode()}")
