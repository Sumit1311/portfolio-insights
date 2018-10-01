/**
 * Created by geek on 4/9/18.
 */

var BaseDAO = require(process.cwd() + "/lib/dao/base/baseDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js'),
    util = require("util");

function navStocksListBSEDAO(client, persistence) {
    var self = this;
    if (persistence) {
        BaseDAO.call(self, persistence);
    }
    this.providedClient = client ? client : undefined;
    return this;
}

util.inherits(navStocksListBSEDAO, BaseDAO);

module.exports = navStocksListBSEDAO;
//private variables
var tableName = "stock_list_bse";

navStocksListBSEDAO.prototype.getAllBSECompanies=function (query, limit) {
    var self = this;return self.dbQuery("SELECT security_code,security_name FROM "+tableName+" WHERE security_name LIKE '%' || $1 ||'%' LIMIT $2",[query, limit] )
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getAllBSECompanies", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};

