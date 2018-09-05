var columnNames = ["securityCode", "transactionType", "transactionDate", "numberOfShares"],
    path = require('path'),
    Q = require('q'),
    navUserProfileDAO = require(process.cwd() + "/lib/dao/stocks/navUserProfileDAO.js"),
    moment = require('moment'),
    xlsxToJson = require("xlsx-to-json-lc");

module.exports = class navExcelFileHandler {
    constructor(options) {
        if(typeof(options) == "string"){
            this.fileName = options;
        } else {
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

    saveToDataBase(columnMapping, userId){
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
            for(var i = 0; i < excelData.length; i++){
                var excelRow ={};
                excelRow.userId = userId;
                //self.validateRow(columnMapping, excelData[i]);
                for(var j = 0; j < columnNames.length; j++){
                    var value = self.parseCellValue(columnNames[j], excelData[i][columnMapping[columnNames[j]]], i);
                    excelRow[columnNames[j]] = value;
                }
                promises.push(userProfileDAO.insertUserProfile(excelRow));
            }
            return Q.allSettled(promises);
        })
        .then(function(results){
            for(var i = 0; i < results.length; i++){
                if(results[i].state == 'rejected'){
                    return Q.reject(results[i].value);
                }
            }
            return Q.resolve();
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
        switch (columnName){
            case "securityCode" :
                return columnData;
            case "transactionType":
                if(columnData != "Buy" && columnData != "Sell"){
                    throw new navValidationException("Provide proper value for transaction type at row number : " + (rowNumber + 1);
                }
                return columnData;
            case "transactionDate":
                if(columnData && columnData == ""){
                    throw new navValidationException("Provide proper value for transaction date at row number : " + (rowNumber + 1);
                }
                var val = moment(columnData);
                if(!val.isValid()){
                    throw new navValidationException("Provide proper value for transaction date at row number : " + (rowNumber + 1);
                }

                return columnData;
            case "numberOfShares":
                var value = parseInt(columnData);

                if(value < 0 && value >  0){


                }
    }
};