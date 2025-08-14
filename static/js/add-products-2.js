/*--------------------------------------------------------------
# Script-1
--------------------------------------------------------------*/

let mainImages = [];
let secondImages = [];
let allColorsSingleImages = [];

// === Main Image ===
document.getElementById("mainImageInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const isDuplicate = mainImages.some(f => f.name === file.name && f.size === file.size);
    if (isDuplicate) {
      alert(`"${file.name}" is already uploaded.`);
      return;
    }
    const imageUrl = URL.createObjectURL(file);
    document.getElementById("mainImagePreview").src = imageUrl;
    mainImages.push(file);
  }
});

// === Second Image ===
document.getElementById("secondImageInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const isDuplicate = secondImages.some(f => f.name === file.name && f.size === file.size);
    if (isDuplicate) {
      alert(`"${file.name}" is already uploaded.`);
      return;
    }
    const imageUrl = URL.createObjectURL(file);
    document.getElementById("secondImagePreview").src = imageUrl;
    secondImages.push(file);
  }
});

// === All Colors Single Image ===
document.getElementById("allColorsImageInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const isDuplicate = allColorsSingleImages.some(f => f.name === file.name && f.size === file.size);
    if (isDuplicate) {
      alert(`"${file.name}" is already uploaded.`);
      return;
    }
    const imageUrl = URL.createObjectURL(file);
    document.getElementById("allColorsImagePreview").src = imageUrl;
    allColorsSingleImages.push(file);
  }
});

// === Multiple product color images ===
let allColorsMultipleImages = [];

const imageInput = document.getElementById('imageUploadInput');
const imageContainer = document.getElementById('uploadedImagesContainer');

imageInput.addEventListener('change', function (event) {
  const files = Array.from(event.target.files);

  files.forEach(file => {
    if (!file.type.startsWith('image/')) return;

    // Check for duplicate by name + size
    const isDuplicate = allColorsMultipleImages.some(
      existingFile => existingFile.name === file.name && existingFile.size === file.size
    );

    if (isDuplicate) {
      alert(`"${file.name}" is already uploaded.`);
      return; // Skip this file
    }

    // Store file
    allColorsMultipleImages.push(file);

    // Create preview
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    imageContainer.appendChild(img);
  });

  // No reset → so duplicate check works next time
});


// === Dupatta Side Custom Dropdown ===
document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".dropdown-wrapper");
    const selectedValue = dropdown.querySelector(".selected-value-color");
    const hiddenInput = document.getElementById("dupatta_side");
    const options = dropdown.querySelectorAll(".dropdown-options div");

    // Toggle dropdown
    dropdown.querySelector(".custom-dropdown").addEventListener("click", function () {
        dropdown.classList.toggle("active");
    });

    // Handle option click
    options.forEach(option => {
        option.addEventListener("click", function () {
            selectedValue.textContent = this.textContent;
            hiddenInput.value = this.getAttribute("data-value");
            dropdown.classList.remove("active");
        });
    });

    // Close if clicking outside
    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove("active");
        }
    });
});



// === Form Submission ===
document.querySelector('.submit-add-products-btn').addEventListener('click', function () {
  const submitButton = document.querySelector('.submit-add-products-btn');
  let btnText = submitButton.querySelector('.btn-text');
  let btnSpinner = submitButton.querySelector('.btn-spinner');

  // Show spinner and update text
  btnText.textContent = "Submitting";
  btnSpinner.style.display = 'inline-block';

  const formData = new FormData();

  // Text inputs
  formData.append('product_name', document.getElementById('product-name').value);
  formData.append('product_id', document.getElementById('product-id').value);
  formData.append('fabric', document.getElementById('product-fabric').value);
  formData.append('sizes', document.getElementById('product-sizes').value);
  formData.append('dupatta_side', document.getElementById('dupatta_side').value);
  formData.append('selling_price', document.getElementById('selling-price').value);

  // Single images
  if (mainImages[0]) formData.append('main_image', mainImages[0]);
  if (secondImages[0]) formData.append('second_image', secondImages[0]);
  if (allColorsSingleImages[0]) formData.append('all_colors_single', allColorsSingleImages[0]);

  // Multiple color images
  allColorsMultipleImages.forEach((file, index) => {
    formData.append('color_images[]', file);
  });

  fetch('/add-products-2/', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {

      if (data.uploaded_urls === 'uploaded') {
        alert('Product added successfully!');
        document.getElementById("mainImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
        document.getElementById("secondImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
        document.getElementById('allColorsImagePreview').src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    
        document.getElementById('uploadedImagesContainer').innerHTML = '';

        document.getElementById("mainImageInput").value = '';
        document.getElementById("secondImageInput").value = '';
        document.getElementById("allColorsImageInput").value = '';
        document.getElementById("imageUploadInput").value = '';

        document.getElementById('product-name').value = '';
        document.getElementById('product-id').value = '';
        document.getElementById('product-fabric').value = '';
        document.getElementById('product-sizes').value = '';
        document.getElementById('dupatta_side').value = '';
        document.getElementById('selling-price').value = '';

        mainImages = [];
        secondImages = [];
        allColorsSingleImages = [];
        allColorsMultipleImages = [];
      }
    })
    .catch(err => {
      console.error("Upload failed:", err);
    })
    .finally(() => {
      // Reset button state
      btnText.textContent = "Submit Form";
      btnSpinner.style.display = 'none';
    });
});



  /*--------------------------------------------------------------
  # Form Validation and Submission
  --------------------------------------------------------------*/

//   productForm1 = document.querySelector('.product-form-model');
//   productForm2 = document.querySelector('.product-form-nomodel');

//   const submitBtn1 = productForm1.querySelector('.submit-add-products-btn');
//   submitBtn1.addEventListener("click", handleSubmitBtn);

//   const submitBtn2 = productForm2.querySelector('.submit-add-products-btn');
//   submitBtn2.addEventListener("click", handleSubmitBtn);

//   async function handleSubmitBtn() {
//     let productForm = null;
//     let submitButton = null;
    // let btnText = null;
    // let btnSpinner = null;
  
//     if (currentMode === "model") {
//       productForm = document.querySelector('.product-form-model');
//     } else if (currentMode === "nomodel") {
//       productForm = document.querySelector('.product-form-nomodel');
//     }
  
//     if (productForm) {
//       submitButton = productForm.querySelector('.submit-add-products-btn');
    //   btnText = submitButton.querySelector('.btn-text');
    //   btnSpinner = submitButton.querySelector('.btn-spinner');
//     }
  
//     if (!submitButton) return;
    
//     const idsArray = Array.from(scannedIds);
//     productData.qrcode_ids = [...idsArray];
  
    // btnText.textContent = "Submitting";
    // btnSpinner.style.display = 'inline-block';
  
//     try {
  
//       if (productData.qrcode_ids.length === 0) {
//         const randomId = Math.floor(10000 + Math.random() * 90000).toString();
//         productData.qrcode_ids.push(randomId);
//       }

//       const formData = new FormData();
//       formData.append('document', JSON.stringify(productData));
//       formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
  
//       // 🖼️ Add images
//       if (currentMode === "model") {
//         productGarmentImages.forEach((file, index) => {
//           formData.append(`garment_${index}`, file);
//         });
  
//         productResultImages.forEach((item, index) => {
//           if (item instanceof File) {
//             formData.append(`result_file_${index}`, item);
//           } else if (typeof item === 'string') {
//             formData.append(`result_url_${index}`, item);
//           }
//         });
  
//       } else if (currentMode === "nomodel") {
//         if (secondImages.length > 0) {
//           secondImages.forEach((file, index) => {
//             formData.append(`garment_${index}`, file);
//           });
//         }
  
//         if (mainImages.length > 0) {
//           mainImages.forEach((item, index) => {
//             formData.append(`result_file_${index}`, item);
//           });
//         }
//       }
  
    //   const response = await fetch('/add-products/', {
    //     method: 'POST',
    //     body: formData
    //   });
  
    //   const contentType = response.headers.get("content-type");
    //   if (contentType && contentType.includes("application/json")) {
    //     const result = await response.json();
  
    //     if (result.uploaded_urls === 'uploaded') {
    //       alert('Product added successfully!');
//           localStorage.setItem('lastSubmittedData', JSON.stringify(productData));
  
//           const suffix = currentMode === 'model' ? '' : '-2';
//           document.getElementById(`brand-name${suffix}`).value = '';
//           document.getElementById(`product-name${suffix}`).value = '';
//           document.getElementById(`product-fabric${suffix}`).value = '';
//           document.getElementById(`product-color${suffix}`).value = '';
//           document.getElementById(`product-quantity${suffix}`).value = '';
//           document.getElementById(`product-price${suffix}`).value = '';
//           document.getElementById(`selling-price${suffix}`).value = '';
//           document.getElementById(`scanned-items${suffix}`).innerHTML = '';
  
//           document.querySelectorAll('input[name="size"]:checked').forEach(c => c.checked = false);
//           showResultImages = []; showGarmentImages = [];
//           showMainImages = []; showSecondImages = [];
//           scannedIds.clear();
  
//           previewImage.src = 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png';
  
//           productData = {
//             qrcode_ids: [],
//             brand_name: '',
//             product_name: '',
//             product_fabric: '',
//             product_sizes: [],
//             product_quantity: 0,
//             product_price: 0,
//             product_selling_price: 0,
//             product_colors: []
//           };
  
//           if (currentMode === "model") {
//             document.getElementById('resultImage').src = '';
//             document.getElementById('resultImage').style.display = 'none';
//             document.querySelector('.selected-value-color').textContent = 'Select Color';
//             document.getElementById('manual-color-input').value = '';
//             document.getElementById('product-color').value = '';
//             document.querySelector('label[for="model-image-upload"]').style.display = 'none';
//           } else {
//             document.querySelector('.selected-value-color').textContent = 'Select Color';
//             document.getElementById('manual-color-input-2').value = '';
//             document.getElementById('product-color-2').value = '';
//           }
  
//           resetCategorySections.forEach(reset => reset());
//           updateVariantsTable();
//         } else {
//           alert('Error: ' + (result.error || 'Something went wrong.'));
//         }
//       } else {
//         const text = await response.text();
//         console.error("❌ Not JSON. Response was:", text);
//         alert("Server returned an unexpected response.");
//       }
//     } catch (error) {
//       console.error('Submission error:', error);
//       alert('Encryption or network/server error occurred.');
    // } finally {
    //   btnText.textContent = "Submit Form";
    //   btnSpinner.style.display = 'none';
    // }
//   }
