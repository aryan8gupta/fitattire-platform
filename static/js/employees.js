document.addEventListener("DOMContentLoaded", () => {
    // Navigation between pages
    const addUserBtn = document.getElementById("addUserBtn")
    if (addUserBtn) {
      addUserBtn.addEventListener("click", () => {
        window.location.href = "https://fitattire.shop/admin-only-user_signup-5famtsp89f1/"
      })
    }
  
    const addEmployeeBtn = document.getElementById("addEmployeeBtn")
    if (addEmployeeBtn) {
      addEmployeeBtn.addEventListener("click", () => {
        window.location.href = "https://fitattire.shop/employee-signup/"
      })
    }
  
    // Mobile sidebar toggle
    const toggleBtn = document.querySelector(".toggle-btn")
    const sidebar = document.querySelector(".sidebar")
  
    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed")
      })
    }
  
    // Search functionality
    const searchInput = document.querySelector(".search-box input")
    const tableRows = document.querySelectorAll(".data-table tbody tr")
  
    if (searchInput && tableRows.length > 0) {
      searchInput.addEventListener("keyup", function () {
        const searchTerm = this.value.toLowerCase()
  
        tableRows.forEach((row) => {
          const text = row.textContent.toLowerCase()
          if (text.includes(searchTerm)) {
            row.style.display = ""
          } else {
            row.style.display = "none"
          }
        })
      })
    }
  
    // Pagination
    const prevBtn = document.querySelector(".prev-btn")
    const nextBtn = document.querySelector(".next-btn")
  
    if (prevBtn && nextBtn) {
      prevBtn.addEventListener("click", () => {
        alert("Previous page functionality will be implemented here")
      })
  
      nextBtn.addEventListener("click", () => {
        alert("Next page functionality will be implemented here")
      })
    }
  })
  
  