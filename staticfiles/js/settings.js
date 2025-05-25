document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".sidebar-nav .nav-link");
    const contentSections = document.querySelectorAll(".content-section");
    const breadcrumbPage = document.getElementById("breadcrumb-page");
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    const appContainer = document.querySelector(".app-container");
  
    // Function to show a specific section
    function showSection(targetId) {
      // Hide all sections
      contentSections.forEach((section) => {
        section.classList.remove("active");
      });
  
      // Show the target section
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add("active");
      }
    }
  
    // Function to update the active state of nav links
    function updateActiveLink(activeLink) {
      navLinks.forEach((link) => {
        link.classList.remove("active");
      });
      activeLink.classList.add("active");
  
      // Update breadcrumbs
      breadcrumbPage.textContent = activeLink.textContent.trim();
    }
  
    // Add click event listeners to nav links
    navLinks.forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        const targetId = link.getAttribute("data-target");
  
        showSection(targetId);
        updateActiveLink(link);
  
        // Close sidebar on mobile after clicking a link
        if (window.innerWidth <= 768) {
          sidebar.classList.remove("open");
          appContainer.classList.remove("sidebar-open");
        }
      });
    });
  
    // Menu toggle functionality for mobile
    menuToggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      appContainer.classList.toggle("sidebar-open");
    });
  
    // Optional: Close sidebar if clicking outside of it on mobile
    document.addEventListener("click", (event) => {
      if (window.innerWidth <= 768 && sidebar.classList.contains("open")) {
        // Check if the click is outside the sidebar and not on the toggle button
        if (
          !sidebar.contains(event.target) &&
          !menuToggle.contains(event.target)
        ) {
          sidebar.classList.remove("open");
          appContainer.classList.remove("sidebar-open");
        }
      }
    });
  
    // --- Optional: Add simple interaction hints ---
  
    // Copy Webhook URL
    const copyButton = document.querySelector(".copy-button");
    const webhookUrlInput = document.getElementById("webhookUrl");
  
    if (copyButton && webhookUrlInput) {
      copyButton.addEventListener("click", () => {
        webhookUrlInput.select(); // Select the text
        webhookUrlInput.setSelectionRange(0, 99999); // For mobile devices
  
        try {
          navigator.clipboard
            .writeText(webhookUrlInput.value)
            .then(() => {
              // Optional: Provide feedback (e.g., change icon, show tooltip)
              const originalIcon = copyButton.innerHTML;
              copyButton.innerHTML = '<i class="fas fa-check"></i>'; // Change to checkmark
              setTimeout(() => {
                copyButton.innerHTML = originalIcon; // Revert after 1.5s
              }, 1500);
            })
            .catch((err) => {
              console.error("Failed to copy text: ", err);
              // Fallback using document.execCommand (deprecated but might work)
              try {
                document.execCommand("copy");
                const originalIcon = copyButton.innerHTML;
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                  copyButton.innerHTML = originalIcon;
                }, 1500);
              } catch (execErr) {
                console.error("Fallback copy failed:", execErr);
                alert("Could not copy text. Please copy manually.");
              }
            });
        } catch (err) {
          console.error("Clipboard API not available:", err);
          alert("Could not copy text. Please copy manually.");
        }
      });
    }
  
    // --- Initial state ---
    // Ensure the default active link corresponds to the default active section
    const defaultActiveLink = document.querySelector(
      ".sidebar-nav .nav-link.active"
    );
    if (defaultActiveLink) {
      const defaultTargetId = defaultActiveLink.getAttribute("data-target");
      showSection(defaultTargetId); // Show the initial section
      breadcrumbPage.textContent = defaultActiveLink.textContent.trim(); // Set initial breadcrumb
    } else {
      // Fallback if no link is marked active initially
      navLinks[0].classList.add("active");
      showSection(navLinks[0].getAttribute("data-target"));
      breadcrumbPage.textContent = navLinks[0].textContent.trim();
    }
  });
  