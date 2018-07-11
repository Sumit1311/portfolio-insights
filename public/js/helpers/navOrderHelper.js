registerOrderHandlers();

function registerOrderHandlers () {
    $("#_nav_order_div > form").submit(function(event){new navOrderHelper().orderHandler(event, this)});
    $(".btn-cancel-order").click(function(event){new navOrderHelper().cancelOrder(event, this);})
}

function navOrderHelper(){
}

navOrderHelper.prototype.orderHandler=function(event, that){
    var form = $(that);
    event.preventDefault();

    $("#_nav_order_button").prop('disabled', true);;
    var self = this;
    this.placeOrder(form)
        .then((result) => {
            $("#_nav_order_div").parent().parent().html(result);    
        })
        .catch(function(error){
            if(typeof error == "string") {
                self.showError(error);
            } else {
                self.showError(error.subMessage);
            }
            $("#_nav_order_button").prop('disabled', false);;
        });
}

navOrderHelper.prototype.placeOrder= function(form){
    var body = form.serialize();
    //console.log(body);
    return navRequestHandler().doRequest(form.attr('action'), 'POST', body, "html");
}

navOrderHelper.prototype.showError = function(message) {
    $("#_nav_order_error .alert").html(message);
    $("#_nav_order_error").removeClass("hidden");
}

navOrderHelper.prototype.cancelOrder =function(event, that) {
    event.preventDefault();
    if(window.confirm("Do you want cancel order ?")) {
        $(that).parent().siblings("form").submit();
    }
}
