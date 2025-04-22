// public class OOBMutator: BaseInstructionMutator {
    
//     // Initialize the mutator with a defined number of simultaneous mutations
//     public init() {
//         super.init(name: "OOBMutator", maxSimultaneousMutations: 3)
//     }

//     // Determines whether a given instruction can be mutated by this mutator
//     // It focuses on operations involving arrays, objects, and typed arrays (buffers)
//     public override func canMutate(_ instr: Instruction) -> Bool {
//         // Check if the operation is relevant for OOB mutation
//         // Example operations: GetProperty, SetProperty, LoadElement (arrays), CreateTypedArray (buffers)
//         return instr.op is GetProperty || instr.op is SetProperty || instr.op is LoadElement || instr.op is CreateTypedArray
//     }

//     // Mutates the given instruction, simulating out-of-bounds read/write vulnerabilities
//     public override func mutate(_ instr: Instruction, _ b: ProgramBuilder) {
//         b.adopt(instr)  // Retain the original instruction in the mutated program

//         // Switch based on the operation type to apply different mutations
//         switch instr.op {
        
//         // Case for manipulating object properties (GetProperty/SetProperty)
//         case is GetProperty, is SetProperty:
//             let objVar = b.randomVariable()  // Select a random variable to act as the object
//             let oobIndex = b.randomVariable()  // Generate an out-of-bounds index
//             b.append(Instruction(SetProperty(propertyName: b.randomPropertyName()), inputs: [objVar, oobIndex]))
//             // Mutation: This simulates an out-of-bounds access by forcing the engine to set a property
//             // in an object at an invalid index or property key.
//             // Purpose: Simulate how JavaScript handles properties that go beyond defined object fields.

//         // Case for array element manipulation (LoadElement)
//         case is LoadElement:
//             let arrayVar = b.randomVariable()  // Select a random array variable
//             let oobIndex = b.randomInt(max: 1000)  // Generate a large index to simulate an OOB read
//             b.append(Instruction(LoadElement(index: oobIndex), inputs: [arrayVar]))
//             // Mutation: This causes the engine to attempt to read from an array index that does not exist.
//             // Purpose: Simulate out-of-bounds read operations, often leading to data leakage or crashes.

//         // Case for manipulating TypedArrays (CreateTypedArray)
//         case is CreateTypedArray:
//             let typedArray = b.randomVariable()  // Select a random TypedArray variable
//             let oobIndex = b.randomInt(max: 2000)  // Generate a large index for an out-of-bounds write
//             b.append(Instruction(StoreElement(index: oobIndex), inputs: [typedArray, b.randomVariable()]))
//             // Mutation: This forces the engine to attempt writing outside the allocated memory of the TypedArray.
//             // Purpose: Simulate out-of-bounds writes, which can result in memory corruption and heap vulnerability.

//         // Default case: if the instruction does not match, no mutation is applied
//         default:
//             break
//         }
//     }
// }
