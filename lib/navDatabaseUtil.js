module.exports = class navDatabaseUtils {
    refactorRows(tableName, rows) {
    var columns = {};
    var refactoredRows = [];
    switch (tableName) {
        case "ps_user":
            columns = {
                _id: "db_userId",
                first_name: "db_firstName",
                last_name: "db_lastName",
                email_address : "db_emailAddress",
                mobile_no: "db_mobileNo",
                password: "db_password",
                email_verification: "db_emailVerification",
                is_active : "db_isActive"
            };
            break;
        }

        for (var r =0; r < rows.length; r++) {
            refactoredRows[r] = {};
            for (var key in rows[r]) {
                if (rows[r].hasOwnProperty(key)) {
                    if (columns[key]) {
                        refactoredRows[r][columns[key]] = rows[r][key];
                    } else {
                        refactoredRows[r][key] = rows[r][key];
                    }
                }
            }
        }
        return refactoredRows;
    }
}

