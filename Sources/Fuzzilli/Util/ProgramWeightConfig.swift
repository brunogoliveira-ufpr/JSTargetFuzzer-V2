import Foundation

public struct ProgramWeightConfig {
    public static var weight: Double = 1000.0

    public static func load(from args: Arguments) {
        if let value = args["--program-weight"], let weightValue = Double(value) {
            weight = weightValue
            print("[Config] Program weight set to \(weight)")
        } else {
            print("[Config] Using default program weight: \(weight)")
        }
    }
}
