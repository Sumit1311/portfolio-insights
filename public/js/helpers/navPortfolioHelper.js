var g_rowContent;

function navPortfolioHelper(type) {
    this.type = type;
}

navPortfolioHelper.prototype.handler = function (event, that) {
    var form = $(that);
    event.preventDefault();
    /*form.validate({
     errorClass : "error help-block",
     rules : {
         email : {
             required : true,
             email : true
         }
     },
     messages : {
         email : {
             required : "Please specify an email address",
             email : "Invalid email address"
         }
     },
     errorElement: "em",
     highlight : function(element, errorClass, validClass) {
         $(element).parent().addClass('has-error');
     },
     submitHandler : self.registration
    })*/
    $("#_nav_" + this.type + "_button").prop('disabled', true);
    var self = this;
    this.takeAction(form)
        .catch(function (error) {

            if (typeof error == "string") {
                self.showError(error, self.type);
            } else {
                self.showError(error.subMessage, self.type);
            }
            $("#_nav_" + self.type + "_button").prop('disabled', false);
        });
}

navPortfolioHelper.prototype.takeAction = function (form) {
    var body = form.serialize();
    var url;
    var self = this;
    if (this.type == "add") {
        url = "/add"
    } else if (this.type == "edit") {
        url = "/edit"
        if(!verifyModified(body)){
            self.showError("Data not modified", self.type);
            return Q.resolve();
        }
    } else if (this.type == "delete") {
        url = "/delete"
    }
    return navRequestHandler().doRequest(form.attr("action"), form.attr("method"), body);
}

navPortfolioHelper.prototype.showError = function (message) {
    $("#_nav_" + this.type + "_error .alert").text(message);
    $("#_nav_" + this.type + "_error").removeClass("hidden");
}

var registerPortfolioHandlers = function () {
    $("#edit form").submit(function (event) {
        new navPortfolioHelper("edit").handler(event, this);
    });
    $("#delete form").submit(function (event) {
        new navPortfolioHelper("delete").handler(event, this);
    });
    $("#add form").submit(function (event) {
        new navPortfolioHelper("add").handler(event, this);
    });
}

registerPortfolioHandlers();

function verifyModified(data) {
    if(data.securityName == g_rowContent[1].textContent &&
        data.numberOfShares == g_rowContent[2].textContent &&
        data.transactionAmount == g_rowContent[3].textContent &&
        data.transactionDate == g_rowContent[4].textContent &&
        data.transactionType == g_rowContent[5].textContent){
        return false;
    }
}