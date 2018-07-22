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





var path = require('path');

var config = require('./config');

var rootDir 	= config.rootDir;
var srcDir 		= config.srcDir;
var destDir 	= config.destDir;

/***********************************************
 *		Application script files
 ************************************************/

/*
    Specifiing the source this way means:

    "take all .js files except /_main/main.js file
    and then take /_main/main.js file"

    This ensures that main.js file is loaded in the end.
    Ignore context.js files.
*/

exports.scripts = [
    srcDir + "/config.js",
    srcDir + "/**/!(_context|config|main|*-helper)*.js",
    srcDir + "/main.js",
    "!" + srcDir + "/_vendor/**"
];

/***********************************************
 *		Application style files
 ************************************************/

exports.styles = [
    srcDir + "/_main.scss",
    srcDir + "/**/!(_main|_variables|*-theme)*.scss",
];

/***********************************************
 *		Application theme files
 ************************************************/

exports.themes = srcDir + "/**/*-theme.scss";

/***********************************************
 *		Application template files
 ************************************************/

/*
    All template files in application.
    Those should registered as handlebars partials
    in order to use feature like includes or layouts
*/

exports.templates = srcDir + "/**/*.hbs";

/***********************************************
 *		Application page files
 ************************************************/

/*
    Each page file represents a page which will be rendered into .html page.
    Pages can extend layouts.

*/

exports.pages = srcDir + "/**/*-page.hbs";

/***********************************************
 *		Application layout files
 ************************************************/

/*
    Layouts are used for "wrapping" the content of individual pages with common elements,
    such as the <head></head> and footer sections, which usually contain necessities
    such as <link> and <script> tags.
*/

exports.layouts = srcDir + "/**/*-layout.hbs";

/***********************************************
 *  	Application handlebars helpers files
 ************************************************/

/*
    Handlebars helpers files
    Read more: http://handlebarsjs.com/block_helpers.html
*/

exports.helpers = [
    srcDir + "/**/*-helper.js",
    rootDir + '/node_modules/handlebars-layouts/index.js',
];



/***********************************************
 *		Application asset files
 ************************************************/

exports.assets = srcDir + "/_assets/**/*";