var navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navConfigParser = require(process.cwd() + "/lib/navConfigParser.js");
var postgresPersistence = require("jive-persistence-postgres");
var that;

module.exports = class navDbConnectionHandler {
    constructor(persistence) {

        if(persistence){
            this.persistence = persistence;
            return;
        }

        //var logger = new navLogUtil(), configParser = new navConfigParser();
        var databaseUrl = "pg://" + navConfigParser.instance().getConfig("DatabaseUser", "admin") + ":" + navConfigParser.instance().getConfig("DatabasePassword","admin") + "@" +navConfigParser.instance().getConfig("DatabaseHost") + ":" + navConfigParser.instance().getConfig("DatabasePort","5432") + "/" +navConfigParser.instance().getConfig("DatabaseName", "navnirmitee");
    if (!databaseUrl) {
        navLogUtil.instance().log.call(this,"constructor", "Please check db url " + databaseUrl, "error");
        return;
    }

        navLogUtil.instance().log.call(this,"constructor", "Configuring database , URL " + databaseUrl, "debug");
        this.persistence = new postgresPersistence({
            databaseUrl: databaseUrl,
            customLogger: navLogUtil.instance().getLogger()
        });
    }

    instance(persistence) {
        if(that)
            return that;
        else
            return (that = new navDbConnectionHandler(persistence));

    }
}
