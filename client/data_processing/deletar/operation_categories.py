control_flow_ops = [
    'BeginFor', 'EndFor', 'BeginWhileLoop', 'EndWhileLoop', 'BeginDoWhileLoop', 'EndDoWhileLoop',
    'BeginRepeatLoop', 'EndRepeatLoop', 'BeginIf', 'EndIf', 'BeginElse', 'BeginSwitch', 'EndSwitch',
    'BeginSwitchCase', 'EndSwitchCase', 'BeginSwitchDefaultCase', 'BeginTry', 'EndTryCatchFinally',
    'BeginCatch', 'BeginFinally', 'BeginWith', 'EndWith'
]
class_ops = [
    'BeginClassDefinition', 'EndClassDefinition', 'BeginClassConstructor', 'EndClassConstructor',
    'BeginClassInstanceMethod', 'EndClassInstanceMethod', 'BeginClassStaticMethod', 'EndClassStaticMethod',
    'BeginClassPrivateStaticMethod', 'EndClassPrivateStaticMethod', 'BeginClassInstanceGetter',
    'EndClassInstanceGetter', 'BeginClassInstanceSetter', 'EndClassInstanceSetter', 'BeginClassStaticGetter',
    'EndClassStaticGetter', 'BeginClassStaticSetter', 'EndClassStaticSetter'
]
function_ops = [
    'BeginPlainFunction', 'EndPlainFunction', 'BeginAsyncFunction', 'EndAsyncFunction',
    'BeginGeneratorFunction', 'EndGeneratorFunction', 'BeginAsyncGeneratorFunction', 'EndAsyncGeneratorFunction',
    'BeginArrowFunction', 'EndArrowFunction', 'BeginAsyncArrowFunction', 'EndAsyncArrowFunction'
]
variable_assignment_ops = [
    'LoadInteger', 'LoadFloat', 'LoadString', 'LoadBoolean', 'LoadBigInt', 'LoadBuiltin', 
    'StoreNamedVariable', 'LoadNamedVariable', 'Reassign', 'DefineNamedVariable', 'Update'
]
exception_ops = [
    'BeginTry', 'EndTryCatchFinally', 'BeginCatch', 'BeginFinally', 'ThrowException'
]
expression_operator_ops = [
    'BinaryOperation', 'UnaryOperation', 'TernaryOperation', 'UpdateElement', 'UpdateProperty', 'UpdateComputedProperty', 'UpdatePrivateProperty', 'UpdateSuperProperty', 'TestIn', 'TestInstanceOf'
]
loop_ops = [
    'BeginFor', 'EndFor', 'BeginWhileLoop', 'EndWhileLoop', 'BeginDoWhileLoop', 'EndDoWhileLoop',
    'BeginRepeatLoop', 'EndRepeatLoop', 'BeginForInLoop', 'EndForInLoop', 'BeginForOfLoop', 'EndForOfLoop', 
    'LoopContinue', 'LoopBreak'
]
higher_order_function_ops = [
    'CallFunction', 'CallMethod', 'CallFunctionWithSpread', 'CallMethodWithSpread', 'CallComputedMethod', 'CallComputedMethodWithSpread', 'CallSuperConstructor', 'CallSuperMethod', 'Await'
]
object_property_ops = [
    'BeginObjectLiteral', 'EndObjectLiteral', 'ObjectLiteralAddProperty', 'ObjectLiteralAddComputedProperty',
    'ObjectLiteralAddElement', 'ObjectLiteralSetPrototype', 'ObjectLiteralCopyProperties', 'GetProperty',
    'SetProperty', 'DeleteProperty', 'GetElement', 'SetElement', 'DeleteElement', 'GetComputedProperty', 'SetComputedProperty',
    'ConfigureProperty', 'ConfigureComputedProperty', 'ConfigureElement', 'GetPrivateProperty', 'SetPrivateProperty'
]
scope_ops = [
    'BeginWith', 'EndWith', 'BeginBlockStatement', 'EndBlockStatement'
]
module_ops = [
    'Import', 'Export', 'ExportDefault'
]
event_handling_ops = [
    'AddEventListener', 'RemoveEventListener', 'DispatchEvent'
]
program_flow_ops = [
    'BeginIf', 'EndIf', 'BeginElse', 'BeginSwitch', 'EndSwitch', 'BeginSwitchCase', 'EndSwitchCase', 'BeginSwitchDefaultCase', 'Break', 'Continue', 'Return'
]
user_interaction_ops = [
    'Prompt', 'Alert', 'Confirm', 'Print'
]
