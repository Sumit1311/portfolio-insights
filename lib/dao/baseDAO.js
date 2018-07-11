/**
 * This file provides the basic access to database. Persist the connection
 * with the help of jive-persistence-postgres module. All DAO classes
 * inherits this to query database. This acts as a interface to query database.
 *
 */

// will be used to save database persistence
var db;
var navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtils = require(process.cwd() + "/lib/navCommonUtil.js");
var navDbConnection = require("./pg-conn.js"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js');

function BaseDAO(persistence) {
    //if some custom persistence provided use it other wise use the default postgres persistence
    
    if (!db) {
        db = persistence ? new navDbConnection(persistence).persistence : new navDbConnection().persistence;
    }
}

module.exports = BaseDAO;

/**
 * Fetches a client from pool.
 *
 * @returns {Q.promise}
 */
BaseDAO.prototype.getClient = function () {
    var self = this, commonUtil = new navCommonUtils();
    return db.getQueryClient()
        .catch(function(error){
            navLogUtil.instance().log.call(self,"getClient","Error occured connecting database : " + error.message, "error");
            return Q.reject(commonUtil.getErrorObject(error, 500, "DBCONN", navDatabaseException));
        })
};

/**
 * This method generates the execute method for transaction related queries.
 * @param query : querystring
 * @param param : query parameters
 * @returns {{setClient: Function, execute: Function}}
 */
BaseDAO.prototype.executeTransaction = function (query, param) {
    var client, commonUtil = new navCommonUtils();
    var self = this;
    return {
        setClient: function (clientToUse) {
            client = clientToUse;
            return this;
        },
        //method to execute the required operation if client is already available uses that (without releasing)
        //other wise gets a client from pool and releases it after the operation
        execute: function () {
            var deferred = Q.defer();
            // if client is not provided; fetch one fresh from the pool
            // and release it when done
            self.providedClient = client;
            self.dbQuery(query, param)
                .then(function (results) {
                    deferred.resolve(results);
                }, function (err) {
                    deferred.reject(err);
                })
            .catch(function(error){
                
                navLogUtil.instance().log.call(self, "executeTransaction","Error : " + error.message, "error");
                return Q.reject(commonUtil.getErrorObject(error, 500, "DBTRANSAC", navDatabaseException));
            })

            return deferred.promise;
        }
    }

};

/**
 * Queries the database using given sql statement
 * Executes the given query on database. and returns the promise for the result
 *
 * @param sql
 * @param params
 * @returns {*}
 */
BaseDAO.prototype.dbQuery = function (sql, params) {
    var client, promise, self = this, commonUtil = new navCommonUtils();

    if (this.providedClient === undefined) {
        navLogUtil.instance().log.call(this, "dbQuery", "No client provided getting new one" + sql + ", " +  params, "debug");
        promise = this.getClient();
    } else {
        navLogUtil.instance().log.call(this, "dbQuery", "Usign provided client, QueryString : "+sql + ", Params : "+params, "debug");
        promise = Q.resolve(this.providedClient)
    }
    return promise
        .then(function (_client) {
            client = _client;
            return query.call(self, client, sql, params);
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "dbQuery","Error executing QueryString : "+ sql +", Params : "+ params +" : " + error.message, "error" );
            return Q.reject(commonUtil.getErrorObject(error, 500, "DBQUERY", navDatabaseException));
        })
        .finally(function () {
            if (self.providedClient === undefined && client) {
                client.release();
            }
        })
    
}

function query(dbClient, sql, params) {
        return dbClient.query(sql, params)
            .then(function () {
                var results = dbClient.results();
                /*
                 results is of form : {
                 rows:[],
                 rowCount:<<number>>
                 }
                 */
                navLogUtil.instance().log("query", "Successfully Executed query " + sql + "with params " + params, "debug");
                return Q.resolve(results);
            })
            .catch(function (error) {
                return Q.reject(new navCommonUtils().getErrorObject(error, 500, "DBQUERY", navDatabaseException));
            })
}

BaseDAO.prototype.startTx = startTx;
BaseDAO.prototype.commitTx = commitTx;
BaseDAO.prototype.rollBackTx = rollbackTx;
//BaseDAO.prototype.savePointTx = savePointTx;

function startTx() {
    if (!this.providedClient) {
        navLogUtil.instance().log.call(this, "startTx", "Invalid Client", "error");
        return Q.reject(new navCommonUtils().getErrorObject({message : "Invalid Client"}, 500, "DBTRANSAC", navDatabaseException));
    }
    navLogUtil.instance().log.call(this, "startTx", "Begin Transaction", "debug");
    return this.dbQuery("BEGIN");
}

function commitTx() {
    if (!this.providedClient) {
        navLogUtil.instance().log.call(this, "commitTx", "Invalid Client", "error");
        return Q.reject(navCommonUtils.getErrorObject({message : "Invalid Client"}, 500, "DBTRANSAC", navDatabaseException));
    }
    navLogUtil.instance().log.call(this, "commitTx", "Commit Transaction", "debug");
    return this.dbQuery("COMMIT");
}

function rollbackTx(clientFromPool, savePointName) {
    if (!this.providedClient) {
        navLogUtil.instance().log.call(this, "rollBackTx", "Invalid Client", "error");
        return Q.reject(new navCommonUtils().getErrorObject({message : "Invalid Client"}, 500, "DBTRANSAC", navDatabaseException));

    }    
    navLogUtil.instance().log.call(this, "rollbackTx", "Rollback Transaction", "debug");

    if (savePointName) {
        return this.dbQuery("ROLLBACK TO SAVEPOINT " + savePointName + ";");
    } else {
        return this.dbQuery("ROLLBACK;");
    }

}

/*function savePointTx(clientFromPool, savePointName) {
 if (!clientFromPool) {
 throwError("Can't start tx, invalid client");
 }
 if (!savePointName) {
 throwError("Need save point name");
 }
 return clientFromPool.query("SAVEPOINT " + savePointName + ";");
 }*/

