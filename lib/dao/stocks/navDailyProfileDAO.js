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
var tableName = "user_stock_profile_daily";

navUserProfileDAO.prototype.clearUserProfile = function(userId){
    var self = this;
    return self.dbQuery("DELETE FROM " +tableName+ 
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
