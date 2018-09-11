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
    registerRecurringAsyncTask(task, isFirst, isFailure){
        if(typeof task !== 'function') {
            throw new Error("Unsupported task");
        }
        var self = this;
        var i = isFailure ? self.failureInterval() : self.successInterval();
        var first = 1000;
        navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + self.taskName +" will start execution in " + (isFirst ? first : i )+ " in ms", "info");
        setTimeout(function(){
            navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "Starting  " + self.taskName + " ..... " , "info");
            task()
                .done(() => {
                    //i =navCommonUtil.getMillisecondTill();
                    navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + self.taskName +" executed successfully ", "info");
                    self.registerRecurringAsyncTask(task, false, false);
                }, (error) => {
                    //i =navCommonUtil.getMillisecondTill();
                    navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "Error occured while executing task "+ self.taskName+ " , " + error, "error");
                    //navLogUtil.instance().log.call(self, self.registerRecurringAsyncTask.name, "The task " + task.name +" will start execution in " + ( i / 1000 ) / 60 + " minutes", "info");
                    self.registerRecurringAsyncTask(task, false, true);
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
        if(typeof interval === 'function') {
            return interval();
        } else if(typeof interval === 'number'){
            return interval;
        } else {
            return 3600000;
        }
    }

    successInterval(){
        return 3600000;
    }

    failureInterval(){
        return 1000;
    }
}
