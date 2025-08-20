/*--------------------------------------------------------------
# Full Working JavaScript (uses your existing IDs)
--------------------------------------------------------------*/

let mainImages = [];
let allColorsSingleImages = [];
let allColorsMultipleImages = [];
let embroideryData = []; // [{ file: File, part: string }]

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

// === Multiple product color images ===
const imageInput = document.getElementById("imageUploadInput");
const imageContainer = document.getElementById("uploadedImagesContainer");

if (imageInput && imageContainer) {
  imageInput.addEventListener("change", function (event) {
    const files = Array.from(event.target.files || []);
    files.forEach(file => {
      if (!file.type.startsWith("image/")) return;
      if (isDuplicate(file, allColorsMultipleImages)) {
        alert(`"${file.name}" is already uploaded.`);
        return;
      }
      allColorsMultipleImages.push(file);
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      imageContainer.appendChild(img);
    });
    // don't reset input -> keeps duplicate protection working
  });
}

/* === Embroidery Parts === */
const embroideryParts = [
  "Front Neck", "Back Neck", "Sleeves", "Dupatta",
  "Border", "Pallu", "Lehenga", "Choli",
  "Kurti", "Sharara", "Plazo", "Blouse"
];

const embroideryInput = document.getElementById("embroideryImageUploadInput");
const embroideryContainer = document.getElementById("embroideryImagesContainer");

if (embroideryInput && embroideryContainer) {
  embroideryInput.addEventListener("change", function () {
    const files = Array.from(this.files || []);

    files.forEach(file => {
      if (!file.type.startsWith("image/")) return;

      // prevent duplicates by name+size
      const dupInData = embroideryData.some(it => it.file.name === file.name && it.file.size === file.size);
      if (dupInData) {
        alert(`"${file.name}" is already uploaded.`);
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        // Wrapper
        const wrapper = document.createElement("div");
        wrapper.classList.add("image-item");

        // --- Dropdown (custom, above image) ---
        const dropdownWrapper = document.createElement("div");
        dropdownWrapper.classList.add("dropdown-wrapper");
        dropdownWrapper.style.position = "relative";

        const customDropdown = document.createElement("div");
        customDropdown.classList.add("custom-dropdown");
        customDropdown.innerHTML = `<span class="selected-value-color">Select Part</span><i class="arrow fas fa-angle-down"></i>`;
        customDropdown.style.userSelect = "none";
        customDropdown.style.cursor = "pointer";

        const dropdownOptions = document.createElement("div");
        dropdownOptions.classList.add("dropdown-options");
        dropdownOptions.style.display = "none";
        dropdownOptions.style.position = "absolute";
        dropdownOptions.style.left = "0";
        dropdownOptions.style.right = "0";
        dropdownOptions.style.zIndex = "9999";
        dropdownOptions.style.maxHeight = "200px";
        dropdownOptions.style.overflowY = "auto";
        dropdownOptions.style.background = "#fff";
        dropdownOptions.style.border = "1px solid #ddd";
        dropdownOptions.style.borderRadius = "8px";
        dropdownOptions.style.boxShadow = "0 8px 16px rgba(0,0,0,0.15)";

        embroideryParts.forEach(part => {
          const opt = document.createElement("div");
          opt.textContent = part;
          opt.dataset.value = part;
          opt.style.padding = "8px 10px";
          opt.style.cursor = "pointer";
          opt.addEventListener("mouseenter", () => (opt.style.background = "#f5f5f5"));
          opt.addEventListener("mouseleave", () => (opt.style.background = ""));
          dropdownOptions.appendChild(opt);
        });

        dropdownWrapper.appendChild(customDropdown);
        dropdownWrapper.appendChild(dropdownOptions);

        // --- Image ---
        const img = document.createElement("img");
        img.src = e.target.result;
        img.style.display = "block";
        img.style.width = "150px";
        img.style.height = "150px";
        img.style.objectFit = "cover";
        img.style.margin = "6px auto";

        // --- Remove Button (below image) ---
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.classList.add("upload-image-button");
        removeBtn.style.background = "#ff4d4d";
        removeBtn.style.color = "#fff";
        removeBtn.style.border = "none";
        removeBtn.style.padding = "6px 12px";
        removeBtn.style.borderRadius = "6px";
        removeBtn.style.display = "block";
        removeBtn.style.margin = "6px auto 0";

        // Track in state
        const item = { file, part: "" };
        embroideryData.push(item);

        // Dropdown toggle
        customDropdown.addEventListener("click", (ev) => {
          ev.stopPropagation();
          // close others first
          closeAllDropdowns();
          dropdownOptions.style.display = dropdownOptions.style.display === "block" ? "none" : "block";
        });

        // Select part
        dropdownOptions.addEventListener("click", (ev) => {
          const target = ev.target;
          if (target && target.dataset && target.dataset.value) {
            const val = target.dataset.value;
            item.part = val;
            customDropdown.querySelector("span").textContent = val;
            dropdownOptions.style.display = "none";
          }
        });

        // Remove block
        removeBtn.addEventListener("click", () => {
          wrapper.remove();
          embroideryData = embroideryData.filter(d => !(d.file.name === file.name && d.file.size === file.size));
        });

        // Build block
        wrapper.appendChild(dropdownWrapper);
        wrapper.appendChild(img);
        wrapper.appendChild(removeBtn);
        embroideryContainer.appendChild(wrapper);
      };
      reader.readAsDataURL(file);
    });

    // allow re-upload of same files later
    embroideryInput.value = "";
  });
}

// Close any open dropdowns when clicking outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".dropdown-wrapper")) {
    closeAllDropdowns();
  }
});

/* === Dupatta Side Custom Dropdown (static one) ===
   Expects:
   <div class="dropdown-wrapper"> 
     <div class="custom-dropdown" id="dupattaDropdown"> ... </div>
     <div class="dropdown-options"> <div data-value="..."> ... </div> ... </div>
   </div>
   <input type="hidden" id="dupatta_side">
*/
(function initDupattaDropdown() {
  const trigger = document.getElementById("dupattaDropdown");
  const hiddenInput = document.getElementById("dupatta_side");
  if (!trigger || !hiddenInput) return;

  const wrapper = trigger.closest(".dropdown-wrapper");
  const options = wrapper ? wrapper.querySelector(".dropdown-options") : null;
  const labelSpan = trigger.querySelector(".selected-value-color");

  if (!wrapper || !options || !labelSpan) return;

  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    closeAllDropdowns();
    options.style.display = options.style.display === "block" ? "none" : "block";
  });

  options.addEventListener("click", (e) => {
    const target = e.target;
    if (target && target.dataset && target.dataset.value) {
      hiddenInput.value = target.dataset.value;
      labelSpan.textContent = target.textContent;
      options.style.display = "none";
    }
  });
})();

/* === Form Submission === */
const submitBtn = document.querySelector(".submit-add-products-btn");
if (submitBtn) {
  submitBtn.addEventListener("click", function () {

    productData.product_name = document.getElementById('product-name').value;
    productData.product_id = document.getElementById('product-id').value;
    productData.product_fabric = document.getElementById('product-fabric').value;
    productData.product_sizes = document.getElementById('product-sizes').value;
    productData.product_selling_price = document.getElementById('selling-price').value;

    if (!productData.product_name || !productData.product_id || !productData.product_fabric || !productData.product_sizes || !productData.product_selling_price === 0) {
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

    // ---- Validation: each embroidery image MUST have a part selected
    if (embroideryData.length > 0) {
      const missing = embroideryData.filter(it => !it.part || it.part.trim() === "");
      if (missing.length > 0) {
        if (btnText) btnText.textContent = "Submit Form";
        if (btnSpinner) btnSpinner.style.display = "none";
        alert("Please select embroidery part for all uploaded embroidery images.");
        return;
      }
    }

    const formData = new FormData();

    // Text inputs
    formData.append("product_name", document.getElementById("product-name")?.value ?? "");
    formData.append("product_id", document.getElementById("product-id")?.value ?? "");
    formData.append("fabric", document.getElementById("product-fabric")?.value ?? "");
    formData.append("sizes", document.getElementById("product-sizes")?.value ?? "");
    formData.append("dupatta_side", document.getElementById("dupatta_side")?.value ?? "");
    formData.append("selling_price", document.getElementById("selling-price")?.value ?? "");

    // Single images
    if (mainImages[0]) formData.append("main_image", mainImages[0]);
    if (allColorsSingleImages[0]) formData.append("all_colors_single", allColorsSingleImages[0]);

    // Multiple color images
    allColorsMultipleImages.forEach(file => formData.append("color_images[]", file));

    // Embroidery images + parts (order-aligned)
    embroideryData.forEach(item => {
      formData.append("embroidery_images[]", item.file);
      formData.append("embroidery_parts[]", item.part);
    });

    fetch("/add-products-2/", {
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
          if (imageContainer) imageContainer.innerHTML = "";
          if (embroideryContainer) embroideryContainer.innerHTML = "";

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
          if (imageInput) imageInput.value = "";
          if (embroideryInput) embroideryInput.value = "";

          // Reset text inputs
          const ids = ["product-name", "product-id", "product-fabric", "product-sizes", "dupatta_side", "selling-price"];
          ids.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "";
          });

          // Reset state
          mainImages = [];
          allColorsSingleImages = [];
          allColorsMultipleImages = [];
          embroideryData = [];
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
