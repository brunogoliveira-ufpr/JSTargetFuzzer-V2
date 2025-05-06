| Loop & Condition               | Math Operations               | Read/Write Operations            | Function Call Generators             | Object & Array Generators            |
|-------------------------------|-------------------------------|----------------------------------|--------------------------------------|--------------------------------------|
| IfElseGenerator               | BinaryOperationGenerator      | PropertyRetrievalGenerator       | PlainFunctionGenerator               | ArrayGenerator                       |
| CompareWithIfElseGenerator    | UnaryOperationGenerator       | PropertyAssignmentGenerator      | ArrowFunctionGenerator               | IntArrayGenerator                    |
| SwitchBlockGenerator          | TernaryOperationGenerator     | PropertyUpdateGenerator          | GeneratorFunctionGenerator           | FloatArrayGenerator                  |
| SwitchCaseGenerator           | UpdateGenerator               | PropertyRemovalGenerator         | AsyncFunctionGenerator               | ObjectLiteralGenerator               |
| SwitchDefaultCaseGenerator    | ComparisonGenerator           | ElementRetrievalGenerator        | AsyncArrowFunctionGenerator          | ObjectLiteralPropertyGenerator       |
| SwitchCaseBreakGenerator      | TypeTestGenerator             | ElementAssignmentGenerator       | AsyncGeneratorFunctionGenerator      | ObjectLiteralElementGenerator        |
| WhileLoopGenerator            | InstanceOfGenerator           | ElementUpdateGenerator           | TrivialFunctionGenerator             | ObjectLiteralComputedPropertyGenerator |
| DoWhileLoopGenerator          | InGenerator                   | ElementRemovalGenerator          | FunctionWithArgumentsAccessGenerator | ObjectLiteralCopyPropertiesGenerator |
| SimpleForLoopGenerator        | NumberComputationGenerator    | ComputedPropertyRetrievalGenerator | ThisGenerator                     | ObjectLiteralPrototypeGenerator      |
| ComplexForLoopGenerator       |                               | ComputedPropertyAssignmentGenerator | ArgumentsAccessGenerator         | ObjectLiteralMethodGenerator         |
| ForInLoopGenerator            |                               | ComputedPropertyUpdateGenerator  | MethodCallGenerator                  | ObjectLiteralComputedMethodGenerator |
| ForOfLoopGenerator            |                               | PrivatePropertyRetrievalGenerator | MethodCallWithSpreadGenerator        | ObjectLiteralGetterGenerator         |
| ForOfWithDestructLoopGenerator|                               | PrivatePropertyAssignmentGenerator| ComputedMethodCallGenerator          | ObjectLiteralSetterGenerator         |
| RepeatLoopGenerator           |                               | PrivatePropertyUpdateGenerator   | ComputedMethodCallWithSpreadGenerator| ClassDefinitionGenerator             |
| LoopBreakGenerator            |                               | PropertyConfigurationGenerator   | FunctionCallGenerator                | ClassConstructorGenerator            |
| ContinueGenerator             |                               | ElementConfigurationGenerator    | ConstructorCallGenerator             | ClassInstancePropertyGenerator       |
| TryCatchGenerator             |                               | ComputedPropertyConfigurationGenerator | FunctionCallWithSpreadGenerator | ClassInstanceElementGenerator        |
| ThrowGenerator                |                               | SuperPropertyRetrievalGenerator  | ConstructorCallWithSpreadGenerator   | ClassInstanceComputedPropertyGenerator |
| EvalGenerator                 |                               | SuperPropertyAssignmentGenerator | SubroutineReturnGenerator            | ClassInstanceMethodGenerator         |
| BlockStatementGenerator       |                               | SuperPropertyUpdateGenerator     | YieldGenerator                       | ClassInstanceGetterGenerator         |
|                               |                               | WellKnownPropertyLoadGenerator   | AwaitGenerator                       | ClassInstanceSetterGenerator         |
|                               |                               | WellKnownPropertyStoreGenerator  | SuperMethodCallGenerator             | ClassStaticPropertyGenerator         |
|                               |                               | PrototypeAccessGenerator         | PrivateMethodCallGenerator           | ClassStaticElementGenerator          |
|                               |                               | PrototypeOverwriteGenerator      | MethodCallWithDifferentThisGenerator | ClassStaticComputedPropertyGenerator |
|                               |                               | CallbackPropertyGenerator        | ImitationGenerator                   | ClassStaticMethodGenerator           |
|                               |                               | LengthChangeGenerator            | WeirdClassGenerator                  | ClassPrivateInstancePropertyGenerator|
|                               |                               | ElementKindChangeGenerator       | ProxyGenerator                       | ClassPrivateInstanceMethodGenerator  |
|                               |                               | DupGenerator                     | PromiseGenerator                     | ClassPrivateStaticPropertyGenerator  |
|                               |                               | ReassignmentGenerator            |                                      | ClassPrivateStaticMethodGenerator    |
|                               |                               | NamedVariableLoadGenerator       |                                      | ArrayWithSpreadGenerator             |
|                               |                               | NamedVariableStoreGenerator      |                                      | BuiltinObjectInstanceGenerator       |
|                               |                               | NamedVariableDefinitionGenerator |                                      | TypedArrayGenerator                  |
|                               |                               |                                  |                                      | RegExpGenerator                      |
|                               |                               |                                  |                                      | ProxyGenerator                       |
|                               |                               |                                  |                                      | WithStatementGenerator               |
|                               |                               |                                  |                                      | DestructArrayGenerator               |
|                               |                               |                                  |                                      | DestructArrayAndReassignGenerator    |
|                               |                               |                                  |                                      | DestructObjectGenerator              |
|                               |                               |                                  |                                      | DestructObjectAndReassignGenerator   |
|                               |                               |                                  |                                      | ResizableArrayBufferGenerator        |
|                               |                               |                                  |                                      | GrowableSharedArrayBufferGenerator   |
|                               |                               |                                  |                                      | FastToSlowPropertiesGenerator        |
|                               |                               |                                  |                                      | IteratorGenerator                    |
