import Foundation

// Estrutura que armazena o resultado da complexidade ciclomática para cada gerador
struct ComplexityResult: Codable {
    let generatorName: String
    let complexity: Int
}

// Função para calcular a complexidade ciclomática de um gerador de código
func calculateCyclomaticComplexity(for generator: CodeGenerator) -> Int {
    var complexity = 1 // Começamos com 1 para a própria função
    
    // Aqui vamos adicionar lógica para analisar diferentes instruções e adicionar ao valor de complexidade
    // Exemplo:
    if generator.containsLoop {
        complexity += 1
    }
    if generator.containsIfElse {
        complexity += 2 // 1 para o if e 1 para o else
    }
    if generator.containsSwitch {
        complexity += generator.switchCasesCount // Cada case adiciona 1
    }
    
    // Adicionar outras regras conforme necessário
    
    return complexity
}

// Função para gerar o JSON com os resultados
func generateComplexityJSON(for generators: [CodeGenerator]) -> String? {
    var results: [ComplexityResult] = []
    
    for generator in generators {
        let complexity = calculateCyclomaticComplexity(for: generator)
        let result = ComplexityResult(generatorName: generator.name, complexity: complexity)
        results.append(result)
    }
    
    // Convertendo os resultados em JSON
    let encoder = JSONEncoder()
    encoder.outputFormatting = .prettyPrinted
    if let jsonData = try? encoder.encode(results) {
        return String(data: jsonData, encoding: .utf8)
    }
    
    return nil
}

// Supondo que a lista de geradores já esteja importada do seu arquivo
let codeGenerators = CodeGenerators // Importado do seu arquivo
if let complexityJSON = generateComplexityJSON(for: codeGenerators) {
    print(complexityJSON)
}
