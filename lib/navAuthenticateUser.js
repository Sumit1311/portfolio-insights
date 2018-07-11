var navPassportInitializer = require(process.cwd() + '/lib/navPassportInitializer.js'),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navValidationException = require(process.cwd() + "/lib/exceptions/navValidationException.js");

module.exports = class navAuthenticateUser {
    authenticate(req, res, deferred) {
        const self = this;
        req.assert("email","Email is Required").notEmpty();
        req.assert("email","Valid Email Required").isEmail();
        req.assert("password","Password is Required").notEmpty();
        req.assert("password","Valid Password Required").isValidPassword();
        var validationErrors = req.validationErrors();
        if(validationErrors)
        {
            return deferred.reject(new navValidationException(validationErrors));
        }
        navLogUtil.instance().log.call(self, self.authenticate.name, `Authenticating using passport`, "debug");
        navPassportInitializer.authenticate(req, res, null, deferred);        
    }
}
