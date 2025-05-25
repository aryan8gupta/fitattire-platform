document.addEventListener("DOMContentLoaded", () => {
    // Form elements
    const employeeRegistrationForm = document.getElementById("employeeRegistrationForm")
    const verifyPhoneBtn = document.getElementById("verifyPhoneBtn")
    const phoneOtpContainer = document.getElementById("phoneOtpContainer")
    const verifyPhoneOtpBtn = document.getElementById("verifyPhoneOtpBtn")
    const resendPhoneOtpBtn = document.getElementById("resendPhoneOtpBtn")
    const phoneOtpTimer = document.getElementById("phoneOtpTimer")
    const phoneOtp = document.getElementById("phoneOtp")
    const resendCountdown = document.getElementById("resendCountdown")
  
    // Password elements
    const passwordInput = document.getElementById("password")
    const confirmPasswordInput = document.getElementById("confirmPassword")
    const reqAlphanumeric = document.getElementById("req-alphanumeric")
    const reqLength = document.getElementById("req-length")
    const reqMatch = document.getElementById("req-match")
  
    // Date picker elements
    const dateOfBirthInput = document.getElementById("dateOfBirth")
    const dateOfJoiningInput = document.getElementById("dateOfJoining")
    const dateOfBirthBtn = document.getElementById("dateOfBirthBtn")
    const dateOfJoiningBtn = document.getElementById("dateOfJoiningBtn")
    const dateOfBirthPicker = document.getElementById("dateOfBirthPicker")
    const dateOfJoiningPicker = document.getElementById("dateOfJoiningPicker")
  
    // Timer variables
    let phoneTimerInterval
    let resendTimerInterval
  
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
  
    // Initialize enhanced date pickers
    initEnhancedDatePicker(dateOfBirthInput, dateOfBirthBtn, dateOfBirthPicker, {
      minYear: new Date().getFullYear() - 70,
      maxYear: new Date().getFullYear() - 18,
    })
  
    initEnhancedDatePicker(dateOfJoiningInput, dateOfJoiningBtn, dateOfJoiningPicker, {
      minYear: new Date().getFullYear() - 10,
      maxYear: new Date().getFullYear() + 1,
    })
  
    // Phone verification
    if (verifyPhoneBtn) {
      verifyPhoneBtn.addEventListener("click", () => {
        const phoneNumber = document.getElementById("phoneNumber").value
        if (!phoneNumber) {
          alert("Please enter a phone number")
          return
        }
  
        // Mock API call to send OTP
        mockSendOTP(phoneNumber)
          .then(() => {
            phoneOtpContainer.classList.remove("hidden")
            startOtpTimer(phoneOtpTimer)
            startResendCountdown(resendPhoneOtpBtn, resendCountdown)
            verifyPhoneBtn.textContent = "Sent"
            verifyPhoneBtn.disabled = true
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
        mockVerifyOTP(otp)
          .then(() => {
            verifyPhoneBtn.textContent = "Verified"
            verifyPhoneBtn.classList.add("verified")
            verifyPhoneBtn.style.backgroundColor = "var(--success-color)"
            phoneOtpContainer.classList.add("hidden")
  
            // Clear the timers when verified
            if (phoneTimerInterval) {
              clearInterval(phoneTimerInterval)
            }
            if (resendTimerInterval) {
              clearInterval(resendTimerInterval)
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
        mockSendOTP(phoneNumber)
          .then(() => {
            // Reset and restart the timers
            startOtpTimer(phoneOtpTimer)
            startResendCountdown(resendPhoneOtpBtn, resendCountdown)
            alert("OTP resent successfully")
          })
          .catch((error) => {
            alert("Error resending OTP: " + error.message)
            // Re-enable the resend button if there's an error
            resendPhoneOtpBtn.disabled = false
          })
      })
    }
  
    // Form submission
    if (employeeRegistrationForm) {
      employeeRegistrationForm.addEventListener("submit", (e) => {
        e.preventDefault()
  
        // Check if phone is verified
        const isPhoneVerified = verifyPhoneBtn.textContent === "Verified"
  
        if (!isPhoneVerified) {
          alert("Please verify phone number before submitting")
          return
        }
  
        // Check if password validation passes
        if (!validatePassword()) {
          alert("Please ensure your password meets all requirements")
          return
        }
  
        // Mock API call to submit form
        alert("Employee account created successfully!")
        window.location.href = "employee-management.html"
      })
    }
  
    // Helper functions
    function startOtpTimer(timerElement) {
      // Clear any existing timer
      if (phoneTimerInterval) {
        clearInterval(phoneTimerInterval)
        phoneTimerInterval = null
      }
  
      let timeLeft = 120 // 2 minutes
  
      // Update timer text
      timerElement.textContent = formatTime(timeLeft)
      timerElement.parentElement.classList.remove("otp-timer-expired")
  
      phoneTimerInterval = setInterval(() => {
        timeLeft--
  
        timerElement.textContent = formatTime(timeLeft)
  
        if (timeLeft <= 0) {
          clearInterval(phoneTimerInterval)
          phoneTimerInterval = null
          timerElement.textContent = "00:00"
          timerElement.parentElement.classList.add("otp-timer-expired")
        }
      }, 1000)
  
      return phoneTimerInterval
    }
  
    function startResendCountdown(resendButton, countdownElement) {
      // Clear any existing timer
      if (resendTimerInterval) {
        clearInterval(resendTimerInterval)
        resendTimerInterval = null
      }
  
      // Initial delay of 10 seconds
      let timeLeft = 10
  
      // Disable resend button initially
      resendButton.disabled = true
  
      // Show countdown
      countdownElement.textContent = `(${timeLeft}s)`
  
      resendTimerInterval = setInterval(() => {
        timeLeft--
  
        countdownElement.textContent = `(${timeLeft}s)`
  
        if (timeLeft <= 0) {
          clearInterval(resendTimerInterval)
          resendTimerInterval = null
          countdownElement.textContent = ""
          resendButton.disabled = false
        }
      }, 1000)
  
      return resendTimerInterval
    }
  
    function formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`
    }
  
    // Enhanced date picker implementation
    function initEnhancedDatePicker(inputElement, buttonElement, pickerElement, options = {}) {
      if (!inputElement || !buttonElement || !pickerElement) return
  
      const today = new Date()
      const currentYear = today.getFullYear()
      const currentMonth = today.getMonth()
  
      const minYear = options.minYear || currentYear - 100
      const maxYear = options.maxYear || currentYear
  
      let selectedDate = null
      let currentViewMonth = currentMonth
      let currentViewYear = currentYear
  
      // Create date picker structure
      createDatePickerUI()
  
      // Open date picker when button is clicked
      buttonElement.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()
  
        // Toggle date picker visibility
        const isActive = pickerElement.classList.contains("active")
  
        // Close all other date pickers first
        document.querySelectorAll(".datepicker.active").forEach((picker) => {
          if (picker !== pickerElement) {
            picker.classList.remove("active")
          }
        })
  
        if (isActive) {
          pickerElement.classList.remove("active")
        } else {
          pickerElement.classList.add("active")
          renderCalendar()
        }
      })
  
      // Close date picker when clicking outside
      document.addEventListener("click", (e) => {
        if (!pickerElement.contains(e.target) && e.target !== buttonElement && e.target !== inputElement) {
          pickerElement.classList.remove("active")
        }
      })
  
      function createDatePickerUI() {
        // Create month and year dropdowns for easier selection
        const monthNames = [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ]
  
        let monthOptions = ""
        for (let i = 0; i < 12; i++) {
          monthOptions += `<option value="${i}">${monthNames[i]}</option>`
        }
  
        let yearOptions = ""
        for (let year = maxYear; year >= minYear; year--) {
          yearOptions += `<option value="${year}">${year}</option>`
        }
  
        pickerElement.innerHTML = `
          <div class="datepicker-selectors">
            <select id="${pickerElement.id}-month" class="datepicker-month-select">
              ${monthOptions}
            </select>
            <select id="${pickerElement.id}-year" class="datepicker-year-select">
              ${yearOptions}
            </select>
          </div>
          <div class="datepicker-grid">
            <div class="datepicker-day-header">Su</div>
            <div class="datepicker-day-header">Mo</div>
            <div class="datepicker-day-header">Tu</div>
            <div class="datepicker-day-header">We</div>
            <div class="datepicker-day-header">Th</div>
            <div class="datepicker-day-header">Fr</div>
            <div class="datepicker-day-header">Sa</div>
          </div>
        `
  
        // Set default values for dropdowns
        const monthSelect = document.getElementById(`${pickerElement.id}-month`)
        const yearSelect = document.getElementById(`${pickerElement.id}-year`)
  
        if (monthSelect && yearSelect) {
          monthSelect.value = currentViewMonth
          yearSelect.value = currentViewYear
  
          // Add event listeners for dropdowns
          monthSelect.addEventListener("change", function () {
            currentViewMonth = Number.parseInt(this.value)
            renderCalendar()
          })
  
          yearSelect.addEventListener("change", function () {
            currentViewYear = Number.parseInt(this.value)
            renderCalendar()
          })
        }
      }
  
      function renderCalendar() {
        // Update month and year dropdowns
        const monthSelect = document.getElementById(`${pickerElement.id}-month`)
        const yearSelect = document.getElementById(`${pickerElement.id}-year`)
  
        if (monthSelect && yearSelect) {
          monthSelect.value = currentViewMonth.toString()
          yearSelect.value = currentViewYear.toString()
        }
  
        // Get the grid to add days to
        const grid = pickerElement.querySelector(".datepicker-grid")
  
        // Clear existing days (except headers)
        const dayElements = grid.querySelectorAll(".datepicker-day")
        dayElements.forEach((day) => day.remove())
  
        // Get first day of month and total days
        const firstDay = new Date(currentViewYear, currentViewMonth, 1).getDay()
        const daysInMonth = new Date(currentViewYear, currentViewMonth + 1, 0).getDate()
  
        // Add empty cells for days before the first day of month
        for (let i = 0; i < firstDay; i++) {
          const emptyDay = document.createElement("div")
          emptyDay.className = "datepicker-day disabled"
          grid.appendChild(emptyDay)
        }
  
        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
          const dayElement = document.createElement("div")
          dayElement.className = "datepicker-day"
          dayElement.textContent = day
  
          // Check if this day is today
          const isToday =
            day === today.getDate() && currentViewMonth === today.getMonth() && currentViewYear === today.getFullYear()
          if (isToday) {
            dayElement.classList.add("today")
          }
  
          // Check if this day is selected
          if (
            selectedDate &&
            day === selectedDate.getDate() &&
            currentViewMonth === selectedDate.getMonth() &&
            currentViewYear === selectedDate.getFullYear()
          ) {
            dayElement.classList.add("selected")
          }
  
          // Check if this date is valid based on min/max year
          const thisDate = new Date(currentViewYear, currentViewMonth, day)
          const isDisabled = thisDate.getFullYear() < minYear || thisDate.getFullYear() > maxYear
  
          if (isDisabled) {
            dayElement.classList.add("disabled")
          } else {
            // Add click event to select date
            dayElement.addEventListener("click", () => {
              selectedDate = new Date(currentViewYear, currentViewMonth, day)
  
              // Format date as MM/DD/YYYY
              const formattedDate = `${(currentViewMonth + 1).toString().padStart(2, "0")}/${day.toString().padStart(2, "0")}/${currentViewYear}`
              inputElement.value = formattedDate
  
              // Close the date picker
              pickerElement.classList.remove("active")
            })
          }
  
          grid.appendChild(dayElement)
        }
      }
    }
  
    // Mock API functions
    function mockSendOTP(phoneNumber) {
      return new Promise((resolve, reject) => {
        // Simulate API delay
        setTimeout(() => {
          // Generate a random 6-digit OTP
          const otp = Math.floor(100000 + Math.random() * 900000)
          console.log(`OTP sent to phone: ${phoneNumber}. OTP: ${otp}`)
  
          // Store OTP in sessionStorage for verification
          sessionStorage.setItem("phoneOtp", otp.toString())
  
          resolve()
        }, 1000)
      })
    }
  
    function mockVerifyOTP(otp) {
      return new Promise((resolve, reject) => {
        // Simulate API delay
        setTimeout(() => {
          const storedOtp = sessionStorage.getItem("phoneOtp")
  
          // For demo purposes, also accept '123456' as a valid OTP
          if (otp === storedOtp || otp === "123456") {
            console.log("OTP verified for phone")
            resolve()
          } else {
            reject(new Error("Invalid OTP"))
          }
        }, 1000)
      })
    }


  /*--------------------------------------------------------------
  # Select Gender Section
  --------------------------------------------------------------*/
  const select = document.getElementById("fake-select");
  const options = document.getElementById("custom-options");
  const hiddenInput = document.getElementById("employee_gender");
  const selectedValue = select.querySelector(".selected-value");

  select.addEventListener("click", () => {
    const isOpen = options.style.display === "block";
    options.style.display = isOpen ? "none" : "block";
    select.classList.toggle("open", !isOpen);
  });

  options.querySelectorAll("div").forEach(option => {
    option.addEventListener("click", () => {
        selectedValue.textContent = option.textContent;
        hiddenInput.value = option.getAttribute("data-value");
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


  /*--------------------------------------------------------------
  # Select Job Section
  --------------------------------------------------------------*/
  const selectJob = document.getElementById("fake-select-job");
  const optionsJob = document.getElementById("custom-options-job");
  const hiddenInputJob = document.getElementById("employee_job");
  const selectedValueJob = selectJob.querySelector(".selected-value-job");

  selectJob.addEventListener("click", () => {
    const isOpen = optionsJob.style.display === "block";
    optionsJob.style.display = isOpen ? "none" : "block";
    selectJob.classList.toggle("open", !isOpen);
  });

  optionsJob.querySelectorAll("div").forEach(option => {
    option.addEventListener("click", () => {
        selectedValueJob.textContent = option.textContent;
        hiddenInputJob.value = option.getAttribute("data-value");
        optionsJob.style.display = "none";
        selectJob.classList.remove("open");
    });
  });

  document.addEventListener("click", (e) => {
    if (!selectJob.contains(e.target) && !optionsJob.contains(e.target)) {
        optionsJob.style.display = "none";
        selectJob.classList.remove("open");
    }
  });

});
  