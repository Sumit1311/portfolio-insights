var Q = require('q'),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");


module.exports = class navSystemUtils {
    executeCommand(command) {
        const exec = require('child_process').exec;
        var self = this;
        var deferred = Q.defer();
        navLogUtil.instance().log.call(self, self.executeCommand.name, `Executing command ${command}`, 'debug');
        exec(command, (error, stdout, stderr) => {
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
}

