import Foundation

public class DuplicateProgramHandler {
    private let filePath: String

    // Initialize the handler with a fixed file path in the execution root
    public init(fileName: String = "duplicate_programs.csv") {
        self.filePath = FileManager.default.currentDirectoryPath + "/" + fileName
        prepareCSV()
    }

    // Prepare the CSV file with the header if it doesn't exist
    private func prepareCSV() {
        let fileManager = FileManager.default
        if !fileManager.fileExists(atPath: filePath) {
            do {
                try "Program ID\n".write(toFile: filePath, atomically: true, encoding: .utf8)
            } catch {
                print("Error creating CSV file: \(error)")
            }
        }
    }

    // Append a new program ID to the CSV file
    public func logDuplicateProgramID(_ programID: UUID) {
        do {
            let entry = "\(programID.uuidString)\n"
            let handle = try FileHandle(forWritingTo: URL(fileURLWithPath: filePath))
            handle.seekToEndOfFile()
            handle.write(entry.data(using: .utf8)!)
            handle.closeFile()
        } catch {
            print("Error appending to CSV file: \(error)")
        }
    }
}
