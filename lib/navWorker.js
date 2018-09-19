var Q = require('q'),
    EventEmitter = require("events"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js");

module.exports = class navWorker extends EventEmitter {
    constructor(id) {
        super();
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
                navLogUtil.instance().log.call(self, self.run.name,
                "Worker "+ self.id+" has encountered error while running"+
                " for user "+workPacket.user._id +
                "Error stack : " + error.stack, "info");
            self.emit("error", error, workPacket);
            return Q.reject(error);
        });
    }
}
