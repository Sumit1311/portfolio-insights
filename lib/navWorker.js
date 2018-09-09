var Q = require('q'),
    EventEmitter = require("events"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js");

module.exports = class navWorker extends EventEmitter {
    constructor(id) {
        if(id) {
            this.id = id;            
        } else {
            this.id = new navCommonUtil().generateUuid();
        }
    }
    
    run(task, workPacket) {
        var self = this;
        if(typeof task !== "function") {
            throw "Unknown Task Type";
        }
        task(workPacket)
        .then(function(result){
            self.emit("done", workPacket);
            return Q.resolve(result);
        })
        .catch(function(error){
            self.emit("error", error);
            return Q.reject(error);
        });
    }
}