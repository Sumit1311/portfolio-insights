const NE = require('node-exceptions')
class navUserNotFoundException extends NE.LogicalException {
    constructor() {
        super("User not found",500,"INVALID_USER");
    }

}
 
module.exports = navUserNotFoundException; 
