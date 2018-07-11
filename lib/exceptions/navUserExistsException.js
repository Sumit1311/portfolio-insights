const NE = require('node-exceptions')
class navUserExistsException extends NE.LogicalException {
    constructor() {
        super("User Exists",400,"DUPL_USER");
    }

}
 
module.exports = navUserExistsException; 
