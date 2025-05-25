document.addEventListener("DOMContentLoaded", () => {
    // Form elements
    const shopRegistrationForm = document.getElementById("shopRegistrationForm")
    const verifyPhoneBtn = document.getElementById("verifyPhoneBtn")
    const hiddenInput = document.getElementById('status-value');
    const sendEmailOtpBtn = document.getElementById("sendEmailOtpBtn")
    const phoneOtpContainer = document.getElementById("phoneOtpContainer")
    const emailOtpContainer = document.getElementById("emailOtpContainer")
    const verifyPhoneOtpBtn = document.getElementById("verifyPhoneOtpBtn")
    const verifyEmailOtpBtn = document.getElementById("verifyEmailOtpBtn")
    const resendPhoneOtpBtn = document.getElementById("resendPhoneOtpBtn")
    const resendEmailOtpBtn = document.getElementById("resendEmailOtpBtn")
    const phoneOtpTimer = document.getElementById("phoneOtpTimer")
    const emailOtpTimer = document.getElementById("emailOtpTimer")
    const phoneOtp = document.getElementById("phoneOtp")
    const emailOtp = document.getElementById("emailOtp")
    const resendCountdown = document.getElementById("resendCountdown")
    const resendEmailCountdown = document.getElementById("resendEmailCountdown")
  
    // Password elements
    const passwordInput = document.getElementById("password")
    const confirmPasswordInput = document.getElementById("confirmPassword")
    const reqAlphanumeric = document.getElementById("user-req-alphanumeric")
    const reqLength = document.getElementById("user-req-length")
    const reqMatch = document.getElementById("user-req-match")
  
    // Timer variables
    let phoneTimerInterval
    let emailTimerInterval
    let resendPhoneTimerInterval
    let resendEmailTimerInterval
  
    // Password toggle
    const togglePasswordBtns = document.querySelectorAll(".toggle-password")
    togglePasswordBtns.forEach((btn) => {
      btn.addEventListener("click", function () {
        const input = this.previousElementSibling
        const type = input.getAttribute("type") === "password" ? "text" : "password"
        input.setAttribute("type", type)
        this.innerHTML = type === "password" ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>'
      })
    })
  
    // Password validation
    if (passwordInput) {
      passwordInput.addEventListener("input", validatePassword)
      confirmPasswordInput.addEventListener("input", validatePassword)
    }
  
    function validatePassword() {
      const password = passwordInput.value
      const confirmPassword = confirmPasswordInput.value
  
      // Check if password contains at least one letter, one number, and allows special characters
      const hasValidChars = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d\W_]+$/.test(password)
      updateRequirement(reqAlphanumeric, hasValidChars)
  
      // Check if password length is between 10 and 20
      const hasValidLength = password.length >= 10 && password.length <= 20
      updateRequirement(reqLength, hasValidLength)
  
      // Check if passwords match
      const passwordsMatch = password === confirmPassword && password !== ""
      updateRequirement(reqMatch, passwordsMatch)
  
      return hasValidChars && hasValidLength && passwordsMatch
    }
  
    function updateRequirement(element, isMet) {
      if (isMet) {
        element.querySelector("i").className = "fas fa-check-circle"
        element.querySelector("i").style.color = "var(--success-color)"
        element.querySelector("span").style.color = "var(--success-color)"
      } else {
        element.querySelector("i").className = "fas fa-times-circle"
        element.querySelector("i").style.color = "var(--danger-color)"
        element.querySelector("span").style.color = "var(--danger-color)"
      }
    }
  
    // Phone verification
    if (verifyPhoneBtn) {
      verifyPhoneBtn.addEventListener("click", () => {
        const phoneNumber = document.getElementById("phoneNumber").value
        if (!phoneNumber) {
          alert("Please enter a phone number")
          return
        }
  
        // Mock API call to send OTP
        mockSendOTP(phoneNumber, "phone")
          .then(() => {
            phoneOtpContainer.classList.remove("hidden")
            startOtpTimer(phoneOtpTimer, phoneTimerInterval)
            startResendCountdown(resendPhoneOtpBtn, resendCountdown, resendPhoneTimerInterval)
            verifyPhoneBtn.textContent = "Sent"
            verifyPhoneBtn.disabled = true
          })
          .catch((error) => {
            alert("Error sending OTP: " + error.message)
          })
      })
    }
  
    // Email verification
    if (sendEmailOtpBtn) {
      sendEmailOtpBtn.addEventListener("click", () => {
        const email = document.getElementById("email").value
        if (!email) {
          alert("Please enter an email address")
          return
        }
  
        // Mock API call to send OTP
        mockSendOTP(email, "email")
          .then(() => {
            emailOtpContainer.classList.remove("hidden")
            startOtpTimer(emailOtpTimer, emailTimerInterval)
            startResendCountdown(resendEmailOtpBtn, resendEmailCountdown, resendEmailTimerInterval)
            sendEmailOtpBtn.textContent = "Sent"
            sendEmailOtpBtn.disabled = true
          })
          .catch((error) => {
            alert("Error sending OTP: " + error.message)
          })
      })
    }
  
    // Verify phone OTP
    if (verifyPhoneOtpBtn) {
      verifyPhoneOtpBtn.addEventListener("click", () => {
        const otp = phoneOtp.value
        if (!otp) {
          alert("Please enter the OTP")
          return
        }
  
        // Mock API call to verify OTP
        mockVerifyOTP(otp, "phone")
          .then(() => {
            verifyPhoneBtn.textContent = "Verified"
            hiddenInput.value = "Verified";
            verifyPhoneBtn.classList.add("verified")
            verifyPhoneBtn.style.backgroundColor = "var(--success-color)"
            phoneOtpContainer.classList.add("hidden")
  
            // Clear the timers when verified
            if (phoneTimerInterval) {
              clearInterval(phoneTimerInterval)
            }
            if (resendPhoneTimerInterval) {
              clearInterval(resendPhoneTimerInterval)
            }
          })
          .catch((error) => {
            alert("Error verifying OTP: " + error.message)
          })
      })
    }
  
    // Verify email OTP
    if (verifyEmailOtpBtn) {
      verifyEmailOtpBtn.addEventListener("click", () => {
        const otp = emailOtp.value
        if (!otp) {
          alert("Please enter the OTP")
          return
        }
  
        // Mock API call to verify OTP
        mockVerifyOTP(otp, "email")
          .then(() => {
            sendEmailOtpBtn.textContent = "Verified"
            sendEmailOtpBtn.classList.add("verified")
            sendEmailOtpBtn.style.backgroundColor = "var(--success-color)"
            emailOtpContainer.classList.add("hidden")
  
            // Clear the timers when verified
            if (emailTimerInterval) {
              clearInterval(emailTimerInterval)
            }
            if (resendEmailTimerInterval) {
              clearInterval(resendEmailTimerInterval)
            }
          })
          .catch((error) => {
            alert("Error verifying OTP: " + error.message)
          })
      })
    }
  
    // Resend phone OTP
    if (resendPhoneOtpBtn) {
      resendPhoneOtpBtn.addEventListener("click", () => {
        const phoneNumber = document.getElementById("phoneNumber").value
  
        // Disable the resend button immediately
        resendPhoneOtpBtn.disabled = true
  
        // Mock API call to resend OTP
        mockSendOTP(phoneNumber, "phone")
          .then(() => {
            // Reset and restart the timers
            startOtpTimer(phoneOtpTimer, phoneTimerInterval)
            startResendCountdown(resendPhoneOtpBtn, resendCountdown, resendPhoneTimerInterval)
            alert("OTP resent successfully")
          })
          .catch((error) => {
            alert("Error resending OTP: " + error.message)
            // Re-enable the resend button if there's an error
            resendPhoneOtpBtn.disabled = false
          })
      })
    }
  
    // Resend email OTP
    if (resendEmailOtpBtn) {
      resendEmailOtpBtn.addEventListener("click", () => {
        const email = document.getElementById("email").value
  
        // Disable the resend button immediately
        resendEmailOtpBtn.disabled = true
  
        // Mock API call to resend OTP
        mockSendOTP(email, "email")
          .then(() => {
            // Reset and restart the timers
            startOtpTimer(emailOtpTimer, emailTimerInterval)
            startResendCountdown(resendEmailOtpBtn, resendEmailCountdown, resendEmailTimerInterval)
            alert("OTP resent successfully")
          })
          .catch((error) => {
            alert("Error resending OTP: " + error.message)
            // Re-enable the resend button if there's an error
            resendEmailOtpBtn.disabled = false
          })
      })
    }
  
    // Form submission
    if (shopRegistrationForm) {
      shopRegistrationForm.addEventListener("submit", (e) => {
        e.preventDefault()
  
        // Check if both phone and email are verified
        const isPhoneVerified = verifyPhoneBtn.textContent === "Verified"
        const isEmailVerified = sendEmailOtpBtn.textContent === "Verified"
  
        if (!isPhoneVerified || !isEmailVerified) {
          alert("Please verify both phone number and email before submitting")
          return
        }
  
        // Check if password validation passes
        if (!validatePassword()) {
          alert("Please ensure your password meets all requirements")
          return
        }
  
        // Mock API call to submit form
        alert("Shop account created successfully!")
        window.location.href = "employee-management.html"
      })
    }
  
    // Helper functions
    function startOtpTimer(timerElement, timerInterval) {
      // Clear any existing timer
      if (timerInterval) {
        clearInterval(timerInterval)
      }
  
      let timeLeft = 120 // 2 minutes
  
      // Update timer text
      timerElement.textContent = formatTime(timeLeft)
      timerElement.parentElement.classList.remove("otp-timer-expired")
  
      const interval = setInterval(() => {
        timeLeft--
  
        timerElement.textContent = formatTime(timeLeft)
  
        if (timeLeft <= 0) {
          clearInterval(interval)
          timerElement.textContent = "00:00"
          timerElement.parentElement.classList.add("otp-timer-expired")
        }
      }, 1000)
  
      // Store the interval ID
      if (timerElement === phoneOtpTimer) {
        phoneTimerInterval = interval
      } else if (timerElement === emailOtpTimer) {
        emailTimerInterval = interval
      }
  
      // Return the interval ID so it can be cleared later
      return interval
    }
  
    function startResendCountdown(resendButton, countdownElement, timerInterval) {
      // Clear any existing timer
      if (timerInterval) {
        clearInterval(timerInterval)
      }
  
      // Initial delay of 10 seconds
      let timeLeft = 10
  
      // Disable resend button initially
      resendButton.disabled = true
  
      // Show countdown
      countdownElement.textContent = `(${timeLeft}s)`
  
      const interval = setInterval(() => {
        timeLeft--
  
        countdownElement.textContent = `(${timeLeft}s)`
  
        if (timeLeft <= 0) {
          clearInterval(interval)
          countdownElement.textContent = ""
          resendButton.disabled = false
        }
      }, 1000)
  
      // Store the interval ID
      if (resendButton === resendPhoneOtpBtn) {
        resendPhoneTimerInterval = interval
      } else if (resendButton === resendEmailOtpBtn) {
        resendEmailTimerInterval = interval
      }
  
      // Return the interval ID so it can be cleared later
      return interval
    }
  
    function formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`
    }
  
    // Mock API functions
    function mockSendOTP(contact, type) {
      return new Promise((resolve, reject) => {
        // Simulate API delay
        setTimeout(() => {
          // Generate a random 6-digit OTP
          const otp = Math.floor(100000 + Math.random() * 900000)
          console.log(`OTP sent to ${type}: ${contact}. OTP: ${otp}`)
  
          // Store OTP in sessionStorage for verification
          sessionStorage.setItem(`${type}Otp`, otp.toString())
  
          resolve()
        }, 1000)
      })
    }
  
    function mockVerifyOTP(otp, type) {
      return new Promise((resolve, reject) => {
        // Simulate API delay
        setTimeout(() => {
          const storedOtp = sessionStorage.getItem(`${type}Otp`)
  
          // For demo purposes, also accept '123456' as a valid OTP
          if (otp === storedOtp || otp === "123456") {
            console.log(`OTP verified for ${type}`)
            resolve()
          } else {
            reject(new Error("Invalid OTP"))
          }
        }, 1000)
      })
    }

    
  /*--------------------------------------------------------------
  # Select GarmentsType Section
  --------------------------------------------------------------*/
  const select = document.getElementById("fake-select");
  const options = document.getElementById("custom-options");
  const hiddenInput1 = document.getElementById("shop_type");
  const selectedValue = select.querySelector(".selected-value");

  select.addEventListener("click", () => {
    const isOpen = options.style.display === "block";
    options.style.display = isOpen ? "none" : "block";
    select.classList.toggle("open", !isOpen);
  });

  options.querySelectorAll("div").forEach(option => {
    option.addEventListener("click", () => {
        selectedValue.textContent = option.textContent;
        hiddenInput1.value = option.getAttribute("data-value");
        options.style.display = "none";
        select.classList.remove("open");
    });
  });

  document.addEventListener("click", (e) => {
    if (!select.contains(e.target) && !options.contains(e.target)) {
        options.style.display = "none";
        select.classList.remove("open");
    }
  });


});
  