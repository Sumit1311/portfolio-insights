var columnNames = ["securityCode", "transactionType", "transactionDate", "numberOfShares", "transactionAmount"],
    path = require('path'),
    Q = require('q'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    navUserProfileDAO = require(process.cwd() + "/lib/dao/stocks/navUserProfileDAO.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    moment = require('moment'),
    xlsxToJson = require("xlsx-to-json-lc");

module.exports = class navExcelFileHandler {
    constructor(options) {
        if(typeof(options) == "string"){
            this.fileName = options;
        } else {
            if(!options) {
                options = {};
            }
            if(!options.fileType) {
                options.fileType = "xlsx"
            }
            if(!options.filePath) {
                options.filePath = path.join(process.cwd() + "data");
            }
            if(!options.fileName) {
                options.fileName = "test.xlsx"
            }
            this.fileName = path.join(options.filePath, options.fileName);
        }
    }

    parseToJson(){
        var deferred = Q.defer();
        var self = this;
        xlsxToJson({
            input: this.fileName,  // input xls
            output: null, // output json
            //sheet: "Sheet1",  // specific sheetname
            lowerCaseHeaders:true
        },(err, result) => {
            if(err) {
                return deferred.reject(err);
            }
            self.parsedData = result;
            return deferred.resolve(result);
        });
        return deferred.promise;
    }

    getColumnNames() {
        return columnNames;
    }

    saveToDataBase(columnMapping, userId, shouldMerge){
    var excelData = this.parsedData;
    var userProfileDAO = new navUserProfileDAO();
    var self = this;
    return userProfileDAO.getClient()
        .then(function (_client) {
            userProfileDAO.providedClient = _client;
            return userProfileDAO.startTx();
        })
        .then(function(){
            var promises = [];
            var parsedExcel = [];
            if(excelData.length == 0){
                throw new navValidationException("Excel file empty");
            }
            for(var i = 0; i < excelData.length; i++){
                var excelRow ={};
                excelRow.userId = userId;
                //self.validateRow(columnMapping, excelData[i]);
                for(var j = 0; j < columnNames.length; j++){

                    if(columnMapping[columnNames[j]] == undefined){

                        throw new navValidationException("One of the required column does not exist in excel file");
                    }
                    var value = self.parseCellValue(columnNames[j], excelData[i][columnMapping[columnNames[j]].toLowerCase()], i);
                    excelRow[columnNames[j]] = value;
                }
                parsedExcel.push(excelRow);
                //promises.push(userProfileDAO.insertUserProfile(excelRow));
            }
            var p = Q.resolve();
            if(!shouldMerge){
                navCommonUtil.validatePortfolioData(parsedExcel);
                p = userProfileDAO.truncate(userId);
            }
            for(var i =0 ;i < parsedExcel.length;i ++){
                promises.push(userProfileDAO.insertUserProfile(parsedExcel[i]));
            }

            return Q.allSettled(promises);
        })
        .then(function(results){
            for(var i = 0; i < results.length; i++){
                if(results[i].state == 'rejected'){
                    return Q.reject(results[i].reason);
                }
            }
            if(shouldMerge) {
                return userProfileDAO.getProfileData(userId);
            } else {
                return Q.resolve();
            }


        })
        .then((portfolioData) => {
            var parsedExcel = [];
            if(shouldMerge){
                for(var i = 0; i < portfolioData.length; i++){
                    var excelRow ={};
                    excelRow.userId = portfolioData[i].user_id;
                    excelRow.transactionDate = portfolioData[i].trxn_date;
                    excelRow.transactionAmount = portfolioData[i].trxn_amount;
                    excelRow.transactionType = portfolioData[i].trxn_type;
                    excelRow.securityCode = portfolioData[i].security_code;
                    //self.validateRow(columnMapping, portfolioData[i]);
                    parsedExcel.push(excelRow);
                    //promises.push(userProfileDAO.insertUserProfile(excelRow));
                }
                navCommonUtil.validatePortfolioData(parsedExcel);
                return Q.resolve();
            } else {
                return Q.resolve();
            }

        })
        .then(function(){
            return userProfileDAO.commitTx();
        })
        .catch(function(error){
           return userProfileDAO.rollBackTx()
                .then(function(){
                    return Q.reject(error);
                })
                .catch(function(rollBackError){
                    return Q.reject(rollBackError);
                });
        })
        .finally(function(){
            if (userProfileDAO.providedClient) {
                userProfileDAO.providedClient.release();
                userProfileDAO.providedClient = undefined;
            }
        })

    }

    parseCellValue(columnName, columnData, rowNumber){
        switch (columnName) {
            case "securityCode" :
                var v = parseInt(columnData)
                if(!Number.isNaN(v)) {
                    return v;
                } else {
                    throw new navValidationException("Provide proper value for security code at row number : " + (rowNumber + 1));
                }
            case "transactionType":
                if (columnData != "Buy" && columnData != "Sell") {
                    throw new navValidationException("Provide proper value for transaction type at row number : " + (rowNumber + 1));
                }
                return columnData;
            case "transactionDate":
                if (columnData && columnData == "") {
                    throw new navValidationException("Provide proper value for transaction date at row number : " + (rowNumber + 1));
                }
                var val = moment(columnData, "DD/MM/YYYY");
                if (!val.isValid() || val.valueOf() > navCommonUtil.getCurrentTime_S()) {
                    throw new navValidationException("Provide proper value for transaction date at row number : " + (rowNumber + 1));
                }


                return val.format();
            case "numberOfShares":
                var value = parseInt(columnData);

                if (Number.isNaN(value) || value <= 0 || value > 10000) {
                    throw new navValidationException("Provide proper value for number of shares max is 10000 " +
                        "and min is greater than 0 at row number : " + (rowNumber + 1));
                }
                return value;

            
            case "transactionAmount":
                var value = parseInt(columnData);
                if (Number.isNaN(value) || value < 0) {
                    throw new navValidationException("Provide proper value for transaction amount " +
                        " at row number : " + (rowNumber + 1));
                }
                return value;
            }
            

        }
        checkIfPortfolioDataExist(userId){
            return new navUserProfileDAO().getProfileData(userId)
                .then((data) => {
                    if(data.length == 0) {
                        return false;
                    } else {
                        return true;
                    }
                })
                .catch(function(error){
                    return Q.reject(error);
                });
        }
        getViewProfileData(userId){
            return new navUserProfileDAO().getViewProfileData(userId)
                .then((data) => {
                    var filteredData = [];
                    var modifiedIds = {};
                    for(var i = 0; i < data.length; i++){
                        var o;
                        data[i].trxn_date = moment(data[i].trxn_date).format("DD/MM/YYYY");
                        data[i].parent_id != null ? modifiedIds[data[i].parent_id] = true : "" ;
                        if(data[i].is_active == 1 ){
                            o = Object.assign(data[i]);
                            filteredData.push(o);
                        }
                    }
                    return Q.resolve({
                        modified : modifiedIds,
                        filteredData : filteredData
                    });
                })
                .catch(function(error){
                    return Q.reject(error);
                });
        }

        deleteFromPortFolio(userId, transactionId){
            //Check if transaction exist with status as trxn_flag = 1 create a new entry with current transaction id as parent id
            //set is_active = 0 save deactivation date
            //if trxn_flag = 0 delete directly from database(No risk here just keep this in where)
            //do all this on only is_active = 1 transactions only
        }

}
