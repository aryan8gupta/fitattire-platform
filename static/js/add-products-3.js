/*--------------------------------------------------------------
# Full Working JavaScript (uses your existing IDs)
--------------------------------------------------------------*/

let mainImages = [];
let allColorsSingleImages = [];

// --- Utils ---
function isDuplicate(file, list) {
  return list.some(f => (f.name ?? f.file?.name) === file.name && (f.size ?? f.file?.size) === file.size);
}
function closeAllDropdowns() {
  document.querySelectorAll(".dropdown-options").forEach(opt => (opt.style.display = "none"));
}

// === Main Image ===
const mainImageInput = document.getElementById("mainImageInput");
if (mainImageInput) {
  mainImageInput.addEventListener("change", function (e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (isDuplicate(file, mainImages)) {
      alert(`"${file.name}" is already uploaded.`);
      return;
    }
    const imageUrl = URL.createObjectURL(file);
    const preview = document.getElementById("mainImagePreview");
    if (preview) preview.src = imageUrl;
    mainImages = [file]; // keep single main image
  });
}

// === All Colors Single Image ===
const allColorsImageInput = document.getElementById("allColorsImageInput");
if (allColorsImageInput) {
  allColorsImageInput.addEventListener("change", function (e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (isDuplicate(file, allColorsSingleImages)) {
      alert(`"${file.name}" is already uploaded.`);
      return;
    }
    const imageUrl = URL.createObjectURL(file);
    const preview = document.getElementById("allColorsImagePreview");
    if (preview) preview.src = imageUrl;
    allColorsSingleImages = [file]; // keep single image
  });
}


// Close any open dropdowns when clicking outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".dropdown-wrapper")) {
    closeAllDropdowns();
  }
});


/* === Form Submission === */
const submitBtn = document.querySelector(".submit-add-products-btn");
if (submitBtn) {
  submitBtn.addEventListener("click", function () {

    product_name = document.getElementById('product-name').value;
    product_id = document.getElementById('product-id').value;
    product_fabric = document.getElementById('product-fabric').value;
    product_selling_price = document.getElementById('selling-price').value;

    if (!product_name || !product_id || !product_fabric || !product_selling_price) {
      alert("Please fill all the main product fields before adding variants.");
      return;
    }

    const btnText = submitBtn.querySelector(".btn-text");
    const btnSpinner = submitBtn.querySelector(".btn-spinner");
    if (btnText) btnText.textContent = "Submitting";
    if (btnSpinner) btnSpinner.style.display = "inline-block";

    const credits = document.getElementById("credits-used").innerText;

    if (credits == "0"){
      alert("No Credits Left");
      return;
    }

    const formData = new FormData();

    // Text inputs
    formData.append("product_name", document.getElementById("product-name")?.value ?? "");
    formData.append("product_id", document.getElementById("product-id")?.value ?? "");
    formData.append("fabric", document.getElementById("product-fabric")?.value ?? "");
    formData.append("selling_price", document.getElementById("selling-price")?.value ?? "");

    // Single images
    if (mainImages[0]) formData.append("main_image", mainImages[0]);
    if (allColorsSingleImages[0]) formData.append("all_colors_single", allColorsSingleImages[0]);


    fetch("/add-products-3/", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === "processing") {
          alert(data.message || "Product is being processed in background.");


          // Reset previews
          const placeholder = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
          const mainPrev = document.getElementById("mainImagePreview");
          const allColorsPrev = document.getElementById("allColorsImagePreview");
          if (mainPrev) mainPrev.src = placeholder;
          if (allColorsPrev) allColorsPrev.src = placeholder;

          fetch('/api/decrease-credits/', {
            method: 'POST',
          })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              document.getElementById("credits-used").innerText = data.new_credits;
            } else {
              alert("Error: " + data.message);
            }
          })
          .catch(err => console.error("Failed to decrease credits:", err));

          // Reset inputs
          if (mainImageInput) mainImageInput.value = "";
          if (allColorsImageInput) allColorsImageInput.value = "";

          // Reset text inputs
          const ids = ["product-name", "product-id", "product-fabric", "selling-price"];
          ids.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "";
          });

          // Reset state
          mainImages = [];
          allColorsSingleImages = [];

        } else {
          alert("Upload failed.");
        }
      })
      .catch(err => {
        console.error("Upload failed:", err);
        alert("Upload failed. Check console for details.");
      })
      .finally(() => {
        if (btnText) btnText.textContent = "Submit Form";
        if (btnSpinner) btnSpinner.style.display = "none";
      });
  });
}
