function navEnquiryHelper(){
}

navEnquiryHelper.prototype.submitEnquiry = function(event, that) {
    
           var form = $(that);
           event.preventDefault();
           $("#_nav_submit_enquiry").prop('disabled', true);
           var self = this;
           this.submit(form)
           .then(function(){
               $("#_nav_enquiry_form .panel-body").text("Query Successfully Submitted");
           })
           .catch(function(error){
               if(typeof error == "string") {
                self.showError(error);
               } else {
                self.showError(error.subMessage);
               }
               $("#_nav_submit_enquiry").prop('disabled', false);
           });
}

navEnquiryHelper.prototype.submit = function(form) {
    var body = form.serialize();
    return navRequestHandler().doRequest(form.attr('action'), 'POST', body);
}

navEnquiryHelper.prototype.showError = function(message) {
    $("#_nav_enquiry_error .alert").text(message);
    $("#_nav_enquiry_error").removeClass("hidden");
    $("#_nav_enquiry_error").focus();
}

registerEnquiryHandlers();

function registerEnquiryHandlers(){
	$("#_nav_enquiry_form").submit(function(event) { new navEnquiryHelper().submitEnquiry(event, this)});
}

