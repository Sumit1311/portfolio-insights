var navCommonUtil = require(process.cwd()+"/lib/navCommonUtil.js"),
    navLogUtil = require(process.cwd()+"/lib/navLogUtil.js"),
    navEmailSender = require(process.cwd() + "/lib/navEmailSender.js");

module.exports = class navEmailVerification extends navEmailSender {
    constructor() {
        super();
    }

    sendVerificationEmail(to, user, verificationLink) {
        var self = this;
        navLogUtil.instance().log.call(self,self.sendVerificationEmail.name, 'Sending verfication email to '+ to + 'with verification link '+verificationLink, "debug");

        return this.sendMail(to, "Action required: Please verify your email address",{

            template: "verificationEmail",
               context: {
                   userName: user ? user : "",
               verificationLink: verificationLink
               }
        });
    }
    sendResetPassword(to, user, resetPasswordLink) {
        var self = this;
        navLogUtil.instance().log.call(self,self.sendResetPassword.name, 'Sending reset password email to '+ to + 'with reset password link '+resetPasswordLink, "debug");

        return this.sendMail(to, "Reset Password",{
            template: "resetPasswordEmail",
               context: {
                   userName: user ? user : "",
                   resetPasswordLink : resetPasswordLink
               }
        });
    }

    generateCode() {
        return new navCommonUtil().generateUuid();
    }
}
