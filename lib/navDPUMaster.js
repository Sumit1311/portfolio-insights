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
                        user : user
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
        var userId = workPacket.user._id;
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
        var userId = workPacket.user._id;
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
        var shouldRunDailyUpdate = workPacket.user.next_daily_update_time == null 
        || (workPacket.user.next_daily_update_time <= navCommonUtil.getCurrentTime_S());
        return new navUserProfileDAO().checkIfEligibleForProfileRefresh(workPacket.user._id)
            .then(function(flag) {
                if(flag) {
                    navLogUtil.instance().log.call(self, self.task.name, 
                        "Running profile refresher "+workPacket.user._id, "info");       
                    return s.runProfileRefresher(workPacket);
                } else {
                    navLogUtil.instance().log.call(self, self.task.name, 
                        "Not eligible for profile refresh : "+workPacket.user._id, "info");       
                    return Q.resolve();
                }
            })
            .then(function(){
                if(shouldRunDailyUpdate) {
                    navLogUtil.instance().log.call(self, self.task.name, 
                        "Running daily refresher for "+workPacket.user._id, "info");       
                    return s.runDailyScheduler(workPacket);
                } else {
                    navLogUtil.instance().log.call(self, self.task.name, 
                        "Not running daily refresher : "+workPacket.user._id, "info");       
                    return Q.resolve();
                }
            })
            .then(function(){
                if(shouldRunDailyUpdate){
                    navLogUtil.instance().log.call(self, self.task.name, 
                        "Updating next execution time for daily profile refresher for "
                        +workPacket.user._id, "info");       
                    return new navUserDAO().updateTimeForNextDailyUpdate(navCommonUtil.getMillisecondTill(18));
                } else {
                    return Q.resolve();
                }
            })
            /*return s.runDailyScheduler(workPacket)*/
            .catch(function(error){
                navLogUtil.instance().log.call(self, self.task.name, 
                    "Error occured while task "+ self.name+" running for "+workPacket.user._id, "error");       
                return Q.reject(error);
            });
    }
}
