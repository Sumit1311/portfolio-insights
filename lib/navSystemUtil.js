var Q = require('q'),
    navConfigParser = require(process.cwd() + "/lib/navConfigParser.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");


module.exports = class navSystemUtils {
    executeCommand(command, options) {
        const exec = require('child_process').exec;
        var self = this;
        var deferred = Q.defer();
        navLogUtil.instance().log.call(self, self.executeCommand.name, `Executing command ${command}`, 'debug');
        exec(command, options , (error, stdout, stderr) => {
            if (error) {
                navLogUtil.instance().log.call(self, self.executeCommand.name, `Exec error: ${error}`, "error");
                deferred.reject(error);
            }
            deferred.resolve({
                stdout : stdout,
                stderr : stderr
            });
        });
        return deferred.promise;
    }
    getNoOfFilesMatchPat (pattern, directory) {
        return this.executeCommand('ls ' + directory + pattern + ' | wc -l')
            .then(function(result){
                return Q.resolve(parseInt(result.stdout));
            })
        .catch(function(err){
            return Q.reject(err);
        })
    }
    fetchBSEStockList (){
        return this.executeCommand(navConfigParser.instance().getConfig("PythonExecutable", "python3") + " scripts/nav_calling_block.py bslu", {
            shell : true,
            env : process.env
        })
        .then(function(result){
            navLogUtil.instance().log.call(self,self.fetchBSEStockList.name, "Successfully executed start-get-bse.", "debug");
            return Q.resolve();
        })
        .catch(function(error){
            navLogUtil.instance().log.call(self,self.fetchBSEStockList.name, 'Failed while executing start-get-bse : ' + error, "error");
            return Q.reject();
        });
    }
    runDailyScheduler () {
        return this.executeCommand(navConfigParser.instance().getConfig("PythonExecutable", "python3") + " scripts/nav_calling_block.py ", {
            shell : true,
            env : process.env
        })
        .then(function(result){
            navLogUtil.instance().log.call(self,self.fetchBSEStockList.name, "Successfully executed start-get-bse.", "debug");
            return Q.resolve();
        })
        .catch(function(error){
            navLogUtil.instance().log.call(self,self.fetchBSEStockList.name, 'Failed while executing start-get-bse : ' + error, "error");
            return Q.reject();
        });
    }
}

