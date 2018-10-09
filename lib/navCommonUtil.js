var uuid = require('node-uuid');
const url = require('url');
var moment = require('moment');
var navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js');


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
    
    static getMillisecondTill(hours) {
        var m = moment();
        var m1 = moment();
        var h = m1.hour();
        if(h > hours) {
            m1.hour(23 + hours).minute(0).second(0).millisecond(0);
        } else {
            m1.hour(hours).minute(0).second(0).millisecond(0);
        }
        var i = Math.abs(m1.valueOf() - m.valueOf());
        return i;
    }

    static validatePortfolioData(portfolioData){
        var validationResult = {};
        portfolioData.sort(function(a, b ){
            if(a.transactionDate == b.transactionDate) {
                if(a.transactionType == "Buy") {
                    return -1;
                } else {
                    return 1;
                }
            }
            return moment(a.transactionDate).valueOf() - moment(b.transactionDate).valueOf();
        });

        for(var i = 0; i < portfolioData.length; i++){
            if(validationResult[portfolioData[i].securityCode] == undefined) {
                validationResult[portfolioData[i].securityCode] = 0;
            }
            if(portfolioData[i].transactionType == "Buy") {
                validationResult[portfolioData[i].securityCode] += portfolioData[i].numberOfShares;
            } else {
                validationResult[portfolioData[i].securityCode] -= portfolioData[i].numberOfShares;
            }
            if(validationResult[portfolioData[i].securityCode] < 0) {
                throw new navValidationException("Invalid data for script : " + portfolioData[i].securityCode);
            }
        }
    }
}

