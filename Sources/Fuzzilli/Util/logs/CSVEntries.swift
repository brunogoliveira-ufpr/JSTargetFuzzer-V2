struct CSVEntries {
    static func generalStatistics(timeString: String, numPrograms: Int, numProgramsWeightTen: Int, numProgramsWeightOne: Int, secCov: Double, totalSecCov: Double, numSecPerEdgeTotal: Double) -> String {
        return "\(timeString),\(numPrograms),\(numProgramsWeightTen),\(numProgramsWeightOne),\(secCov),\(totalSecCov),\(numSecPerEdgeTotal)\n"
    }

    static func detailedStatistics(timeString: String, accumulatedSecCovPerEdges: [Double], numSecPerEdgeTotal: Double) -> String {
        let secCovPerEdges = accumulatedSecCovPerEdges.map { "\($0)" }.joined(separator: ",")
        return "\(timeString),\(secCovPerEdges),\(numSecPerEdgeTotal)\n"
    }

    static func simpleSecCov(timeString: String, secCovPerEdge: Double) -> String {
        return "\(timeString),\(secCovPerEdge)\n"
    }
}
