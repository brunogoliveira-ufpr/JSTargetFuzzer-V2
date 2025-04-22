import Foundation

public class StatisticsLogger {
    private let fileURL: URL

    public init(filePath: String, header: String) {
        self.fileURL = URL(fileURLWithPath: filePath)
        createFileIfNeeded(header: header)
    }

    private func createFileIfNeeded(header: String) {
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
            writeHeader(header: header)
        }
    }

    private func writeHeader(header: String) {
        do {
            let fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle.seekToEndOfFile()
            fileHandle.write(header.data(using: .utf8)!)
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
