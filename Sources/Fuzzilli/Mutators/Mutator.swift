// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/// A mutator takes an existing program and mutates it in some way, thereby producing a new program.

import Foundation



public class Mutator: Contributor {
    /// Mutates the given program.
    ///
    /// - Parameters:
    ///   - program: The program to mutate.
    ///   - fuzzer: The fuzzer context for the mutation.
    /// - Returns: The mutated program or nil if the given program could not be mutated.
    public final func mutate(_ program: Program, for fuzzer: Fuzzer) -> Program? {
        let b = fuzzer.makeBuilder(forMutating: program)
        b.traceHeader("Mutating \(program.id) with \(name)")

        //var childProgram: Program? = nil

        let childProgram = mutate(program, using: b, for: fuzzer)
        //childProgram = mutate(program, using: b, for: fuzzer)

        // Adjust the weight of the child program if the parent weight is 1000
        //if program.weight == programWeight1, let child = childProgram {
        //    child.weight = programWeight2
        //}

        if let childProgram = childProgram {
            //logParentChildRelation(
            //    parentID: program.id,
            //    parentWeight: program.weight,
            //    childID: childProgram.id,
            //    childWeight: childProgram.weight
            //)
            childProgram.contributors.insert(self)
        }

        return childProgram
    }

    func mutate(_ program: Program, using b: ProgramBuilder, for fuzzer: Fuzzer) -> Program? {
        fatalError("This method must be overridden")
    }

    public override init(name: String? = nil) {
        let name = name ?? String(describing: type(of: self))
        super.init(name: name)
    }
}
