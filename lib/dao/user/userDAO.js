/**
 * UserDAO --
 *  Used to interact with the table user_master. Has methods for CRUD operations on this table.
 *
 *  Note about user_type column :
 *      0 --- Super Admin
 *      1 --- Admin
 *      2 --- Normal User
 *      3 --- Moderator
 *      4 --- Guest
 *
 */

"use strict";

var BaseDAO = require(process.cwd() + "/lib/dao/base/baseDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navPasswordUtil = require(process.cwd() + "/lib/navPasswordUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js'),
    util = require("util");

function UserDAO(client, persistence) {
    if (persistence) {
        BaseDAO.call(self, persistence);
    }
    this.providedClient = client ? client : undefined;
    return this;
}

util.inherits(UserDAO, BaseDAO);

module.exports = UserDAO;
//private variables
var tableName = "nav_user",
    rootUserId = "45058a54-b3e2-4a3b-96ab-c13dcf3023e3",
    fileName = 'user/masterDAO';

/**
 * Get login details for the user specified by loginName
 *
 * @returns {*}
 */
UserDAO.prototype.getLoginDetails = function (loginName) {
    var self = this;
    return this.dbQuery("SELECT _id,password,email_verification,email_address,mobile_no,first_name,last_name,user_type, deposit" +
    " FROM " + tableName + " WHERE email_address=$1", [loginName])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getLoginDetails", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};

/**
 * Get address for the user specified by id
 *
 * @returns {*}
 */
UserDAO.prototype.getAddress = function (userId) {
    var self = this;
    return this.dbQuery("SELECT address, city, state" +
    " FROM " + tableName + " WHERE _id=$1", [userId])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getAddress", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};
/**
 * Creates the super admin of the application.
 *
 * @returns {*}
 */
UserDAO.prototype.createRootUser = function (client) {
    var self = this;
    return self.dbQuery('select * from ' + tableName + ' where _id=$1', [rootUserId])
        .then(function (result) {
            if (result.rowCount == 0) {
                return self.dbQuery('INSERT INTO ' + tableName + '(_id,first_name,user_type,email_address,password) ' +
                'VALUES($1,$2,$3,$4,$5)', [rootUserId, "Admin", 0, "_root_@localhost.com", new navPasswordUtil().encryptPassword("_toor_")]);
            } else {
                return Q.resolve();
            }
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getAddress", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};

/**
 * This method retireves email verification details for the given user
 *
 * @param email : user's email id
 * @returns {*}
 */
UserDAO.prototype.getEmailVerificationDetails = function (email) {
    var self = this;
    return this.dbQuery("select email_address,mobile_no,email_verification " +
    "from " + tableName + " where email_address = $1", [email])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getAddress", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        })
};

/**
 * This method inserts basic registration data of a new user.
 *
 * @param email
 * @param phone
 * @param verificationCode
 * @returns {*}
 */
UserDAO.prototype.insertRegistrationData = function (email, phone, password, verificationCode) {
    var self = this;
    return this.dbQuery("INSERT INTO " + tableName +
    " (_id,email_address,mobile_no,email_verification, password)" +
    " VALUES($1,$2,$3,$4,$5)", [new navCommonUtil().generateUuid(), email, phone, verificationCode, password])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "insertRegistrationData", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};

/**
 * This method updates the user's basic profile details at time of email verification.
 *
 * @param pkey
 * @param loginPassword
 * @param firstName
 * @param lastName
 * @param userType
 * @returns {*}
 */
UserDAO.prototype.updateUserDetails = function (pkey, firstName, lastName, address, membershipExpiry, enrollmentDate) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName +
    " SET " +
    " first_name=$1," +
    " last_name=$2," +
    " address = $3," +
    " membership_expiry = $4," +
    " enrollment_date = $5" +
    " WHERE _id=$6", [ firstName, lastName, address, membershipExpiry, enrollmentDate, pkey])
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "updateUserDetails", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        });
};

/**
 * Clear email verification code as verification has been successful. for given user_id
 *
 * @param _id
 * @returns {*}
 */
UserDAO.prototype.clearVerificationCode = function (_id) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName + "" +
    " SET email_verification=$1" +
    " WHERE _id=$2", [null, _id])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "clearVerificationCode", error.message, "error");
            return Q.reject(navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
};

/**
 * This method retrieves user data based on verification code. Used for email verification step.
 *
 * @param verifCode
 * @returns {*}
 */
UserDAO.prototype.getUserDetailsByCode = function (verifCode) {
    var self = this;
    return this.dbQuery("SELECT _id,password,email_verification,email_address,mobile_no,first_name,last_name,user_type" +
    " FROM " + tableName +
    " WHERE email_verification=$1", [verifCode])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getUserDetailsByCode", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        })
};

UserDAO.prototype.updatePlan = function (userId, plan){
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET subscribed_plan = $1 WHERE _id = $2;",
    [plan, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}

UserDAO.prototype.getUserDetails = function(userId) {
    var self = this;
    
    return this.dbQuery("SELECT subscribed_plan, points, balance, membership_expiry, enrollment_date, deposit" +
    " FROM " + tableName +
    " WHERE _id=$1", [userId])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getUserDetails", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        })

}
UserDAO.prototype.updatePoints = function (userId, points, membershipExpiry){
    var i = 1;
    var query = "UPDATE " + tableName +
        " SET balance = $" + i;
    i++;
    var params = [points];
    if(membershipExpiry) {
        query += ", membership_expiry = $" + i;
        i++;
        params.push(membershipExpiry);
    }
    query += " WHERE _id = $" + i;
    params.push(userId);
    console.log(query, params);
    var self = this;
    return this.dbQuery(query, params)
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePoints", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });

}

UserDAO.prototype.updateMembershipExpiry =function (userId, membershipExpiry) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET membership_expiry = $1  WHERE _id = $2;",
    [membershipExpiry, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
	
}
UserDAO.prototype.updateBalance = function (userId, amount){
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET balance = balance + $1 WHERE _id = $2;",
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}
UserDAO.prototype.updateDeposit = function (userId, amount){
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET deposit = deposit + $1 WHERE _id = $2;",
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}
