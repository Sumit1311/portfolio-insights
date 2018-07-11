var navMainRouter = require(process.cwd() + "/lib/navMainRouter.js"),
    navSignInRouter = require(process.cwd() + "/lib/navSignInRouter.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navRegistrationRouter = require(process.cwd() + "/lib/navRegistrationRouter.js"),
    navUserAccountRouter = require(process.cwd() + "/lib/navUserAccountRouter.js"),
    navAdminRouter = require(process.cwd() + "/lib/navAdminRouter.js"),
    navPGRouter = require(process.cwd() + "/lib/navPGRouter.js"),
    navToysRouter = require(process.cwd() + "/lib/navToysRouter.js");


module.exports = class navRoutesInitializer {
    init(app) {
            // Global Vars
            app.use(function (req, res, next) {
                res.locals.success_msg = req.flash('success_msg');
                res.locals.error_msg = req.flash('error_msg');
                res.locals.error = req.flash('error');
                res.locals.user = req.user || null;
                next();
            });
            app.use('/ping',function(req,res){
                res.status(200).send('pong');
            });
            navLogUtil.instance().log.call(this, this.init.name, "Setting up routes for /", "debug");
            app.use('/', new navMainRouter().setup().getRouter());
            app.use('/', new navSignInRouter().setup().getRouter());
            app.use('/', new navRegistrationRouter().setup().getRouter());
            app.use('/', require(process.cwd() + '/lib/temp.js'));	
            //app.use('/registration', require('./routes/regAndAuth/registration.js'));
            navLogUtil.instance().log.call(this, this.init.name, "Setting up routes for /toys", "debug");
            app.use('/toys',new navToysRouter().setup().getRouter());
            navLogUtil.instance().log.call(this, this.init.name, "Setting up routes for /user", "debug");
            app.use('/user',new navUserAccountRouter().setup().getRouter());
            navLogUtil.instance().log.call(this, this.init.name, "Setting up routes for /pg", "debug");
            app.use('/pg',new navPGRouter().setup().getRouter());
            navLogUtil.instance().log.call(this, this.init.name, "Setting up routes for /admin", "debug");
            app.use('/admin',new navAdminRouter().setup().getRouter());
        
    }
}
