/*var constants = {
    "QUARTER" : 3,
    "HALF_YEAR" : 6,
    "MONTH" : 1,
    "YEAR" : 12
}*/

module.exports = class navConstants {
    constructor(){
    }
    getValue(key){
        if(this[key] != undefined) {
            return this[key];
        }
    }
}
