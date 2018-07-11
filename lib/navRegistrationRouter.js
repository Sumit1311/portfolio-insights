var navBaseRouter = require(process.cwd() + '/lib/navBaseRouter.js'),
    Q = require('q'),
    navResponseUtil = require(process.cwd() + '/lib/navResponseUtil.js'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    navLogicalException = require("node-exceptions").LogicalException,
    navEmailVerification= require(process.cwd() + "/lib/navEmailVerification.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navAccount = require(process.cwd() + "/lib/navAccount.js");

module.exports = class navRegistration extends navBaseRouter {
    constructor() {
        super();
    }
    setup(){
        var self = this;
        this.router.post('/register', function(req,res, next) {self.doRegistration(req,res,next)});
        this.router.get('/verify', function(req,res, next) {self.doEmailVerification(req,res,next)}); 
        this.router.get('/resetPassword', function(req,res, next) {self.getResetPasswordInfo(req,res,next)}); 
        this.router.post('/resetPassword', function(req,res, next) {self.resetPassword(req,res,next)}); 
        this.router.post('/reset', function(req,res, next) {self.doResetPassword(req,res,next)}); 
        this.router.get('/reset', function(req,res, next) {self.getResetPassword(req,res,next)}); 
        this.router.post("/registrationDetails", function(req,res, next) {self.saveAdditionalDetails(req,res,next)});
        this.router.get("/registrationSuccess",this.getRegistrationSuccess.bind(this));
        this.router.get("/resetPasswordSuccess",this.getResetPasswordSuccess.bind(this));
        return this;
    }
    doRegistration(req, res){
        var email = req.body.email, password = req.body.password, contactNo = req.body.mobileNo = req.body.mobileNo, passwordConf = req.body.passwordConf;
        var verificationCode;
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        deferred.promise
            .done(function(){
                respUtil.redirect(req, res, "/registrationSuccess");
        },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
            /*response = new navResponseUtil().generateErrorResponse(error);
            res.status(response.status).render("errorDocument",{
                errorResponse : response,
                user : req.user,
                isLoggedIn : false,
                layout : 'nav_bar_layout',
            });*/

        })
        req.assert("email","Email is Required").notEmpty();
        req.assert("email","Valid Email Required").isEmail();
        req.assert("password","Password is Required").notEmpty();
        req.assert("password","Valid Password Required").isValidPassword();
        req.assert("passwordConf","Password is Required").notEmpty();
        req.assert("passwordConf","Valid Password Required").isValidPassword();
        req.assert("mobileNo","Mobile No Required").notEmpty();
        //req.assert("mobileNo","Valid Mobile No Required").isMobilePhone(contactNo, "any");
        var validationErrors = req.validationErrors();
        //console.log(validationErrors);
        if(validationErrors) {
            return deferred.reject(new navValidationException(validationErrors));
        }
        if(password != passwordConf) {
            return deferred.reject(new navLogicalException());
        }
        navLogUtil.instance().log.call(self, self.doRegistration.name, "New user registration : " + email, "info")

        new navAccount().checkIfUserExists(email)
        .then(function(){
            var emailVer = new navEmailVerification();
            verificationCode = emailVer.generateCode();
            var base = new navCommonUtil().getBaseURL(req);
            base.pathname = "/verify";
            base.search = "?id=" + verificationCode;
            var verificationLink = base.format();
            navLogUtil.instance().log.call(self, self.doRegistration.name, "Verification link for user : " + email + " "+ verificationLink, "info");

             //return userDAO.insertRegistrationData(email, contactNo, password,verificationCode);
             //todo : uncomment when want to send verification email
             return emailVer.sendVerificationEmail(email, email, verificationLink)
        })
        .then(function (response) {
             navLogUtil.instance().log.call(self, self.doRegistration.name," Sent verificiation email" + response, 'info');
             return new navAccount().registerUser({ 
                 email :email, 
                 contactNo : contactNo, 
                 password : password, 
                 verificationCode : verificationCode
             });
        })
        .done(function(){
             return deferred.resolve();
        },
        function (error) {
             navLogUtil.instance().log.call(self, self.doRegistration.name,"Error Occured : " + error, 'error');
             return deferred.reject(error);
        });

    }
    doEmailVerification(req, res ) {
        var self = this;
        var code = req.query.id;
        var deferred = Q.defer();
        var ageGroups = navCommonUtil.getAgeGroups();

        deferred.promise
            .done((user) => {
                res.render('registrationDetails',{
                    layout : "nav_bar_layout",
                    isLoggedIn : true,
                    user : user,
                    ageGroups : ageGroups,
                    verificationCode : user.email_verification
                } );
            },(error) => {
                var respUtil =  new navResponseUtil();
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
        
            });
        req.assert("id","Id is Required").notEmpty();
        req.assert("id","Id not valid").isUUID();

        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navLogicalException());
        }
        (new navAccount()).getDetailsForCode(code)
            .done(function (userDetails) {
                deferred.resolve(userDetails);
            }, (error) => {
                navLogUtil.instance().log.call(self, self.doEmailVerification.name, "Error Occured  Reason : " + error.stack, "error");
                deferred.reject(error);
            })
        
    }
    saveAdditionalDetails(req,res) {
        var self = this;
        var body = req.body;
        var loginEmailId = body.email,
            firstName = body.firstName,
            lastName = body.lastName,
            address = body.shippingAddress,
            verificationCode = req.query.code,
            pinCode = req.body.pinCode,
            ageGroup = req.body.ageGroup,
            gender = req.body.gender,
            hobbies = req.body.hobbies;

        var deferred = Q.defer();
        deferred.promise
            .done(() => {
                new navResponseUtil().redirect(req, res, "/");
            },(error) => {
                var respUtil =  new navResponseUtil();
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
        
             })
        req.assert("email","Email is Required").notEmpty();
        req.assert("email","Valid Email is Required").isEmail();
        req.assert("firstName","First Name is Required").notEmpty();
        req.assert("firstName","Max length of First name is 10").len(1,10);
        req.assert("lastName","First Name is Required").notEmpty();
        req.assert("shippingAddress","First Name is Required").notEmpty();
        req.assert("code","Code is Required").notEmpty();
        req.assert("code","Bad Request").isUUID();
        req.assert("pinCode","Pin Code Required").notEmpty();
        //req.assert("ageGroup","Age Group Required").notEmpty();
        //req.assert("gender","Gender Required").notEmpty();


        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navValidationException(validationErrors));
        }
        new navAccount().completeVerification(verificationCode, {
            loginEmailId : loginEmailId,
            firstName : firstName,
            lastName : lastName,
            address : address,
            pinCode : pinCode,
            ageGroup : ageGroup,
            hobbies : hobbies,
            gender : gender
        })
        .done((user) => {
            req.logIn(user, err => {
                if (err) {
                    return deferred.reject(err);
                }
                // Redirect to homepage
                return deferred.resolve();
            }) 
        },(error) => {
            navLogUtil.instance().log.call(self,self.saveAdditionalDetails.name, 'Error while doing registration step 2' + error, "error");
            return deferred.reject(error);
        });
    }
    getRegistrationSuccess(req, res) {
                res.render('registrationSuccess',{
                    layout : 'nav_bar_layout',
                    isLoggedIn : req.user ? true : false,
                });
    }
    getResetPasswordSuccess(req, res) {
        res.render('resetPasswordSuccess',{
            layout : 'nav_bar_layout',
            isLoggedIn : req.user ? true : false,
        });
    }

    getResetPasswordInfo(req, res) {
        res.render('resetPasswordInfo',{
            layout : 'nav_bar_layout',
            isLoggedIn : req.user ? true : false,
        });
    }

    resetPassword(req, res) {
        var email = req.body.email;
        var verificationCode;
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        deferred.promise
            .done(function(){
                respUtil.redirect(req, res, "/resetPassword");
        },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
            /*response = new navResponseUtil().generateErrorResponse(error);
            res.status(response.status).render("errorDocument",{
                errorResponse : response,
                user : req.user,
                isLoggedIn : false,
                layout : 'nav_bar_layout',
            });*/

        })
        req.assert("email","Email is Required").notEmpty();
        req.assert("email","Valid Email Required").isEmail();

        var validationErrors = req.validationErrors();
        //console.log(validationErrors);
        if(validationErrors) {
            return deferred.reject(new navValidationException(validationErrors));
        }
        navLogUtil.instance().log.call(self, self.resetPassword.name, "Reset User Password : " + email, "info")

        new navAccount().checkIfUserExistsWithoutExp(email)
        .then(function(flag){
            if(flag) {
            var emailVer = new navEmailVerification();
            verificationCode = emailVer.generateCode();
            var base = new navCommonUtil().getBaseURL(req);
            base.pathname = "/reset";
            base.search = "?id=" + verificationCode;
            var verificationLink = base.format();
            navLogUtil.instance().log.call(self, self.resetPassword.name, "Reset Password link for user : " + email + " "+ verificationLink, "info");

             //return userDAO.insertRegistrationData(email, contactNo, password,verificationCode);
             //todo : uncomment when want to send verification email
             return emailVer.sendResetPassword(email, null, verificationLink)
            } else {
                return Q.reject(new navLogicalException());
            }

        })
        .then(function (response) {
             navLogUtil.instance().log.call(self, self.resetPassword.name," Sent reset password email" + response, 'info');
             return new navAccount().resetUserPassword({ 
                 email :email, 
                 verificationCode : verificationCode
             });
        })
        .done(function(){
             return deferred.resolve();
        },
        function (error) {
             navLogUtil.instance().log.call(self, self.resetPassword.name,"Error Occured : " + error, 'error');
             return deferred.reject(error);
        });
    
    }

    getResetPassword(req, res) {
        var self = this;
        var code = req.query.id;
        var deferred = Q.defer();

        deferred.promise
            .done((user) => {
                res.render('resetPasswordPage',{
                    layout : "nav_bar_layout",
                    isLoggedIn : false,
                    user : user,
                    verificationCode : user.reset_password
                } );
            },(error) => {
                var respUtil =  new navResponseUtil();
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
        
            });
        req.assert("id","Id is Required").notEmpty();
        req.assert("id","Id not valid").isUUID();

        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navLogicalException());
        }
        (new navAccount()).getDetailsForCode(code, true)
            .done(function (userDetails) {
                deferred.resolve(userDetails);
            }, (error) => {
                navLogUtil.instance().log.call(self, self.getResetPassword.name, "Error Occured  Reason : " + error.stack, "error");
                deferred.reject(error);
            })
         
    }
    doResetPassword(req, res) {
        var self = this;
        var body = req.body;
        var code = req.query.code,
            password = body.password,
            passwordConf = body.passwordConf;

        var deferred = Q.defer();
        deferred.promise
            .done(() => {
                new navResponseUtil().redirect(req, res, "/resetPasswordSuccess");
            },(error) => {
                var respUtil =  new navResponseUtil();
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',

                });

            })
        req.assert("code","Email is Required").notEmpty();
        req.assert("code","Email is Required").isUUID();
        req.assert("password","Password not provided").notEmpty();
        req.assert("passwordConf","Password Confirmation necessary").notEmpty();


        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navValidationException(validationErrors));
        }
        if(password != passwordConf) {
            return deferred.reject(new navLogicalException());
        }
        new navAccount().completeResetPassword(code, {
            password : password,
            passwordConf : passwordConf,
        })
            .done(() => {
                /*req.logIn(user, err => {
                    if (err) {
                        return deferred.reject(err);
                    }
                    // Redirect to homepage
                },(error) => {
                    navLogUtil.instance().log.call(self,self.saveAdditionalDetails.name, 'Error while doing registration step 2' + error, "error");
                    return deferred.reject(error);
                });*/
                    return deferred.resolve();
            }, (error) => {
                    navLogUtil.instance().log.call(self,self.doResetPassword.name, 'Error while doing registration step 2' + error, "error");
                    return deferred.reject(error);
            
            })
    }
}
