import Foundation

public class StatisticsService {
    private static var instances: [String: StatisticsService] = [:]
    
    // Static properties to hold the total counts
    private static var totalPrograms: Int = 0
    private static var totalPrograms1: Int = 0
    private static var totalPrograms10: Int = 0

    public static func getInstance(for engineName: String) -> StatisticsService {
        if let instance = instances[engineName] {
            return instance
        } else {
            let newInstance = StatisticsService(engineName: engineName, configManager: ConfigManager(configPath: "Sources/Fuzzilli/Util/logs/config.json"))
            instances[engineName] = newInstance
            return newInstance
        }
    }

    private let rawDataLogger: CSVDataManager
    private let logManager: LogManager
    private let programFileManager: ProgramFileManager

    private init(engineName: String, configManager: ConfigManager) {
        let rawCSVConfig = configManager.getCSVConfig(for: "rawData")
        let logFilePath = configManager.getLogFilePath()
        let programsBaseDirectory = configManager.getProgramsBaseDirectory()

        let rawDataFilePath = StatisticsService.addTimestampToFilePath(rawCSVConfig.filePath, engineName: engineName)
        let logFilePathWithTimestamp = StatisticsService.addTimestampToFilePath(logFilePath, engineName: engineName)

        self.rawDataLogger = CSVDataManager(filePath: rawDataFilePath, header: rawCSVConfig.header)
        self.logManager = LogManager(filePath: logFilePathWithTimestamp)
        self.programFileManager = ProgramFileManager(baseDirectory: programsBaseDirectory)
    }

    private static func addTimestampToFilePath(_ filePath: String, engineName: String) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyyMMdd_HHmmss"
        let timestamp = formatter.string(from: Date())
        
        let url = URL(fileURLWithPath: filePath)
        let directory = url.deletingLastPathComponent().path
        let filename = url.deletingPathExtension().lastPathComponent
        let extensionType = url.pathExtension
        
        return "\(directory)/\(filename)_\(timestamp).\(extensionType)"
    }

    public func logRawData(program: Program, fuzzer: Fuzzer, engineName: String) {
        
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let timeString = formatter.string(from: Date())
        
        let programID = program.id.uuidString
        let weight = program.weight
        let numEdges = fuzzer.evaluator.numEdges
        let numSecCov = fuzzer.evaluator.numSecCov
        let numSecCovTotal = fuzzer.evaluator.numSecCovTotal
        //let numSecPerEdge = fuzzer.evaluator.numSecPerEdge
        //let numSecPerEdgeTotal = fuzzer.evaluator.numSecPerEdgeTotal
        
        // Incrementar contadores de programas
        StatisticsService.totalPrograms += 1
        if weight == programWeight3 {
            StatisticsService.totalPrograms1 += 1
        } else if weight > programWeight3 {
            StatisticsService.totalPrograms10+=1
        }
        
        // OLD: Save the program code to a file, passing the weight parameter 
        // let codeFilePath = programFileManager.saveProgramCode(program.code, programID: program.id, weight: Int(weight))?.path ?? "Failed to save code"
        let codeFilePath = ""

        let jsCode = FuzzILLifter().lift(program)
        
       // IL to JS
        let jsFilePath = programFileManager.saveProgramAsProtobuf(program, programID: program.id, weight: Int(weight))?.path ?? "Failed to save JS code"
       

        //let logEntry = "\(engineName),\(timeString),\(programID),\(weight),\(numEdges),\(numSecCov),\(numSecCovTotal),\(numSecPerEdge),\(numSecPerEdgeTotal),\(StatisticsService.totalPrograms),\(StatisticsService.totalPrograms1),\(StatisticsService.totalPrograms10),\(codeFilePath)\n"
        let logEntry = "\(engineName),\(timeString),\(programID),\(weight),\(numEdges),\(numSecCov),\(numSecCovTotal),\(StatisticsService.totalPrograms),\(StatisticsService.totalPrograms1),\(StatisticsService.totalPrograms10),\(codeFilePath)\n"
        // let logEntry = "\(numSecCov),\(numSecCovTotal)\n"
        rawDataLogger.log(logEntry)
    }

    public func log(_ message: String) {
        logManager.log(message)
    }
}
