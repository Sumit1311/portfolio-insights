//var Excel = require("exceljs");

var node_xj = require("xlsx-to-json-lc");
node_xj({
    input: "./data/test.xlsx",  // input xls
    output: "output.json", // output json
    //sheet: "Sheet1",  // specific sheetname
    lowerCaseHeaders:true
}, function(err, result) {
    if(err) {
        console.error(err);
    } else {
        console.log(result);
    }
});

/*var workbook = new Excel.Workbook();
workbook.xlsx.readFile("./data/test.xlsx")
    .then(function(data) {
        // use workbook
        console.log(data);
    });*/
