const querystring = require('querystring');
var navBaseRouter = require(process.cwd() + '/lib/navBaseRouter.js'),
    navResponseUtil = require(process.cwd() + '/lib/navResponseUtil.js'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    validator = require('validator'),
    navAccount = require(process.cwd() + "/lib/navAccount.js"),
    navCommonUtil = require(process.cwd() + '/lib/navCommonUtil.js'),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navOrders = require(process.cwd() + "/lib/navOrders.js"),
    navPayments = require(process.cwd() + "/lib/navPayments.js"),
    navPaymentsDAO = require(process.cwd() + "/lib/dao/payments/navPaymentsDAO.js"),
    navRentalsDAO = require(process.cwd() + "/lib/dao/rentals/navRentalsDAO.js"),
    navMembershipParser = require(process.cwd() + "/lib/navMembershipParser.js"),
    Q = require('q');

module.exports = class navUserAccountRouter extends navBaseRouter {
    constructor() {
        super(); 
    }
    setup(){
        var self = this;
        this.router.use(this.isSessionAvailable.bind(this), this.ensureAuthenticated.bind(this), this.ensureVerified.bind(this))
        this.router.get('/rechargeDetails', function(req,res, next) {self.getRechargeDetails(req,res,next)});
        this.router.get('/orderDetails', function(req,res, next) {self.getOrderDetails(req,res,next)}); 
        this.router.get("/accountDetails", function(req,res, next) {self.getAccountDetails(req,res,next)});
        this.router.post("/accountDetails", function(req,res, next) {self.postAccountDetails(req,res,next)});
        this.router.post("/childDetails", function(req,res, next) {self.postChildDetails(req,res,next)});
        return this;
    }

    getRechargeDetails(req, res) {
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        var user = req.user, userDetails, debitTransactions = [], creditTransactions = [], plans, membershipPlans;
        deferred.promise
            .done(function(){
                var transactions = debitTransactions.concat(creditTransactions);
                transactions.sort(function(a, b){
                    if(a.dateMilis < b.dateMilis) {
                        return true;
                    }
                    return false;
                })
                res.render("rechargeDetails",{
                    user : req.user,
                    userDetails : {
                        enrollmentDate : new navCommonUtil().getDateString(parseInt(userDetails.enrollment_date)),
                        membershipExpiryDate : userDetails.membership_expiry !== null ? new navCommonUtil().getDateString(parseInt(userDetails.membership_expiry)) : false,
                        deposit : userDetails.deposit,
                        balance : userDetails.balance === null ? 0 : userDetails.balance,
                        membershipStatus :   (userDetails.membership_expiry === null ? true : ( parseInt(userDetails.membership_expiry) > new navCommonUtil().getCurrentTime()) ? true : false),
                    },
                    transactions : transactions,
                    isLoggedIn : req.user ? true : false,
                    layout : 'nav_bar_layout',
                    plans : plans,
                    membershipPlans : membershipPlans,
                    helpers : {
                        getClass : function(status) {
                            var lableClass;
                            switch(status) {
                                case navPaymentsDAO.getStatus().PENDING :
                                case navPaymentsDAO.getStatus().PENDING_COD :
                                    lableClass = "warning";
                                    break;
                                case navRentalsDAO.getStatus().DELIVERED:
                                case navRentalsDAO.getStatus().PLACED:
                                case navRentalsDAO.getStatus().RETURNED:
                                case navPaymentsDAO.getStatus().COMPLETED :
                                case navPaymentsDAO.getStatus().COMPLETED_CASH :
                                    lableClass = "success";
                                    break;
                                case navRentalsDAO.getStatus().CANCELLED:
                                case navPaymentsDAO.getStatus().CANCELLED :
                                case navPaymentsDAO.getStatus().FAILED :
                                    lableClass = "danger";
                                    break;

                                default :
                                    lableClass = "default";
                                    break;

                            }
                            return lableClass;
                        }
                    }
                
                });
        },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',
            
                });
        });
        new navAccount().getWalletDetails(user._id)
            .then((_userDetails) =>{
                userDetails = _userDetails[0];
                return new navPayments().getPayments(user._id);
            } )
            .then((_transactions) => {
                creditTransactions = _transactions;
                return new navOrders().getDebitTransactions(user._id);
            })
            .done((_transactions) => {
                debitTransactions = _transactions;
                plans = navMembershipParser.instance().getConfig("plans",[]); 
                membershipPlans =  navMembershipParser.instance().getConfig("membership",[]); 
                deferred.resolve();
            },(error) => {
                navLogUtil.instance().log.call(self, self.getRechargeDetails.name, "Error occured Details : " + error.stack, "error");
                deferred.reject(error);
            });
    
    }

    getOrderDetails(req, res){
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        var user = req.user;
        deferred.promise
            .done(function(orders){
                res.render("orderDetails",{
                    user : req.user,
                    isLoggedIn : req.user ? true : false,
                    layout : 'nav_bar_layout',
                    orders : orders,
                    helpers : {
                        getClass : function(status) {
                            var lableClass;
                            //console.log(status);
                            switch(status) {
                                case navRentalsDAO.getStatus().DELIVERED:
                                    lableClass = "success";
                                    break;
                                case navRentalsDAO.getStatus().PLACED:
                                    lableClass = "info";
                                    break;
                                case navRentalsDAO.getStatus().RETURNED:
                                    lableClass = "warning";
                                    break;
                                case navRentalsDAO.getStatus().CANCELLED:
                                    lableClass = "danger";
                                    break;
                                default :
                                    lableClass = "default";
                                    break;
                            }
                            return lableClass;
                        },
                        disableCancel : function(status, options) {
                            if(status === "PLACED" || status === "PENDING_GATEWAY") {
                                return options.inverse(this);
                            }
                            return options.fn(this);

                        }
                    }

                });
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',

                });
            });
        return new navOrders().getAllUserOrders(user._id)
            .done((_orders) => {
                deferred.resolve(_orders);
            },(error) => {
                navLogUtil.instance().log.call(self, self.getOrderDetails.name, "Error occured Details : " + error, "error");
                deferred.reject(error);
            });
    
    }

    getAccountDetails(req, res) {
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        var user = req.user;
        deferred.promise
            .done(function(result){
                res.render("accountDetails",{
                    user : user,
                    isLoggedIn : req.user ? true : false,
                    layout : 'nav_bar_layout',
                    children : result,
                    ageGroups : navCommonUtil.getAgeGroups(),
                    helpers : {
                    }

                });
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'nav_bar_layout',

                });
            });
        return new navAccount().getCommunicationDetails(user._id)
            .then((address) => {
                user.shippingAddress = address.address;
                user.pinCode = address.pin_code;
                return new navAccount().getChildDetails(user._id);
            })
            .done((children) => {
                deferred.resolve(children);
            }, (error) => {
                navLogUtil.instance().log.call(self, self.getAccountDetails.name, "Error occured Details : " + error, "error");
                deferred.reject(error);
                
            })
    }

    postAccountDetails(req, res) {
        var self = this;
        var body = req.body;
        var firstName = body.firstName,
            lastName = body.lastName,
            address = body.shippingAddress,
            pinCode = req.body.pinCode;

        var deferred = Q.defer();
        deferred.promise
            .done(() => {
                new navResponseUtil().sendAjaxResponse(res, {
                    message : "Success"
                });
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
        req.assert("firstName","First Name is Required").notEmpty();
        req.assert("firstName","Max length of First name is 10").len(1,10);
        req.assert("lastName","First Name is Required").notEmpty();
        req.assert("shippingAddress","First Name is Required").notEmpty();
        req.assert("pinCode","Pin Code Required").notEmpty();
        //req.assert("ageGroup","Age Group Required").notEmpty();
        //req.assert("gender","Gender Required").notEmpty();


        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navValidationException(validationErrors));
        }

        var password = req.body.newPassword, passwordConf = req.body.newPasswordConf;
        if(password !== passwordConf) {
            return deferred.reject(new navValidationException(validationErrors));
        }
        new navAccount().updateAccountDetails(req.user._id, {
            firstName : firstName,
            lastName : lastName,
            address : address,
            pinCode : pinCode,
            password : password === undefined ? "" : password,
            passwordConf : passwordConf === undefined ? "" : passwordConf
        })
        .done(() => {
            deferred.resolve();
        },(error) => {
            navLogUtil.instance().log.call(self,self.postAccountDetails.name, 'Error while doing registration step 3' + error, "error");
            return deferred.reject(error);
        });
    }

    postChildDetails(req, res) {
        var self = this;
        var childDetails = req.body, children = [], validationFlag = false;
        for(var i = 0; i < childDetails.length; i++) {
            var de = querystring.parse(childDetails[i]);
            if(!validator.isEmpty(de.childId) &&
                validator.isUUID(de.childId)) { 
                children.push(de);
            } else {
                validationFlag = true;
            }

        }

       
        var deferred = Q.defer();
        if(validationFlag) {
            return deferred.reject(new navValidationException());
        }
        deferred.promise
            .done(() => {
                new navResponseUtil().sendAjaxResponse(res, {
                    message : "Success"
                });
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


        new navAccount().updateChildrenDetails(req.user._id, children)
        .done(() => {
            deferred.resolve();
        },(error) => {
            navLogUtil.instance().log.call(self,self.postChildDetails.name, 'Error while doing registration step 3' + error, "error");
            return deferred.reject(error);
        });
    }
}
