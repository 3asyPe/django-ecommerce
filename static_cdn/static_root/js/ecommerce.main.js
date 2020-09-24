$(document).ready(() => {
    var stripeFormModule = $(".stripe-payment-form")
    var stripeModuleToken = stripeFormModule.attr("data-token")
    var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card"

    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publishKey: stripeModuleToken,
        nextUrl: stripeModuleNextUrl,
        btnTitle: stripeModuleBtnTitle,
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)
    
    var paymentForm = $(".payment-form")
    
    if (paymentForm.length > 1){
        alert("Only one payment form is allowed per page")
        paymentForm.css("display", "none")
    }
    else if (paymentForm.length == 1){
        
        var pubKey = paymentForm.attr("data-token")
        var nextUrl = paymentForm.attr("data-next-url")
        
        var stripe = Stripe(pubKey);
        var elements = stripe.elements();    
        
        // Custom styling can be passed to options when creating an Element.
        var style = {
            base: {
                // Add your base input styles here. For example:
                fontSize: '16px',
                color: '#32325d',
            },
        };
        
        // Create an instance of the card Element.
        var card = elements.create('card', {style: style});
        
        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');
        
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            stripe.createToken(card).then(function(result) {
                if (result.error) {
                    // Inform the customer that there was an error.
                    var errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Send the token to your server.
                    stripeTokenHandler(nextUrl, result.token);
                    card.clear()
                }
            });
        });
        
        function redirectToNext(nextPath, timeoffset){
            if (nextPath){
                setTimeout(() => {
                    window.location.href = nextUrl
                }, timeoffset)
            }
        }
        
        function stripeTokenHandler(nextUrl, token){
            console.log(token)
            
            var paymentMethodEndpoint = "/billing/payment-method/create"
            var data = {
                "token": token.id
            }
            
            $.ajax({
                data: data,
                url: paymentMethodEndpoint,
                method: "POST",
                success: (data) => {
                    var successMsg = data.message || "Success! Your card was added."
                    if (nextUrl){
                        successMsg += "<br/><br/><i class='fa fa-spin fa-spinner'></i>Redirecting..."
                    }
                    if ($.alert){
                        $.alert(successMsg)
                    }
                    else{
                        alert(successMsg)
                    }
                    redirectToNext(nextUrl, 1500)
                },
                error: (error) => {
                    console.log(error)
                }
            })
        }
    }
})