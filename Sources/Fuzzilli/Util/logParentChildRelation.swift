import Foundation

func logParentChildRelation(parentID: UUID?, parentWeight: Double?, childID: UUID, childWeight: Double, filePath: String = "parent_child_map.csv") {
    let parentIDString = parentID?.uuidString ?? "None"
    let parentWeightString = parentWeight != nil ? String(format: "%.2f", parentWeight!) : "None"
    let childIDString = childID.uuidString
    let childWeightString = String(format: "%.2f", childWeight)

    // Monta a linha CSV com os pesos do pai e do filho
    //let line = "\(parentIDString),\(parentWeightString),\(childIDString),\(childWeightString)\n"

    // Verifica se o arquivo já existe
    //let fileManager = FileManager.default
    //if !fileManager.fileExists(atPath: filePath) {
        // Cria o arquivo com cabeçalho
        //let header = "Parent ID,Parent Weight,Child ID,Child Weight\n"
        //try? header.write(toFile: filePath, atomically: true, encoding: .utf8)
    //}

    // Adiciona a linha ao arquivo
    //if let fileHandle = FileHandle(forWritingAtPath: filePath) {
    //    fileHandle.seekToEndOfFile()
    //    if let data = line.data(using: .utf8) {
    //        fileHandle.write(data)
    //    }
    //    fileHandle.closeFile()
    //} else {
    //    try? line.write(toFile: filePath, atomically: true, encoding: .utf8)
    //}
}

