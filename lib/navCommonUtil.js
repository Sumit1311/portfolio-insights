var uuid = require('node-uuid');
const url = require('url');
var moment = require('moment');
var navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");

var that = {
    name : "navCommonUtil"
}

module.exports = class navCommonUtils {
    constructor() {
        //super();

    }
    generateUuid() {
        return uuid.v4();
    }

    static generateUuid_S() {
        return uuid.v4();
    }

    getErrorObject(error, status, code ,exception) {
        if(error.name != exception.name)
        {
            return new exception(error.message, status, code);
        }
        else
        {
            return error;
        }
    }

    getCurrentTime() {
        return moment().valueOf();
    }
    static getCurrentTime_S() {
        return moment().valueOf();
    }
    static getTimeinMillis(dateString) {
        return dateString === "" ? null : moment(dateString).valueOf();
    }
    getDateString(timeInMilis, format) {
        if(timeInMilis) {
            return moment(timeInMilis).format(format ? format : "ddd, MMM Do YYYY");
        } else {
            return "";
        }
    }

    static getDateFormat() {
        return "ddd, MMM Do YYYY";
    }

    getBaseURL(req) {
        const self = this;
        var base = new url.Url();
        base.protocol = req.protocol;
        base.host = req.get("host");
        navLogUtil.instance().log.call(self, self.getBaseURL.name, "Server base url is "+base, "debug")
        return base;
    }    
    static getBaseURL_S(req) {
        var base = new url.Url();
        base.protocol = req.protocol;
        base.host = req.get("host");
        navLogUtil.instance().log.call(that, "getBaseURL_S", "Server base url is "+base, "debug")
        return base;
    }    
}

