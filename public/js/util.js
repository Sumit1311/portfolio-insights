/**
 * This class is used to make an AJAX request to the server. Using given parameters
 *
 * @returns {{doRequest: Function}}
 * @constructor
 */
function navRequestHandler() {
    return {
        doRequest: function (url, method, body, responseType) {
            var deferred = Q.defer();
            var ajaxOptions = {
                url: url,
                method: method,
                processData: false,
                dataType: responseType,
                success: function (result, status, xhr) {
                    if (responseType) {
                        deferred.resolve(result);
                        return;
                    }
                    debugger;
                    if(result != "") {
                        try{
                            var response = JSON.parse(result);
                        } catch(exception) {
                            var response = {};
                        }
                    } else {
                        var response = {};
                    }
                    if(response.redirect && response.redirect.length != 0)
                    {
                       deferred.resolve(window.location.replace(response.redirect));
                       return;
                    }
                    deferred.resolve({
                        status : 200,
                        body : response,
                        code : response.code ? response.code : "UNKNOWN"
                    });
                    return;

                },
                error: function (xhr, status, error) {
                    if(xhr.status == 400 || xhr.status == 404 || xhr.status == 500 || xhr.status == 401) {
                        if(xhr.responseText != "" ){
                            try{
                            var response = JSON.parse(xhr.responseText);
                            } catch(e) {
                                response = "Server Error";
                            }
                            return deferred.reject(response);
                        }
                    }
 
                    debugger;
                    deferred.reject(error);
                }
            };

            if (method == "POST") {
                if (typeof body == "object") {
                    ajaxOptions['data'] = JSON.stringify(body);
                    ajaxOptions['contentType'] = "application/json";
                }
                else if (typeof body == "string") {
                    ajaxOptions['data'] = body;
                    ajaxOptions['contentType'] = "application/x-www-form-urlencoded";
                }
            }
            debugger;
            $.ajax(ajaxOptions);
            return deferred.promise;
        }
    }
}

/**
 * Escapes the characters from id of a particular html element.
 *
 * @param myid
 * @returns {*}
 */
function getEscapedId(myid) {
    return myid.replace(/(:|\.|\[|\]|,|@)/g, "\\$1");
}
