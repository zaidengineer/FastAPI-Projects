// =====================================================
// API CONFIGURATION
// =====================================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =====================================================
// ELEMENTS
// =====================================================

const wrapper = document.getElementById("wraper");

const signUpBtn = document.getElementById("signUpBtn");
const signInBtn = document.getElementById("signInBtn");

const forgotPasswordBtn =
    document.getElementById("forgotPasswordBtn");

const backToLoginBtn =
    document.getElementById("backToLoginBtn");


const loginForm =
    document.getElementById("loginForm");

const registerForm =
    document.getElementById("registerForm");

const forgotForm =
    document.getElementById("forgotForm");


const loginMsg =
    document.getElementById("loginMsg");

const registerMsg =
    document.getElementById("registerMsg");

const forgotMsg =
    document.getElementById("forgotMsg");


// =====================================================
// SWITCH TO SIGN UP
// =====================================================

signUpBtn.addEventListener("click", function (e) {

    e.preventDefault();

    wrapper.classList.remove("forgot");

    wrapper.classList.add("active");

    loginMsg.textContent = "";
    registerMsg.textContent = "";
});


// =====================================================
// SWITCH TO LOGIN
// =====================================================

signInBtn.addEventListener("click", function (e) {

    e.preventDefault();

    wrapper.classList.remove(
        "active",
        "forgot"
    );

    loginMsg.textContent = "";
    registerMsg.textContent = "";
});


// =====================================================
// SWITCH TO FORGOT PASSWORD
// =====================================================

forgotPasswordBtn.addEventListener(
    "click",
    function (e) {

        e.preventDefault();

        wrapper.classList.remove("active");

        wrapper.classList.add("forgot");

        forgotMsg.textContent = "";
    }
);


// =====================================================
// BACK TO LOGIN
// =====================================================

backToLoginBtn.addEventListener(
    "click",
    function (e) {

        e.preventDefault();

        wrapper.classList.remove("forgot");

        forgotForm.reset();

        forgotMsg.textContent = "";
    }
);


// =====================================================
// LOGIN
// =====================================================

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const inputs = loginForm.querySelectorAll("input");

    const username = inputs[0].value.trim();
    const password = inputs[1].value;

    try {
        const formData = new URLSearchParams();

        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(
            `${API_BASE_URL}/auth/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Invalid username or password"
            );
        }

        // Save tokens
        localStorage.setItem(
            "access_token",
            data.access_token
        );

        localStorage.setItem(
            "refresh_token",
            data.refresh_token
        );

        // Success message
        alert("Login successful!");

    } catch (error) {
        alert(error.message || "Login failed");
        console.error(error);
    }
});

// =====================================================
// SIGN UP
// =====================================================

registerForm.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();


        registerMsg.style.color = "#0ef";

        registerMsg.textContent =
            "Creating account...";


        const username =
            document.getElementById(
                "registerUsername"
            ).value.trim();


        const email =
            document.getElementById(
                "registerEmail"
            ).value.trim();


        const password =
            document.getElementById(
                "registerPassword"
            ).value;


        const confirmPassword =
            document.getElementById(
                "registerConfirmPassword"
            ).value;


        // Password confirmation

        if (password !== confirmPassword) {

            registerMsg.style.color =
                "#ff6b6b";

            registerMsg.textContent =
                "Passwords do not match.";

            return;
        }


        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/auth/signup`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            username: username,

                            email: email,

                            password: password

                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Registration failed."
                );

            }


            registerMsg.style.color =
                "#0ef";

            registerMsg.textContent =
                "Account created successfully!";


            registerForm.reset();


            // After 1.5 seconds go to login

            setTimeout(function () {

                wrapper.classList.remove(
                    "active"
                );

                registerMsg.textContent = "";

            }, 1500);


        } catch (error) {

            registerMsg.style.color =
                "#ff6b6b";

            registerMsg.textContent =
                error.message ||
                "Registration failed.";

            console.error(
                "Signup error:",
                error
            );

        }

    }
);


// =====================================================
// FORGOT PASSWORD
// =====================================================

forgotForm.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();


        const email =
            document.getElementById(
                "forgotEmail"
            ).value.trim();


        const newPassword =
            document.getElementById(
                "forgotNewPassword"
            ).value;


        forgotMsg.style.color = "#0ef";

        forgotMsg.textContent =
            "Please wait...";


        try {

            // -----------------------------------------
            // STEP 1
            // Request reset token
            // -----------------------------------------

            const forgotResponse =
                await fetch(
                    `${API_BASE_URL}/auth/forgot-password`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email: email

                        })
                    }
                );


            const forgotData =
                await forgotResponse.json();


            if (!forgotResponse.ok) {

                throw new Error(
                    forgotData.detail ||
                    "Unable to process request."
                );

            }


            /*
             * Your current backend returns the
             * reset token directly for testing.
             */

            const resetToken =
                forgotData.reset_token;


            if (!resetToken) {

                forgotMsg.textContent =
                    forgotData.message ||
                    "If the email exists, a reset link has been sent.";

                return;
            }


            // -----------------------------------------
            // STEP 2
            // Reset password
            // -----------------------------------------

            const resetResponse =
                await fetch(
                    `${API_BASE_URL}/auth/reset-password`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            token: resetToken,

                            new_password:
                                newPassword

                        })
                    }
                );


            const resetData =
                await resetResponse.json();


            if (!resetResponse.ok) {

                throw new Error(
                    resetData.detail ||
                    "Password reset failed."
                );

            }


            forgotMsg.style.color =
                "#0ef";

            forgotMsg.textContent =
                "Password reset successfully!";


            forgotForm.reset();


            // Return to login

            setTimeout(function () {

                wrapper.classList.remove(
                    "forgot"
                );

                forgotMsg.textContent = "";

            }, 1500);


        } catch (error) {

            forgotMsg.style.color =
                "#ff6b6b";

            forgotMsg.textContent =
                error.message ||
                "Something went wrong.";

            console.error(
                "Reset password error:",
                error
            );

        }

    }
);