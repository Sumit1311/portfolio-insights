function navRegistrationHelper() {
}

navRegistrationHelper.prototype.registrationHandler = function(event, that) {
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
           $("#_nav_register_button").prop('disabled', true);
           var self = this;
           this.registration(form)
           .catch(function(error){
                   debugger;
               if(typeof error == "string") {
                self.showError(error);
               } else {
                self.showError(error.subMessage);
               }
               $("#_nav_register_button").prop('disabled', false);
           });
}

navRegistrationHelper.prototype.registration = function(form) {
    var body = form.serialize();
    return navRequestHandler().doRequest('/register', 'POST', body);
}

navRegistrationHelper.prototype.showError = function(message) {
    $("#_nav_register_error .alert").text(message);
    $("#_nav_register_error").removeClass("hidden");
}

