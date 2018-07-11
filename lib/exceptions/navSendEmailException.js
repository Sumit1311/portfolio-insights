const NE = require('node-exceptions')
class navSendEmailException extends NE.LogicalException {
    constructor(error) {
        if(error && error.name == "Error") {
            super(error.message, 500, error.code ? error.code : "SEND_MAIL");
            return;
        }
        super("Email not sent out properly", 500, "SEND_EMAIL");
    }
}
 
module.exports = navSendEmailException; 

