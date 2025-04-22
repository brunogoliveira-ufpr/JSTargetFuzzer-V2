if (typeof fuzzilli === 'undefined') fuzzilli = function() {};

const explore = (function() {


    const ProxyConstructor = Proxy;
    const BigIntConstructor = BigInt;
    const SetConstructor = Set;

    const ObjectPrototype = Object.prototype;

    const getOwnPropertyNames = Object.getOwnPropertyNames;
    const getPrototypeOf = Object.getPrototypeOf;
    const setPrototypeOf = Object.setPrototypeOf;
    const stringify = JSON.stringify;
    const hasOwnProperty = Object.hasOwn;
    const defineProperty = Object.defineProperty;
    const propertyValues = Object.values;
    const parseInteger = parseInt;
    const NumberIsInteger = Number.isInteger;
    const isNaN = Number.isNaN;
    const isFinite = Number.isFinite;
    const random = Math.random;
    const truncate = Math.trunc;
    const apply = Reflect.apply;
    const construct = Reflect.construct;
    const ReflectGet = Reflect.get;
    const ReflectSet = Reflect.set;
    const ReflectHas = Reflect.has;

    const concat = Function.prototype.call.bind(Array.prototype.concat);
    const findIndex = Function.prototype.call.bind(Array.prototype.findIndex);
    const includes = Function.prototype.call.bind(Array.prototype.includes);
    const shift = Function.prototype.call.bind(Array.prototype.shift);
    const pop = Function.prototype.call.bind(Array.prototype.pop);
    const push = Function.prototype.call.bind(Array.prototype.push);
    const filter = Function.prototype.call.bind(Array.prototype.filter);
    const execRegExp = Function.prototype.call.bind(RegExp.prototype.exec);
    const stringSlice = Function.prototype.call.bind(String.prototype.slice);
    const toUpperCase = Function.prototype.call.bind(String.prototype.toUpperCase);
    const numberToString = Function.prototype.call.bind(Number.prototype.toString);
    const bigintToString = Function.prototype.call.bind(BigInt.prototype.toString);
    const stringStartsWith = Function.prototype.call.bind(String.prototype.startsWith);
    const setAdd = Function.prototype.call.bind(Set.prototype.add);
    const setHas = Function.prototype.call.bind(Set.prototype.has);

    const MIN_SAFE_INTEGER = Number.MIN_SAFE_INTEGER;
    const MAX_SAFE_INTEGER = Number.MAX_SAFE_INTEGER;

    function EmptyArray() {
        let array = [];
        setPrototypeOf(array, null);
        return array;
    }

    function isObject(v) {
        return typeof v === 'object';
    }
    function isFunction(v) {
        return typeof v === 'function';
    }
    function isString(v) {
        return typeof v === 'string';
    }
    function isNumber(v) {
        return typeof v === 'number';
    }
    function isBigint(v) {
        return typeof v === 'bigint';
    }
    function isSymbol(v) {
        return typeof v === 'symbol';
    }
    function isBoolean(v) {
        return typeof v === 'boolean';
    }
    function isUndefined(v) {
        return typeof v === 'undefined';
    }

    function isInteger(n) {
        return isNumber(n) && NumberIsInteger(n) && n>= MIN_SAFE_INTEGER && n <= MAX_SAFE_INTEGER;
    }

    const simpleStringRegExp = /^[0-9a-zA-Z_$]+$/;
    function isSimpleString(s) {
        if (!isString(s)) throw "Non-string argument to isSimpleString: " + s;
        return s.length < 50 && execRegExp(simpleStringRegExp, s) !== null;
    }

    function isNumericString(s) {
        if (!isString(s)) return false;
        let number = parseInteger(s);
        return number >= MIN_SAFE_INTEGER && number <= MAX_SAFE_INTEGER && numberToString(number) === s;
    }

    function tryAccessProperty(prop, obj) {
        try {
            obj[prop];
            return true;
        } catch (e) {
            return false;
        }
    }

    function tryHasProperty(prop, obj) {
        try {
            return prop in obj;
        } catch (e) {
            return false;
        }
    }

    function tryGetProperty(prop, obj) {
        try {
            return obj[prop];
        } catch (e) {
            return undefined;
        }
    }

    function tryGetOwnPropertyNames(obj) {
        try {
            return getOwnPropertyNames(obj);
        } catch (e) {
            return new Array();
        }
    }

    function tryGetPrototypeOf(obj) {
        try {
            return getPrototypeOf(obj);
        } catch (e) {
            return null;
        }
    }

    function wrapInTryCatch(f) {
        return function() {
            try {
                return apply(f, this, arguments);
            } catch (e) {
                return false;
            }
        };
    }

    function probability(p) {
        if (p < 0 || p > 1) throw "Argument to probability must be a number between zero and one";
        return random() < p;
    }

    function randomIntBetween(start, end) {
        if (!isInteger(start) || !isInteger(end)) throw "Arguments to randomIntBetween must be integers";
        return truncate(random() * (end - start) + start);
    }

    function randomBigintBetween(start, end) {
        if (!isBigint(start) || !isBigint(end)) throw "Arguments to randomBigintBetween must be bigints";
        if (!isInteger(Number(start)) || !isInteger(Number(end))) throw "Arguments to randomBigintBetween must be representable as regular intergers";
        return BigIntConstructor(randomIntBetween(Number(start), Number(end)));
    }

    function randomIntBelow(n) {
        if (!isInteger(n)) throw "Argument to randomIntBelow must be an integer";
        return truncate(random() * n);
    }

    function randomElement(array) {
        return array[randomIntBelow(array.length)];
    }




    function enumeratePropertiesOf(o) {
        let properties = EmptyArray();

        let currentWeight = 1.0;
        properties.totalWeight = 0.0;
        function recordProperty(p) {
            push(properties, {name: p, weight: currentWeight});
            properties.totalWeight += currentWeight;
        }

        let obj = o;
        while (obj !== null) {
            let maybeLength = tryGetProperty('length', obj);
            if (isInteger(maybeLength) && maybeLength > 100) {
                for (let i = 0; i < 10; i++) {
                    let randomElement = randomIntBelow(maybeLength);
                    recordProperty(randomElement);
                }
            } else {
                let allOwnPropertyNames = tryGetOwnPropertyNames(obj);
                let allOwnElements = EmptyArray();
                for (let i = 0; i < allOwnPropertyNames.length; i++) {
                    let p = allOwnPropertyNames[i];
                    let index = parseInteger(p);
                    if (index >= 0 && index <= MAX_SAFE_INTEGER && numberToString(index) === p) {
                        push(allOwnElements, index);
                    } else if (isSimpleString(p) && tryAccessProperty(p, o)) {
                        recordProperty(p);
                    }
                }

                for (let i = 0; i < 10 && allOwnElements.length > 0; i++) {
                    let index = randomIntBelow(allOwnElements.length);
                    recordProperty(allOwnElements[index]);
                    allOwnElements[index] = pop(allOwnElements);
                }
            }

            obj = tryGetPrototypeOf(obj);
            currentWeight /= 2.0;

            if (obj === ObjectPrototype) {
                currentWeight /= 8.0;

                if (properties.length == 0) {
                    return properties;
                }
            }
        }

        return properties;
    }

    function randomPropertyOf(o) {
        let properties = enumeratePropertiesOf(o);

        if (properties.length === 0) {
            return null;
        }

        let selectedProperty;
        let remainingWeight = random() * properties.totalWeight;
        for (let i = 0; i < properties.length; i++) {
            let candidate = properties[i];
            remainingWeight -= candidate.weight;
            if (remainingWeight < 0) {
                selectedProperty = candidate.name;
                break;
            }
        }

        if (!tryHasProperty(selectedProperty, o)) return null;

        return selectedProperty;
    }



    const OP_CALL_FUNCTION = 'CALL_FUNCTION';
    const OP_CONSTRUCT = 'CONSTRUCT';
    const OP_CALL_METHOD = 'CALL_METHOD';
    const OP_CONSTRUCT_METHOD = 'CONSTRUCT_METHOD';
    const OP_GET_PROPERTY = 'GET_PROPERTY';
    const OP_SET_PROPERTY = 'SET_PROPERTY';
    const OP_DELETE_PROPERTY = 'DELETE_PROPERTY';

    const OP_ADD = 'ADD';
    const OP_SUB = 'SUB';
    const OP_MUL = 'MUL';
    const OP_DIV = 'DIV';
    const OP_MOD = 'MOD';
    const OP_INC = 'INC';
    const OP_DEC = 'DEC';
    const OP_NEG = 'NEG';

    const OP_LOGICAL_AND = 'LOGICAL_AND';
    const OP_LOGICAL_OR = 'LOGICAL_OR';
    const OP_LOGICAL_NOT = 'LOGICAL_NOT';

    const OP_BITWISE_AND = 'BITWISE_AND';
    const OP_BITWISE_OR = 'BITWISE_OR';
    const OP_BITWISE_XOR = 'BITWISE_XOR';
    const OP_LEFT_SHIFT = 'LEFT_SHIFT';
    const OP_SIGNED_RIGHT_SHIFT = 'SIGNED_RIGHT_SHIFT';
    const OP_UNSIGNED_RIGHT_SHIFT = 'UNSIGNED_RIGHT_SHIFT';
    const OP_BITWISE_NOT = 'BITWISE_NOT';

    const OP_COMPARE_EQUAL = 'COMPARE_EQUAL';
    const OP_COMPARE_STRICT_EQUAL = 'COMPARE_STRICT_EQUAL';
    const OP_COMPARE_NOT_EQUAL = 'COMPARE_NOT_EQUAL';
    const OP_COMPARE_STRICT_NOT_EQUAL = 'COMPARE_STRICT_NOT_EQUAL';
    const OP_COMPARE_GREATER_THAN = 'COMPARE_GREATER_THAN';
    const OP_COMPARE_LESS_THAN = 'COMPARE_LESS_THAN';
    const OP_COMPARE_GREATER_THAN_OR_EQUAL = 'COMPARE_GREATER_THAN_OR_EQUAL';
    const OP_COMPARE_LESS_THAN_OR_EQUAL = 'COMPARE_LESS_THAN_OR_EQUAL';
    const OP_TEST_IS_NAN = 'TEST_IS_NAN';
    const OP_TEST_IS_FINITE = 'TEST_IS_FINITE';

    const OP_SYMBOL_REGISTRATION = 'SYMBOL_REGISTRATION';

    function Action(operation, inputs = EmptyArray()) {
        this.operation = operation;
        this.inputs = inputs;
        this.isGuarded = false;
    }

    function GuardedAction(operation, inputs = EmptyArray()) {
        this.operation = operation;
        this.inputs = inputs;
        this.isGuarded = true;
    }

    const NO_ACTION = null;

    function ArgumentInput(index) {
        if (!isInteger(index)) throw "ArgumentInput index is not an integer: " + index;
        return { argument: { index } };
    }
    function SpecialInput(name) {
        if (!isString(name) || !isSimpleString(name)) throw "SpecialInput name is not a (simple) string: " + name;
        return { special: { name } };
    }
    function IntInput(value) {
        if (!isInteger(value)) throw "IntInput value is not an integer: " + value;
        return { int: { value } };
    }
    function FloatInput(value) {
        if (!isNumber(value) || !isFinite(value)) throw "FloatInput value is not a (finite) number: " + value;
        return { float: { value } };
    }
    function BigintInput(value) {
        if (!isBigint(value)) throw "BigintInput value is not a bigint: " + value;
        return { bigint: { value: bigintToString(value) } };
    }
    function StringInput(value) {
        if (!isString(value) || !isSimpleString(value)) throw "StringInput value is not a (simple) string: " + value;
        return { string: { value } };
    }

    function isArgumentInput(input) { return hasOwnProperty(input, 'argument'); }
    function isSpecialInput(input) { return hasOwnProperty(input, 'special'); }
    function isIntInput(input) { return hasOwnProperty(input, 'int'); }
    function isFloatInput(input) { return hasOwnProperty(input, 'float'); }
    function isBigintInput(input) { return hasOwnProperty(input, 'bigint'); }
    function isStringInput(input) { return hasOwnProperty(input, 'string'); }

    function getArgumentInputIndex(input) { return input.argument.index; }
    function getSpecialInputName(input) { return input.special.name; }
    function getIntInputValue(input) { return input.int.value; }
    function getFloatInputValue(input) { return input.float.value; }
    function getBigintInputValue(input) { return BigIntConstructor(input.bigint.value); }
    function getStringInputValue(input) { return input.string.value; }

    const ACTION_HANDLERS = {
      [OP_CALL_FUNCTION]: (inputs, currentThis) => { let f = shift(inputs); return apply(f, currentThis, inputs); },
      [OP_CONSTRUCT]: (inputs) => { let c = shift(inputs); return construct(c, inputs); },
      [OP_CALL_METHOD]: (inputs) => { let o = shift(inputs); let m = shift(inputs); return apply(o[m], o, inputs); },
      [OP_CONSTRUCT_METHOD]: (v, inputs) => { let o = shift(inputs); let m = shift(inputs); return construct(o[m], inputs); },
      [OP_GET_PROPERTY]: (inputs) => { let o = inputs[0]; let p = inputs[1]; return o[p]; },
      [OP_SET_PROPERTY]: (inputs) => { let o = inputs[0]; let p = inputs[1]; let v = inputs[2]; o[p] = v; },
      [OP_DELETE_PROPERTY]: (inputs) => { let o = inputs[0]; let p = inputs[1]; return delete o[p]; },
      [OP_ADD]: (inputs) => inputs[0] + inputs[1],
      [OP_SUB]: (inputs) => inputs[0] - inputs[1],
      [OP_MUL]: (inputs) => inputs[0] * inputs[1],
      [OP_DIV]: (inputs) => inputs[0] / inputs[1],
      [OP_MOD]: (inputs) => inputs[0] % inputs[1],
      [OP_INC]: (inputs) => inputs[0]++,
      [OP_DEC]: (inputs) => inputs[0]--,
      [OP_NEG]: (inputs) => -inputs[0],
      [OP_LOGICAL_AND]: (inputs) => inputs[0] && inputs[1],
      [OP_LOGICAL_OR]: (inputs) => inputs[0] || inputs[1],
      [OP_LOGICAL_NOT]: (inputs) => !inputs[0],
      [OP_BITWISE_AND]: (inputs) => inputs[0] & inputs[1],
      [OP_BITWISE_OR]: (inputs) => inputs[0] | inputs[1],
      [OP_BITWISE_XOR]: (inputs) => inputs[0] ^ inputs[1],
      [OP_LEFT_SHIFT]: (inputs) => inputs[0] << inputs[1],
      [OP_SIGNED_RIGHT_SHIFT]: (inputs) => inputs[0] >> inputs[1],
      [OP_UNSIGNED_RIGHT_SHIFT]: (inputs) => inputs[0] >>> inputs[1],
      [OP_BITWISE_NOT]: (inputs) => ~inputs[0],
      [OP_COMPARE_EQUAL]: (inputs) => inputs[0] == inputs[1],
      [OP_COMPARE_STRICT_EQUAL]: (inputs) => inputs[0] === inputs[1],
      [OP_COMPARE_NOT_EQUAL]: (inputs) => inputs[0] != inputs[1],
      [OP_COMPARE_STRICT_NOT_EQUAL]: (inputs) => inputs[0] !== inputs[1],
      [OP_COMPARE_GREATER_THAN]: (inputs) => inputs[0] > inputs[1],
      [OP_COMPARE_LESS_THAN]: (inputs) => inputs[0] < inputs[1],
      [OP_COMPARE_GREATER_THAN_OR_EQUAL]: (inputs) => inputs[0] >= inputs[1],
      [OP_COMPARE_LESS_THAN_OR_EQUAL]: (inputs) => inputs[0] <= inputs[1],
      [OP_TEST_IS_NAN]: (inputs) => Number.isNaN(inputs[0]),
      [OP_TEST_IS_FINITE]: (inputs) => Number.isFinite(inputs[0]),
      [OP_SYMBOL_REGISTRATION]: (inputs) => Symbol.for(inputs[0].description),
    };

    function execute(action, context) {
        if (action === NO_ACTION) {
            return true;
        }

        let concreteInputs = EmptyArray();
        for (let i = 0; i < action.inputs.length; i++) {
            let input = action.inputs[i];
            if (isArgumentInput(input)) {
                let index = getArgumentInputIndex(input);
                if (index >= context.arguments.length) throw "Invalid argument index: " + index;
                push(concreteInputs, context.arguments[index]);
            } else if (isSpecialInput(input)) {
                let name = getSpecialInputName(input);
                if (!hasOwnProperty(context.specialValues, name)) throw "Unknown special value: " + name;
                push(concreteInputs, context.specialValues[name]);
            } else if (isIntInput(input)) {
                push(concreteInputs, getIntInputValue(input));
            } else if (isFloatInput(input)) {
                push(concreteInputs, getFloatInputValue(input));
            } else if (isBigintInput(input)) {
                push(concreteInputs, getBigintInputValue(input));
            } else if (isStringInput(input)) {
                push(concreteInputs, getStringInputValue(input));
            } else {
                throw "Unknown action input: " + stringify(input);
            }
        }

        let handler = ACTION_HANDLERS[action.operation];
        if (isUndefined(handler)) throw "Unhandled operation " + action.operation;

        try {
            context.output = handler(concreteInputs, context.currentThis);
            if (action.isGuarded) action.isGuarded = false;
        } catch (e) {
            return action.isGuarded;
        }

        return true;
    }

    const SHIFT_OPS = [OP_LEFT_SHIFT, OP_SIGNED_RIGHT_SHIFT, OP_UNSIGNED_RIGHT_SHIFT];
    const BIGINT_SHIFT_OPS = [OP_LEFT_SHIFT, OP_SIGNED_RIGHT_SHIFT];
    const BITWISE_OPS = [OP_BITWISE_OR, OP_BITWISE_AND, OP_BITWISE_XOR];
    const ARITHMETIC_OPS = [OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD];
    const UNARY_OPS = [OP_INC, OP_DEC, OP_NEG, OP_BITWISE_NOT];
    const COMPARISON_OPS = [OP_COMPARE_EQUAL, OP_COMPARE_STRICT_EQUAL, OP_COMPARE_NOT_EQUAL, OP_COMPARE_STRICT_NOT_EQUAL, OP_COMPARE_GREATER_THAN, OP_COMPARE_LESS_THAN, OP_COMPARE_GREATER_THAN_OR_EQUAL, OP_COMPARE_LESS_THAN_OR_EQUAL];
    const BOOLEAN_BINARY_OPS = [OP_LOGICAL_AND, OP_LOGICAL_OR];
    const BOOLEAN_UNARY_OPS = [OP_LOGICAL_NOT];


    const customPropertyNames = ["a", "b", "c", "d", "e", "f", "g", "h"];

    const MAX_PARAMETERS = 10;

    const WELL_KNOWN_INTEGERS = filter([-9223372036854775808, -9223372036854775807, -9007199254740992, -9007199254740991, -9007199254740990, -4294967297, -4294967296, -4294967295, -2147483649, -2147483648, -2147483647, -1073741824, -536870912, -268435456, -65537, -65536, -65535, -4096, -1024, -256, -128, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 64, 127, 128, 129, 255, 256, 257, 512, 1000, 1024, 4096, 10000, 65535, 65536, 65537, 268435439, 268435440, 268435441, 536870887, 536870888, 536870889, 268435456, 536870912, 1073741824, 1073741823, 1073741824, 1073741825, 2147483647, 2147483648, 2147483649, 4294967295, 4294967296, 4294967297, 9007199254740990, 9007199254740991, 9007199254740992, 9223372036854775807], isInteger);
    const WELL_KNOWN_NUMBERS = concat(WELL_KNOWN_INTEGERS, [-1e6, -1e3, -5.0, -4.0, -3.0, -2.0, -1.0, -0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 1e3, 1e6]);
    const WELL_KNOWN_BIGINTS = [-9223372036854775808n, -9223372036854775807n, -9007199254740992n, -9007199254740991n, -9007199254740990n, -4294967297n, -4294967296n, -4294967295n, -2147483649n, -2147483648n, -2147483647n, -1073741824n, -536870912n, -268435456n, -65537n, -65536n, -65535n, -4096n, -1024n, -256n, -128n, -2n, -1n, 0n, 1n, 2n, 3n, 4n, 5n, 6n, 7n, 8n, 9n, 10n, 16n, 64n, 127n, 128n, 129n, 255n, 256n, 257n, 512n, 1000n, 1024n, 4096n, 10000n, 65535n, 65536n, 65537n, 268435439n, 268435440n, 268435441n, 536870887n, 536870888n, 536870889n, 268435456n, 536870912n, 1073741824n, 1073741823n, 1073741824n, 1073741825n, 2147483647n, 2147483648n, 2147483649n, 4294967295n, 4294967296n, 4294967297n, 9007199254740990n, 9007199254740991n, 9007199254740992n, 9223372036854775807n];



    let exploreArguments;

    let exploredValueInput;

    let currentlyExploring = false;


    const results = { __proto__: null };

    function reportError(msg) {
        fuzzilli('FUZZILLI_PRINT', 'EXPLORE_ERROR: ' + msg);
    }

    function recordFailure(id) {
        delete results[id];
        defineProperty(results, id, {__proto__: null, value: NO_ACTION});

        fuzzilli('FUZZILLI_PRINT', 'EXPLORE_FAILURE: ' + id);
    }

    function recordAction(id, action) {
        if (hasOwnProperty(results, id)) {
            throw "Duplicate action for " + id;
        }

        if (action === NO_ACTION) {
            return recordFailure(id);
        }

        action.id = id;

        defineProperty(results, id, {__proto__: null, value: action, configurable: true});

        fuzzilli('FUZZILLI_PRINT', 'EXPLORE_ACTION: ' + stringify(action));
    }

    function hasActionFor(id) {
        return hasOwnProperty(results, id);
    }

    function getActionFor(id) {
        return results[id];
    }

    let Inputs = {
        randomArgument() {
            return new ArgumentInput(randomIntBelow(exploreArguments.length));
        },

        randomArguments(n) {
            let args = EmptyArray();
            for (let i = 0; i < n; i++) {
                push(args, new ArgumentInput(randomIntBelow(exploreArguments.length)));
            }
            return args;
        },

        randomArgumentForReplacing(propertyName, obj) {
            let curValue = tryGetProperty(propertyName, obj);
            if (isUndefined(curValue)) {
                return Inputs.randomArgument();
            }

            function isCompatible(arg) {
                let sameType = typeof curValue === typeof arg;
                if (sameType && isObject(curValue)) {
                    sameType = arg instanceof curValue.constructor;
                }
                return sameType;
            }

            let idx = findIndex(exploreArguments, wrapInTryCatch(isCompatible));
            if (idx != -1) return new ArgumentInput(idx);
            return Inputs.randomArgument();
        },

        randomInt() {
            let idx = findIndex(exploreArguments, isInteger);
            if (idx != -1) return new ArgumentInput(idx);
            return new IntInput(randomElement(WELL_KNOWN_INTEGERS));
        },

        randomNumber() {
            let idx = findIndex(exploreArguments, isNumber);
            if (idx != -1) return new ArgumentInput(idx);
            return new FloatInput(randomElement(WELL_KNOWN_NUMBERS));
        },

        randomBigint() {
            let idx = findIndex(exploreArguments, isBigint);
            if (idx != -1) return new ArgumentInput(idx);
            return new BigintInput(randomElement(WELL_KNOWN_BIGINTS));
        },

        randomIntBetween(start, end) {
            if (!isInteger(start) || !isInteger(end)) throw "Arguments to randomIntBetween must be integers";
            let idx = findIndex(exploreArguments, wrapInTryCatch((e) => NumberIsInteger(e) && (e >= start) && (e < end)));
            if (idx != -1) return new ArgumentInput(idx);
            return new IntInput(randomIntBetween(start, end));
        },

        randomBigintBetween(start, end) {
            if (!isBigint(start) || !isBigint(end)) throw "Arguments to randomBigintBetween must be bigints";
            if (!isInteger(Number(start)) || !isInteger(Number(end))) throw "Arguments to randomBigintBetween must be representable as regular integers";
            let idx = findIndex(exploreArguments, wrapInTryCatch((e) => (e >= start) && (e < end)));
            if (idx != -1) return new ArgumentInput(idx);
            return new BigintInput(randomBigintBetween(start, end));
        },

        randomNumberCloseTo(v) {
            if (!isFinite(v)) throw "Argument to randomNumberCloseTo is not a finite number: " + v;
            let idx = findIndex(exploreArguments, wrapInTryCatch((e) => (e >= v - 10) && (e <= v + 10)));
            if (idx != -1) return new ArgumentInput(idx);
            let step = randomIntBetween(-10, 10);
            let value = v + step;
            if (isInteger(value)) {
              return new IntInput(value);
            } else {
              return new FloatInput(v + step);
            }
        },

        randomBigintCloseTo(v) {
            if (!isBigint(v)) throw "Argument to randomBigintCloseTo is not a bigint: " + v;
            let idx = findIndex(exploreArguments, wrapInTryCatch((e) => (e >= v - 10n) && (e <= v + 10n)));
            if (idx != -1) return new ArgumentInput(idx);
            let step = randomBigintBetween(-10n, 10n);
            let value = v + step;
            return new BigintInput(value);
        }
    }

    function shouldTreatAsConstructor(f) {
        let name = tryGetProperty('name', f);

        if (!isString(name) || name.length < 1) {
            return probability(0.1);
        }

        if (name[0] === 'f' && !isNaN(parseInteger(stringSlice(name, 1)))) {
          return probability(0.2);
        }

        if (name[0] === toUpperCase(name[0])) {
          return probability(0.9);
        } else {
          return probability(0.1);
        }
    }

    function exploreObject(o) {
        if (o === null) {
            return NO_ACTION;
        }


        let propertyName = randomPropertyOf(o);

        if (propertyName === null) {
            let propertyNameInput = new StringInput(randomElement(customPropertyNames));
            return new Action(OP_SET_PROPERTY, [exploredValueInput, propertyNameInput, Inputs.randomArgument()]);
        } else if (isInteger(propertyName)) {
            let propertyNameInput = new IntInput(propertyName);
            if (probability(0.5)) {
                return new Action(OP_GET_PROPERTY, [exploredValueInput, propertyNameInput]);
            } else {
                let newValue = Inputs.randomArgumentForReplacing(propertyName, o);
                return new Action(OP_SET_PROPERTY, [exploredValueInput, propertyNameInput, newValue]);
            }
        } else if (isString(propertyName)) {
            let propertyNameInput = new StringInput(propertyName);
            let propertyValue = tryGetProperty(propertyName, o);
            if (isFunction(propertyValue)) {
                let numParameters = tryGetProperty('length', propertyValue);
                if (!isInteger(numParameters) || numParameters > MAX_PARAMETERS || numParameters < 0) return NO_ACTION;
                let inputs = EmptyArray();
                push(inputs, exploredValueInput);
                push(inputs, propertyNameInput);
                for (let i = 0; i < numParameters; i++) {
                    push(inputs, Inputs.randomArgument());
                }
                if (shouldTreatAsConstructor(propertyValue)) {
                  return new GuardedAction(OP_CONSTRUCT_METHOD, inputs);
                } else {
                  return new GuardedAction(OP_CALL_METHOD, inputs);
                }
            } else {
                if (probability(1/3)) {
                    propertyNameInput = new StringInput(randomElement(customPropertyNames));
                    return new Action(OP_SET_PROPERTY, [exploredValueInput, propertyNameInput, Inputs.randomArgument()]);
                } else if (probability(0.5)) {
                    return new Action(OP_GET_PROPERTY, [exploredValueInput, propertyNameInput]);
                } else {
                    let newValue = Inputs.randomArgumentForReplacing(propertyName, o);
                    return new Action(OP_SET_PROPERTY, [exploredValueInput, propertyNameInput, newValue]);
                }
            }
        } else {
          throw "Got unexpected property name from Inputs.randomPropertyOf(): " + propertyName;
        }
    }

    function exploreFunction(f) {
        if (probability(0.5)) {
            return exploreObject(f);
        }

        let numParameters = tryGetProperty('length', f);
        if (!isInteger(numParameters) || numParameters > MAX_PARAMETERS || numParameters < 0) {
            numParameters = 0;
        }
        let inputs = EmptyArray();
        push(inputs, exploredValueInput);
        for (let i = 0; i < numParameters; i++) {
            push(inputs, Inputs.randomArgument());
        }
        let operation = shouldTreatAsConstructor(f) ? OP_CONSTRUCT : OP_CALL_FUNCTION;
        return new GuardedAction(operation, inputs);
    }

    function exploreString(s) {
        if (probability(0.1) && isSimpleString(s)) {
            return new Action(OP_COMPARE_EQUAL, [exploredValueInput, new StringInput(s)]);
        } else {
            return exploreObject(new String(s));
        }
    }

    const ALL_NUMBER_OPERATIONS = concat(SHIFT_OPS, BITWISE_OPS, ARITHMETIC_OPS, UNARY_OPS);
    const ALL_NUMBER_OPERATIONS_AND_COMPARISONS = concat(ALL_NUMBER_OPERATIONS, COMPARISON_OPS);
    function exploreNumber(n) {
        let operation = randomElement(probability(0.5) ? ALL_NUMBER_OPERATIONS : ALL_NUMBER_OPERATIONS_AND_COMPARISONS);

        let action = new Action(operation);
        push(action.inputs, exploredValueInput);
        if (includes(COMPARISON_OPS, operation)) {
            if (isNaN(n)) {
                action.operation = OP_TEST_IS_NAN;
            } else if (!isFinite(n)) {
                action.operation = OP_TEST_IS_FINITE;
            } else {
                push(action.inputs, Inputs.randomNumberCloseTo(n));
            }
        } else if (includes(SHIFT_OPS, operation)) {
            push(action.inputs, Inputs.randomIntBetween(1, 32));
        } else if (includes(BITWISE_OPS, operation)) {
            push(action.inputs, Inputs.randomInt());
        } else if (includes(ARITHMETIC_OPS, operation)) {
            if (isInteger(n)) {
                push(action.inputs, Inputs.randomInt());
            } else {
                push(action.inputs, Inputs.randomNumber());
            }
        }
        return action;
    }

    const ALL_BIGINT_OPERATIONS = concat(BIGINT_SHIFT_OPS, BITWISE_OPS, ARITHMETIC_OPS, UNARY_OPS);
    const ALL_BIGINT_OPERATIONS_AND_COMPARISONS = concat(ALL_BIGINT_OPERATIONS, COMPARISON_OPS);
    function exploreBigint(b) {
        let operation = randomElement(probability(0.5) ? ALL_BIGINT_OPERATIONS : ALL_BIGINT_OPERATIONS_AND_COMPARISONS);

        let action = new Action(operation);
        push(action.inputs, exploredValueInput);
        if (includes(COMPARISON_OPS, operation)) {
            push(action.inputs, Inputs.randomBigintCloseTo(b));
        } else if (includes(BIGINT_SHIFT_OPS, operation)) {
            push(action.inputs, Inputs.randomBigintBetween(1n, 128n));
        } else if (includes(BITWISE_OPS, operation) || includes(ARITHMETIC_OPS, operation)) {
            push(action.inputs, Inputs.randomBigint());
        }
        return action;
    }

    function exploreSymbol(s) {
        return new Action(OP_SYMBOL_REGISTRATION, [exploredValueInput]);
    }

    const ALL_BOOLEAN_OPERATIONS = concat(BOOLEAN_BINARY_OPS, BOOLEAN_UNARY_OPS);
    function exploreBoolean(b) {
        let operation = randomElement(ALL_BOOLEAN_OPERATIONS);

        let action = new Action(operation);
        push(action.inputs, exploredValueInput);
        if (includes(BOOLEAN_BINARY_OPS, operation)) {
            push(action.inputs, Inputs.randomArgument());
        }
        return action;
    }

    function exploreValue(id, v) {
        if (isObject(v)) {
            return exploreObject(v);
        } else if (isFunction(v)) {
            return exploreFunction(v);
        } else if (isString(v)) {
            return exploreString(v);
        } else if (isNumber(v)) {
            return exploreNumber(v);
        } else if (isBigint(v)) {
            return exploreBigint(v);
        } else if (isSymbol(v)) {
            return exploreSymbol(v);
        } else if (isBoolean(v)) {
            return exploreBoolean(v);
        } else if (isUndefined(v)) {
            return NO_ACTION;
        } else {
            throw "Unexpected value type: " + typeof v;
        }
    }

    function explore(id, v, currentThis, args) {
        if (isUndefined(args) || args.length < 1) throw "Exploration requires at least one additional argument";

        if (currentlyExploring) return;
        currentlyExploring = true;

        exploreArguments = args;
        exploredValueInput = new SpecialInput("exploredValue");

        let action;
        if (hasActionFor(id)) {
            action = getActionFor(id);
        } else {
            action = exploreValue(id, v);
            recordAction(id, action);
        }

        let context = { arguments: args, specialValues: { "exploredValue": v }, currentThis: currentThis };
        let success = execute(action, context);

        if (!success) {
            recordFailure(id);
        }

        currentlyExploring = false;
    }

    function exploreWithErrorHandling(id, v, thisValue, args) {
        try {
            explore(id, v, thisValue, args);
        } catch (e) {
            let line = tryHasProperty('line', e) ? tryGetProperty('line', e) : tryGetProperty('lineNumber', e);
            if (isNumber(line)) {
                reportError("In line " + line + ": " + e);
            } else {
                reportError(e);
            }
        }
    }

    return exploreWithErrorHandling;
})();

const v0 = [-536870912];
const v1 = [6,17062,7,38482,-11,-9223372036854775808];
const v2 = [-1043144008,1000,-4294967297,14];
const v4 = new WeakMap();
const v5 = [-178006.00901462138,-502.2034902180734,NaN];
explore("v5", v5, this, [v4, v2, v1, v5, v0]);
const v6 = [318.8804884920132,-9.896186784169452e+306,-1.4546319624268671e+307,2.2250738585072014e-308,-141.1404114638317,651.5249145839391,-8.674159840388416e+307,-612.2791561483567,-8.35382525582563];
const v7 = [732.0730774382639,280.7631168959315,-1000.0,3.0,0.4504889843894504,-3.3323191972298165,-874768.6411152837,-1000000000000.0,-4.179065838242786e+307];
class C8 {
    a = v5;
    #toString(a10, a11, a12, a13) {
        explore("v11", a11, this, [v1, v0, a10, a11, v5]);
        explore("v13", a13, this, [v2, v4, a11, C8, v5]);
        super.a %= a11;
        super.b /= a11;
        explore("v14", WeakSet, this, [v2, WeakSet, a10, v7, a11]);
        new WeakSet();
        explore("v18", -1897762182, this, [a11, v4, -1897762182, this, a13]);
        return v4;
    }
}
const v19 = new C8();
const v20 = new C8();
const v21 = new C8();
explore("v21", v21, this, [v21, v6, v20, v2, v1]);
explore("v22", Date, this, [Date, v2, v6, v0, v19]);
const v23 = new Date();
explore("v24", 64, this, [C8, Date, v6, v21, v20]);
Int16Array.h = Int16Array;
const v26 = new Int16Array(64);
explore("v28", Float64Array, this, [v19, v6, 4, Float64Array, WeakMap]);
const v29 = Float64Array.name;
const v30 = new Float64Array(4);
v30[0] = v30;
const v32 = 345 <= 345;
explore("v33", Uint8Array, this, [v19, v4, C8, Float64Array, Uint8Array]);
const v34 = new Uint8Array(345);
const v35 = v34.BYTES_PER_ELEMENT;
class C39 {
    static 1073741824 = 1612537377;
    #p(a41) {
        explore("v41", a41, this, [64, v1, v20, a41, v30]);
        let v43 = 9007199254740991;
        let v44 = v43 + 1612537377;
        Math.random();
        v44--;
        Math.cos(1612537377);
        return v43++;
    }
    [0.6930799121345798] = 0.6930799121345798;
    static c;
    #g;
}
const v49 = C39[1073741824];
explore("v49", v49, this, [v32, v49, Float64Array, v0, v2]);
const v50 = new C39();
explore("v50", v50, this, [345, v26, v50, 1612537377, Float64Array]);
const v51 = new C39();
explore("v51", v51, this, [v21, Uint8Array, WeakMap, v29, C39]);
const v52 = new C39();
const v53 = v52?.constructor;
explore("v53", v53, this, [C8, v21, v7, v34, Date]);
let v54;
try { v54 = new v53(); } catch (e) {}
const v55 = v52.constructor;
explore("v55", v55, this, [v55, v6, 1073741825, 4, v0]);
let v56;
try { v56 = new v55(); } catch (e) {}
let v57;
try { v57 = new v55(); } catch (e) {}
const v58 = [v52,v52,0.6930799121345798];
const v59 = v58[2];
const v60 = v59 >>> v59;
const v61 = [v52,v58];
let v62;
try { v62 = v61.findLast(v55); } catch (e) {}
explore("v62", v62, this, [v56, v62, 4, v21, v49]);
const v63 = [1073741825,C39,v61,v61];
explore("v63", v63, this, [WeakMap, v63, v35, 1612537377, 1073741825]);
let v64;
try { v64 = v63.concat(0.6930799121345798); } catch (e) {}
explore("v64", v64, this, [v4, v62, v6, v29, v23]);
let v65;
try { v65 = v64.some(v64); } catch (e) {}
explore("v65", v65, this, [v65, v6, v2, v56, WeakMap]);
const v68 = new Uint16Array(14);
v68[1] = v68;
explore("v69", 127, this, [v26, v58, v30, 127, v20]);
const v71 = new Int32Array(127);
let v72 = 8;
const v73 = v72++;
let v75;
try { v75 = new Uint8ClampedArray(4, Uint8ClampedArray, 1612537377); } catch (e) {}
const v76 = new Uint8ClampedArray(v72);
explore("v76", v76, this, [v65, v29, v19, v68, v76]);
let v77;
try { v77 = v76.values(); } catch (e) {}
explore("v77", v77, this, [v75, 1612537377, 1073741825, v29, v77]);
const v78 = v77?.constructor;
explore("v78", v78, this, [v23, v32, v63, Uint8ClampedArray, Int32Array]);
let v79;
try { v79 = new v78(v76); } catch (e) {}
explore("v79", v79, this, [v23, v79, Int16Array, 1073741825, v68]);
const v80 = /[x]+/dmui;
const v81 = /q[]+/dvmgy;
const v82 = /(?<a>)/du;
let v83 = 64;
const v84 = v83--;
explore("v85", Int16Array, this, [Int16Array, v64, 1612537377, v26, v83]);
const v86 = Date.prototype;
v57 >>>= v64;
v30[Int16Array] = v32;
const v87 = v80 instanceof Int32Array;
explore("v87", v87, this, [v73, v19, v87, 14, v1]);
let v89 = -1722969848;
const v90 = Math.round(v56);
const v91 = v89 || v56;
const v92 = Math.exp(v91);
const v93 = v89++;
const v94 = v93 >>> v91;
let v95;
try { v95 = new Int16Array(1612537377, Int16Array, Uint8Array); } catch (e) {}
explore("v95", v95, this, [v77, v51, Float64Array, Uint16Array, 64]);
let v96;
try { v96 = new Int16Array(v52, Uint16Array, Uint16Array); } catch (e) {}
explore("v96", v96, this, [v59, v29, v96, v6, v94]);
let v97;
try { v97 = v96.some(v64); } catch (e) {}
const v98 = new Int16Array(v83);
const v99 = v98[45];
explore("v100", 3, this, [v51, v90, v68, v94, v92]);
const v102 = Int16Array.name;
const v103 = new Int16Array(3);
explore("v103", v103, this, [v63, v103, WeakMap, v53, v91]);
const v104 = v103?.constructor;
explore("v104", v104, this, [14, v104, v23, C39, v78]);
const v106 = new Float64Array();
class C107 {
}
class C108 {
    #n(a110) {
        explore("v109", this, this, [v94, this, a110, C39, v63]);
        explore("v110", a110, this, [v78, v60, v82, a110, this]);
    }
}
const v111 = v104.length;
let v112;
try { v112 = new v104(v61, Uint8ClampedArray, 3); } catch (e) {}
explore("v112", v112, this, [v23, Date, v78, v111, v112]);
let v113 = 61;
const v114 = v113 / v113;
explore("v114", v114, this, [v104, v114, Uint8ClampedArray, v50, v94]);
let v116;
try { v116 = new Int16Array(v82, v63, v63); } catch (e) {}
explore("v116", v116, this, [v4, v116, v61, v26, 4]);
const v117 = Int16Array.length;
explore("v117", v117, this, [v91, v97, Uint16Array, v49, v117]);
const v118 = v117 << v117;
const v119 = new Int16Array(v113);
const v120 = v119[7];
const v121 = v120 * v120;
explore("v121", v121, this, [v54, v63, v117, Int16Array, v86]);
const v122 = v121 + v121;
class C123 {
    static 536870887;
    constructor(a125, a126) {
        explore("v126", a126, this, [this, a125, v91, a126, v93]);
        this[2] = this;
        a125[1];
        const v128 = a126.length;
        explore("v128", v128, this, [v128, 4, a126, v50, 127]);
        const v129 = a125 & a125;
        this[2] = this;
        let v130;
        try { v130 = a125.from(v80); } catch (e) {}
        explore("v130", v130, this, [v26, C107, v72, v93, v130]);
        for (let v132 = 0; v132 < 25; v132++) {
            class C134 extends Array {
                constructor(a136, a137) {
                    explore("v136", a136, this, [a137, v59, a136, Float64Array, this]);
                    super(a136);
                    this[a137] %= 1133;
                    explore("v138", [0.5963328477523332,5.0,2.220446049250313e-16], this, [v128, v81, 345, v26, v58]);
                    [-1000000000000.0,-93.38544242416776,884021.2241825557,-1.7976931348623157e+308,2.220446049250313e-16,7.767066469745572,-833.6298837501688,1000.0];
                }
            }
            new C134(Array, 1133);
        }
        a126 === a126;
        v80[1073741825] = v78;
        a126?.[536870888];
        v78[this] = v2;
        const v144 = v98 >> a126;
        explore("v144", v144, this, [Math, v144, v83, v2, C8]);
        [64,Int16Array];
        !Math;
        const v147 = v20.a;
        let v151 = v129 & -8;
        explore("v151", v151, this, [Math, v130, v95, v151, v121]);
        const v152 = Math.max(v129);
        v151++;
        v129 || -8;
        const v155 = v103.__proto__;
        explore("v155", v155, this, [4, v62, v152, v84, 65535]);
        const v156 = v155?.fill;
        let v157;
        try { v157 = new v156(v72); } catch (e) {}
        explore("v157", v157, this, [a126, this, v62, v147, v157]);
        const v158 = v155.BYTES_PER_ELEMENT;
        explore("v158", v158, this, [v96, v61, v129, v55, v155]);
        v158 === v158;
        try { v155.reduce(a125); } catch (e) {}
        v113 &&= a126;
        const v163 = 8 / 8;
        v163 << v163;
    }
    set c(a167) {
        explore("v166", this, this, [a167, v119, v50, v112, v4]);
        explore("v167", a167, this, [v64, v0, v21, 3, this]);
        let {"e":v168,"g":v169,} = a167;
        explore("v168", v168, this, [v169, a167, this, v168, v116]);
        this > v168;
        this[8] = v98;
        for (let v171 = 0; v171 < 32; v171++) {
            explore("v171", v171, this, [Uint8Array, Int16Array, v171, Int16Array, v169]);
            v103["p" + v171] = v171;
        }
    }
}
let v174;
try { v174 = new C123(v82, Int16Array); } catch (e) {}
let v175;
try { v175 = new C123(v61, v61); } catch (e) {}
explore("v175", v175, this, [v98, v95, v102, v56, v54]);
const v176 = new C123(v83, 3);
explore("v176", v176, this, [v76, v112, v58, v57, 127]);
const v177 = new C123(Int16Array, v113);
v177[2] = v177;
const v178 = new C123(Int16Array, 3);
explore("v178", v178, this, [v79, v26, v104, v75, v64]);
const v179 = v178[2];
const v180 = v179[2];
explore("v180", v180, this, [v35, v121, Int16Array, v180, v75]);
v179[2] = v179;
new C123(Int16Array, v113);
const v182 = [];
let v183;
try { v183 = v182.with(v103, v102); } catch (e) {}
explore("v183", v183, this, [v183, v63, v77, v34, v78]);
const v184 = [Infinity,-1.7440943668712117e+307,-690.1469745267084,1000000000.0];
const v185 = v184?.groupToMap;
explore("v185", v185, this, [v78, v86, v103, v0, v19]);
let v186;
try { v186 = new v185(v61); } catch (e) {}
explore("v186", v186, this, [v32, v63, v4, v61, 1073741825]);
const v187 = [2.220446049250313e-16,1000000000.0,0.6421508525960655,-1.0];
const v188 = [3.0,-2.2250738585072014e-308,-1000000000.0];
explore("v188", v188, this, [v7, v51, v26, v111, v188]);
let v189;
try { v189 = v188.toSorted(v52); } catch (e) {}
let v190;
try { v190 = v188.copyWithin(Int16Array, v184); } catch (e) {}
explore("v190", v190, this, [v99, v104, v75, Float64Array, Int16Array]);
const v191 = v188[0];
const v192 = v191 ^ v191;
const v193 = [-4.0,0.3129128068897348,-1.6709464384558029e+308,5.52942036580264,-141.72976494770853,2.2250738585072014e-308,1.9128738095819434e+307];
explore("v193", v193, this, [v193, v80, v186, v57, v83]);
const v194 = v193?.some;
explore("v194", v194, this, [Int16Array, v194, Uint8Array, v116, Int16Array]);
let v195;
try { v195 = v194.bind(v119); } catch (e) {}
let v196;
try { v196 = v194(v81); } catch (e) {}
explore("v196", v196, this, [v186, v21, v196, v92, 345]);
let v197;
try { v197 = new v194(Int16Array); } catch (e) {}
explore("v197", v197, this, [v71, 0.6930799121345798, v62, v75, v191]);
const v198 = [-1000000.0,6.78476738360228e+307,1e-15];
explore("v198", v198, this, [v81, v75, C123, v198, v96]);
let v199;
try { v199 = v198.toSorted(v68); } catch (e) {}
let v200;
try { v200 = v198.entries(); } catch (e) {}
explore("v200", v200, this, [v193, C8, v186, v94, v63]);
v200.next();
v198.g = v198;
[1.0777506560049588,-4.0,-0.0,-533.4418220276043,Infinity];
const v203 = [-1.6528616820241986];
explore("v203", v203, this, [v111, v104, v19, v78, v203]);
v203[0] = v203;
const v204 = [3.0];
v204[0] = v204;
const v205 = [-3.7839805505167037e+307,2.2250738585072014e-308,-1e-15,231.25426429460185,0.5354214515760234,3.0,-1.7976931348623157e+308];
explore("v205", v205, this, [v205, v30, v65, v20, v29]);
class C206 {
    static n(a208, a209) {
        explore("v209", a209, this, [a208, this, a209, v90, v119]);
        [691836.0348632259,-4.0,-148.7620312582809,-1000000.0,-811094.5829977263,552544.6630049313];
        [0.5388570470605992,1e-15,-8.090702689373172e+307,-6.067507680581121e+307];
        [1.7976931348623157e+308,-1000.0,-0.0,-6.597213663863699,-5.0,-Infinity,7.771214230141901,-2.3738337473391727e+307];
    }
    #e = v188;
    static o(a214, a215, a216) {
        explore("v213", this, this, [this, v104, a215, v53, a216]);
        explore("v214", a214, this, [v64, v84, v89, v177, a215]);
        explore("v216", a216, this, [v82, v174, a214, v4, a216]);
        v193 ^ v184;
        let v219 = 14;
        explore("v219", v219, this, [a215, a214, v30, this, v203]);
        explore("v220", 2147483649, this, [2147483649, v122, v68, a214, Math]);
        let v222 = !(-v219);
        const v223 = v188 && v188;
        explore("v223", v223, this, [a214, v192, 2147483649, v82, 3]);
        const v224 = v219--;
        const v225 = v219 + v223;
        explore("v225", v225, this, [v224, v222, v219, Uint8ClampedArray, v225]);
        v222--;
        return v204;
    }
    100;
    static #a;
    e = v63;
    10 = v7;
    static #h = Uint8ClampedArray;
}
let v227;
try { v227 = new C206(); } catch (e) {}
const v228 = v227?.constructor;
explore("v228", v228, this, [v228, Math, v190, v120, Int16Array]);
let v229;
try { v229 = new v228(); } catch (e) {}
const v230 = new C206();
let v231;
try { v231 = v230.__lookupSetter__(v61); } catch (e) {}
explore("v231", v231, this, [v231, v197, 14, Uint8Array, v119]);
const v232 = v230?.constructor;
let v233;
try { v233 = new v232(); } catch (e) {}
const v234 = v233?.constructor;
try { new v234(); } catch (e) {}
let v236;
try { v236 = new v232(); } catch (e) {}
const v237 = v230?.constructor;
explore("v237", v237, this, [v51, v71, v87, v237, Float64Array]);
let v238;
try { v238 = v237.o(v76, v72, v102); } catch (e) {}
explore("v238", v238, this, [v19, v119, v197, v73, 1612537377]);
let v239;
try { v239 = new v237(); } catch (e) {}
const v240 = new C206();
const v241 = v240?.constructor;
explore("v241", v241, this, [v234, v86, v77, v106, 345]);
let v242;
try { v242 = new v241(); } catch (e) {}
const v243 = v240?.__defineSetter__;
explore("v243", v243, this, [v21, v106, v29, v116, v241]);
let v244;
try { v244 = new v243(v203, v198); } catch (e) {}
const v245 = new C206();
const v246 = v245?.hasOwnProperty;
explore("v246", v246, this, [v84, v228, v232, Int16Array, v246]);
let v247;
try { v247 = new v246(v26); } catch (e) {}
const v248 = v245?.constructor;
let v249;
try { v249 = v248.constructor(); } catch (e) {}
let v250;
try { v250 = v249(); } catch (e) {}
explore("v250", v250, this, [v247, v250, Date, v4, v229]);
let v251;
try { v251 = new v248(); } catch (e) {}
explore("v251", v251, this, [v184, v231, v199, v1, v7]);
const v252 = v251?.__lookupGetter__;
let v253;
try { v253 = new v252(Uint16Array); } catch (e) {}
const v254 = v245?.constructor;
explore("v254", v254, this, [v6, v254, v65, Int16Array, v253]);
const v255 = v254.name;
explore("v255", v255, this, [v255, 1073741825, v203, v192, v196]);
let v256;
try { v256 = new v254(); } catch (e) {}
explore("v256", v256, this, [v199, v76, v21, v84, v53]);
const v257 = v256?.__lookupSetter__;
explore("v257", v257, this, [v52, v199, v116, 64, v189]);
try { new v257(Int16Array); } catch (e) {}
let v259;
try { v259 = new v254(); } catch (e) {}
explore("v259", v259, this, [v259, v254, v52, v185, v174]);
const v260 = v259?.toString;
let v261;
try { v261 = new v260(); } catch (e) {}
explore("v261", v261, this, [14, Int16Array, v187, v259, 3]);
let v262;
try { v262 = v259.toString(); } catch (e) {}
v262[10] = v262;
const v263 = v259?.constructor;
let v264;
try { v264 = new v263(); } catch (e) {}
const v265 = v263.length;
explore("v265", v265, this, [v79, v265, v198, Float64Array, 345]);
let v266;
try { v266 = new v263(); } catch (e) {}
explore("v266", v266, this, [v175, v0, v54, v264, v266]);
const v267 = v266?.constructor;
explore("v267", v267, this, [v5, v244, Int32Array, v63, Int16Array]);
let v268;
try { v268 = new v267(); } catch (e) {}
explore("v268", v268, this, [v60, Float64Array, WeakMap, v102, v268]);
try { v268.valueOf(); } catch (e) {}
let v271;
try { v271 = new Set(); } catch (e) {}
explore("v271", v271, this, [v245, v34, v271, v72, v174]);
let v272;
try { v272 = new Set(); } catch (e) {}
const v273 = v272.size;
explore("v273", v273, this, [v273, v227, v203, v261, C8]);
Set.length = Set;
const v274 = new Set();
explore("v274", v274, this, [v23, v71, v64, v114, v195]);
let v275;
try { v275 = v274.has(v237); } catch (e) {}
const v276 = v30 << v30;
explore("v276", v276, this, [v94, v276, v252, Int32Array, v175]);
const v277 = v276 != v32;
explore("v278", 16, this, [v97, v193, v19, v120, 16]);
explore("v279", -9223372036854775808, this, [v79, -9223372036854775808, v77, v21, v87]);
const v281 = v275 || v275;
explore("v281", v281, this, [v2, v64, v281, 14, v118]);
try { v274.keys(); } catch (e) {}
class C283 extends Set {
    set g(a285) {
        explore("v285", a285, this, [a285, v50, v102, this, v264]);
        const v287 = Symbol.iterator;
        const o288 = {
        };
        explore("v292", o288, this, [v277, v98, this, v287, v50]);
    }
}
let v289;
try { v289 = new C283(); } catch (e) {}
let v290;
try { v290 = v289.keys(); } catch (e) {}
explore("v294", v290, this, [v290, v187, v242, C283, C39]);
class C291 {
    #p() {
        explore("v296", this, this, [this, v56, Int16Array, v237, Int16Array]);
    }
}
explore("v295", C291, this, [v248, v78, 1612537377, v93, v241]);
class C293 {
    constructor(a295, a296, a297, a298) {
        explore("v301", a297, this, [v234, a298, v281, a297, v0]);
        for (let v299 = 0; v299 < 32; v299++) {
            explore("v303", v299, this, [v299, a297, v94, a298, v86]);
            class C300 {
            }
            explore("v304", C300, this, [v299, C300, v205, this, v78]);
        }
    }
}
explore("v305", Float64Array, this, [v236, v241, 127, Float64Array, v0]);
class C302 extends Float64Array {
}
explore("v306", C302, this, [v272, v256, 4, v50, v191]);
class C304 extends Float64Array {
    get h() {
    }
    static #p(a307, a308, a309, a310) {
        explore("v311", a307, this, [v176, v256, a309, v182, v248]);
        explore("v312", a308, this, [v56, this, v87, C107, v274]);
        explore("v314", a310, this, [a309, Int16Array, a308, v50, Float64Array]);
    }
}
explore("v308", C304, this, [C8, C302, v240, v184, v246]);
const v312 = new WeakMap();
class C313 {
    constructor(a315) {
        explore("v318", this, this, [a315, this, v289, 1073741825, v186]);
    }
}
explore("v317", C313, this, [v57, v272, v265, v239, v79]);
C313.g = C313;
new C313(v312);
