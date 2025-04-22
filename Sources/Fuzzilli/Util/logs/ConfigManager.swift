import Foundation

public class ConfigManager {
    private let config: [String: Any]

    public init(configPath: String) {
        let fullPath = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent(configPath).path
        do {
            let data = try Data(contentsOf: URL(fileURLWithPath: fullPath))
            self.config = try JSONSerialization.jsonObject(with: data, options: []) as! [String: Any]
        } catch {
            fatalError("Failed to load configuration file at path \(fullPath): \(error)")
        }
    }

    public func getLogFilePath() -> String {
        let logFilePath = config["logFilePath"] as! String
        return URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent(logFilePath).path
    }

    public func getCSVConfig(for key: String) -> (filePath: String, header: String) {
        let csvConfig = config["csvConfig"] as! [String: [String: String]]
        let configForKey = csvConfig[key]!
        let filePath = configForKey["filePath"]!
        let fullPath = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent(filePath).path
        return (filePath: fullPath, header: configForKey["header"]!)
    }
    
    public func getProgramsBaseDirectory() -> String {
        let baseDirectory = config["programsBaseDirectory"] as! String
        return URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent(baseDirectory).path
    }
}
