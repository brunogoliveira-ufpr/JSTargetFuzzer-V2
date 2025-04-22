from pyjsparser import PyJsParser

# Função para classificar o código baseado em Loops, Operações Numéricas e Variáveis
def classify_js_code(js_code):
    categories = {"Loops": [], "Numeric Operations": [], "Variables": []}
    
    # Inicializa o parser
    parser = PyJsParser()
    tree = parser.parse(js_code)

    # Função auxiliar para percorrer o AST
    def traverse(node):
        if isinstance(node, dict):
            # Classificar loops
            if node.get('type') == 'ForStatement' or node.get('type') == 'WhileStatement':
                categories["Loops"].append(node)
            # Classificar operações numéricas
            elif node.get('type') == 'BinaryExpression' or node.get('type') == 'AssignmentExpression':
                categories["Numeric Operations"].append(node)
            # Classificar variáveis
            elif node.get('type') == 'VariableDeclaration':
                categories["Variables"].append(node)
            # Recursão para visitar todos os filhos
            for key, value in node.items():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    # Percorrer a AST para classificar
    traverse(tree)
    
    return categories

# Exemplo de código JavaScript para análise
js_code = '''
let v0 = [];
function f1() {
    return v0;
}
const v7 = new Set();
for (let i = 0; i < 10; i++) {
    v0.push(i);
}
let result = Math.sign(37136);
let a = 5 + 10;
'''

# Classificar o código
categories = classify_js_code(js_code)

# Exibir os resultados
print("Loops:", len(categories["Loops"]))
print("Numeric Operations:", len(categories["Numeric Operations"]))
print("Variables:", len(categories["Variables"]))
