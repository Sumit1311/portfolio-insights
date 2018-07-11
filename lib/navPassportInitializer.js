var LocalStrategy = require('passport-local').Strategy,
    passport = require('passport'),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navUserNotFoundException = require(process.cwd() + "/lib/exceptions/navUserNotFoundException.js"),
    navPasswordUtil = require(process.cwd() + "/lib/navPasswordUtil.js"),
    UserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js");

var that = {
    name : "navPassportInitializer"
};

module.exports = class navPassportHandler {
    constructor(p) {
        var self = this;
        if(!p) {
            p = passport;
        }
        p.serializeUser(this.serializeUser);
        // used to deserialize the user
        p.deserializeUser(this.deserializeUser);
        navLogUtil.instance().log.call(self, "constructor", `Configuring the email and password as default key name on UI for passport` , "info");
        p.use(new LocalStrategy({
            usernameField: 'email',
            passwordField: 'password'
        }, this.authenticateHandler));
        this.passport = p;
    }

    register(app) {
        app.use(this.passport.initialize());
        app.use(this.passport.session());    
    }

    serializeUser (user, done) {
        //console.log("User Details while serialize : ", user);
        done(null, {userId: user.email_address});
    }
    deserializeUser(user, done) {
        var self = this;
        return (new UserDAO()).getLoginDetails(user.userId)
            .then(function (userData) {
                if (userData.length !== 0) {
                    if (userData[0].email_address == user.userId) {
                        return done(null, userData[0]);
                    } else {
                        navLogUtil.instance().log.call(self, self.deserializeUser.name, `User does not exist ${userData[0].email_address}`, "debug");
                        return done(null, false);
                    }
                } else {
                    return done(null, false);
                }
            })
            .catch(function (error) {
                return done(error);
            });
    }

    authenticateHandler(email, password, done) {
        var self = this;
        return (new UserDAO()).getLoginDetails(email)
            .then(function (user) {
                if (user.length !== 0) {
                    if (password && new navPasswordUtil().comparePassword(password, user[0].password)) {
                        return done(null, user[0]);
                    } else {
                        navLogUtil.instance().log.call(self, self.authenticateHandler.name, `Password mismatch for user ${email}`, "debug");
                        return done(new navUserNotFoundException());
                    }
                } else {
                    return done(new navUserNotFoundException());
                }
            })
        .catch(function (error) {
            navLogUtil.instance().log.call(self, self.authenticateHandler.name, `Error occured while authenticating user ${error}`, "error");
            return done(error);
        });
    }

    static authenticate(req, res, next, deferred){
        passport.authenticate('local',function(err, user){
            if(err) {
                navLogUtil.instance().log.call(that ,"authenticate", `Error occured while authenticating ${err}`, "error");
                return deferred.reject(err);
            }
            if(!user) {
                navLogUtil.instance().log.call(that ,"authenticate", `No user exist`, "error");
                return deferred.reject();
            }
            req.logIn(user, err => {
                if (err) {
                    navLogUtil.instance().log.call(that ,"authenticate", `Error occured ${err}`, "error");
                    return deferred.reject(err);
                }
                // Redirect to homepage
                return deferred.resolve();
            }) 
        })(req,res);
    }
}

