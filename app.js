#!/usr/bin/env node
var navPassportHandler = require(process.cwd() + "/lib/navPassportInitializer.js"),
    navSessionStoreInitializer = require(process.cwd() + "/lib/navSessionStoreInitializer.js"),
    navDatabaseInitializer = require(process.cwd() + "/lib/dao/navDBInitializer.js"),
    navAppInitializer = require(process.cwd() + "/lib/navAppInitializer.js"),
    navRoutesInitializer = require(process.cwd() + "/lib/navRoutesInitializer.js"),
    navHandleBarInitializer = require(process.cwd() + "/lib/navHandleBarInitializer.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js");


//create schema for app
navLogUtil.instance("web-server");
new navDatabaseInitializer()
    .init()
    .then(function () {
        //Express App Initialization
        var app = new navAppInitializer().init()
        // Handle Bars Init
        navHandleBarInitializer.instance().init();
        navHandleBarInitializer.instance().register(app);
        //Redis and Session Init
        var sessionInit = new navSessionStoreInitializer()
            sessionInit.init();
        sessionInit.register(app);
        // Passport init
        (new navPassportHandler()).register(app);
        //Routes Initializer
        new navRoutesInitializer().init(app);
        // Start App
        new navAppInitializer().start(app);
    }, function (error) {
        navLogUtil.instance().log.call(this,"app.js","Error setting up database"+ error,"fatal");
        process.exit(-1);
    })
    .done(() => {
        navLogUtil.instance().log.call(this, "app.js", "App Successfully Started", "info");
    },(error) => {
        navLogUtil.instance().log.call(this, "app.js", "Fatal Error Occured : " + error.stack, "fatal");
        navLogUtil.instance().log.call(this, "app.js", "Exiting Now", "fatal");
        process.exit(-1);
    });

process.on('uncaughtException', function (err) {
    console.error(new Date().toUTCString() + ' uncaughtException:', err.message)
    console.error(err.stack)
    process.exit(-1)
})
