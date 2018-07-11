var     bcrypt = require('bcrypt-nodejs');

module.exports = class navPasswordUtil {

    constructor() {
    
    }
    encryptPassword(password) {
        return bcrypt.hashSync(password);
    }
    comparePassword(password, hash) {
        return bcrypt.compareSync(password, hash);
    }
}

