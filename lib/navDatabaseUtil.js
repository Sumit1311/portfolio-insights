module.exports = class navDatabaseUtils {
    refactorRows(tableName, rows) {
    var columns = {};
    var refactoredRows = [];
    switch (tableName) {
        case "nav_user":
            columns = {
                _id: "db_userId",
                first_name: "db_firstName",
                last_name: "db_lastName",
                email_address : "db_emailAddress",
                mobile_no: "db_mobileNo",
                password: "db_password",
                email_verification: "db_emailVerification",
                address: "db_shippingAddress",
                city: "db_city",
                state : "db_state",
                is_active : "db_isActive"
            };
            break;

        case "nav_toys":
            columns = {
                _id: "db_toyId",
                name: "db_toyName",
                "stock": "db_toyStock",
                "price": "db_toyPrice",
                "short_description": "db_shortDescription",
                "long_descritpion": "db_longDescription",
                "points": "db_points",
                "age_group" : "db_ageGroup",
                "category" : "db_category",
                "parent_toys_id" : "db_parentToyId"
            };
            break;
        case "nav_rentals":
            columns = {
                "_id": "db_rentalId",
                "user_id": "db_userId",
                "toys_id": "db_toyId",
                 "shipping_address" : "db_shippingAddress",
                 "lease_start_date" : "db_leaseStartDate",
                 "lease_end_date" : "db_leaseEndDate"
            };
            break;
        case "nav_payments":
            columns = {
                "_id": "db_paymentId",
                "last_payment_date": "db_lastPaymentDate",
                "user_id": "db_userId",
                "balance_points": "db_balancePoints",
                "balance_amount" : "sb_balanceAmount"
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

