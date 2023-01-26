// Get Stripe publishable key
fetch("/billing/config")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);
        // Event handler
        let submitBtn = document.querySelector("#subscribeButton");
        if (submitBtn !== null) {
            submitBtn.addEventListener("click", () => {
                // Get Checkout Session ID
                fetch("/billing/create-checkout-session")
                    .then((result) => {
                        return result.json();
                    })
                    .then((data) => {
                        console.log(data);
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({sessionId: data.sessionId})
                    })
                    .then((res) => {
                        console.log(res);
                    });
            });
        }
    });