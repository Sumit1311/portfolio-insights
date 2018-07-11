#!/usr/bin/env node

//if with background processing set spawn a seperate child for that
//by default launch the customer facing webserver
//with arguments launch the admin component

var argv = process.argv;
var LAUNCH_BACKGROUND = false, LAUNCH_ADMIN = false, LAUNCH_WEB = false; 

if(argv.length <= 1) {
   console.log("Usage ./laundher.js ....");
   process.exit(-1); 
}

readArguments();
launchApp();

function readArguments(){
    console.log(argv);
    
    for(var i = 2; i < argv.length; i++) { 
        if(argv[i] == "--with-background") {
            LAUNCH_BACKGROUND = true;
        }    
        else if(argv[i] == "--with-admin") {
            LAUNCH_ADMIN = true;
        }
        else if(argv[i] == "--with-web") {
            LAUNCH_WEB = true;
        }
        else if(argv[i] == "./launcher.js") {
            continue;
        }
        else {
            console.log("Invalid Arguments");
            process.exit(-1);
        }
    }
}

function launchApp() {
    if(LAUNCH_BACKGROUND) {
        
    }   
    if(LAUNCH_ADMIN) {
    
    } 
    if(LAUNCH_WEB) {
        var spawn = require('child_process').spawn;
        spawn("./app.js");
    }

}
