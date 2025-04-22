import Foundation

public class CSVManager {
    private let fileURL: URL
    private let header: String

    public init(filePath: String, header: String) {
        self.fileURL = URL(fileURLWithPath: filePath)
        self.header = header
        createFileIfNeeded()
    }

    private func createFileIfNeeded() {
        let fileManager = FileManager.default
        let directoryURL = fileURL.deletingLastPathComponent()

        if !fileManager.fileExists(atPath: directoryURL.path) {
            do {
                try fileManager.createDirectory(atPath: directoryURL.path, withIntermediateDirectories: true, attributes: nil)
            } catch {
                print("Failed to create directory: \(error)")
                return
            }
        }

        if !fileManager.fileExists(atPath: fileURL.path) {
            fileManager.createFile(atPath: fileURL.path, contents: nil, attributes: nil)
            writeHeader()
        }
    }

    private func writeHeader() {
        do {
            let fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle.seekToEndOfFile()
            fileHandle.write((header + "\n").data(using: .utf8)!)
            fileHandle.closeFile()
        } catch {
            print("Failed to write header to file: \(error)")
        }
    }

    public func log(_ logEntry: String) {
        do {
            let fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle.seekToEndOfFile()
            fileHandle.write(logEntry.data(using: .utf8)!)
            fileHandle.closeFile()
        } catch {
            print("Failed to write to file: \(error)")
        }
    }
}
