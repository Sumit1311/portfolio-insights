var navWorker = require(process.cwd() + "/lib/navWorker.js"),
    Q = require('q'),
    moment = require('moment'),
    navSystemUtil = require(process.cwd() + "/lib/navSystemUtil.js"),
    navUserProfileDAO = require(process.cwd() + "/lib/dao/stocks/navUserProfileDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navUserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js");
module.exports = class navDPUMaster{
    constructor(){
        this.name = "Daily Profile Update Master";
        this.workerPool = [];
        var self = this;
        for(var i = 0; i < 5; i++){
            var worker = new navWorker();
            worker.on("done", (workPacket) => {
                self.successHandler(workPacket);
            });
            worker.on("error", (error) => {
                self.errorHandler(workPacket);
            });
            this.workerPool.push(worker);
        }
    }

    start(){
        var self = this;
        var userDAO = new navUserDAO();
        var u;
        if(self.workerPool.length == 0){
            return Q.resolve();
        }
        return userDAO.getUsersForDailyUpdate(1)
            .then(function(users){
                
                if(users.length == 0) {
                    navLogUtil.instance().log.call(self, self.start.name, 
                        "No users eligible for daily update", "info");
                    return Q.resolve();
                }
                u = users[0];
                navLogUtil.instance().log.call(self, self.start.name, 
                    "Fetched for daily update " + u._id, "info");
                return userDAO.lockUserForDailyUpdate(u._id);
            })
            .then((res) => {
                if(typeof u === 'undefined') {
                    return Q.resolve();
                }
                else if(res.rowCount == 0) {
                    return self.start();
                } else {
                    navLogUtil.instance().log.call(self, self.start.name, 
                        "Running for daily update "+u._id, "info");
                    var worker = self.workerPool.pop();
                    worker.run(
                        self.task.bind(self)
                        , {
                        userId : u._id
                    });
                    if(self.workerPool.length != 0) {
                        return self.start();
                    } else {
                        return Q.resolve();
                    }
                }
            })
            .catch((error) => {
                return Q.reject(error);
            })
    }

    successHandler(workPacket) {
        var userId = workPacket.userId;
        var w = workPacket.worker;
        navLogUtil.instance().log.call(self, self.start.name, 
            "Successful run for daily update with user "+userId, "info");       
        new navUserDAO().unlockUserForDailyUpdate(userId)
        .catch((error) => {
            return Q.reject(error);
        })
        .finally(() =>{
            this.workerPool.push(w);
        } )
        return;
    }

    errorHandler(workPacket) {
        var userId = workPacket.userId;
        var w = workPacket.worker;
        navLogUtil.instance().log.call(self, self.start.name, 
            "Error occured while running for daily update with user "+userId, "info");       
        new navUserDAO().unlockUserForDailyUpdate(userId)
         .then(() => {
            return self.start();
         })
         .catch((error) => {
            return Q.reject(error);
         })
        .finally(() =>{
                this.workerPool.push(w);
        } )
    }

    task(workPacket) {
        var s = new navSystemUtil();
        /*return new navUserProfileDAO().checkIfEligibleForProfileRefresh(workPacket.userId)
            .then(function(flag) {
                if(flag) {
                    return s.runProfileRefresher(workPacket);
                } else {
                    return Q.resolve();
                }
            })
            .then(function(){
                if(moment().hours() == 18) {
                    return s.runDailyScheduler(workPacket);
                } else {
                    return Q.resolve();
                }
            })*/
            return s.runDailyScheduler(workPacket)
            .catch(function(error){
                return Q.reject(error);
            });
    }
}
