(() => {
    function __hookProperty(object, property, tag, getter = false, setter = false) {
        try {
            let __propGetter, __propSetter;
            try {
                __propGetter = object["__lookupGetter__"](property).bind(object);
            } catch (e) {
                __propGetter = function () { };
            }
    
            try {
                __propSetter = object["__lookupSetter__"](property).bind(object);
            } catch (e) {
                __propSetter = function () { };
            }
    
            let __hookedGetter = function () {
                let data, caller, callerString, callerName, callerData, stacktrace;
                try {
                    data = __propGetter(...arguments);
                    try {
                        caller = arguments?.callee?.caller;
                        callerString = caller?.toString();
                        callerName = caller?.name;
                        if (callerString.startsWith("async function (api, data)")) {
                            callerString = undefined;
                            caller = undefined;
                        } else if (callerName.startsWith("_hook") || callerName.startsWith("__hook")) {
                            caller = caller?.arguments?.callee?.caller;
                            callerString = caller?.toString();
                            callerName = caller?.name;
                        }
                    } catch (e) { }
    
                    try {
                        stacktrace = (new Error()).stack.split("\n");
                        stacktrace.shift();
                        stacktrace.shift();
                    } catch (e) { }
    
                    try {
                        callerData = {};
                        let seenCallers = new WeakSet();
                        while (true && caller != null && caller != '') {
                            if (seenCallers.has(caller)) break;
                            seenCallers.add(caller);
                            parent_caller = caller?.arguments?.callee?.caller;
                            parent_caller_name = parent_caller?.name;
                            parent_caller_string = parent_caller?.toString();
                            if (Object.keys(callerData).includes(parent_caller_name)) {
                                callerData[parent_caller_name].push(parent_caller_string)
                            } else {
                                callerData[parent_caller_name] = [parent_caller_string];
                            }
                            caller = parent_caller;
                        }
                    } catch (e) { }
                    let detail = {
                        type: tag,
                        dis: data,
                        arguments,
                        caller: callerString,
                        callerName,
                        callerData,
                        stacktrace
                    };
                    if (stacktrace?.toString().indexOf('_hooked') > -1) return data;
                    try {
                        console.log(detail, tag);
                    } catch (e) { console.error(e); }
                } finally {
                    return data;
                }
            };
    
            let __hookedSetter = function () {
                let data, caller, callerString, callerName, callerData, stacktrace;
                try {
                    data = __propSetter(...arguments);
                    try {
                        caller = arguments?.callee?.caller;
                        callerString = caller?.toString();
                        callerName = caller?.name
                        if (callerString.startsWith("async function (api, data)")) {
                            callerString = undefined;
                            caller = undefined;
                        } else if (callerName.startsWith("_hook") || callerName.startsWith("__hook")) {
                            caller = caller?.arguments?.callee?.caller;
                            callerString = caller?.toString();
                            callerName = caller?.name;
                        }
                    } catch (e) { console.error(e); }
    
                    try {
                        stacktrace = (new Error()).stack.split("\n");
                        stacktrace.shift();
                        stacktrace.shift();
                    } catch (e) { console.error(e); }
    
                    try {
                        callerData = {};
                        let seenCallers = new WeakSet();
                        while (true && caller != null && caller != '') {
                            if (seenCallers.has(caller)) break;
                            seenCallers.add(caller);
                            parent_caller = caller?.arguments?.callee?.caller;
                            parent_caller_name = parent_caller?.name;
                            parent_caller_string = parent_caller?.toString();
                            if (Object.keys(callerData).includes(parent_caller_name)) {
                                callerData[parent_caller_name].push(parent_caller_string)
                            } else {
                                callerData[parent_caller_name] = [parent_caller_string];
                            }
                            caller = parent_caller;
                        }
                    } catch (e) { }
                    let detail = {
                        type: tag,
                        dis: data,
                        arguments,
                        caller: callerString,
                        callerName,
                        callerData,
                        stacktrace
                    };
                    if (stacktrace?.toString().indexOf('_hooked') > -1) return data;
                    try {
                        console.log(tag, detail);
                    } catch (e) { console.error(e); }
                } finally {
                    return data;
                }
            };
    
            let __defaultGetter = function () {
                return __propGetter(...arguments);
            }
    
            let __defaultSetter = function () {
                return __propSetter(...arguments);
            }
    
            Object.defineProperty(object, property, {
                get: getter ? __hookedGetter : __defaultGetter,
                set: setter ? __hookedSetter : __defaultSetter,
            });
        } catch (e) { console.error(e); }
    }
    __hookProperty(navigator, "gpu", "navigator.gpu", true, false);
})();