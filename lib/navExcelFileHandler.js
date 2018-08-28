let columnNames = ["company name", "transaction type", "date", "number of shares", "amount"],
    path = require('path'),
    Q = require('q'),
    xlsxToJson = require("xlsx-to-json-lc");

module.exports = class navExcelFileHandler {
    constructor(options) {
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

    parseToJson(){
        var deferred = Q.defer();
        var self = this;
        xlsxToJson({
            input: this.fileName,  // input xls
            //output: "output.json", // output json
            //sheet: "Sheet1",  // specific sheetname
            lowerCaseHeaders:true
        },(err, result) => {
            if(err) {
                return deferred.reject(err);
            }
            self.parsedData = result;
            return deferred.resolve(result);
        })
    }

    readAndVerifyColumnNames() {
        if (!this.parsedData || this.parsedData.length == 0) {
            throw new Error("Can't be called without parsing data or empty file");
        }
        var row = this.parsedData[0];
        var self = this;
        self.columns = [];
        for (var key in row) {
            if (row.hasOwnProperty(key)) {
                self.columns.push(key);
                if (columnNames.find(key.toLowerCase()) == -1) {
                    return false;
                }
            }
        }
        return true;
    }

    getColumnNames() {
        return columnNames;
    }
};