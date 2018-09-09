var navWorker = require(process.cwd() + "/lib/navWorker.js"),
    navSystemUtil = require(process.cwd() + "/lib/navSystemUtil.js"),
    navUserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js");
module.exports = class navUPRMaster{
    constructor(){
        this.name = "User Profile Refresh Master";
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
            this.workerPool.push();
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
                    return Q.resolve();
                }
                u = users[0];
                return userDAO.lockUserForDailyUpdate(u._id);
            })
            .then((res) => {
                if(typeof u === 'undefined') {
                    return Q.resolve();
                }
                else if(res.rowCount == 0) {
                    return self.start();
                } else {
                    var s = new navSystemUtil();
                    var worker = self.workerPool.pop();
                    worker.run(s.runDailyScheduler.bind(s), {
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
             
            })
    }

    successHandler(workPacket) {
        var userId = workPacket.userId;
        new navUserDAO().unlockUserForDailyUpdate(userId)
        .catch((error) => {

        })
        return;
    }

    errorHandler(workPacket) {
        new navUserDAO().unlockUserForDailyUpdate(userId)
         .then(() => {
            return self.start();
         })
         .catch((error) => {

         })
    }
}