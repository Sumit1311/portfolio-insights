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


var BaseDAO = require(process.cwd() + "/lib/dao/base/baseDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navPasswordUtil = require(process.cwd() + "/lib/navPasswordUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js'),
    util = require("util");

function UserDAO(client, persistence) {
    var self = this;
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
    rootUserId = "45058a54-b3e2-4a3b-96ab-c13dcf3023e3";

/**
 * Get login details for the user specified by loginName
 *
 * @returns {*}
 */
UserDAO.prototype.getLoginDetails = function (loginName) {
    var self = this;
    navLogUtil.instance().log.call(this, "getLoginDetails", "Getting information for "+loginName, "info");

    return this.dbQuery("SELECT _id,password,email_verification,email_address,mobile_no,first_name,last_name,user_type, deposit, address, balance" +
    " FROM " + tableName + " WHERE email_address=$1", [loginName])
        .then(function (result) {
            navLogUtil.instance().log.call(self, "getLoginDetails", "Login Details for "+ loginName + "with id ", "debug");
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
    navLogUtil.instance().log.call(this, "getAddress", "Get Address details for "+userId, "info");
    return this.dbQuery("SELECT address, city, state, pin_code" +
    " FROM " + tableName + " WHERE _id=$1", [userId])
        .then(function (result) {
            navLogUtil.instance().log.call(self, "getAddress", "Get Address details for "+userId, "debug");
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
UserDAO.prototype.createRootUser = function () {
    var self = this;
    navLogUtil.instance().log.call(this, "createRootUser", "Create root user", "info");
    return self.dbQuery('select * from ' + tableName + ' where _id=$1', [rootUserId])
        .then(function (result) {
            if (result.rowCount === 0) {
                return self.dbQuery('INSERT INTO ' + tableName + '(_id,first_name,user_type,email_address,password) ' +
                'VALUES($1,$2,$3,$4,$5)', [rootUserId, "Admin", 0, "_root_@localhost.com", new navPasswordUtil().encryptPassword("_toor_")]);
            } else {
                return Q.resolve();
            }
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "createRootUser", error.message, "error");
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
    navLogUtil.instance().log.call(this, "getEmailVerificationDetails", "Getting verification details "+email, "debug");
    return this.dbQuery("select email_address,mobile_no,email_verification " +
    "from " + tableName + " where email_address = $1", [email])
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getEmailVerificationDetails", error.message, "error");
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
    navLogUtil.instance().log.call(this, "insertRegistrationData", "Insert registration data for "+email +", "+ ", " + phone , "debug");
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
UserDAO.prototype.updateUserDetails = function (pkey, firstName, lastName, address, membershipExpiry, enrollmentDate, pinCode, password) {
    var self = this;
    navLogUtil.instance().log.call(this, "updateUserDetails", "Update user details for : "+ pkey , "debug");
    var queryString = "UPDATE " + tableName +
            " SET " +
            " first_name=$1," +
            " last_name=$2," +
            " address = $3," +
            " pin_code = $4 ";
    var params = [firstName, lastName, address,  pinCode]
    var count = 5;
    if(membershipExpiry) {
        queryString += " ,membership_expiry = $" + count+" ";
        count++;
        params.push(membershipExpiry);
    }

    if(password) {
        queryString += " ,password = $" + count+" ";
        count++;
        params.push(password); 
    }
    if(enrollmentDate) {
        queryString += ", enrollment_date = $" +count + " ";
        count++
        params.push(enrollmentDate);
    }

    queryString += " WHERE _id=$"+count;
    params.push(pkey);

    return this.dbQuery(queryString, params)
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
    navLogUtil.instance().log.call(this, "clearVerificationCode", "Clearing verification : "+ _id , "debug");
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
UserDAO.prototype.getUserDetailsByCode = function (verifCode, isResetPassword) {
    var self = this;
    navLogUtil.instance().log.call(this, "getUserDetailsByCode", "Get details for verification code : "+ verifCode , "debug");
    return this.dbQuery("SELECT _id,password," + (isResetPassword ? "reset_password, " :  " email_verification," )+"email_address,mobile_no,first_name,last_name,user_type" +
    " FROM " + tableName +
    " WHERE "+ (isResetPassword ? "reset_password" : "email_verification") +"=$1", [verifCode])
        .then(function (result) {
            navLogUtil.instance().log.call(self, "getUserDetailsByCode", "Details for verification code : "+ verifCode, "debug");
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getUserDetailsByCode", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        })
};

UserDAO.prototype.updatePlan = function (userId, plan){
    var self = this;
    navLogUtil.instance().log.call(this, "getUserDetailsByCode", "Update plan  "+ userId , "debug");
    return this.dbQuery("UPDATE " + tableName + 
    " SET subscribed_plan = $1 WHERE _id = $2;",
    [plan, userId])
        .then(function (result) {
            navLogUtil.instance().log.call(self, "getUserDetailsByCode", "Updated rows "+ result.rowCount , "debug");
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}

UserDAO.prototype.getUserDetails = function(userId) {
    var self = this;
    
    navLogUtil.instance().log.call(this, "getUserDetails", "Get additional details for : "+ userId , "debug");
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
UserDAO.prototype.updatePoints = function (userId, points, decrement, membershipExpiry){
    var i = 1;
    var query = "UPDATE " + tableName +
        " SET balance = balance "+ (decrement ? " - " : " + ") +"$" + i;
    i++;
    var params = [points];
    if(membershipExpiry) {
        query += ", membership_expiry = $" + i;
        i++;
        params.push(membershipExpiry);
    }
    query += " WHERE _id = $" + i;
    params.push(userId);
    var self = this;
    navLogUtil.instance().log.call(this, "updatePoints", "Points for user id : "+ userId + "updated to "+points , "debug");
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
    navLogUtil.instance().log.call(this, "updateMembershipExpiry", "Membership expiry of "+ userId + " updating to "+membershipExpiry , "debug");
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
UserDAO.prototype.updateBalance = function (userId, amount, decrement){
    var self = this;
    navLogUtil.instance().log.call(this, "updateBalance", "Update balance to user id : "+ userId + " with "+ decrement+ amount , "debug");
    return this.dbQuery("UPDATE " + tableName + 
    " SET balance = balance"+(decrement ? "-" : "+") + "$1 WHERE _id = $2;",
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}
UserDAO.prototype.updateDeposit = function (userId, amount, decrement){
    var self = this;
    navLogUtil.instance().log.call(this, "updateDeposit", "Update deposit for user id : "+ userId + "updated to "+decrement +amount , "debug");
    return this.dbQuery("UPDATE " + tableName + 
    " SET deposit = deposit" + (decrement ? "-" : "+") + "$1 WHERE _id = $2;",
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updatePlan", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}

UserDAO.prototype.getAllUsers = function() {
    var self = this;
    
    return this.dbQuery("SELECT _id,email_address" +
    " FROM " + tableName)
        .then(function (result) {
            return result.rows;
        })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "getAllUsers", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));
        })

}

UserDAO.prototype.updateResetPassword = function(email, code) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET reset_password = $1 WHERE email_address = $2;",
    [code, email])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "updateResetPassword", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}

UserDAO.prototype.resetPassword = function(userId, password) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET reset_password = $1, password=$2 WHERE _id = $3;",
    [null, password, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "resetPassword", error.message, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}
UserDAO.prototype.transferFromDepositToBalance = function(userId , amount) {
    var self = this;
    return this.dbQuery("UPDATE " + tableName + 
    " SET deposit = deposit - $1, balance = balance + $1 WHERE _id = $2;",
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "transferFromDepositToBalance", error.stack, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
    


}

UserDAO.prototype.doTransfer = function(userId, from, to, amount) {
    var query = "UPDATE "+tableName + " SET "+from + " =  " + from + " - $1, "+ to + " = "+to+" + $1 WHERE _id = $2";

    var self = this;
    return this.dbQuery(query,
    [amount, userId])
        .then(function (result) {
            return result.rowCount;
        })
        .catch(function (error) {
            new navLogUtil().log.call(self, "doTransfer", error.stack, "error");
            return Q.reject(new navCommonUtil().getErrorObject(error, 500, "DBUSER", navDatabaseException));

        });
}
