// /*--------------------------------------------------------------
// # Script-1
// --------------------------------------------------------------*/

// let mainImages = [];
// let secondImages = [];
// let allColorsSingleImages = [];

// // === Main Image ===
// document.getElementById("mainImageInput").addEventListener("change", function (e) {
//   const file = e.target.files[0];
//   if (file) {
//     const isDuplicate = mainImages.some(f => f.name === file.name && f.size === file.size);
//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }
//     const imageUrl = URL.createObjectURL(file);
//     document.getElementById("mainImagePreview").src = imageUrl;
//     mainImages.push(file);
//   }
// });

// // === Second Image ===
// document.getElementById("secondImageInput").addEventListener("change", function (e) {
//   const file = e.target.files[0];
//   if (file) {
//     const isDuplicate = secondImages.some(f => f.name === file.name && f.size === file.size);
//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }
//     const imageUrl = URL.createObjectURL(file);
//     document.getElementById("secondImagePreview").src = imageUrl;
//     secondImages.push(file);
//   }
// });

// // === All Colors Single Image ===
// document.getElementById("allColorsImageInput").addEventListener("change", function (e) {
//   const file = e.target.files[0];
//   if (file) {
//     const isDuplicate = allColorsSingleImages.some(f => f.name === file.name && f.size === file.size);
//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }
//     const imageUrl = URL.createObjectURL(file);
//     document.getElementById("allColorsImagePreview").src = imageUrl;
//     allColorsSingleImages.push(file);
//   }
// });

// // === Multiple product color images ===
// let allColorsMultipleImages = [];

// const imageInput = document.getElementById('imageUploadInput');
// const imageContainer = document.getElementById('uploadedImagesContainer');

// imageInput.addEventListener('change', function (event) {
//   const files = Array.from(event.target.files);

//   files.forEach(file => {
//     if (!file.type.startsWith('image/')) return;

//     // Check for duplicate by name + size
//     const isDuplicate = allColorsMultipleImages.some(
//       existingFile => existingFile.name === file.name && existingFile.size === file.size
//     );

//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return; // Skip this file
//     }

//     // Store file
//     allColorsMultipleImages.push(file);

//     // Create preview
//     const img = document.createElement('img');
//     img.src = URL.createObjectURL(file);
//     imageContainer.appendChild(img);
//   });

//   // No reset → so duplicate check works next time
// });



// const embroideryParts = [
//   "Neckline",
//   "Kurti Bottom",
//   "Dupatta",
//   "Sleeves / Hands",
//   "Back Design",
//   "Other"
// ];

// document.getElementById("embroideryImageUploadInput").addEventListener("change", function(event) {
//   const container = document.getElementById("embroideryImagesContainer");

//   Array.from(event.target.files).forEach(file => {
//     const reader = new FileReader();

//     reader.onload = function(e) {
//       // Create block
//       const block = document.createElement("div");
//       block.classList.add("embroidery-block");
//       block.style.display = "inline-block";
//       block.style.margin = "10px";
//       block.style.textAlign = "center";

//       // Image preview
//       const img = document.createElement("img");
//       img.src = e.target.result;
//       img.width = 150;
//       img.height = 150;
//       img.style.display = "block";
//       img.style.marginBottom = "5px";

//       // Select field
//       const select = document.createElement("select");
//       embroideryParts.forEach(part => {
//         const option = document.createElement("option");
//         option.value = part;
//         option.textContent = part;
//         select.appendChild(option);
//       });
//       select.style.display = "block";
//       select.style.marginBottom = "5px";

//       // Remove button
//       const removeBtn = document.createElement("button");
//       removeBtn.type = "button";
//       removeBtn.textContent = "Remove";
//       removeBtn.classList.add("upload-image-button");
//       removeBtn.style.background = "#ff4d4d";
//       removeBtn.style.color = "white";
//       removeBtn.style.border = "none";
//       removeBtn.style.padding = "5px 10px";
//       removeBtn.style.borderRadius = "5px";
//       removeBtn.addEventListener("click", () => {
//         block.remove();
//       });

//       // Hidden input to keep file reference (for form submit)
//       const hiddenFileInput = document.createElement("input");
//       hiddenFileInput.type = "file";
//       hiddenFileInput.name = "embroidery_images[]";  // Django will receive as list
//       hiddenFileInput.files = new DataTransfer().files; // placeholder

//       // Append all
//       block.appendChild(img);
//       block.appendChild(select);
//       block.appendChild(removeBtn);

//       container.appendChild(block);
//     };

//     reader.readAsDataURL(file);
//   });
// });



// // === Dupatta Side Custom Dropdown ===
// document.addEventListener("DOMContentLoaded", function () {
//     const dropdown = document.querySelector(".dropdown-wrapper");
//     const selectedValue = dropdown.querySelector(".selected-value-color");
//     const hiddenInput = document.getElementById("dupatta_side");
//     const options = dropdown.querySelectorAll(".dropdown-options div");

//     // Toggle dropdown
//     dropdown.querySelector(".custom-dropdown").addEventListener("click", function () {
//         dropdown.classList.toggle("active");
//     });

//     // Handle option click
//     options.forEach(option => {
//         option.addEventListener("click", function () {
//             selectedValue.textContent = this.textContent;
//             hiddenInput.value = this.getAttribute("data-value");
//             dropdown.classList.remove("active");
//         });
//     });

//     // Close if clicking outside
//     document.addEventListener("click", function (event) {
//         if (!dropdown.contains(event.target)) {
//             dropdown.classList.remove("active");
//         }
//     });
// });



// // === Form Submission ===
// document.querySelector('.submit-add-products-btn').addEventListener('click', function () {
//   const submitButton = document.querySelector('.submit-add-products-btn');
//   let btnText = submitButton.querySelector('.btn-text');
//   let btnSpinner = submitButton.querySelector('.btn-spinner');

//   // Show spinner and update text
//   btnText.textContent = "Submitting";
//   btnSpinner.style.display = 'inline-block';

//   const formData = new FormData();

//   // Text inputs
//   formData.append('product_name', document.getElementById('product-name').value);
//   formData.append('product_id', document.getElementById('product-id').value);
//   formData.append('fabric', document.getElementById('product-fabric').value);
//   formData.append('sizes', document.getElementById('product-sizes').value);
//   formData.append('dupatta_side', document.getElementById('dupatta_side').value);
//   formData.append('selling_price', document.getElementById('selling-price').value);

//   // Single images
//   if (mainImages[0]) formData.append('main_image', mainImages[0]);
//   if (secondImages[0]) formData.append('second_image', secondImages[0]);
//   if (allColorsSingleImages[0]) formData.append('all_colors_single', allColorsSingleImages[0]);

//   // Multiple color images
//   allColorsMultipleImages.forEach((file, index) => {
//     formData.append('color_images[]', file);
//   });

//   fetch('/add-products-2/', {
//     method: 'POST',
//     body: formData
//   })
//     .then(res => res.json())
//     .then(data => {

//       if (data.uploaded_urls === 'uploaded') {
//         alert('Product added successfully!');
//         document.getElementById("mainImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
//         document.getElementById("secondImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
//         document.getElementById('allColorsImagePreview').src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    
//         document.getElementById('uploadedImagesContainer').innerHTML = '';

//         document.getElementById("mainImageInput").value = '';
//         document.getElementById("secondImageInput").value = '';
//         document.getElementById("allColorsImageInput").value = '';
//         document.getElementById("imageUploadInput").value = '';

//         document.getElementById('product-name').value = '';
//         document.getElementById('product-id').value = '';
//         document.getElementById('product-fabric').value = '';
//         document.getElementById('product-sizes').value = '';
//         document.getElementById('dupatta_side').value = '';
//         document.getElementById('selling-price').value = '';

//         mainImages = [];
//         secondImages = [];
//         allColorsSingleImages = [];
//         allColorsMultipleImages = [];
//       }
//     })
//     .catch(err => {
//       console.error("Upload failed:", err);
//     })
//     .finally(() => {
//       // Reset button state
//       btnText.textContent = "Submit Form";
//       btnSpinner.style.display = 'none';
//     });
// });



//   /*--------------------------------------------------------------
//   # Form Validation and Submission
//   --------------------------------------------------------------*/

// //   productForm1 = document.querySelector('.product-form-model');
// //   productForm2 = document.querySelector('.product-form-nomodel');

// //   const submitBtn1 = productForm1.querySelector('.submit-add-products-btn');
// //   submitBtn1.addEventListener("click", handleSubmitBtn);

// //   const submitBtn2 = productForm2.querySelector('.submit-add-products-btn');
// //   submitBtn2.addEventListener("click", handleSubmitBtn);

// //   async function handleSubmitBtn() {
// //     let productForm = null;
// //     let submitButton = null;
//     // let btnText = null;
//     // let btnSpinner = null;
  
// //     if (currentMode === "model") {
// //       productForm = document.querySelector('.product-form-model');
// //     } else if (currentMode === "nomodel") {
// //       productForm = document.querySelector('.product-form-nomodel');
// //     }
  
// //     if (productForm) {
// //       submitButton = productForm.querySelector('.submit-add-products-btn');
//     //   btnText = submitButton.querySelector('.btn-text');
//     //   btnSpinner = submitButton.querySelector('.btn-spinner');
// //     }
  
// //     if (!submitButton) return;
    
// //     const idsArray = Array.from(scannedIds);
// //     productData.qrcode_ids = [...idsArray];
  
//     // btnText.textContent = "Submitting";
//     // btnSpinner.style.display = 'inline-block';
  
// //     try {
  
// //       if (productData.qrcode_ids.length === 0) {
// //         const randomId = Math.floor(10000 + Math.random() * 90000).toString();
// //         productData.qrcode_ids.push(randomId);
// //       }

// //       const formData = new FormData();
// //       formData.append('document', JSON.stringify(productData));
// //       formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
  
// //       // 🖼️ Add images
// //       if (currentMode === "model") {
// //         productGarmentImages.forEach((file, index) => {
// //           formData.append(`garment_${index}`, file);
// //         });
  
// //         productResultImages.forEach((item, index) => {
// //           if (item instanceof File) {
// //             formData.append(`result_file_${index}`, item);
// //           } else if (typeof item === 'string') {
// //             formData.append(`result_url_${index}`, item);
// //           }
// //         });
  
// //       } else if (currentMode === "nomodel") {
// //         if (secondImages.length > 0) {
// //           secondImages.forEach((file, index) => {
// //             formData.append(`garment_${index}`, file);
// //           });
// //         }
  
// //         if (mainImages.length > 0) {
// //           mainImages.forEach((item, index) => {
// //             formData.append(`result_file_${index}`, item);
// //           });
// //         }
// //       }
  
//     //   const response = await fetch('/add-products/', {
//     //     method: 'POST',
//     //     body: formData
//     //   });
  
//     //   const contentType = response.headers.get("content-type");
//     //   if (contentType && contentType.includes("application/json")) {
//     //     const result = await response.json();
  
//     //     if (result.uploaded_urls === 'uploaded') {
//     //       alert('Product added successfully!');
// //           localStorage.setItem('lastSubmittedData', JSON.stringify(productData));
  
// //           const suffix = currentMode === 'model' ? '' : '-2';
// //           document.getElementById(`brand-name${suffix}`).value = '';
// //           document.getElementById(`product-name${suffix}`).value = '';
// //           document.getElementById(`product-fabric${suffix}`).value = '';
// //           document.getElementById(`product-color${suffix}`).value = '';
// //           document.getElementById(`product-quantity${suffix}`).value = '';
// //           document.getElementById(`product-price${suffix}`).value = '';
// //           document.getElementById(`selling-price${suffix}`).value = '';
// //           document.getElementById(`scanned-items${suffix}`).innerHTML = '';
  
// //           document.querySelectorAll('input[name="size"]:checked').forEach(c => c.checked = false);
// //           showResultImages = []; showGarmentImages = [];
// //           showMainImages = []; showSecondImages = [];
// //           scannedIds.clear();
  
// //           previewImage.src = 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png';
  
// //           productData = {
// //             qrcode_ids: [],
// //             brand_name: '',
// //             product_name: '',
// //             product_fabric: '',
// //             product_sizes: [],
// //             product_quantity: 0,
// //             product_price: 0,
// //             product_selling_price: 0,
// //             product_colors: []
// //           };
  
// //           if (currentMode === "model") {
// //             document.getElementById('resultImage').src = '';
// //             document.getElementById('resultImage').style.display = 'none';
// //             document.querySelector('.selected-value-color').textContent = 'Select Color';
// //             document.getElementById('manual-color-input').value = '';
// //             document.getElementById('product-color').value = '';
// //             document.querySelector('label[for="model-image-upload"]').style.display = 'none';
// //           } else {
// //             document.querySelector('.selected-value-color').textContent = 'Select Color';
// //             document.getElementById('manual-color-input-2').value = '';
// //             document.getElementById('product-color-2').value = '';
// //           }
  
// //           resetCategorySections.forEach(reset => reset());
// //           updateVariantsTable();
// //         } else {
// //           alert('Error: ' + (result.error || 'Something went wrong.'));
// //         }
// //       } else {
// //         const text = await response.text();
// //         console.error("❌ Not JSON. Response was:", text);
// //         alert("Server returned an unexpected response.");
// //       }
// //     } catch (error) {
// //       console.error('Submission error:', error);
// //       alert('Encryption or network/server error occurred.');
//     // } finally {
//     //   btnText.textContent = "Submit Form";
//     //   btnSpinner.style.display = 'none';
//     // }
// //   }






/*--------------------------------------------------------------
# Script-1 (Updated)
--------------------------------------------------------------*/

// let mainImages = [];
// let allColorsSingleImages = [];
// let allColorsMultipleImages = [];
// let embroideryData = []; // { file, part }

// /* === Main Image === */
// document.getElementById("mainImageInput").addEventListener("change", function (e) {
//   const file = e.target.files[0];
//   if (file) {
//     const isDuplicate = mainImages.some(f => f.name === file.name && f.size === file.size);
//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }
//     const imageUrl = URL.createObjectURL(file);
//     document.getElementById("mainImagePreview").src = imageUrl;
//     mainImages.push(file);
//   }
// });

// /* === All Colors Single Image === */
// document.getElementById("allColorsImageInput").addEventListener("change", function (e) {
//   const file = e.target.files[0];
//   if (file) {
//     const isDuplicate = allColorsSingleImages.some(f => f.name === file.name && f.size === file.size);
//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }
//     const imageUrl = URL.createObjectURL(file);
//     document.getElementById("allColorsImagePreview").src = imageUrl;
//     allColorsSingleImages.push(file);
//   }
// });

// /* === Multiple product color images === */
// const imageInput = document.getElementById('imageUploadInput');
// const imageContainer = document.getElementById('uploadedImagesContainer');

// imageInput.addEventListener('change', function (event) {
//   const files = Array.from(event.target.files);

//   files.forEach(file => {
//     if (!file.type.startsWith('image/')) return;

//     const isDuplicate = allColorsMultipleImages.some(
//       existingFile => existingFile.name === file.name && existingFile.size === file.size
//     );

//     if (isDuplicate) {
//       alert(`"${file.name}" is already uploaded.`);
//       return;
//     }

//     allColorsMultipleImages.push(file);

//     const img = document.createElement('img');
//     img.src = URL.createObjectURL(file);
//     imageContainer.appendChild(img);
//   });
// });

// /* === Embroidery Parts === */
// const embroideryParts = [
//   "Front Neck", "Back Neck", "Sleeves", "Dupatta", "Pants"
// ];

// const embroideryInput = document.getElementById("embroideryImageUploadInput");
// const embroideryContainer = document.getElementById("embroideryImagesContainer");

// embroideryInput.addEventListener("change", function () {
//   const files = Array.from(this.files);

//   files.forEach(file => {
//     const reader = new FileReader();
//     reader.onload = function (e) {
//       // Create wrapper
//       const wrapper = document.createElement("div");
//       wrapper.classList.add("image-item");

//       // Dropdown
//       const dropdownWrapper = document.createElement("div");
//       dropdownWrapper.classList.add("dropdown-wrapper");

//       const customDropdown = document.createElement("div");
//       customDropdown.classList.add("custom-dropdown");
//       customDropdown.innerHTML = `<span class="selected-value-color">Select Part</span><i class="arrow fas fa-angle-down"></i>`;

//       const dropdownOptions = document.createElement("div");
//       dropdownOptions.classList.add("dropdown-options");
//       embroideryParts.forEach(part => {
//         const option = document.createElement("div");
//         option.dataset.value = part;
//         option.textContent = part;
//         dropdownOptions.appendChild(option);
//       });

//       dropdownWrapper.appendChild(customDropdown);
//       dropdownWrapper.appendChild(dropdownOptions);

//       // Image
//       const img = document.createElement("img");
//       img.src = e.target.result;

//       // Remove Button
//       const removeBtn = document.createElement("button");
//       removeBtn.textContent = "Remove";
//       removeBtn.classList.add("remove-btn");

//       // Add file to embroideryData
//       const embroideryItem = { file, part: "" };
//       embroideryData.push(embroideryItem);

//       // Remove Button action
//       removeBtn.addEventListener("click", () => {
//         wrapper.remove();
//         embroideryData = embroideryData.filter(item => item.file !== file);
//       });

//       // Dropdown toggle
//       customDropdown.addEventListener("click", () => {
//         dropdownOptions.style.display =
//           dropdownOptions.style.display === "block" ? "none" : "block";
//       });

//       // Option select
//       dropdownOptions.addEventListener("click", (ev) => {
//         if (ev.target.dataset.value) {
//           customDropdown.querySelector("span").textContent = ev.target.dataset.value;
//           embroideryItem.part = ev.target.dataset.value; // ✅ update embroideryData
//           dropdownOptions.style.display = "none";
//         }
//       });

//       // Append all
//       wrapper.appendChild(dropdownWrapper);
//       wrapper.appendChild(img);
//       wrapper.appendChild(removeBtn);

//       embroideryContainer.appendChild(wrapper);
//     };
//     reader.readAsDataURL(file);
//   });
// });




// /* === Dupatta Side Custom Dropdown === */
// document.addEventListener("DOMContentLoaded", function () {
//   const dropdown = document.querySelector(".dropdown-wrapper");
//   const selectedValue = dropdown.querySelector(".selected-value-color");
//   const hiddenInput = document.getElementById("dupatta_side");
//   const options = dropdown.querySelectorAll(".dropdown-options div");

//   dropdown.querySelector(".custom-dropdown").addEventListener("click", function () {
//     dropdown.classList.toggle("active");
//   });

//   options.forEach(option => {
//     option.addEventListener("click", function () {
//       selectedValue.textContent = this.textContent;
//       hiddenInput.value = this.getAttribute("data-value");
//       dropdown.classList.remove("active");
//     });
//   });

//   document.addEventListener("click", function (event) {
//     if (!dropdown.contains(event.target)) {
//       dropdown.classList.remove("active");
//     }
//   });
// });

// /* === Form Submission === */
// document.querySelector('.submit-add-products-btn').addEventListener('click', function () {
//   const submitButton = document.querySelector('.submit-add-products-btn');
//   let btnText = submitButton.querySelector('.btn-text');
//   let btnSpinner = submitButton.querySelector('.btn-spinner');

//   btnText.textContent = "Submitting";
//   btnSpinner.style.display = 'inline-block';

//   const formData = new FormData();

//   // Text inputs
//   formData.append('product_name', document.getElementById('product-name').value);
//   formData.append('product_id', document.getElementById('product-id').value);
//   formData.append('fabric', document.getElementById('product-fabric').value);
//   formData.append('sizes', document.getElementById('product-sizes').value);
//   formData.append('dupatta_side', document.getElementById('dupatta_side').value);
//   formData.append('selling_price', document.getElementById('selling-price').value);

//   // Single images
//   if (mainImages[0]) formData.append('main_image', mainImages[0]);
//   if (allColorsSingleImages[0]) formData.append('all_colors_single', allColorsSingleImages[0]);

//   // Multiple color images
//   allColorsMultipleImages.forEach((file) => {
//     formData.append('color_images[]', file);
//   });

//   // Embroidery images + parts
//   embroideryData.forEach(item => {
//     formData.append('embroidery_images[]', item.file);
//     formData.append('embroidery_parts[]', item.part || ""); // send empty if not chosen
//   });

//   fetch('/add-products-2/', {
//     method: 'POST',
//     body: formData
//   })
//     .then(res => res.json())
//     .then(data => {
//       if (data.uploaded_urls === 'uploaded') {
//         alert('Product added successfully!');

//         // Reset images
//         document.getElementById("mainImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
//         document.getElementById('allColorsImagePreview').src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
//         document.getElementById('uploadedImagesContainer').innerHTML = '';
//         document.getElementById("embroideryImagesContainer").innerHTML = '';

//         // Reset inputs
//         document.getElementById("mainImageInput").value = '';
//         document.getElementById("allColorsImageInput").value = '';
//         document.getElementById("imageUploadInput").value = '';
//         document.getElementById("embroideryImageUploadInput").value = '';

//         document.getElementById('product-name').value = '';
//         document.getElementById('product-id').value = '';
//         document.getElementById('product-fabric').value = '';
//         document.getElementById('product-sizes').value = '';
//         document.getElementById('dupatta_side').value = '';
//         document.getElementById('selling-price').value = '';

//         mainImages = [];
//         allColorsSingleImages = [];
//         allColorsMultipleImages = [];
//         embroideryData = [];
//       }
//     })
//     .catch(err => {
//       console.error("Upload failed:", err);
//     })
//     .finally(() => {
//       btnText.textContent = "Submit Form";
//       btnSpinner.style.display = 'none';
//     });
// });



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
