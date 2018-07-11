const NE = require('node-exceptions')
class navEmailVerificationException extends NE.LogicalException {
    constructor() {
        super("Please verify email id...",400,"VERIFY_EMAIL");
    }

}
 
module.exports = navEmailVerificationException; 
