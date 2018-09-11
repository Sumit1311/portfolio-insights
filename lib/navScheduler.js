var schedule = require("node-schedule"),
    moment = require('moment'),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");

module.exports = class navScheduler {

    registerTask(task, cronString) {
        if(typeof task !== 'function') {
            throw new Error("Unsupported task");
        }
        var self = this;
        schedule.scheduleJob(cronString ? cronString : "59 * * * * *",function(fireDate){
            navLogUtil.instance().log.call(self, self.registerTask.name, "The task " + task.name +" will start execution", "info");
            task();
        })
    }

    //interval in seconds
    registerRecurringAsyncTask(task, interval, isFirst){
        if(typeof task !== 'function') {
            throw new Error("Unsupported task");
        }
        var self = this;
        var i = self.getInterval(interval);

        var first = 1000;
        navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + task.name +" will start execution in " + (isFirst ? first : i )+ " in ms", "info");
        setTimeout(function(){
            navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "Starting  " + task.name + " ..... " , "info");
            task()
                .done(() => {
                    //i =navCommonUtil.getMillisecondTill();
                    //navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + task.name +" will start execution in " + ( i / 1000) / 60 + " minutes", "info");
                    self.registerRecurringAsyncTask(task, i);
                }, (error) => {
                    //i =navCommonUtil.getMillisecondTill();
                    navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "Error occured while executing task "+ task.name + error, "error");
                    //navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + task.name +" will start execution in " + ( i / 1000 ) / 60 + " minutes", "info");
                    self.registerRecurringAsyncTask(task, i);
                });
        }, isFirst ? first : i );

    }

    registerRecurringSyncTask(task, interval){
        if(typeof task !== 'function') {
            throw new Error("Unsupported task");
        }
        var i = interval ? interval : 10800000;
        var self = this;
        setTimeout(function(){
            task();
            self.registerRecurringSyncTask(task, i);
        }, i);
        
    }

    getInterval(interval) {
        var i;
        return i;
    }
}
