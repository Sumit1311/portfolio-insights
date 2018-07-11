function navAccountDetailsHelper() {
}

navAccountDetailsHelper.prototype.accountDetailsHandler = function(event, that) {
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
            submitHandler : self.logIn
           })*/
           $(form).children("button[type=\"submit\"]").prop('disabled', true);
           var self = this;
           this.submitForm(form)
            .then(function(){
                self.showSuccessMessage("Successfully Saved");
               $(form).children("button[type=\"submit\"]").prop('disabled', false);
            })
           .catch(function(error){
               if(typeof error == "string") {
                self.showErrorMessage(error);
               } else {
                self.showErrorMessage(error.subMessage);
               }
               $(form).children("button[type=\"submit\"]").prop('disabled', false);
           });
}

navAccountDetailsHelper.prototype.childDetailsHandler = function(event, that) {
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
            submitHandler : self.logIn
           })*/
                    debugger;
           var childrenDetails = $(".nav-child-detail");
           var body = [];
           for(var i = 0; i < childrenDetails.length; i++) {
               var child = $(childrenDetails[0])
               body.push(child.serialize());
           }
           $(form).children("button[type=\"submit\"]").prop('disabled', true);
           var self = this;
           this.submitForm(form, body)
            .then(function(){
                self.showSuccessMessage("Successfully Saved");
               $(form).children("button[type=\"submit\"]").prop('disabled', false);
            })
           .catch(function(error){
               if(typeof error == "string") {
                self.showErrorMessage(error);
               } else {
                self.showErrorMessage(error.subMessage);
               }
               $(form).children("button[type=\"submit\"]").prop('disabled', false);
           });
}
navAccountDetailsHelper.prototype.submitForm = function(form, body) {
    if(!body) {
        body = form.serialize();
    }
    //console.log(body);
    return navRequestHandler().doRequest(form.attr('action'), 'POST', body);
}

navAccountDetailsHelper.prototype.showSuccessMessage = function(message) {
    $('#_nav_account_details_alert').addClass('alert-success');
    $("#_nav_account_details_alert").text(message);
    $("#_nav_account_details_alert").removeClass("hidden");
    $("#_nav_account_details_alert").removeClass("alert-danger");
}

navAccountDetailsHelper.prototype.showErrorMessage = function(message) {
    $('#_nav_account_details_alert').addClass('alert-danger');
    $("#_nav_account_details_alert").text(message);
    $("#_nav_account_details_alert").removeClass("hidden");
    $("#_nav_account_details_alert").removeClass("alert-success");

}
registerAccountDetailsHandlers();

function registerAccountDetailsHandlers(){
    $("#_nav_change_password").click(showResetPassword);
    $("#_nav_change_pass_reset").click(showChangePassword);
	$("#_nav_account_details_form").submit(function(event) { new navAccountDetailsHelper().accountDetailsHandler(event, this)});
	$("#_nav_child_details_form").submit(function(event) { new navAccountDetailsHelper().childDetailsHandler(event, this)});
}

function showResetPassword() {
    $(this).parent().parent().addClass('hidden');
    $('#_nav_change_pass_reset').parent().parent().removeClass('hidden');
    var resetDiv = $('#_nav_change_pass_reset').parent().parent();
    $(resetDiv).find('input[type="password"]').prop("disabled", false);
}

function showChangePassword() {
    $('input[name="newPasword"]').val("");
    $('input[name="newPaswordConf"]').val("");
    $(this).parent().parent().addClass('hidden');
    $('#_nav_change_password').parent().parent().removeClass('hidden');
    var resetDiv = $('#_nav_change_pass_reset').parent().parent();
    $(resetDiv).find('input[type="password"]').prop("disabled", true);

} 
