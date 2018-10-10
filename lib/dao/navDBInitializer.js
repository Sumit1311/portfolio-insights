/**
 * This file will be used for Setting up and initializing db related stuff.
 * Like creating database tables, indices, any required views etc..
 *  Inherits the BaseDAO and uses it's API to query database.
 */

var BaseDAO = require(process.cwd() + "/lib/dao/base/baseDAO.js"),
    navLogUtil = require(process.cwd() + "/lib/navLogUtil.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    UserDAO = require("./user/userDAO"),
    Q = require("q"),
    navDatabaseException = require(process.cwd()+'/lib/dao/exceptions/navDatabaseException.js'),
    util = require("util");

function navDatabaseInitializer(persistence) {
    BaseDAO.call(this, persistence);
    return this;
}

util.inherits(navDatabaseInitializer, BaseDAO);

module.exports = navDatabaseInitializer;


/**
 * Sets up the schema for the app.
 *
 * @returns Q.Promise
 */
navDatabaseInitializer.prototype.init = function () {
    var self = this;
    return this.dbQuery('CREATE TABLE IF NOT EXISTS nav_user( ' +
        '_id varchar(36) NOT NULL, ' +
        'first_name text, ' +
        'last_name text, ' +
        'email_address varchar(100), ' +
        'mobile_no varchar(15), ' +
        'password text, ' +
        'email_verification VARCHAR(36), ' +
        'user_type smallint, ' +
        'reset_password VARCHAR(36), ' +
        'address VARCHAR(255), ' +
        'next_execution_time bigint,' +
        'time_taken bigint,' +
        'next_daily_update_time bigint,' +
        'need_full_refresh numeric(1,0), '+
        'CONSTRAINT nav_user_id_pk PRIMARY KEY (_id));')
        .then(function () {
            //create the root user who is super admin and have all the accesses by default
            var userDAO = new UserDAO();
            return userDAO.createRootUser();
        })
        .then(function(){
            var q = 'CREATE TABLE IF NOT EXISTS stock_list_bse ('
                + ' security_code integer NOT NULL, '
                + ' security_id text COLLATE pg_catalog."default" NOT NULL,'
                + ' security_name text COLLATE pg_catalog."default" NOT NULL,'
                + ' status text COLLATE pg_catalog."default" NOT NULL,'
                + ' security_group text COLLATE pg_catalog."default",'
                + ' face_value real,'
                + ' isin_no text COLLATE pg_catalog."default",'
                + ' industry text COLLATE pg_catalog."default",'
                + ' instrument text COLLATE pg_catalog."default" NOT NULL,'
                + ' CONSTRAINT stock_list_bse_pkey PRIMARY KEY ("security_code") ) '
                + 'WITH ( OIDS = FALSE )';
            return self.dbQuery(q);
        })
        .then(function(){
            return self.dbQuery('CREATE SEQUENCE IF NOT EXISTS  ' +
            ' user_stock_profile_daily_seq_id');
        })
        .then(function(){
            return self.dbQuery('CREATE TABLE IF NOT EXISTS user_stock_profile_daily (' +
                ' user_id varchar(36) NOT NULL,' +
                ' stock_date date NOT NULL,' +
                ' security_count numeric(100,0),' +
                ' profile_value double precision,' +
                ' units double precision,' +
                ' nav double precision,' +
                ' _id bigint PRIMARY KEY DEFAULT nextval(\'user_stock_profile_daily_seq_id\'::regclass),' +
                ' CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES nav_user(_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION ) WITH ( OIDS = FALSE )' )
        })
        .then(function(){
            return self.dbQuery('CREATE SEQUENCE IF NOT EXISTS  ' +
            ' user_stocks_trxn_seq_id');
        })
        .then(function(){
            return self.dbQuery('CREATE TABLE IF NOT EXISTS user_stocks_trxn( ' +
                '   _id varchar(36) PRIMARY KEY DEFAULT nextval(\'user_stocks_trxn_seq_id\'::regclass),' +
                '    user_id varchar(36) NOT NULL,' +
                '    security_code integer NOT NULL,' +
                '    security_count integer NOT NULL,' +
                '    trxn_date date,' +
                '    trxn_type character varying(10) COLLATE pg_catalog."default",' +
                '    trxn_flag numeric(1,0),' +
                '    is_active numeric(1,0) DEFAULT 1,' +
                '    deactivation_date bigint DEFAULT NULL,' +
                '    parent_id varchar(36),' +
                '    trxn_amount double precision,' +
                ' time_taken bigint,' +
                '    CONSTRAINT user_stocks_trxn_user_id_fk FOREIGN KEY (user_id)' +
                '        REFERENCES nav_user(_id) MATCH SIMPLE' +
                '        ON UPDATE NO ACTION' +
                '        ON DELETE NO ACTION,' +
                '    CONSTRAINT user_stocks_trxn_parent_id_fk FOREIGN KEY (parent_id)' +
                '        REFERENCES user_stocks_trxn(_id) MATCH SIMPLE' +
                '        ON UPDATE NO ACTION' +
                '        ON DELETE SET NULL,' +
                '   CONSTRAINT user_stocks_trxn_security_code_fk FOREIGN KEY (security_code)' +
                '        REFERENCES stock_list_bse(security_code) MATCH SIMPLE' +
                '        ON UPDATE NO ACTION' +
                '        ON DELETE NO ACTION' +
                ')');
        })
        .then(()=>{
            return self.dbQuery("CREATE SEQUENCE IF NOT EXISTS public.session_variables_var_se_id_seq;")
        })
        .then(()=>{
            return self.dbQuery(
                "CREATE TABLE IF NOT EXISTS session_variables ("+
                "var_seq_id bigint NOT NULL DEFAULT nextval('session_variables_var_se_id_seq'::regclass),"+
                "var_name text ,"+
                "var_value text ,"+
                "var_site text ,"+
                "var_type text ,"+
                "is_active char,"+
                "CONSTRAINT session_variables_pkey PRIMARY KEY (var_seq_id))");

        })
        .then(()=>{
            return self.dbQuery(
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTTARGET','ctl00$ContentPlaceHolder1$lnkDownload','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTARGUMENT',NULL,'https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__VIEWSTATE',NULL,'https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__VIEWSTATEGENERATOR','CF507786','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTVALIDATION',NULL,'https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('myDestination','#','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('WINDOW_NAMER','1','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hdnCode',NULL,'https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$ddSegment','Segment','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$ddlStatus','Select','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$getTExtData',NULL,'https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$ddlGroup','Select','https://www.bseindia.com/corporates/List_Scrips.aspx','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','https://www.bseindia.com/corporates/List_Scrips.aspx','HeaderFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('Content-Type','application/x-www-form-urlencoded','https://www.bseindia.com/corporates/List_Scrips.aspx','HeaderFields','Y');" +
            "" +
            "" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTTARGET','ctl00$ContentPlaceHolder1$lnkDownload','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTARGUMENT',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__VIEWSTATE',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__VIEWSTATEGENERATOR','EC4662D7','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('__EVENTVALIDATION',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('myDestination','#','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('WINDOW_NAMER','1','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hdnCode','532540','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$DDate',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidDMY','D','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hdflag','0','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidCurrentDate','5/14/2018 12:00:00 AM','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidYear',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidFromDate','05/17/2017','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidToDate','05/01/2018','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidOldDMY',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hiddenScripCode','532540','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$hidCompanyVal','TCS','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$btnDownload.x','4','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$btnDownload.y','3','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$search','rad_no1','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$Hidden1',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$GetQuote1_smartSearch','TATA CONSULTANCY SERVICES LTD','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$Hidden2',NULL,'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$GetQuote1_smartSearch2','Enter Security Name / Code / ID','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$DMY','rdbDaily','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$txtFromDate','17/05/2017','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('ctl00$ContentPlaceHolder1$txtToDate','01/05/2018','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','FormFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','HeaderFields','Y');" +
            "insert into public.session_variables(var_name,var_value,var_site,var_type,is_active) values('Content-Type', 'application/x-www-form-urlencoded','https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0','HeaderFields','Y');");
        })

    /*.then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS nav_child (_id varchar(36), age_group smallint, hobbies TEXT, user_id VARCHAR(36), gender smallint,  CONSTRAINT nav_child_id PRIMARY KEY (_id), CONSTRAINT nav_child_id_user_id_fk FOREIGN KEY (user_id) REFERENCES nav_user(_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE) ');
    })
    .then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS nav_toys (_id varchar(36), name varchar(50), stock integer, price integer, short_description VARCHAR(100), long_description TEXT, points integer, age_group smallint, parent_toys_id varchar(36), rent_duration integer, brand integer, category smallint, deposit integer, popular boolean DEFAULT false, CONSTRAINT nav_toys_id_pk PRIMARY KEY (_id), CONSTRAINT nav_toys_parent_toys_id_fk FOREIGN KEY (parent_toys_id) REFERENCES  nav_toys (_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE)');
    })
    .then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS nav_rentals( _id VARCHAR(36), user_id varchar(36), toys_id varchar(36), transaction_date bigint, lease_start_date bigint, lease_end_date bigint, shipping_address TEXT, status VARCHAR(30), delivery_date bigint, returned_date bigint, release_date bigint, CONSTRAINT nav_rental_id_pk PRIMARY KEY (_id),CONSTRAINT nav_rentals_toys_id_fk FOREIGN KEY (toys_id) REFERENCES  nav_toys (_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE,CONSTRAINT nav_rentals_user_id_fk FOREIGN KEY (user_id) REFERENCES  nav_user (_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE); ');
    })
    .then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS nav_toys_skills( _id varchar(36), toys_id varchar(36), skill integer, CONSTRAINT nav_toys_skills_id_pk PRIMARY KEY (_id), CONSTRAINT nav_toys_skills_id_fk FOREIGN KEY (toys_id) REFERENCES  nav_toys (_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE); ');
    })
    .then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS  nav_payments(_id varchar(36), user_id varchar(36), amount_payable integer, reason VARCHAR(30), credit_date bigint, paid_date bigint, status VARCHAR(30),transaction_id VARCHAR(36), transaction_summary TEXT, next_retry_date bigint, expiration_date bigint, transaction_type VARCHAR(20), is_order smallint, CONSTRAINT nav_payments_id PRIMARY KEY (_id),CONSTRAINT nav_payments_user_id FOREIGN KEY (user_id) REFERENCES  nav_user (_id) MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE NOT DEFERRABLE);');
    })
    .then(() => {
        return self.dbQuery('CREATE TABLE IF NOT EXISTS  nav_enquiry(_id varchar(36), name varchar(50), email varchar(50), contact_no VARCHAR(15), message varchar(500), submission_date bigint, CONSTRAINT nav_enquiry_id PRIMARY KEY (_id));');
    })*/
        .catch(function (error) {
            navLogUtil.instance().log.call(self, "setupSchema",  error.message, "error" );
            return Q.reject(new navCommonUtil().getErrorObject(error,500,"DBSETUP", navDatabaseException));
        });
};


/**
 * This function creates Indexes by calling executeIndex function and on its success it calls recursively until
 * the indices to be created.
 * @param dbClient - use same dbClient
 * @param keys
 * @param values
 */
/*function indicesList(dbClient, keys, values) {
    var dbClient;
    var self = this;
    if (keys.length === 0 || values.length === 0) {
        return Q.resolve();
    } else {
        var key = keys.shift();
        var value = values.shift();
        return executeIndex(dbClient, key, value)
         .then(function () {
                return indicesList.call(self, dbClient, keys, values);
            });
    }
}*/

/**
 * This function creates Indexes in Database after checking its existence.
 * @param dbClient
 * @param indexName
 * @param createSql
 * @returns {*}
 */
/*function executeIndex(dbClient, indexName, createSql) {
    return dbClient.query(
        "SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = $1 and n.nspname = 'public'", [indexName]
    ).then(function () {
            if (dbClient.results().rowCount > 0) {
                //jive.logger.debug("[DBUtils]:[executeIndex] : Index - ", indexName, " - already Exist!");
                return Q.resolve();
            } else {
                //jive.logger.debug("[DBUtils]:[executeIndex] : Index - ", indexName, " - Created Successfully");
                return dbClient.query(createSql);
            }
        });
}*/

