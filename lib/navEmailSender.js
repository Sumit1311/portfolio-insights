var Q = require('q'),
    nodemailer = require('nodemailer'),
    navSendEmailException = require(process.cwd() + "/lib/exceptions/navSendEmailException.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    exphbs = require('express-handlebars'),
    navConfigParser = require(process.cwd() + "/lib/navConfigParser.js"),
    handleBars = require('nodemailer-express-handlebars');
const htmlToText = require('html-email-to-text');

module.exports = class navEmailSender {
    constructor(smtpServerURL) {
        if(!smtpServerURL) {
            smtpServerURL = navConfigParser.instance().getConfig("SmtpURL","localhost");
        }
        if(smtpServerURL === 'localhost') {
            this.transporter = nodemailer.createTransport({
                sendmail : true,
                newline:'unix',
                path:'/usr/sbin/sendmail',
                args :["-f", "sumittoshniwal92@gmail.com"],
                debug:true
            });
        } else {
            this.transporter = nodemailer.createTransport(smtpServerURL);
        }

        this.transporter.use('compile', handleBars({
            viewEngine: exphbs({
                layout:"nav_email_layout",
                extname : ".hbs"
            }),
            viewPath: process.cwd() + "/views",
            extName : ".hbs"
        }))
   }    

 

//use handlebars as a template handler

/**
 * Send email using the specified htmltemplate as body of the email
 *
 * @param to
 * @param subject
 * @param htmlTemplate
 * @returns {*}
 */
    sendMail(to, subject, htmlTemplate) {

        var self = this;
        if (!to || !subject || !htmlTemplate) {
            return Q.reject(new Error("Please provide subject, to and body of email"));
        }
        var def = Q.defer();
        var mailOptions = {
            to: to, // list of receivers
            subject: subject, // Subject line
            from : "Ajab Gajab <sales@ajab-gajab.com>",
            //text: htmlToText(htmlText), // plaintext body
            //html: htmlText// html body
            template: htmlTemplate.template,
            context: htmlTemplate.context
        };

        exphbs.create().render(process.cwd() + "/views/"+htmlTemplate.template+".hbs", htmlTemplate.context)
            .then((string) => {
                // send mail with defined transport object
                mailOptions.text = htmlToText(string);
                self.transporter.sendMail(mailOptions, function (error, info) {
                    if (error) {
                        navLogUtil.instance().log.call(self,self.sendMail.name,'Error sending mail ' + error, "error");
                        return def.reject(new navSendEmailException(error));
                    }
                    navLogUtil.instance().log.call(self,self.sendMail.name, 'Sent mail to '+ to + ' : ' + info.response, "debug");
                    def.resolve(info);
                });
            
            })

        return def.promise;
    }
}
