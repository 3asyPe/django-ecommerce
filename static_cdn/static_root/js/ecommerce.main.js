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
        
        var form = $('#payment-form');
        var btnLoad = form.find(".btn-load");
        var btnLoadDefaultHtml = btnLoad.html();
        var btnLoadDefaultClasses = btnLoad.attr("class");

        form.on('submit', function(event) {
            event.preventDefault();
            // get the btn
            // display new btn ui

            var $this = $(this)
            btnLoad.blur()
            var loadTime = 1500
            var currentTimeout;
            var erorrHtml = "<i class='fa fa-warning'></i> An error occured"
            var errorClasses = "btn  btn-danger disabled btn-primary my-3"
            var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
            var loadingClasses = "btn  btn-success disabled btn-primary my-3"

            stripe.createToken(card).then(function(result) {
                if (result.error) {
                    // Inform the customer that there was an error.
                    var errorElement = $('#card-errors');
                    errorElement.textContent = result.error.message;
                    currentTimeout = displayBtnStatus(
                        btnLoad, 
                        errorHtml, 
                        errorClasses, 
                        1000, 
                        currentTimeout
                    )
                } else {
                    // Send the token to your server.
                    currentTimeout = displayBtnStatus(
                        btnLoad, 
                        loadingHtml, 
                        loadingClasses, 
                        5000, 
                        currentTimeout
                    )
                    stripeTokenHandler(nextUrl, result.token);
                    card.clear()
                }
            });
        });

        function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout){
            if (!loadTime){
                loadTime = 1500
            }
            element.html(newHtml)
            element.removeClass(btnLoadDefaultClasses)
            element.addClass(newClasses)
            return setTimeout(() => {
                element.html(btnLoadDefaultHtml)
                element.removeClass(newClasses)
                element.addClass(btnLoadDefaultClasses)
            }, loadTime)
        }

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
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr('class', btnLoadDefaultClasses)
                    redirectToNext(nextUrl, 1500)
                },
                error: (error) => {
                    // console.log(error)
                    $.alert({
                        title: 'An error occured',
                        content: "Please try adding your card again"
                    })
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr('class', btnLoadDefaultClasses)
                }
            })
        }
    }
})