var navResponseUtil = require(process.cwd() + '/lib/navResponseUtil.js'),
    navLogUtil = require(process.cwd() + '/lib/navLogUtil.js'),
    express = require('express'); 

module.exports = class navBaseRouter {
    constructor() {
        this.router = express.Router();
    }

    getRouter() {
        return this.router;
    }

    ensureSuperAdmin(req, res, next) {
        var self = this;
        if(req.user && req.user.user_type === 0) {
            return next();
        }
        navLogUtil.instance().log.call(self, self.ensureSuperAdmin.name, "User is not super admin", "debug");

        return res.render('login',{
            layout: 'nav_bar_layout',
            hideNavBar : true,
            redirection : req.query.redirect ? req.query.redirect : req.originalUrl
        });
    }

    ensureAuthenticated(req, res, next) {
        var self = this;
        if (req.isAuthenticated()) {
            next();
            return;
        }
        navLogUtil.instance().log.call(self, self.ensureAuthenticated.name, "User is not authenticated , redirecting", "debug");
        // Redirect if not authenticated
        if(req.xhr) {
            new navResponseUtil.redirect(req, res, "/login"); 
        }else {
            //:w
            //console.log(req.originalUrl);
            return res.render('login',{
                layout: 'nav_bar_layout',
                hideNavBar : true,
                redirection : req.query.redirect ? req.query.redirect : encodeURIComponent(req.originalUrl)
            });
        }
    }
    ensureVerified(req, res, next) {
        var self = this;
        if (req.user === undefined || (req.user && req.user.email_verification === null)  ) {
            return next();
        }
        navLogUtil.instance().log.call(self, self.ensureVerified.name, "User has not verified email", "debug");

        // Redirect if not authenticated
        if(req.xhr) {
            new navResponseUtil.redirect(req, res, "/"); 
        } else {
            res.render('completeRegistration',{
                isLoggedIn : true,
                layout : 'nav_bar_layout'
            });
        }
    }
    ensurePassword(req, res, next) {
        var self = this;
        if (req.user === undefined || (req.user && req.user.reset_password === null)  ) {
            return next();
        }
        navLogUtil.instance().log.call(self, self.ensurePassword.name, "User has not reset password", "debug");

        // Redirect if not authenticated
        if(req.xhr) {
            new navResponseUtil.redirect(req, res, "/"); 
        } else {
            res.render('completeResetPassword',{
                isLoggedIn : true,
                layout : 'nav_bar_layout'
            });
        }
    }
    isSessionAvailable(req, res, next) {
        var userDetails = req.user, self = this;
        if (userDetails && userDetails._id) {
            next();
        } else {
        navLogUtil.instance().log.call(self, self.isSessionAvailable.name, "Session not available", "warn");
            new navResponseUtil().redirect(req,res,"/login");
        }
    }
}
