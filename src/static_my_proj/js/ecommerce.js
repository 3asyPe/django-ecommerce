$(document).ready(() => {
    // Contact form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Submitting...")
        }
        else{
            submitBtn.remove("disabled")
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        var thisForm =$(this)
        displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: (data) => {
                thisForm[0].reset()
                $.alert({
                    title: "Success!",
                    content: data.message,
                    theme: "modern",
                })
                setTimeout(() => {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 2000)
            },
            error: (error) => {
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""

                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "<br>"
                })
                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern",
                })
                setTimeout(() => {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 2000)
            }
        })
    })


    // Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer; 
    var typingInterval = 1000;

    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        clearInterval(typingTimer)
    })
    
    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(() => {
            window.location.href='/search/?q=' + query
        }, 500)
    }

    // Cart + Add Products
    var productForm = $(".form-product-ajax");

    console.log(productForm);

    productForm.submit(function(event) {
        event.preventDefault();
        console.log("Form is sending");
        var thisForm = $(this)
        console.log(thisForm);
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        console.log(actionEndpoint, httpMethod, formData);

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: (data) => {
                console.log("success");
                console.log(data);
                console.log("added:", data.added);
                console.log("removed:", data.removed);
                var submitSpan = thisForm.find(".submit-span");
                if (data.added){
                    submitSpan.html('In cart <button type="submit" class="btn btn-sm btn-danger">Remove?</button>');
                }
                else{
                    submitSpan.html('<button type="submit" class="btn btn-sm btn-success">Add to cart</button>');
                }
                var navbarCount = $(".navbar-cart-count");
                cartItemCount = data.cartItemCount
                text = cartItemCount !== 0 ? cartItemCount : ""; 
                navbarCount.text(text);

                if (window.location.href.indexOf("cart") != -1) {
                    refreshCart();
                }
            },
            error: (errorData) => {
                $.alert({
                    title: "Oops!",
                    content: "An error occured",
                    theme: "modern",
                })
                console.log("error");
                console.log(errorData);
            },
        })
    })

    function refreshCart(){
        console.log("in current cart");
        var cartTable = $(".cart-table");
        var cartBody = cartTable.find(".cart-body");
        
        var productRows = cartBody.find(".cart-product");
        var currentUrl = window.location.href;

        var refreshCartUrl = "/api/cart/";
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form");

                if (data.products.length > 0){
                    productRows.html(" ");
                    i = data.products.length;
                    $.each(data.products, function(index, value){
                        console.log(value);
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css('display', "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend(
                            "<tr>" +
                                "<th scope=\"row\">" + i + "</th>" +
                                "<td>" +
                                    "<a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() +
                                "</td>" + 
                                "<td>" + value.price + "</td>" +
                            "</tr>"
                        );
                        i--;
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal);
                    cartBody.find(".cart-total").text(data.total);
                }
                else{
                    window.location.href = ""
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oops!",
                    content: "An error occured",
                    theme: "modern",
                })
                console.log("error");
                console.log(errorData);
            }
        })
    }

})