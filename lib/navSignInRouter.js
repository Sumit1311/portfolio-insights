var navBaseRouter = require(process.cwd() + '/lib/navBaseRouter.js'),
    navResponseUtil = require(process.cwd() + "/lib/navResponseUtil.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navAuthenticateUser = require(process.cwd() + "/lib/navAuthenticateUser.js"),
    Q = require('q');
    

module.exports = class navSignInRouter extends navBaseRouter {
    constructor(){
        super();
    }

    setup(){
        this.router.post('/', this.authentication.bind(this));
        this.router.get('/logout', this.ensureAuthenticated.bind(this), this.isSessionAvailable.bind(this), this.logOut.bind(this));        
        //the path which will be used to login this is the route for displaying sign in page to user
        this.router.get('/login', this.ensureAuthenticated.bind(this),this.ensureVerified.bind(this) , this.isSessionAvailable.bind(this), this.logIn.bind(this));
        return this;
    }

    authentication(req, res) {    
        var self = this;
        var deferred = Q.defer();
        deferred.promise
            .done(function(){
                navLogUtil.instance().log.call(self, self.authentication.name, "Authenticating user : " + req.user.email_address, "info");
                //console.log("Re : ", req.query.redirect);
                if(req.query.redirect) {
                    return new navResponseUtil().redirect(req, res, req.query.redirect);
                }
                new navResponseUtil().redirect(req, res, '/');
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
        new navAuthenticateUser().authenticate(req, res, deferred);
    }
    logOut(req, res) {
        var self = this;
        navLogUtil.instance().log.call(self, self.logOut.name, "Logging out user : " + req.user.email_address, "info");
        req.session.destroy();
        new navResponseUtil().redirect(req, res, '/');
    }
    logIn (req, res) {
        var self = this;
        navLogUtil.instance().log.call(self, self.logIn.name, "Logging In user : " + req.user.email_address, "info");
        //if the user is already authenticated i.e. exist in the session then continue to the home page
        new navResponseUtil().redirect(req, res, '/');
    }
}
