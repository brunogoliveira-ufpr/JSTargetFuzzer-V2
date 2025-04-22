import Foundation

public class LogManager {
    private let fileURL: URL

    public init(filePath: String) {
        self.fileURL = URL(fileURLWithPath: filePath)
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
        }
    }

    public func log(_ message: String) {
        do {
            let fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle.seekToEndOfFile()
            let timestamp = DateFormatter.localizedString(from: Date(), dateStyle: .short, timeStyle: .medium)
            let logEntry = "[\(timestamp)] \(message)\n"
            fileHandle.write(logEntry.data(using: .utf8)!)
            fileHandle.closeFile()
        } catch {
            print("Failed to write to file: \(error)")
        }
    }
}
