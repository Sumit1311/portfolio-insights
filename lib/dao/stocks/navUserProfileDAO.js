/**
 * Created by geek on 4/9/18.
 */

var BaseDAO = require(process.cwd() + "/lib/dao/base/baseDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js'),
    util = require("util");

function navUserProfileDAO(client, persistence) {
    var self = this;
    if (persistence) {
        BaseDAO.call(self, persistence);
    }
    this.providedClient = client ? client : undefined;
    return this;
}

util.inherits(navUserProfileDAO, BaseDAO);

module.exports = navUserProfileDAO;
//private variables
var tableName = "user_stocks_trxn";

navUserProfileDAO.prototype.insertUserProfile = function(profileData){
    var self = this;
    var p = profileData;
    return self.dbQuery("INSERT INTO "+tableName+" (user_id, security_code, security_count, trxn_date, trxn_type, trxn_flag, trxn_amount ) " +
        "VALUES($1,$2,$3,$4,$5,$6,$7)",
    [profileData.userId, profileData.securityCode,
        profileData.numberOfShares, profileData.transactionDate, profileData.transactionType,
    0, profileData.transactionAmount])
        .then(function (result) {
            //navLogUtil.instance().log.call(self, "insertUserProfile", "Failed to insert data", "debug");
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "insertUserProfile", error.message, "error");
            navLogUtil.instance().log.call(self, "insertUserProfile", "Failing for : " + profileData.securityCode, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.checkIfEligibleForProfileRefresh = function(userId) {
    var self = this;
    return self.dbQuery("SELECT DISTINCT user_id FROM "+tableName+" WHERE trxn_flag = 0 AND user_id = $1", [userId] )
    .then(function (result) {
        return result.rows.length == 0 ? false : true;
    })
    .catch(function (error) {
        navLogUtil.instance().log.call(self, "insertUserProfile", error.message, "error");
        return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
    });
}