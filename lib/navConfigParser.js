var that, fs = require('fs');
var mustache = require("mustache");

module.exports = class navConfigParser {
    constructor(fileName) {
            if(fileName) {
                try {
                    this.config = JSON.parse(fs.readFileSync(process.cwd() + "/" + fileName));
                    //this.config = mustache.render(this.config, process.env);
                    setMandatoryConfig.call(this);
                } catch(e){
                    //throw e;
                    this.config = getDefaultConfig();
                }
            } else {
                try {
                    var configString = fs.readFileSync(process.cwd() + "/config/ajab-gajab.json");
                    configString = mustache.render(configString.toString(), process.env);
                    this.config = JSON.parse(configString);
                    setMandatoryConfig.call(this);
                } catch(e){
                    console.log(e);
                    this.config = getDefaultConfig();
                }
            }
    }
   
    getConfig(key, defaultValue) {
        if(this.config[key] === undefined || this.config[key] === '') {
            return defaultValue;
        }
        return this.config[key];
    }

    static instance() {
            if(that) {
                return that;
            }
            else{
                that= new navConfigParser();        
                return that;
            }
    }
};
function getDefaultConfig() {
    return {
        DatabaseHost: process.env.DB_HOST || "localhost",
        DatabaseUser: process.env.DB_USER || "admin",
        DatabasePassword: process.env.DB_PASS || "admin",
        DatabaseName: process.env.DB_NAME || "ajab_gajab",
        DatabasePort: process.env.DB_PORT || "5432",
        RedisServerURL: process.env.REDISCLOUD_URL,
        ListeningPort : process.env.PORT,
        HostName : process.env.HOST_NAME || "localhost",
        PaymentGateway : {
            Domain : "https://pguat.paytm.com",
            MerchantID : "Navnir15330216551133",
            MerchantKey : "arT6cMm%V#qgIy#X",
            Website : "WEB_STAGING",
            ChannelID : "WEB",
            IndustryType : "Retail",
            CallbackURLPath : "/callback", 
            TransactionURLPath : "/oltp-web/processTransaction",
            StatusAPIPath : "/oltp/HANDLER_INTERNAL/getTxnStatus",
            RetryInterval : 8, //hours
            ExpirationInterval : 72 //hours
        },
        BackgroundProcessing : {
            TransactionInterval : 60000, // ms,
            OrderInterval : 60000
        },
        LogLevel : {
            "web-server" : "DEBUG"
        }
    }
}

function setMandatoryConfig() {
    if(this.config.LogLevel === undefined) {
        this.config.LogLevel = {};
    }
    if(this.config.PaymentGateway === undefined) {
        this.config.PaymentGateway = {};
    }
}
