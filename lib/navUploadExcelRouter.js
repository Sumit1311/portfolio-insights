var navBaseRouter = require(process.cwd() + '/lib/navBaseRouter.js'),
    Q = require('q'),
    navResponseUtil = require(process.cwd() + '/lib/navResponseUtil.js'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    navLogicalException = require("node-exceptions").LogicalException,
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navExcelFileHandler = require(process.cwd() + "/lib/navExcelFileHandler.js"),
    multipart = require('connect-multiparty'),
    navStockList = require(process.cwd() + "/lib/navStockList.js"),
    navAccount = require(process.cwd() + "/lib/navAccount.js");

module.exports = class navUploadExcel extends navBaseRouter {
    constructor() {
        super();
    }
    setup(){
        var self = this;
        this.router.use(this.isSessionAvailable.bind(this), this.ensureAuthenticated.bind(this), this.ensureVerified.bind(this))
        //this.router.get('/signup', function(req,res, next) {self.doSignup(req,res,next)});
        this.router.get('/uploadExcelPage', this.getUploadExcelPage.bind(this));
        this.router.post('/doExcelColumnMapping', multipart(), function(req,res, next) {self.doExcelColumnMapping(req,res,next)});
        this.router.post('/uploadExcelData', multipart(), function(req,res, next) {self.uploadExcelData(req,res,next)});
        this.router.get('/viewProfileData', function(req,res, next) {self.getViewProfilePage(req,res,next)});
        this.router.post('/delete', function(req,res, next) {self.deleteTransaction(req,res,next)});
        this.router.post('/add', function(req,res, next) {self.addTransaction(req,res,next)});
        this.router.post('/edit', function(req,res, next) {self.editTransaction(req,res,next)});
        this.router.get('/getBSEListing', function(req,res, next) {self.getBSEListing(req,res,next)});
        return this;
    }

    getUploadExcelPage(req, res){

        var deferred = Q.defer();
        var respUtil = new navResponseUtil();

        deferred.promise
            .done(function(dataExist){
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
                res.render('upload-excel/upload-excel-page', {
                    user : req.user,
                    isLoggedIn : req.user ? true : false,
                    dataExist : dataExist,
                    layout : 'modular-main-layout'
                    /*title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'*/
                });
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });

        new navExcelFileHandler().checkIfPortfolioDataExist(req.user._id)
            .then((flag) => {
                deferred.resolve(flag);
            })
            .catch((error) => {
                deferred.reject(error);
            })
    }

    getViewProfilePage(req, res){
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();

        deferred.promise
            .done(function(portfolioData){
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
                res.render('upload-excel/view-profile-page', {
                    user : req.user,
                    isLoggedIn : req.user ? true : false,
                    portfolioData : portfolioData,
                    bseCompanies : portfolioData.companyList,
                    layout : 'modular-main-layout',
                    helpers:{
                        isModified : function(context, options) {
                            if (portfolioData.modified[context] &&
                                portfolioData.modified[context] == true) {
                                return options.fn();
                            }
                        }
                    }
                    /*title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'*/
                });
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });
        var finalData;
        return new navExcelFileHandler().getViewProfileData(req.user._id)
            .then((data) => {
                deferred.resolve(data);
            })
            .catch((error) => {
                return Q.reject(error);
            })
    }

    uploadExcelData(req, res){
        var body = req.body;
        var files = req.files;
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();
        deferred.promise
            .done(function(){
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
                res.render('upload-excel/compare-excel-page', {
                    user : req.user,
                    isLoggedIn : req.user ? true : false,
                    layout : 'modular-main-layout'
                    /*title : 'Portfolio-Insights',
                     themeTitle : 'Portfolio-Insights'*/
                });
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });

        req.assert("securityCode", "securityCode is required ").notEmpty();
        req.assert("transactionType", "transactionType is required ").notEmpty();
        req.assert("transactionDate", "transactionDate is required ").notEmpty();
        req.assert("numberOfShares", "numberOfShares is required ").notEmpty();
        req.assert("transactionAmount", "transactionAmount is required ").notEmpty();
        req.assert("actionType", "actionType is required ").notEmpty();
        var errors = req.validationErrors();
        if(errors){
            return deferred.reject(new navValidationException(errors));
        }

        if(files == undefined || files.excelFile == undefined || files.excelFile.path == undefined) {
            return deferred.reject(new navValidationException("File data required"));
        }
        if(files.excelFile.path.split('.').pop() != 'xlsx'){
            return deferred.reject(new navValidationException("Please provide file of format .xlsx"));
        }
        var excelHandler = new navExcelFileHandler(files.excelFile.path);
        var self = this;
        var respUtil =  new navResponseUtil();
        var shouldMerge = false;
        if(req.body.actionType == "merge") {
            shouldMerge = true;
        }
        else if(req.body.actionType == "overwrite") {
            shouldMerge = false;
        } else {
            return deferred.reject(new navValidationException("Invalid value for action type"));
        }
        excelHandler.parseToJson()
            .then(function(){
                return excelHandler.saveToDataBase(req.body, req.user._id, shouldMerge);
            })
            .then(function(result){
                return deferred.resolve();
            })
            .catch(function(error){
                return deferred.reject(error);
            })

    }

    doExcelColumnMapping(req, res){
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
        var files = req.files;
        if(files && files.excelFile == undefined && (files.excelFile && files.excelFile.path == undefined) ) {
            return deferred.reject(new navValidationException("File data required"));
        }
        var excelHandler = new navExcelFileHandler(files.excelFile.path);
        var keys = null;
        var xlsxToJson = require("xlsx-to-json-lc");
        xlsxToJson({
            input: files.excelFile.path,
            output: null,
            lowerCaseHeaders:true
        },(err, result) => {
            if(err) {
                res.end('{"failure" : "Something went wrong. File is either empty or corrupt. Please try again!!"}');
            }else{
                keys = Object.keys(result[0]);
                console.log(keys);
                res.end('{"keys" : "'+keys+'"}');
            }
        });
    }

    deleteTransaction(req, res) {
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();
        deferred.promise
            .done(function(){
                respUtil.redirect(req, res, "/viewProfileData")
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });
        
        var transactionId = req.body.id;
        if(transactionId == undefined || transactionId == ""){
            return deferred.reject(new navValidationException("Transaction id can't be empty"))
        }
        return new navExcelFileHandler().deleteFromPortFolio(req.user._id, transactionId)
            .then((data) => {
                deferred.resolve(data);
            })
            .catch((error) => {
                deferred.reject(error);
            })

    }

    addTransaction(req, res) {
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();
        deferred.promise
            .done(function(){
                respUtil.redirect(req, res, "/viewProfileData")
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });

        var data = req.body;
        return new navExcelFileHandler().addPortFolio(req.user._id, data)
            .then((data) => {
                deferred.resolve(data);
            })
            .catch((error) => {
                deferred.reject(error);
            })

    }

    editTransaction(req, res) {
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();
        deferred.promise
            .done(function(){
                respUtil.redirect(req, res, "/viewProfileData")
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });

        var transactionId = req.body.id;
        if(transactionId == undefined || transactionId == ""){
            return deferred.reject(new navValidationException("Transaction id can't be empty"))
        }
        var data = req.body;
        return new navExcelFileHandler().editFromPortFolio(req.user._id, transactionId, data)
            .then((data) => {
                deferred.resolve(data);
            })
            .catch((error) => {
                deferred.reject(error);
            })

    }

    getBSEListing(req, res){
        var deferred = Q.defer();
        var respUtil = new navResponseUtil();
        deferred.promise
            .done(function(data){
                respUtil.sendAjaxResponse(res, {
                    status : 200,
                    body : JSON.stringify(data),
                    code :"OK"

                })
                // respUtil.redirect(req, res, "../views/auth/signup/registration-success-page");
            },function(error){
                var response = respUtil.generateErrorResponse(error);
                respUtil.renderErrorPage(req, res, {
                    errorResponse : response,
                    user : req.user,
                    isLoggedIn : false,
                    layout : 'modular-auth-layout',
                    title : 'Portfolio-Insights',
                    themeTitle : 'Portfolio-Insights'
                });
            });

        var query = req.query.query;

        req.assert("query", "Please provide query string").notEmpty();

        return new navStockList().getBSECompanyList(query, 50)
            .then((data) => {
                var finalData = [];
                for(var i =0; i < data.length; i++){
                    finalData.push(data[i].security_name);
                }
                deferred.resolve(finalData);
            })
            .catch((error) => {
                deferred.reject(error);
            })

    }
}


