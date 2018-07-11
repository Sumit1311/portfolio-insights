var client, redisServerURL;
var redisStore;
var redis = require("redis");
var navConfigParser = require(process.cwd() + "/lib/navConfigParser.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    session = require('express-session');

module.exports = class navSessionStoreInitializer {
	constructor(url) {
        if(url) {
            redisServerURL = url;
        } else {
            redisServerURL = navConfigParser.instance().getConfig("RedisServerURL", "redis://127.0.0.1:6379");
        }   
        navLogUtil.instance().log.call(this, this.constructor.name, "Configured redis server url "+redisServerURL,"info")
    }

    init() {
        client = redis.createClient(redisServerURL);
    }

    getSessionStore(session) {
         redisStore = require('connect-redis')(session);
         return new redisStore({
                    client: client, ttl: 181440000
                });
    }

    register(app) {
            // Express Session
            app.use(session({
                secret: navConfigParser.instance().getConfig("SessionSecret", "session_secret"),
                // create new redis store.
                store: this.getSessionStore(session),
                saveUninitialized: false,
                resave: false
            }));
    }
}
