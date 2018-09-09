var navScheduler = require(process.cwd() + "/lib/navScheduler.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navSystemUtil = require(process.cwd() + "/lib/navSystemUtil.js");

module.exports = class navBackgroundTaskInitializer {
    constructor() {

    }

    init() {

    }

    register(){
        //Register the task of fetching the BSE list
        new navScheduler().registerRecurringAsyncTask(new navSystemUtil().fetchBSEStockList.bind(new navSystemUtil()), navCommonUtil.getMillisecondTill(18));
        
    }
}