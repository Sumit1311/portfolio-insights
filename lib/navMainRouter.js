var navBaseRouter = require(process.cwd() + "/lib/navBaseRouter.js"),
    navUserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js"),
    repeatHelper = require('handlebars-helper-repeat'),
    navResponseUtil = require(process.cwd() + "/lib/navResponseUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navAccount = require(process.cwd() + "/lib/navAccount.js"),
    navValidationException = require(process.cwd() + "/lib/exceptions/navValidationException.js"),
    helpers = require('handlebars-helpers')(),
    Q = require('q');

module.exports = class navMainRouter extends navBaseRouter {
    constructor(){
       super();
    }

    setup(){        
        this.router.get('/', this.ensureVerified.bind(this), this.ensureAuthenticated.bind(this), this.getHome.bind(this));
        this.router.get('/about', this.getAbout.bind(this));
        //this.router.get('/logout', this.doLogout.bind(this));
        return this;
    }

    getAbout(req,res) {
        res.render('about', {
            user : req.user,
            isLoggedIn : req.user ? true : false,
            layout : 'nav_bar_layout'
        });

    }

    getHome(req, res){
        res.render('index-page', {
            user : req.user,
            isLoggedIn : req.user ? true : false,
            layout : 'modular-main-layout',
            title : 'Portfolio-Insights',
            themeTitle : 'Portfolio-Insights',
            helpers : {
                repeat : repeatHelper
            }
        });
    }

}
