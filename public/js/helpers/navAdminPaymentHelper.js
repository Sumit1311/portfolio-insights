function AdminPaymentHelper() {

}

AdminPaymentHelper.prototype.savePayments = function() {
    var editedForms = $(".row-edited > form");
    var edited = [];
    for(var i = 0;i < editedForms.length; i++) {
        var sArray = $(editedForms[i]).serializeArray();
        sArray.push({name:"paymentId",value: $(editedForms[i]).attr("id")})
            edited.push(sArray);
    }
    return navRequestHandler().doRequest("/admin/payments/save", 'POST', edited)
        .catch(function(error){
            $("#_nav_error_div").text(error.message);
            $("#_nav_error_div").removeClass("hidden");
        })
}

AdminPaymentHelper.prototype.monitorChange =function(event) {
    var closestTr = $(event.currentTarget).closest("tr");
    $(closestTr).addClass("row-edited");
}

registerHandler();

function registerHandler() {
    $(function(){
        $("table input").change(function(event) { new AdminPaymentHelper().monitorChange(event, this)});
        $("table select").change(function(event) { new AdminPaymentHelper().monitorChange(event, this)});
        $("table textarea").change(function(event) { new AdminPaymentHelper().monitorChange(event, this)});
        $("table .datetimepicker").on("dp.change",function(event) { new AdminPaymentHelper().monitorChange(event, this)});
        $("#_nav_btn_save").click(function(event){ new AdminPaymentHelper().savePayments();
        });
    });
}

