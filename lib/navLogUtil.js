var that, logger;
var navConfigParser = require(process.cwd() + '/lib/navConfigParser.js');

var log4jsConfig = {
    appenders : {
        "web-server" : {
            type  : "dateFile",
            filename : process.cwd() + "/log/web-server.log",
            compress : true
        },

        "background-processing" : {
            type  : "dateFile",
            filename : process.cwd() + "/log/background-processing.log",
            compress : true
        },
        "out" : {
            type : "stdout"
        }
    },
    categories : {
        "default" : {
            appenders : ["out"],
            level : "INFO"
        },
        "web-server" : {
            appenders : ["web-server"],
            level : "INFO"
        },
        "background-processing" : {
            appenders : ["background-processing"],
            level : "INFO"
        }

    }
}

var log4js = require('log4js');
log4js.configure(log4jsConfig);

function init(_logger) {
    var loggingConfig =  navConfigParser.instance().getConfig("LogLevel");
    logger = log4js.getLogger(_logger ? _logger : "ajab-gajab");
    logger.level = loggingConfig[_logger] || "INFO";
}

module.exports = class navLogUtil {
    constructor() {
    }
    log (functionName, message, level){
        logger[level]("["+ this.constructor.name +"] ["+ functionName  +"] " + message );
    }
    static log_s (level, functionName, message){
        logger[level]("["+ this.constructor.name +"] ["+ functionName  +"] " + message );
    }
    getLogger() {
        return logger;
    }
    static instance(_logger) {
        if(typeof that === "object"){
            return that;
        }
        else{
            that = new navLogUtil(); 
            init(_logger);
            return that;
        }

    }

}



