var navStocksListBSEDAO = require(process.cwd() + "/lib/dao/stocks/navStocksListBSEDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navLogicalException = require("node-exceptions").LogicalException,
    navUserExistsException = require(process.cwd() + "/lib/exceptions/navUserExistsException.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navPasswordUtil = require(process.cwd() + "/lib/navPasswordUtil.js"),
    Q = require('q');

module.exports = class navStockList {

    getBSECompanyList(query, limit) {
        return new navStocksListBSEDAO().getAllBSECompanies(query, limit)
            .catch(function(error){
                return Q.reject(error);
            });
    }
}

