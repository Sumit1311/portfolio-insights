var navUserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navLogicalException = require("node-exceptions").LogicalException,
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navUserExistsException = require(process.cwd() + "/lib/exceptions/navUserExistsException.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navPasswordUtil = require(process.cwd() + "/lib/navPasswordUtil.js"),
    Q = require('q');

module.exports = class navAccount {

    checkIfUserExists(email) {
        return new navUserDAO().getLoginDetails(email)
        .then((user) => {
            if(user.length !== 0) {
                return Q.reject(new navUserExistsException());
            }
            return Q.resolve();
        })
    }
    checkIfUserExistsWithoutExp(email) {
        return new navUserDAO().getLoginDetails(email)
        .then((user) => {
            if(user.length !== 0) {
                return true;
            }
            return false;
        })
    }

    registerUser(userDetails) {
        return new navUserDAO().insertRegistrationData(userDetails.email, userDetails.contactNo, new navPasswordUtil().encryptPassword(userDetails.password), userDetails.verificationCode);
    }

    getDetailsForCode(code, isResetPassword) {
        return (new navUserDAO()).getUserDetailsByCode(code, isResetPassword)
        .then(function(userDetails){
            if(userDetails.length === 0) {
                return Q.reject(new navLogicalException("Invalid Code"));
            }
            return Q.resolve(userDetails[0]);
        })
        .catch((error) => {
            return Q.reject(error);
        })

    }

    completeVerification(verificationCode ,additionalDetails) {
        var self = this;
        var userDAO = new navUserDAO(), user; 
        return userDAO.getClient()
            .then(function (_client) {
            userDAO.providedClient = _client;
            return userDAO.startTx();
        })
        .then(function () {
            return userDAO.getUserDetailsByCode(verificationCode);
        })
        //todo : uncomment once email verification done and comment above then
        .then(function (userDetails) {
            if(userDetails.length === 0) {
                return Q.reject(new navLogicalException());
            }
            if(userDetails[0].email_address != additionalDetails.loginEmailId) {
                return Q.reject(new navLogicalException());
            }

            user = userDetails[0];
            if (user.email_verification == verificationCode) {
                return userDAO.clearVerificationCode(user._id)
            } else {
                return Q.reject(new navLogicalException());
            }
        })
        .then(function () {
            var time = new navCommonUtil().getCurrentTime();
            //enable whenever want to enable membership
            //TODO : PORTFOLIO need to check what to do with this
            return userDAO.updateUserDetails(user._id, additionalDetails.firstName, additionalDetails.lastName, additionalDetails.address, null/*moment().add(30, "days").valueOf()*/, time, additionalDetails.pinCode);
        })
        .then(function () {
            return userDAO.commitTx();
        })
        .then(() => {
            return Q.resolve(user);
        })
        .catch(
        function (error) {
            //logg error
            navLogUtil.instance().log.call(self,self.completeVerification.name, 'Error while doing registration step 2' + error, "error");
            return userDAO.rollBackTx()
                .then(function () {
                    return Q.reject(error);
                    //res.status(500).send("Internal Server Error");
                })
                .catch(function (err) {
                    //log error
                    navLogUtil.instance().log.call(self,self.completeVerification.name, 'Error while doing registration step 2' + err, "error");
                    return Q.reject(err)
                })
        })
        .finally(function () {
            if (userDAO.providedClient) {
                userDAO.providedClient.release();
                userDAO.providedClient = undefined;
            }
        })
    }
    
    getWalletDetails(userId) {
        return new navUserDAO().getUserDetails(userId);
    
    }
    
    getCommunicationDetails(userId) {
        var userDAO = new navUserDAO();
        return userDAO.getAddress(userId)
            .then((userDetails) => {
                return Q.resolve(userDetails[0]);
            })
            .catch((error) => {
                return Q.reject(error);
            });
        
    }


    resetUserPassword(userDetail) {
        return new navUserDAO().updateResetPassword(userDetail.email, userDetail.verificationCode);
    }

    completeResetPassword(code, userDetail) {
        var self = this;
        var userDAO = new navUserDAO(), user; 
        return userDAO.getClient()
            .then(function (_client) {
            userDAO.providedClient = _client;
            return userDAO.startTx();
        })
        .then(function () {
            return userDAO.getUserDetailsByCode(code, true);
        })
        //todo : uncomment once email verification done and comment above then
        .then(function (userDetails) {
            if(userDetails.length === 0) {
                return Q.reject(new navLogicalException());
            }

            user = userDetails[0];
            if (user.reset_password == code) {
                return userDAO.resetPassword(user._id, new navPasswordUtil().encryptPassword(userDetail.password));
            } else {
                return Q.reject(new navLogicalException());
            }
        })
        .then(function () {
            return userDAO.commitTx();
        })
        .then(() => {
            return Q.resolve(user);
        })
        .catch(
        function (error) {
            //logg error
            navLogUtil.instance().log.call(self,self.saveAdditionalDetails.name, 'Error while doing registration step 2' + error, "error");
            return userDAO.rollBackTx()
                .then(function () {
                    return Q.reject(error);
                    //res.status(500).send("Internal Server Error");
                })
                .catch(function (err) {
                    //log error
                    navLogUtil.instance().log.call(self,self.saveAdditionalDetails.name, 'Error while doing registration step 2' + err, "error");
                    return Q.reject(err)
                })
        })
        .finally(function () {
            if (userDAO.providedClient) {
                userDAO.providedClient.release();
                userDAO.providedClient = undefined;
            }
        })
    
    }



    updateAccountDetails(userId, userDetail) {
        var p;
        if(userDetail.password !== "") {
            p = new navPasswordUtil().encryptPassword(userDetail.password);
        }
            return new navUserDAO().updateUserDetails(userId, userDetail.firstName, userDetail.lastName, userDetail.address, null, null, userDetail.pinCode, p);
    }
}

