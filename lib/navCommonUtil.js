var uuid = require('node-uuid');
const url = require('url');
var AGE_GROUPS = [];
var CATEGORIES = [];
var moment = require('moment');
var COUNTRIES =["INDIA"], STATES = { "INDIA" : ["Maharashtra"] }, DISTRICTS = {"Maharashtra" : ["Pune"]};
var navToysParser = require(process.cwd() + "/lib/navToysParser.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");

var that = {
    name : "navCommonUtil"
}

function readCategories() {
    var categories = navToysParser.instance().config.categories;
    for(var i =0; i < categories.length; i++) {
        CATEGORIES.push(categories[i].name);    
    }

}
function readAgeGroups() {
    var ageGroups = navToysParser.instance().config.ageGroups;
    for(var i =0; i < ageGroups.length; i++) {
        AGE_GROUPS.push(ageGroups[i].name);    
    }

}

readCategories();
readAgeGroups();

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

    static getAgeGroups() {
        return AGE_GROUPS;        
    }
    static getStates(country) {
        return country ? STATES[country] : STATES;        
    }
    static getDistricts(state) {
        return state ? DISTRICTS[state] : DISTRICTS;        
    }

    static getCountries() {
        return COUNTRIES;        
    }
    static getCategories() {
        return CATEGORIES;
    }

    static getSkills() {
        return  navToysParser.instance().config.skills;
    }
    static getBrands() {
        return  navToysParser.instance().config.brands;
    }
}

