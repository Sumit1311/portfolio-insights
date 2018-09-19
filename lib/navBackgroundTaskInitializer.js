var navScheduler = require(process.cwd() + "/lib/navScheduler.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navDPUMaster = require(process.cwd() + "/lib/navDPUMaster.js"),
    navSystemUtil = require(process.cwd() + "/lib/navSystemUtil.js");

module.exports = class navBackgroundTaskInitializer {
    constructor() {

    }

    init() {

    }

    register(){
        //Register the task of fetching the BSE list
        var scheduler = new navScheduler();
        scheduler.successInterval = function(){
            return navCommonUtil.getMillisecondTill(18);
        };
        scheduler.failureInterval = function(){
            return 1000;
        };
        scheduler.taskName = "fetchBSEStockList";
        scheduler.registerRecurringAsyncTask(new navSystemUtil().fetchBSEStockList.bind(new navSystemUtil()), true, false);
        //Register the task of daily profile updater
        var s = new navDPUMaster();
        scheduler = new navScheduler();
        scheduler.successInterval = function(){
            return 60000;
        };
        scheduler.failureInterval = function(){
            return 1000;
        };
        scheduler.taskName = "navDPUMaster";
        scheduler.registerRecurringAsyncTask(s.start.bind(s), true, false);
    }
}
