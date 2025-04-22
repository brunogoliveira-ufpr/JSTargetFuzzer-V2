if (typeof fuzzilli === 'undefined') fuzzilli = function() {};

const Probe = (function() {


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

    const PROPERTY_LOAD = "loads";
    const PROPERTY_STORE = "stores";

    const PROPERTY_NOT_FOUND = 0;
    const PROPERTY_FOUND = 1;

    let results = { __proto__: null };

    function reportError(msg) {
        fuzzilli('FUZZILLI_PRINT', 'PROBING_ERROR: ' + msg);
    }

    function reportResults() {
        fuzzilli('FUZZILLI_PRINT', 'PROBING_RESULTS: ' + stringify(results));
    }

    function recordAction(action, id, target, key) {
        let outcome = PROPERTY_NOT_FOUND;
        if (ReflectHas(target, key)) {
            outcome = PROPERTY_FOUND;
        }

        let keyString = key;
        if (typeof keyString !== 'string') {
            try {
                keyString = key.toString();
                if (typeof keyString !== 'string') throw 'not a string';
            } catch(e) {
                return;
            }
        }

        if (!isSimpleString(keyString) && !isNumericString(keyString) && !isSymbol(key)) {
            return;
        }

        if (isSymbol(key) && !stringStartsWith(keyString, 'Symbol(Symbol.')) {
            return;
        }

        if (!hasOwnProperty(results, id)) {
            results[id] = { [PROPERTY_LOAD]: { __proto__: null }, [PROPERTY_STORE]: { __proto__: null } };
        }

        results[id][action][keyString] = outcome;
    }

    function recordActionWithErrorHandling(action, id, target, key) {
        try {
            recordAction(action, id, target, key);
        } catch(e) {
            reportError(e);
        }
    }

    function probe(id, value) {
        let originalPrototype, newPrototype;
        let handler = {
            get(target, key, receiver) {
                if (key === '__proto__' && receiver === value) return originalPrototype;
                if (receiver === newPrototype) return ReflectGet(target, key);
                recordActionWithErrorHandling(PROPERTY_LOAD, id, target, key);
                return ReflectGet(target, key, receiver);
            },
            set(target, key, value, receiver) {
                if (receiver === newPrototype) return ReflectSet(target, key, value);
                recordActionWithErrorHandling(PROPERTY_STORE, id, target, key);
                return ReflectSet(target, key, value, receiver);
            },
            has(target, key) {
                recordActionWithErrorHandling(PROPERTY_LOAD, id, target, key);
                return ReflectHas(target, key);
            },
        };

        try {
            originalPrototype = getPrototypeOf(value);
            newPrototype = new ProxyConstructor(originalPrototype, handler);
            setPrototypeOf(value, newPrototype);
        } catch (e) {}
    }

    function probeWithErrorHandling(id, value) {
        try {
            probe(id, value);
        } catch(e) {
            reportError(e);
        }
    }

    return {
        probe: probeWithErrorHandling,
        reportResults: reportResults
    };
})();

for (let v1 = 0; v1 < 5; v1++) {
    const v3 = new WeakMap();
    Probe.probe("v3", v3);
    function f4() {
        Probe.probe("v5", Array);
        const v6 = Array.fromAsync();
        Probe.probe("v6", v6);
        v6.then(v6, Array);
        return WeakMap;
    }
    f4.caller = f4;
    function f8(a9) {
        return a9;
    }
    Probe.probe("v8", f8);
    Object.defineProperty(v3, "constructor", { configurable: true, enumerable: true, get: f4, set: f8 });
    class C10 {
        constructor(a12, a13) {
            Probe.probe("v12", a12);
            try { a12.constructor(); } catch (e) {}
        }
    }
    Probe.probe("v10", C10);
    try { new C10(WeakMap, C10); } catch (e) {}
    new C10(v3);
}
class C19 {
    [-1073741824];
    static [-1073741824];
    16 = -1073741824;
    e = 1000;
    static #n(a21, a22) {
        Probe.probe("v21", a21);
        a21 = -1073741824;
        Probe.probe("v23", Math);
        let v24 = -897014274;
        Math.fround(-1073741824);
        --v24;
        ~v24;
        a22 | a22;
        return --a22;
    }
}
Probe.probe("v19", C19);
C19.name;
const v31 = new C19();
Probe.probe("v31", v31);
const v32 = new C19();
new C19();
Probe.probe("v34", 35414);
[-2.0,-1.0,0.9749486214529169,-1000000.0,3.543077103585146,0.9048538098208798,-1.0];
const v38 = [1.0,2.220446049250313e-16,-992208.5106291195,0.6877078287130777,-795.7633379232085,0.0];
const v39 = [802.9961078524698,Infinity,0.4829874701378024];
Probe.probe("v39", v39);
try { v39.lastIndexOf(v38); } catch (e) {}
class C41 extends C19 {
    static #b;
    valueOf(a43, a44, a45, a46) {
        Probe.probe("v42", this);
        this.e;
        const o48 = {
            ...v31,
            "a": a46,
            __proto__: C19,
            "d": 1000,
        };
        return v32;
    }
    #f = 35414;
    static #d;
    #a;
    static #c;
}
const v49 = new C41();
new C41();
new C41();
try { new Uint32Array(1073741824, 1000, -9223372036854775807); } catch (e) {}
const v54 = [Uint32Array,Uint32Array,Uint32Array,Uint32Array,Uint32Array];
Probe.probe("v54", v54);
function f55() {
    class C56 {
    }
    Probe.probe("v56", C56);
    const v57 = new C56();
    const v58 = v57?.toString;
    Probe.probe("v58", v58);
    try { new v58(); } catch (e) {}
    Probe.probe("v60", createGlobalObject);
    const v61 = createGlobalObject?.constructor;
    Probe.probe("v61", v61);
    try { new v61(v49); } catch (e) {}
    const v64 = createGlobalObject().Reflect;
    Probe.probe("v64", v64);
    v64.valueOf(f55, f55, createGlobalObject, C56, v57).get(v57);
    return createGlobalObject;
}
Probe.probe("v55", f55);
f55.d = f55;
const v67 = v54.constructor();
try { v67.includes(-9223372036854775807); } catch (e) {}
const v69 = new Uint32Array(v54, v67);
Probe.probe("v69", v69);
v69.valueOf = f55;
v69.copyWithin(v69, v67);
Probe.reportResults();

