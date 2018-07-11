const NE = require('node-exceptions')
class navValidationException extends NE.LogicalException {
    constructor(errorList) {
        super("Field Validation Failed", 400, "INVALID_FIELDS");
        this.errorList = errorList;
    }
}
 
module.exports = navValidationException; 
