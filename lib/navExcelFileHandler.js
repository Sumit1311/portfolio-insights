var columnNames = ["securityCode", "transactionType", "transactionDate", "numberOfShares", "transactionAmount"],
    path = require('path'),
    Q = require('q'),
    navValidationException = require(process.cwd() + '/lib/exceptions/navValidationException.js'),
    navUserProfileDAO = require(process.cwd() + "/lib/dao/stocks/navUserProfileDAO.js"),
    navDailyProfileDAO = require(process.cwd() + "/lib/dao/stocks/navDailyProfileDAO.js"),
    navUserDAO = require(process.cwd() + "/lib/dao/user/userDAO.js"),
    navCommonUtil = require(process.cwd() + "/lib/navCommonUtil.js"),
    moment = require('moment'),
    xlsxToJson = require("xlsx-to-json-lc");

module.exports = class navExcelFileHandler {
    constructor(options) {
        if (typeof(options) == "string") {
            this.fileName = options;
        } else {
            if (!options) {
                options = {};
            }
            if (!options.fileType) {
                options.fileType = "xlsx"
            }
            if (!options.filePath) {
                options.filePath = path.join(process.cwd() + "data");
            }
            if (!options.fileName) {
                options.fileName = "test.xlsx"
            }
            this.fileName = path.join(options.filePath, options.fileName);
        }
    }

    parseToJson() {
        var deferred = Q.defer();
        var self = this;
        xlsxToJson({
            input: this.fileName,  // input xls
            output: null, // output json
            //sheet: "Sheet1",  // specific sheetname
            lowerCaseHeaders: true
        }, (err, result) => {
            if (err) {
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

    saveToDataBase(columnMapping, userId, shouldMerge) {
        var excelData = this.parsedData;
        var userProfileDAO = new navUserProfileDAO();
        var self = this;
        return userProfileDAO.getClient()
            .then(function (_client) {
                userProfileDAO.providedClient = _client;
                return userProfileDAO.startTx();
            })
            .then(function () {
                var promises = [];
                var parsedExcel = [];
                if (excelData.length == 0) {
                    throw new navValidationException("Excel file empty");
                }
                for (var i = 0; i < excelData.length; i++) {
                    var excelRow = {};
                    excelRow.userId = userId;
                    //self.validateRow(columnMapping, excelData[i]);
                    for (var j = 0; j < columnNames.length; j++) {

                        if (columnMapping[columnNames[j]] == undefined) {

                            throw new navValidationException("One of the required column does not exist in excel file");
                        }
                        var value = self.parseCellValue(columnNames[j], excelData[i][columnMapping[columnNames[j]].toLowerCase()], i);
                        excelRow[columnNames[j]] = value;
                    }
                    parsedExcel.push(excelRow);
                    //promises.push(userProfileDAO.insertUserProfile(excelRow));
                }
                var p = Q.resolve();
                if (!shouldMerge) {
                    navCommonUtil.validatePortfolioData(parsedExcel);
                    p = userProfileDAO.truncate(userId);
                }
                for (var i = 0; i < parsedExcel.length; i++) {
                    promises.push(userProfileDAO.insertUserProfile(parsedExcel[i]));
                }

                return Q.allSettled(promises);
            })
            .then(function (results) {
                for (var i = 0; i < results.length; i++) {
                    if (results[i].state == 'rejected') {
                        return Q.reject(results[i].reason);
                    }
                }
                if (shouldMerge) {
                    return self.validateDatabasePortfolio(userId, userProfileDAO);
                } else {
                    return Q.resolve();
                }


            })
            .then(function () {
                return userProfileDAO.commitTx();
            })
            .catch(function (error) {
                return userProfileDAO.rollBackTx()
                    .then(function () {
                        return Q.reject(error);
                    })
                    .catch(function (rollBackError) {
                        return Q.reject(rollBackError);
                    });
            })
            .finally(function () {
                if (userProfileDAO.providedClient) {
                    userProfileDAO.providedClient.release();
                    userProfileDAO.providedClient = undefined;
                }
            })

    }

    validateDatabasePortfolio(userId, accessObject) {
        (accessObject == undefined ? accessObject = new navUserProfileDAO() : "")
        return accessObject.getProfileData(userId)
            .then((portfolioData) => {
                var parsedExcel = [];
                for (var i = 0; i < portfolioData.length; i++) {
                    var excelRow = {};
                    excelRow.userId = portfolioData[i].user_id;
                    excelRow.transactionDate = portfolioData[i].trxn_date;
                    excelRow.transactionAmount = portfolioData[i].trxn_amount;
                    excelRow.transactionType = portfolioData[i].trxn_type;
                    excelRow.securityCode = portfolioData[i].security_code;
                    excelRow.numberOfShares = portfolioData[i].security_count;
                    //self.validateRow(columnMapping, portfolioData[i]);
                    parsedExcel.push(excelRow);
                    //promises.push(userProfileDAO.insertUserProfile(excelRow));
                }
                navCommonUtil.validatePortfolioData(parsedExcel);
                return Q.resolve();
            })
    }

    parseCellValue(columnName, columnData, rowNumber) {
        switch (columnName) {
            case "securityCode" :
                if (columnData == undefined || columnData == "") {
                    throw new navValidationException("The security code  can't be empty" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                var v = parseInt(columnData)
                if (!Number.isNaN(v)) {
                    return v;
                } else {
                    throw new navValidationException("Provide proper value for security code  " + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
            case "transactionType":
                if (columnData == undefined || columnData == "") {
                    throw new navValidationException("The transaction type can't be empty" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                if (columnData != "Buy" && columnData != "Sell") {
                    throw new navValidationException("Provide proper value for transaction type" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                return columnData;
            case "transactionDate":
                if (columnData == undefined || columnData == "") {
                    throw new navValidationException("The transaction date can't be empty" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                if (columnData && columnData == "") {
                    throw new navValidationException("Provide proper value for transaction date" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                var val = moment(columnData, "DD/MM/YYYY");
                if (!val.isValid() || val.valueOf() > navCommonUtil.getCurrentTime_S()) {
                    throw new navValidationException("Provide proper value for transaction date " + rowNumber == undefined ? "" : "at row number : " + (rowNumber + 1));
                }


                return val.format();
            case "numberOfShares":
                if (columnData == undefined || columnData == "") {
                    throw new navValidationException("The number of shares can't be empty" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                var value = parseInt(columnData);

                if (Number.isNaN(value) || value <= 0 || value > 10000) {
                    throw new navValidationException("Provide proper value for number of shares max is 10000 " +
                    "and min is greater than 0 " + rowNumber == undefined ? "" : "at row number : " + (rowNumber + 1));
                }
                return value;


            case "transactionAmount":
                if (columnData == undefined || columnData == "") {
                    throw new navValidationException("The transaction amount can't be empty" + rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                var value = parseFloat(columnData);
                if (Number.isNaN(value) || value < 0) {
                    throw new navValidationException("Provide proper value for transaction amount " +
                    rowNumber == undefined ? "" : " at row number : " + (rowNumber + 1));
                }
                return value;
        }


    }

    checkIfPortfolioDataExist(userId) {
        return new navUserProfileDAO().getProfileData(userId)
            .then((data) => {
                if (data.length == 0) {
                    return false;
                } else {
                    return true;
                }
            })
            .catch(function (error) {
                return Q.reject(error);
            });
    }

    getViewProfileData(userId) {
        return new navUserProfileDAO().getViewProfileData(userId)
            .then((data) => {
                var filteredData = [];
                var modifiedIds = {};
                for (var i = 0; i < data.length; i++) {
                    var o;
                    data[i].trxn_date = moment(data[i].trxn_date).format("DD/MM/YYYY");
                    data[i].parent_id != null ? modifiedIds[data[i].parent_id] = true : "";
                    data[i].is_active = parseInt(data[i].is_active);
                    data[i].trxn_flag = parseInt(data[i].trxn_flag);
                    if (data[i].is_active == 1) {
                        o = Object.assign(data[i]);
                        filteredData.push(o);
                    }
                }
                return Q.resolve({
                    modified: modifiedIds,
                    filteredData: filteredData
                });
            })
            .catch(function (error) {
                return Q.reject(error);
            });
    }

    deleteFromPortFolio(userId, transactionId) {
        //Check if transaction exist with status as trxn_flag = 1 create a new entry with current transaction id as parent id
        //set is_active = 0 save deactivation date
        //if trxn_flag = 0 delete directly from database(No risk here just keep this in where)
        //do all this on only is_active = 1 transactions only
        var transaction, da = new navUserProfileDAO(), updateCount, isLocked = false, isTransActive = false;
        var self = this;
        return da.lockRow(transactionId, true)
            .then((count) => {
                if (count == 1) {
                    isLocked = true;
                    return da.getTransaction(transactionId);
                } else {
                    throw new Error("The row is under processing please try again later.");
                }

            })
            .then((data) => {
                if (data.length == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                transaction = data[0];
                return da.getClient();
            })
            .then(function (_client) {
                da.providedClient = _client;
                return da.startTx();
            })
            //})
            .then(() => {
                isTransActive = true;
                if (transaction.is_active == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                if (transaction.trxn_flag == 0) {
                    return da.deleteTransaction(transactionId);
                } else if (transaction.trxn_flag == 1) {
                    return da.markTransactionInactive(transactionId);
                } else {
                    throw new Error("Something went wrong");
                }
            })
            .then((count) => {
                if (count == 0) {
                    throw new Error("");
                }
                return self.validateDatabasePortfolio(userId, da);
            })
            .then(() => {
                return da.commitTx();
            })
            .then((count) => {
                isTransActive = false;
                return da.unlockRow(transactionId);
            })
            .then(() => {
                isLocked = false;
                return Q.resolve();
            })
            .catch((error) => {
                var promise = Q.resolve();
                if (isLocked) {
                    promise = da.unlockRow(transactionId);
                }
                if (isTransActive) {
                    promise = promise
                        .then(() => {
                            return da.rollBackTx();
                        })
                        .catch((rollbackError) => {
                            return Q.reject(rollbackError)
                        })
                    //promise = da.unlockRow(transactionId);
                }
                return promise
                    .then(() => {
                        return Q.reject(error);
                    })
                    .catch((otherError) => {
                        return Q.reject(otherError);
                    })
            })
            .finally(function () {
                if (da.providedClient) {
                    da.providedClient.release();
                    da.providedClient = undefined;
                }
            })
    }

    editFromPortFolio(userId, transactionId, data) {
        var transaction, da = new navUserProfileDAO(), updateCount, isLocked = false, isTransActive = false;
        var self = this;
        return da.lockRow(transactionId, true)
            .then((count) => {
                if (count == 1) {
                    isLocked = true;
                    return da.getTransaction(transactionId);
                } else {
                    throw new Error("The row is under processing please try again later.");
                }

            })
            .then((data) => {
                if (data.length == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                transaction = data[0];
                return da.getClient();
            })
            .then(function (_client) {
                da.providedClient = _client;
                return da.startTx();
            })
            //})
            .then(() => {
                isTransActive = true;
                if (transaction.is_active == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                if (transaction.trxn_flag == 0) {
                    var updateData = {
                        securityCode: self.parseCellValue("securityCode", data.securityCode, undefined),
                        numberOfShares: self.parseCellValue("numberOfShares", data.numberOfShares, undefined),
                        transactionDate: self.parseCellValue("transactionDate", data.transactionDate, undefined),
                        transactionType: self.parseCellValue("transactionType", data.transactionType, undefined),
                        transactionAmount: self.parseCellValue("transactionAmount", data.transactionAmount, undefined)
                    };
                    return da.editTransaction(transactionId, updateData);
                } else if (transaction.trxn_flag == 1) {
                    var newTransactionId = navCommonUtil.generateUuid_S();
                    var insertData = {
                        userId: userId,
                        securityCode: self.parseCellValue("securityCode", data.securityCode, undefined),
                        numberOfShares: self.parseCellValue("numberOfShares", data.numberOfShares, undefined),
                        transactionDate: self.parseCellValue("transactionDate", data.transactionDate, undefined),
                        transactionType: self.parseCellValue("transactionType", data.transactionType, undefined),
                        transactionAmount: self.parseCellValue("transactionAmount", data.transactionAmount, undefined)
                    };
                    return da.insertUserProfile(insertData, newTransactionId)
                        .then(() => {
                            //Insert new row with edited data
                            return da.markTransactionInactive(transactionId, newTransactionId);
                        })
                } else {
                    throw new Error("Something went wrong");
                }
            })
            .then(() => {
                return self.validateDatabasePortfolio(userId, da);
            })
            .then(() => {
                return da.commitTx();
            })
            .then(() => {
                isTransActive = false;
                return da.unlockRow(transactionId);
            })
            .then(() => {
                isLocked = false;
                return Q.resolve();
            })
            .catch((error) => {
                var promise = Q.resolve();
                if (isLocked) {
                    promise = da.unlockRow(transactionId);
                }
                if (isTransActive) {
                    promise = promise
                        .then(() => {
                            return da.rollBackTx();
                        })
                }
                return promise
                    .then(() => {
                        return Q.reject(error);
                    })
                    .catch((otherError) => {
                        return Q.reject(otherError);
                    })
            })
            .finally(function () {
                if (da.providedClient) {
                    da.providedClient.release();
                    da.providedClient = undefined;
                }
            })
    }

    addPortFolio(userId, data) {
        var self = this;
        var da = new navUserProfileDAO()
        var insertData = {
            userId: userId,
            securityCode: self.parseCellValue("securityCode", data.securityCode, undefined),
            numberOfShares: self.parseCellValue("numberOfShares", data.numberOfShares, undefined),
            transactionDate: self.parseCellValue("transactionDate", data.transactionDate, undefined),
            transactionType: self.parseCellValue("transactionType", data.transactionType, undefined),
            transactionAmount: self.parseCellValue("transactionAmount", data.transactionAmount, undefined)
        };
        return da.getClient()
            .then(function (_client) {
            da.providedClient = _client;
            return da.startTx();
        })
        //})
            .then(() => {
                return da.insertUserProfile(insertData, navCommonUtil.generateUuid_S())
            })
            .then(() => {
                return self.validateDatabasePortfolio(userId, da);
            })

            .then(() => {
                return da.commitTx();
            })
            .catch((error) => {
                return da.rollBackTx()
                    .then(() => {
                        return Q.reject(error);
                    })
                    .catch((otherError) => {
                        return Q.reject(otherError);
                    })
            })
            .finally(function () {
                if (da.providedClient) {
                    da.providedClient.release();
                    da.providedClient = undefined;
                }
            })
    }

    deleteFromPortFolioFullRefresh(userId, transactionId) {
        var transaction, da = new navUserProfileDAO();
        var self = this;
        return da.getTransaction(transactionId)
            .then((data) => {
                if (data.length == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                transaction = data[0];
                return da.getClient();
            })
            .then(function (_client) {
                da.providedClient = _client;
                return da.startTx();
            })
            //})
            .then(() => {
                if (transaction.trxn_flag == 0) {
                    return da.deleteTransaction(transactionId, false);
                } else if (transaction.trxn_flag == 1) {
                    return da.deleteTransaction(transactionId, true);
                } else {
                    throw new Error("Something went wrong");
                }
            })
            .then((count) => {
                if (count == 0) {
                    throw new Error("");
                }
                return self.validateDatabasePortfolio(userId, da);
            })
            .then(() => {
                if (transaction.trxn_flag == 1) {
                    return self.markForFullRefresh(userId, da.providedClient);
                } else {
                    return Q.resolve();
                }
            })
            .then(() => {
                return da.commitTx();
            })
            .catch((error) => {
                return da.rollBackTx()
                    .catch((rollbackError) => {
                        return Q.reject(rollbackError)
                    })
                //promise = da.unlockRow(transactionId);
            })
            .finally(function () {
                if (da.providedClient) {
                    da.providedClient.release();
                    da.providedClient = undefined;
                }
            })
    }

    editFromPortFolioFullRefresh(userId, transactionId, data) {
        var transaction, da = new navUserProfileDAO(), updateCount, isLocked = false, isTransActive = false;
        var self = this;
        return da.getTransaction(transactionId)
            .then((data) => {
                if (data.length == 0) {
                    throw new navValidationException("Transaction Id not valid");
                }
                transaction = data[0];
                return da.getClient();
            })
            .then(function (_client) {
                da.providedClient = _client;
                return da.startTx();
            })
            //})
            .then(() => {
                var updateData = {
                    securityCode: self.parseCellValue("securityCode", data.securityCode, undefined),
                    numberOfShares: self.parseCellValue("numberOfShares", data.numberOfShares, undefined),
                    transactionDate: self.parseCellValue("transactionDate", data.transactionDate, undefined),
                    transactionType: self.parseCellValue("transactionType", data.transactionType, undefined),
                    transactionAmount: self.parseCellValue("transactionAmount", data.transactionAmount, undefined)
                };
                if (transaction.trxn_flag == 0) {
                    return da.editTransaction(transactionId, updateData, false);
                } else if (transaction.trxn_flag == 1) {
                    return da.editTransaction(transactionId, updateData, true);
                } else {
                    throw new Error("Something went wrong");
                }
            })
            .then(() => {
                return self.validateDatabasePortfolio(userId, da);
            })
            .then(() => {
                if (transaction.trxn_flag == 1) {
                    return self.markForFullRefresh(userId, da.providedClient);
                } else {
                    return Q.resolve();
                }
            })
            .then(() => {
                return da.commitTx();
            })
            .catch((error) => {
                return da.rollBackTx()
                    .then(() => {
                        return Q.reject(error);
                    })
                    .catch((otherError) => {
                        return Q.reject(otherError);
                    })
            })
            .finally(function () {
                if (da.providedClient) {
                    da.providedClient.release();
                    da.providedClient = undefined;
                }
            })
    }

    markForFullRefresh(userId, client) {
	var userAccess = new navUserDAO(client), profileAccess = new navUserProfileDAO(client),
	dailyProfileAccess = new navDailyProfileDAO(client);
	return userAccess.markForFullRefresh(userId)
	.then(() => {
		return profileAccess.resetTransactionFlag(userId);
	}) 
	.then(() => {
		return dailyProfileAccess.clearUserProfile(userId);
	}) 
    }
}
