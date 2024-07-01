(() => {
    function __hookAPI(object, property, tag) {
        try {
            let old_fun = object[property];
    
            function _hooked() {
                let caller, callerString, callerName, callerData, stacktrace;
                try {
                    caller = arguments?.callee?.caller;
                    callerString = caller?.toString();
                    callerName = caller?.name;
                    if (callerString.startsWith("async function (api, data)")) {
                        callerString = undefined;
                        caller = undefined;
                    } else if (callerName.startsWith("_hooked")) {
                        caller = caller?.arguments?.callee?.caller;
                        callerString = caller?.toString();
                        callerName = caller?.name;
                    }
                } catch (e) { }
                try {
                    stacktrace = (new Error()).stack;
                    stacktrace = stacktrace.split("\n");
                    stacktrace.shift();
                    stacktrace.shift();
                } catch (e) { }
    
                try {
                    callerData = {};
                    let seenCallers = new WeakSet();
                    while (true && caller != null && caller.toString() != '') {
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
                } catch (e) {
                    console.error("Something wrong here!", e);
                }
                if (stacktrace !== "skip") {
                    try {
                        console.log({
                            dis: tag.startsWith("Date.") ? undefined : this,
                            caller: callerString,
                            callerName,
                            callerData,
                            stacktrace,
                            arguments: Array.from(arguments)
                        });
                    } catch (e) {
                        console.error("Something wrong!", e.message);
                    }
                }
                if (old_fun === undefined) return undefined;
                else return old_fun.apply(this, arguments);
            }
            object[property] = _hooked;
        } catch (e) { }
    }

    __hookAPI(GPUDevice.prototype, "createBuffer", "GPUDevice.createBuffer");
    __hookAPI(GPUDevice.prototype, "createCommandEncoder", "GPUDevice.createCommandEncoder");
    __hookAPI(GPUDevice.prototype, "createComputePipeline", "GPUDevice.createComputePipeline");
    __hookAPI(GPUDevice.prototype, "createRenderPipeline", "GPUDevice.createRenderPipeline");
    __hookAPI(GPUDevice.prototype, "createRenderPipelineAsync", "GPUDevice.createRenderPipelineAsync");
    __hookAPI(GPUDevice.prototype, "createShaderModule", "GPUDevice.createShaderModule");
})();
