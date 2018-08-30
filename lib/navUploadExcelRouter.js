var navBaseRouter = require(process.cwd() + '/lib/navBaseRouter.js'),
    Q = require('q'),
    navResponseUtil = require(process.cwd() + '/lib/navResponseUtil.js'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    navLogicalException = require("node-exceptions").LogicalException,
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navAccount = require(process.cwd() + "/lib/navAccount.js");

module.exports = class navUploadExcel extends navBaseRouter {
    constructor() {
        super();
    }
    setup(){
        var self = this;
        //this.router.get('/signup', function(req,res, next) {self.doSignup(req,res,next)});
        this.router.get('/uploadExcelPage', this.getUploadExcelPage.bind(this));
        this.router.get('/doExcelColumnMapping', function(req,res, next) {self.doExcelColumnMapping(req,res,next)});
        return this;
    }

    getUploadExcelPage(req, res){
        res.render('upload-excel/upload-excel-page', {
            user : req.user,
            isLoggedIn : req.user ? true : false,
            layout : 'modular-main-layout'
            /*title : 'Portfolio-Insights',
            themeTitle : 'Portfolio-Insights'*/
        });
    }

    doExcelColumnMapping(req, res){
        /*res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader("Content-Disposition", "attachment; filename=" + process.cwd() + "/config/sample-file.xlsx");
        return res;*/
        var deferred = Q.defer(), self = this;
        var respUtil =  new navResponseUtil();
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
            })
        return deferred.resolve();

    }
}


