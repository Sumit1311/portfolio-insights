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
        new navScheduler().registerRecurringAsyncTask(new navSystemUtil().fetchBSEStockList.bind(new navSystemUtil()), function(){
            return navCommonUtil.getMillisecondTill(18);
        } , true);
        //Register the task of daily profile updater
        var s = new navDPUMaster();
        new navScheduler().registerRecurringAsyncTask(s.start.bind(s), 3600000, true);
    }
}
