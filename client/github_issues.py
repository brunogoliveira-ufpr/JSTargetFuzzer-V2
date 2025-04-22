import csv
import pandas as pd
from github import Github
import re
from collections import defaultdict, Counter
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Autenticação na API do GitHub usando um token de acesso pessoal
g = Github("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")

# Função para filtrar por palavras-chave e retornar a palavra encontrada
def filter_by_keywords(text, keywords):
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
            return True, keyword
    return False, None

# Palavras-chave para filtrar
keywords = [
    "access", "auth", "bypass", "confuse", "CVE", "CWE", "danger", 
    "denial of service", "disclosure", "ensure", "exception", 
    "exploit", "failure", "harmful", "incorrect", "issue", "leak", 
    "malicious", "null", "overflow", "pass", "password", "prevent", 
    "safe", "secure", "sensitive", "state", "unauthorized", "uninitialized", 
    "use-after-free", "vulnerable"
]

# Coletar repositório
repo_name = "jerryscript-project/jerryscript"
logging.info(f"Coletando repositório: {repo_name}")
repo = g.get_repo(repo_name)

# Coletar issues
logging.info("Coletando issues...")
issues = repo.get_issues(state='all')

def get_issue_text(issue):
    title = issue.title if issue.title else ""
    body = issue.body if issue.body else ""
    return title + " " + body

# Armazenar dados em uma lista para criar o DataFrame posteriormente
data = []

logging.info(f"Total de issues coletadas: {issues.totalCount}")
logging.info("Filtrando issues por palavras-chave...")
for issue in issues:
    issue_text = get_issue_text(issue)
    contains_keyword, keyword = filter_by_keywords(issue_text, keywords)
    if contains_keyword:
        logging.info(f"Issue #{issue.number} contém a palavra-chave '{keyword}'. Verificando commits associados...")
        events = issue.get_events()
        has_commit = any(event.event == 'referenced' and event.commit_id for event in events)
        if not has_commit:
            logging.info(f"Issue #{issue.number} não tem commits associados. Adicionando à lista filtrada.")
            data.append({
                "Type": "Issue",
                "ID": issue.number,
                "Title": issue.title,
                "Keyword": keyword,
                "Associated Commits": None,
                "Files": None
            })
        else:
            logging.info(f"Issue #{issue.number} tem commits associados. Ignorando.")
            for event in events:
                if event.event == 'referenced' and event.commit_id:
                    try:
                        commit = repo.get_commit(event.commit_id)
                        files = [file.filename for file in commit.files]
                        data.append({
                            "Type": "Issue",
                            "ID": issue.number,
                            "Title": issue.title,
                            "Keyword": keyword,
                            "Associated Commits": commit.sha,
                            "Files": ", ".join(files)
                        })
                    except Exception as e:
                        logging.warning(f"Não foi possível encontrar o commit {event.commit_id} associado à issue #{issue.number}. Erro: {e}")
    else:
        logging.info(f"Issue #{issue.number} não contém palavras-chave. Ignorando.")

# Coletar commits
logging.info("Coletando commits...")
commits = repo.get_commits()

logging.info("Filtrando commits por palavras-chave...")
for commit in commits:
    commit_message = commit.commit.message
    contains_keyword, keyword = filter_by_keywords(commit_message, keywords)
    if contains_keyword:
        logging.info(f"Commit {commit.sha} contém a palavra-chave '{keyword}'.")
        files = [file.filename for file in commit.files]
        data.append({
            "Type": "Commit",
            "ID": commit.sha,
            "Title": commit_message,
            "Keyword": keyword,
            "Associated Commits": None,
            "Files": ", ".join(files)
        })
    else:
        logging.info(f"Commit {commit.sha} não contém palavras-chave. Ignorando.")

# Criar DataFrame com os dados coletados
df = pd.DataFrame(data)

# Salvar DataFrame em CSV
csv_filename = "issues_commits_analysis.csv"
logging.info(f"Gerando arquivo CSV: {csv_filename}")
df.to_csv(csv_filename, index=False)

# Análise usando pandas
logging.info("Realizando análise com pandas...")
# Exemplo de análise: contagem de arquivos mais modificados
file_counts = df['Files'].str.split(', ').explode().value_counts().head(10)
print("\nTop 10 arquivos mais modificados:")
print(file_counts)

# Exemplo de análise: contagem de tipos de registros (Issues vs Commits)
type_counts = df['Type'].value_counts()
print("\nContagem de tipos de registros (Issues vs Commits):")
print(type_counts)

logging.info("Processo concluído.")
