var navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    exphbs = require('express-handlebars');

var hbshelpers = require('handlebars-helpers');
var path = require('path');
var that;

module.exports = class navHandleBarInitializer {
    constructor() {
        this.hbs = exphbs.create({
                extname : '.hbs',
                //layout : 'app-layout',
            layoutsDir : process.cwd() + '/src',
                partialsDir : process.cwd() + '/src'
            });

    }
    static instance() {
        if(that) {
            return that;
        }
        else {
            that = new navHandleBarInitializer();
    
            return that;
        }
    }

    init(){
        var self = this;
         hbshelpers({
            handlebars: this.hbs.handlebars
         });
         navLogUtil.instance().log.call(self,self.init.name, 'Handlebars template engine initialization done', "debug");
    }
    
    register(app) {
            app.set('views', path.join(process.cwd() , 'src'));
            app.engine('hbs', this.hbs.engine);
            app.set('view engine', 'hbs');
    }

    
}
