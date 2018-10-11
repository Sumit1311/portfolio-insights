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

navUserProfileDAO.prototype.insertUserProfile = function(profileData, transactionId){
    var self = this;
    var p = profileData;
    return self.dbQuery("INSERT INTO "+tableName+" (_id, user_id, security_code, security_count, trxn_date, trxn_type, trxn_flag, trxn_amount ) " +
        "VALUES($1,$2,$3,$4,$5,$6,$7,$8)",
    [transactionId == undefined ? navCommonUtil.generateUuid_S() : transactionId ,profileData.userId, profileData.securityCode,
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
    return self.dbQuery("SELECT DISTINCT user_id, trxn_date FROM "+tableName+" " +
        "WHERE trxn_flag = 0 AND user_id = $1 " +
        " ORDER BY trxn_date", [userId] )
    .then(function (result) {
        return result.rows.length == 0 ? false : true;
    })
    .catch(function (error) {
        navLogUtil.instance().log.call(self, "insertUserProfile", error.message, "error");
        return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
    });
}

navUserProfileDAO.prototype.truncate = function(userId) {
    var self = this;
    return self.dbQuery("DELETE FROM "+tableName+" WHERE user_id = $1", [userId] )
        .then(function (result) {
            return result;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.getProfileData = function(userId) {
    var self = this;
    return self.dbQuery("SELECT * FROM "+tableName+" WHERE user_id = $1 AND is_active = 1", [userId] )
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getProfileData", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.getViewProfileData = function(userId) {
    var self = this;
    return self.dbQuery("select u.*, s.security_id, s.security_name" +
        " FROM user_stocks_trxn u INNER JOIN stock_list_bse s ON u.security_code = s.security_code" +
        " WHERE u.user_id = $1 AND is_active = 1 ORDER BY u.trxn_date", [userId] )
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.lockRow = function(transactionId, activeOnly){
    var self = this;

    return self.dbQuery("UPDATE user_stocks_trxn SET time_taken=$1 WHERE time_taken IS NULL AND _id=$2 " + (activeOnly ? " AND is_active=1" : " ") +"",
        [navCommonUtil.getCurrentTime_S(), transactionId] )
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.getTransaction = function(transactionId) {
    var self = this;

    return self.dbQuery("select * " +
                " FROM user_stocks_trxn " +
                " WHERE _id = $1", [transactionId] )
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.deleteTransaction = function(transactionId, deleteProcessed) {
    var self = this;
    return self.dbQuery("DELETE " +
        " FROM user_stocks_trxn " +
        " WHERE _id = $1 AND is_active = 1 AND"+(deleteProcessed == undefined || deleteProcessed == false? +" trxn_flag = 0" : + " trxn_flag = 1"), [transactionId] )
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "deleteTransaction", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.markTransactionInactive = function(transactionId, newTransactionId) {
    var self = this;
    var  params = [transactionId , navCommonUtil.getCurrentTime_S()];
    if(newTransactionId != undefined) {
        params.push(newTransactionId);
    }
    return self.dbQuery("UPDATE user_stocks_trxn" +
        " SET is_active = 0, trxn_flag = 0, deactivation_date = $2" +
        (newTransactionId == undefined ? "" : ", parent_id = $3") +
        " WHERE _id = $1 AND " +
        " (SELECT count(_id)" +
        " FROM user_stocks_trxn" +
        " WHERE " +
        " is_active = 0 AND trxn_flag = 0) = 0",
         params)
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "markTransactionInactive", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.unlockRow = function(transactionId){
    var self = this;

    return self.dbQuery("UPDATE user_stocks_trxn SET time_taken=NULL WHERE time_taken IS NOT NULL AND _id = $1",
        [transactionId] )
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "unlockRow", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}


navUserProfileDAO.prototype.editTransaction = function(transactionId, portfolioData, editProcessed) {
    var self = this;
    return self.dbQuery("UPDATE user_stocks_trxn " +
        " SET  security_code = $1, security_count = $2, trxn_date = $3, trxn_type = $4, trxn_amount = $5" +
        " WHERE _id = $6 AND is_active = 1 AND "+
        (editProcessed == undefined || editProcessed == false ? "trxn_flag = 0" : "trxn_flag = 1"),
        [portfolioData.securityCode, portfolioData.numberOfShares, portfolioData.transactionDate,
            portfolioData.transactionType, portfolioData.transactionAmount, transactionId] )
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}

navUserProfileDAO.prototype.resetTransactionFlag = function (userId) {
    var self = this;
    return self.dbQuery("UPDATE user_stocks_trxn " +
        " SET  trxn_flag = 0" +
        " WHERE user_id=$1",
        [userId] )
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "truncate", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
}
