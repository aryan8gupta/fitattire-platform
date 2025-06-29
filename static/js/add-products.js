/*--------------------------------------------------------------
# Script-1
--------------------------------------------------------------*/

const data = {
  "Men": {
    "T-Shirts": {
      "Half Sleeve T-Shirts": ["Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts", "Sweatshirts"],
      "Full Sleeve T-Shirts": ["Striped T-Shirts", "Plain T-Shirts", "Graphic T-Shirts"]
    },
    "Shirts": ["Formal Shirts", "Casual Shirts", "Denim Shirts", "Printed Shirts"],
    "Jeans": ["Slim Fit Jeans", "Regular Fit Jeans", "Tapered Jeans"],
    "Lowers": ["Track Pants", "Joggers", "Pyjamas"],
    "Jackets": ["Bomber Jackets", "Denim Jackets", "Leather Jackets"],
    "Hoodies": ["Zip-up Hoodies", "Pullover Hoodies"],
    "Suits": ["Business Suits", "Wedding Suits"],
    "Sweater": ["Crew Neck Sweater", "V-Neck Sweater"],
    "Shorts": ["Casual Shorts", "Sports Shorts"],
    "Tank Top": ["Gym Tank Tops", "Casual Tank Tops"]
  },
  "Women": {
    "Kurtis": ["Anarkali Kurtis", "Straight Kurtis", "A-line Kurtis"],
    "Suits": ["Salwar Suits", "Anarkali Suits", "Straight Suits", "A-line Suits", "Churidar Suits"],
    "Tops": ["Crop Tops", "Blouse Tops", "Off-Shoulder Tops"],
    "Dresses": ["Maxi Dresses", "Bodycon Dresses", "A-Line Dresses"],
    "Shirts": ["Over Sized T-shirts"],
    "T-Shirts": {
      "Half Sleeve T-Shirts": ["Over Sized T-shirts", "Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts", "Sweatshirts"],
      "Full Sleeve T-Shirts": ["Striped T-Shirts", "Plain T-Shirts", "Graphic T-Shirts"]
    },
    "Jeans": ["Skinny Jeans", "Boyfriend Jeans", "High-waist Jeans"],
    "Skirts": ["Mini Skirts", "Pencil Skirts"],
    "Jackets": ["Denim Jackets", "Blazers"],
    "Sweaters": ["Pullover Sweaters", "Cardigans"]
  }
};


// Image file mapping (real filenames)
// const images = {};
// const azureBaseUrl = "https://fitattirestorage.blob.core.windows.net/fitattire-assets"
// Object.keys(data).forEach(gender => {
//   Object.keys(data[gender]).forEach(category => {
//     const sub = data[gender][category];
//     if (typeof sub === 'object' && !Array.isArray(sub)) {
//       // sub is an object (example: T-Shirts have Half Sleeve, Full Sleeve)
//       Object.keys(sub).forEach(subCategory => {
//         const finalSub = sub[subCategory];
//         if (Array.isArray(finalSub)) {
//           finalSub.forEach(final => {
//           images[final] = Array.from({ length: 5 }, (_, i) => 
//             `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${subCategory.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
//           });
//         }
//       });
//     } else if (Array.isArray(sub)){
//       sub.forEach(final => {
//         images[final] = Array.from({ length: 5 }, (_, i) => 
//           `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
//       });
//     }
//   });
// });


const images = {};
const azureBaseUrl = "https://fitattirestorage.blob.core.windows.net/fitattire-assets";

Object.keys(data).forEach(gender => {
  Object.keys(data[gender]).forEach(category => {
    const sub = data[gender][category];
    if (typeof sub === 'object' && !Array.isArray(sub)) {
      Object.keys(sub).forEach(subCategory => {
        const finalSub = sub[subCategory];
        if (Array.isArray(finalSub)) {
          finalSub.forEach(final => {
            const key = `${gender}:${final}`;  // Unique key to avoid collision
            images[key] = Array.from({ length: 5 }, (_, i) => 
              `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${subCategory.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`
            );
          });
        }
      });
    } else if (Array.isArray(sub)){
      sub.forEach(final => {
        const key = `${gender}:${final}`;
        images[key] = Array.from({ length: 5 }, (_, i) => 
          `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`
        );
      });
    }
  });
});


const categoryGrid = document.querySelector('.category-grid');
const subCategoryGrid = document.querySelector('.sub-category-grid');
const finalCategoryGrid = document.querySelector('.final-category-grid');
const finalSubCategoryGrid = document.querySelector('.final-sub-category-grid');
const imagesSection = document.querySelector('.images-section');
const heading = document.getElementById('image-section-heading');
const detailBox = document.getElementById("result-image-box");
const spinner = document.querySelector('.spinner');

// Selections
let selectedGender = "";
let selectedCategory = "";
let selectedSubCategory = "";
let selectedFinalCategory = "";
let selectedImagePath = "";
let productGarmentImages = []; 
let productResultImages = []; 

let showGarmentImages = [];
let showResultImages = [];

let documentData = {
  gender: null,
  category: null,
  subCategory: null,
  finalCategory: null,
  modelImagePath: null,
  swapCategory: null
};
let idsArray = [];

const clothes_swap_category = document.getElementById("swap_category").value;


function clearGrid(grid) {
  grid.innerHTML = '';
}


// Attach Click Listener to whole category grid
categoryGrid.addEventListener('click', function (e) {
  const target = e.target.closest('[data-gender]');
  if (!target) return;

  const gender = target.dataset.gender;
  showSubCategories(gender);

  // Optional: Active class handling
  Array.from(categoryGrid.children).forEach(item => item.classList.remove('active'));
  target.classList.add('active');
});
document.querySelectorAll('.category-item').forEach(item => {
  item.addEventListener('click', function () {
    selectedGender = this.dataset.gender;
    console.log("Selected gender:", selectedGender);
  });
});

function createCategoryItem(name, icon = 'fas fa-tshirt') {
  const div = document.createElement('div');
  div.className = 'category-item';
  div.innerHTML = `<i class="${icon}"></i><span>${name}</span>`;
  div.addEventListener('click', () => {
    // Active class handling
    const siblings = div.parentElement.querySelectorAll('.category-item');
    siblings.forEach(sib => sib.classList.remove('active'));
    div.classList.add('active');
  });
  return div;
}

function showSubCategories(gender) {
  if (gender == "None") {
    clearGrid(subCategoryGrid);
    clearGrid(finalCategoryGrid);
    clearGrid(finalSubCategoryGrid);
    clearGrid(imagesSection);
    heading.style.display = 'none';
    detailBox.style.display = "none";
  } else {
    clearGrid(subCategoryGrid);
    clearGrid(finalCategoryGrid);
    clearGrid(finalSubCategoryGrid);
    clearGrid(imagesSection);
    heading.style.display = 'none';
    detailBox.style.display = "none";

    const categories = Object.keys(data[gender]);
    categories.forEach(cat => {
      const item = createCategoryItem(cat);
      item.addEventListener('click', function (e) { 
        showFinalCategories(gender, cat);
        selectedCategory = cat;
      });
      subCategoryGrid.appendChild(item);
    });
  }
}


function showFinalCategories(gender, category) {
  clearGrid(finalCategoryGrid);
  clearGrid(finalSubCategoryGrid);
  clearGrid(imagesSection);
  heading.style.display = 'none';
  detailBox.style.display = "none";

  const sub = data[gender][category];
  if (Array.isArray(sub)) {
    sub.forEach(subCat => {
      const item = createCategoryItem(subCat);
      item.addEventListener('click', function (e) {  
        showImages(gender, subCat);
        selectedSubCategory = subCat;
      });
      finalCategoryGrid.appendChild(item);
    });
  } else if (typeof sub === 'object') {
    const subCategories = Object.keys(sub);
    subCategories.forEach(subCat => {
      const item = createCategoryItem(subCat);
      item.addEventListener('click', function (e) { 
        showFinalSubCategories(gender, category, subCat);
        selectedSubCategory = subCat;
      });
      finalCategoryGrid.appendChild(item);
    });
  }
}

function showFinalSubCategories(gender, category, subCat) {
  clearGrid(finalSubCategoryGrid);
  clearGrid(imagesSection);
  heading.style.display = 'none';
  detailBox.style.display = "none";

  const sub = data[gender][category][subCat];
  if (Array.isArray(sub)) {
    sub.forEach(final => {
      const item = createCategoryItem(final);
      item.addEventListener('click', function (e) { 
        showImages(gender, final);
        selectedFinalCategory = final;
      });
      finalSubCategoryGrid.appendChild(item);
    });
  }
}

// function showImages(final) {
//   clearGrid(imagesSection);
  
//   // Show Heading
//   heading.style.display = 'block';
//   heading.textContent = `Choose Models`;

//   spinner.style.display = 'block';
//   setTimeout(() => {
//     spinner.style.display = 'none';
//     images[final].forEach(src => {
//       const img = document.createElement('img');
//       img.src = src;
//       img.alt = final;
//       img.loading = "lazy";
//       img.style.width = "200px";
//       img.style.height = "250px";
//       img.style.objectFit = "contain";
//       img.style.margin = "10px";
//       img.className = 'image-item'; // <-- add class

//       img.addEventListener('click', function() {
//         // Remove active from all images
//         document.querySelectorAll('.images-section img').forEach(i => i.classList.remove('active'));
//         // Add active to clicked image
//         this.classList.add('active');

//         detailBox.style.display = "block";
//         detailBox.style.margin = "10px";

//         selectedImagePath = this.src;
//         console.log("Selected image path:", selectedImagePath);
//       });
//       imagesSection.appendChild(img);
//     });
//   }, 500);
// }

function showImages(gender, final) {
  clearGrid(imagesSection);
  
  heading.style.display = 'block';
  heading.textContent = `Choose Models`;

  spinner.style.display = 'block';
  setTimeout(() => {
    spinner.style.display = 'none';

    const key = `${gender}:${final}`;
    const imageList = images[key];

    if (!imageList) {
      console.warn(`No images found for key: ${key}`);
      return;
    }

    imageList.forEach(src => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = final;
      img.loading = "lazy";
      img.style.width = "200px";
      img.style.height = "250px";
      img.style.objectFit = "contain";
      img.style.margin = "10px";
      img.className = 'image-item';

      img.addEventListener('click', function() {
        document.querySelectorAll('.images-section img').forEach(i => i.classList.remove('active'));
        this.classList.add('active');

        detailBox.style.display = "block";
        detailBox.style.margin = "10px";

        selectedImagePath = this.src;
        console.log("Selected image path:", selectedImagePath);
      });

      imagesSection.appendChild(img);
    });
  }, 500);
}


async function uploadImages() {
  const modelImage = selectedImagePath;
  const uploadFile = document.getElementById("product-image-upload").files[0];
  // const cameraFile = document.getElementById("product-image-camera").files[0];
  // const garmentImage = uploadFile || cameraFile;
  const garmentImage = uploadFile;

  const credits = document.getElementById("credits-used").innerText;

  if (credits == "0"){
    alert("No Credits Left");
    return;
  }

  if (!modelImage || !garmentImage) {
    alert("Please select both images.");
    return;
  }  
  
  const spinner2 = document.getElementById("spinner2");

  spinner2.style.display = 'block';

  const formData = new FormData();
  formData.append("category", clothes_swap_category);
  formData.append("garment_image", garmentImage);
  formData.append("model_image_url", modelImage);

  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });   

    const result = await response.json();
    console.log(result)

    if (result && result.upscaled_path) {
      document.getElementById("result-heading").style.display="block";
      const imageElement = document.getElementById('resultImage');
      imageElement.src = result.upscaled_path;
      imageElement.style.display = 'block';

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

      // Set hidden input with actual URL
      spinner2.style.display = 'none';
      document.getElementById('resultImageURL').value = result.upscaled_path;

    } else {
      document.getElementById('response').innerText = result.error || 'Error processing image.';
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById('response').innerText = "Error occurred while processing.";
  }
}

const resultImageInput = document.getElementById('product-result-image-upload');
const resultImage1 = document.getElementById('resultImage');
const resultHeading = document.getElementById('result-heading');

resultImageInput.addEventListener('change', function () {
  const file = resultImageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      resultImage1.src = e.target.result;
      resultImage1.style.display = 'block';
      resultHeading.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
});




/*--------------------------------------------------------------
# Script-2 
--------------------------------------------------------------*/

// Add Products Page JavaScript
// document.addEventListener('DOMContentLoaded', function() {
  // Image Upload Preview
  const previewImage = document.getElementById('preview-image');
  // const inputCamera = document.getElementById('product-image-camera');
  const inputUpload = document.getElementById('product-image-upload');
  
  function handleImageChange2(input) {
    input.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
          const formData = new FormData();
          formData.append("garment_image", file);

          // 👀 Preview original image immediately (optional)
          const reader = new FileReader();
          reader.onload = function () {
            previewImage.src = reader.result; // show raw image for now
          };
          reader.readAsDataURL(file);

          // 📤 Upload to Django for processing
          fetch("/get-garment/", {
            method: "POST",
            body: formData
          })
          .then(res => res.json())
          .then(data => {
            console.log(data);
            if (!data.error) {
              alert("✅ Product processed");

              // ✅ Show final processed image from backend
              previewImage.src = data.image_url || data.image_base64;

            } else {
              alert(data.error || "❌ Processing failed");
            }
          })
          .catch(err => {
            console.error("Error:", err);
            alert("❌ Server error");
          });
        }
    });
  }
  function handleImageChange1(input) {
    input.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function () {
                previewImage.src = reader.result;
            };
            reader.readAsDataURL(file);
        }
    });
  }

  // if (inputCamera) handleImageChange2(inputCamera);
  if (inputUpload) handleImageChange1(inputUpload);

  
  // Category Selection
  const categoryItems = document.querySelectorAll('.category-item');
  
  categoryItems.forEach(item => {
      item.addEventListener('click', function() {
          // Remove active class from all categories
          categoryItems.forEach(cat => cat.classList.remove('active'));
          
          // Add active class to clicked category
          this.classList.add('active');
          
          // In a real app, this would update the subcategories based on the selected category
          // For now, we'll just log the selected category
          const categoryName = this.querySelector('span').textContent;
          console.log('Selected category:', categoryName);
      });
  });
  
  // Subcategory Selection
  const subcategoryItems = document.querySelectorAll('.subcategory-item');
  
  subcategoryItems.forEach(item => {
      item.addEventListener('click', function() {
          // Remove active class from all subcategories
          subcategoryItems.forEach(subcat => subcat.classList.remove('active'));
          
          // Add active class to clicked subcategory
          this.classList.add('active');
          
          // In a real app, this would update the form based on the selected subcategory
          // For now, we'll just log the selected subcategory
          const subcategoryName = this.querySelector('span').textContent;
          console.log('Selected subcategory:', subcategoryName);
      });
  });


  /*--------------------------------------------------------------
  # Select Category Section
  --------------------------------------------------------------*/
  const select = document.getElementById("fake-select");
  const options = document.getElementById("custom-options");
  const hiddenInput = document.getElementById("swap_category");
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
  # Select Color Section
  --------------------------------------------------------------*/
  const dropdown = document.getElementById("color-select");
  const optionsContainer = dropdown.nextElementSibling;
  const hiddenInput1 = document.getElementById("product-color");
  const selectedValue1 = dropdown.querySelector(".selected-value-color");

  dropdown.addEventListener("click", () => {
    dropdown.classList.toggle("open");
  });

  optionsContainer.querySelectorAll("div").forEach(option => {
    option.addEventListener("click", (e) => {
      const value = e.target.getAttribute("data-value");
      const text = e.target.textContent;
      selectedValue1.textContent = text;
      hiddenInput1.value = value;
      dropdown.classList.remove("open");
    });
  });

  // Close dropdown if clicked outside
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target) && !optionsContainer.contains(e.target)) {
      dropdown.classList.remove("open");
    }
  });
  function getSelectedColor() {
    const manualColor = document.getElementById("manual-color-input").value.trim();
    const dropdownColor = document.getElementById("product-color").value.trim();

    // Priority: manual color
    if (manualColor !== "") {
      return manualColor;
    }
    return dropdownColor;
  }


  /*--------------------------------------------------------------
  # Handle Variant Button Section
  --------------------------------------------------------------*/

  const btn5 = document.getElementById("submit-variant-btn");
  btn5.addEventListener("click", handleSubmitVariant);

  let productData = {
    qrcode_ids: [],
    brand_name: '',
    product_name: '',
    product_fabric: '',
    product_sizes: [],
    product_quantity: 0,
    product_price: 0,
    product_selling_price: 0,
    product_colors: []
  };

  function handleSubmitVariant() {
    // Then call backend to decrease credits
    // fetch('/api/decrease-credits/', {
    //   method: 'POST',
    // })
    // .then(res => res.json())
    // .then(data => {
    //   if (data.success) {
    //     document.getElementById("credits-used").innerText = data.new_credits;
    //   } else {
    //     alert("Error: " + data.message);
    //   }
    // })
    // .catch(err => console.error("Failed to decrease credits:", err));

    console.log("Add Variant Function Started")
    // If brand etc not set, read them once
    if (!productData.brand_name) {
      productData.brand_name = document.getElementById('brand-name').value;
      productData.product_name = document.getElementById('product-name').value;
      productData.product_fabric = document.getElementById('product-fabric').value;
      productData.product_quantity = document.getElementById('product-quantity').value;
      productData.product_price = document.getElementById('product-price').value;
      productData.product_selling_price = document.getElementById('selling-price').value;
      productData.product_sizes = Array.from(document.querySelectorAll('input[name="size"]:checked')).map(cb => cb.value);

      if (!productData.brand_name || !productData.product_name || !productData.product_fabric || !productData.product_quantity || !productData.product_price || !productData.product_selling_price || productData.product_sizes.length === 0) {
        alert("Please fill all the main product fields before adding variants.");
        return;
      }
    }
    const resultImage = document.getElementById('resultImage').src;
    const urlInput = document.getElementById('resultImageURL').value;
    const uploadResultImage = document.getElementById('product-result-image-upload').files[0];
    const productColor = getSelectedColor();
    const uploadFile = document.getElementById("product-image-upload").files[0];

    // const cameraFile = document.getElementById("product-image-camera").files[0];
    // const garmentImages2 = uploadFile || cameraFile;

    const garmentImages2 = uploadFile;
    const productResult = urlInput || uploadResultImage;

    // Validate images and color inputs for the variant
    if (!garmentImages2 || !productResult || resultImage === "about:blank" || !productColor) {
      alert("Please upload garment image, generate result image and select a color.");
      return;
    }

    console.log(productResult)
    // Append variant data to arrays

    productData.product_colors.push(productColor);
    
    // To show Images in Result Table Starts  ----------------------------------------->
    if (productResult && typeof productResult === 'string' && 
      (productResult.startsWith('http') || productResult.startsWith('/'))) {

      // It's likely a URL (absolute or relative)
      console.log('resultImage is a URL:');
      showResultImages.push(productResult);

    } else if (productResult instanceof File) {
      // Not a valid URL or empty
      console.log('resultImage is not a URL or is empty:');
      const resultImageURL = URL.createObjectURL(productResult);
      showResultImages.push(resultImageURL);
    }

    const garmentImageURL = URL.createObjectURL(garmentImages2);
    showGarmentImages.push(garmentImageURL)

    // To show Images in Result Table Ends  ----------------------------------------->


    productGarmentImages.push(garmentImages2);

    productResultImages.push(productResult);

    console.log(showResultImages);
    console.log("10000");

    console.log(productGarmentImages)
    console.log(productResultImages)

    documentData = {
      gender: selectedGender,
      category: selectedCategory,
      subCategory: selectedSubCategory,
      finalCategory: selectedFinalCategory,
      modelImagePath: selectedImagePath,
      swapCategory: clothes_swap_category
    };
    console.log("documentData:", documentData)
    

    console.log("Current productData:", productData);
    console.log("Current documentData:", documentData);

    // Update the table with the new variant added
    updateVariantsTable();

    // Reset variant-specific fields (images, color)
    resetVariantFields();
  }


  function resetVariantFields() {
    document.getElementById('preview-image').src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    document.getElementById('resultImage').src = "";
    document.getElementById('resultImage').style.display = "none";
    document.getElementById('product-color').value = "";
    document.querySelector('.selected-value-color').textContent = "Select Color";

    // Reset file inputs
    document.getElementById('manual-color-input').value = "";
    // document.getElementById('product-image-camera').value = "";
    document.getElementById('product-image-upload').value = "";
    document.getElementById('product-result-image-upload').value = "";
    document.getElementById('resultImageURL').value = "";
    selectedImagePath = "";
  }

  function updateVariantsTable() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = ""; // clear existing rows

    for (let i = 0; i < productData.product_colors.length; i++) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${i + 1}</td>
        <td><img src="${showResultImages[i]}" alt="Result Image" width="60" height="95"></td>
        <td><img src="${showGarmentImages[i]}" alt="Garment Image" width="60" height="90"></td>
        <td>${productData.product_colors[i]}</td>
        <td style="padding: 0;">
          <div style="display: flex; justify-content: center; align-items: center; height: 100%; width: 100%; padding: 10px;">
            <svg class="delete-icon" viewBox="0 0 24 24" data-index="${i}" style="cursor: pointer; width: 24px; height: 24px;">
              <path d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-4.5l-1-1z"/>
            </svg>
          </div>
        </td>
      `;
      tableBody.appendChild(row);
    }
    // Attach event listeners to all delete icons
    const deleteIcons = document.querySelectorAll(".delete-icon");
    deleteIcons.forEach(icon => {
      icon.addEventListener("click", (event) => {
        const index = parseInt(event.currentTarget.getAttribute("data-index"));
        deleteVariant(index);
      });
    });
  }

  function deleteVariant(index) {
    productData.product_colors.splice(index, 1);

    showResultImages.splice(index, 1);
    showGarmentImages.splice(index, 1);

    productResultImages.splice(index, 1);
    productGarmentImages.splice(index, 1);
  
    updateVariantsTable(); // Re-render the table
  }
  

  /*--------------------------------------------------------------
  # Multiple QR Code Scanner Section
  --------------------------------------------------------------*/
  const scanBtn = document.getElementById("scan-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const readerDiv = document.getElementById("reader");
  const scannedItemsDiv = document.getElementById("scanned-items");
  const html5QrCode = new Html5Qrcode("reader");

  let isScanning = false;
  const scannedIds = new Set(); // to avoid duplicates

  scanBtn.addEventListener("click", async () => {
    scanBtn.style.display = "none";
    cancelBtn.style.display = "block";
    readerDiv.style.display = "block";

    try {
      const devices = await Html5Qrcode.getCameras();
      if (devices.length === 0) {
        alert("No cameras found.");
        return;
      }

      let cameraId = devices[0].id;
      for (let device of devices) {
        if (/back|rear/i.test(device.label)) {
            cameraId = device.id;
            break;
        }
      }

      await html5QrCode.start(
        cameraId,
        { fps: 10, qrbox: { width: 250, height: 250 } },
        (decodedText) => {

          const shortId = decodedText.slice(-10); // ✅ get last 10 characters
          if (!scannedIds.has(shortId)) {
            scannedIds.add(shortId);
            const div = document.createElement("div");
            div.className = "scanned-item";
            div.innerText = shortId; // ✅ show only shortId
            scannedItemsDiv.appendChild(div);
          }
          
          // Optional: Send to backend
          // fetch("/save-qrcode", {
          //   method: "POST",
          //   headers: { "Content-Type": "application/json" },
          //   body: JSON.stringify({ qr_id: decodedText })
          // });
        }
      );

      isScanning = true;

    } catch (err) {
      alert("Error accessing the camera. Please allow permission.");
      console.error(err);
      cancelBtn.style.display = "none";
      scanBtn.style.display = "block";
    }
  });

  cancelBtn.addEventListener("click", () => {
      if (isScanning) {
          html5QrCode.stop().then(() => {
              isScanning = false;
              cancelBtn.style.display = "none";
              readerDiv.style.display = "none";
              scanBtn.style.display = "block";
          });
      }
  });

  /*--------------------------------------------------------------
  # Load Previous Data
  --------------------------------------------------------------*/
  const loadPreviousButton = document.getElementById('load-previous-btn');

  if (loadPreviousButton) {
    loadPreviousButton.addEventListener('click', function () {
      const savedData = localStorage.getItem('lastSubmittedData');
      if (!savedData) {
        alert("No previous data found.");
        return;
      }

      const parsedData = JSON.parse(savedData);
      productData = { ...parsedData }; // restore into productData

      // Fill form fields
      document.getElementById('brand-name').value = parsedData.brand_name || '';
      document.getElementById('product-name').value = parsedData.product_name || '';
      document.getElementById('product-fabric').value = parsedData.product_fabric || '';
      document.getElementById('product-quantity').value = parsedData.product_quantity || 0;
      document.getElementById('product-price').value = parsedData.product_price || 0;
      document.getElementById('selling-price').value = parsedData.product_selling_price || 0;

      // Set sizes checkboxes
      document.querySelectorAll('input[name="size"]').forEach(checkbox => {
        checkbox.checked = parsedData.product_sizes?.includes(checkbox.value) || false;
      });

      alert("Previous data loaded!");
    });
  }



  /*--------------------------------------------------------------
  # Form Validation and Submission
  --------------------------------------------------------------*/
  const productForm = document.querySelector('.product-form');
  const submitButton = productForm ? productForm.querySelector('.submit-add-products-btn') : null;
  const btnText = submitButton.querySelector('.btn-text');
  const btnSpinner = submitButton.querySelector('.btn-spinner');

  if (submitButton) {
    submitButton.addEventListener('click', async function(e) {
        e.preventDefault();
        const idsArray = Array.from(scannedIds); // ✅ move it here
        productData.qrcode_ids = [...idsArray];

        btnText.textContent = "Submitting";
        btnSpinner.style.display = 'inline-block';


        const formData = new FormData();
        formData.append('document', JSON.stringify(productData));
        formData.append('selectedmiddlebuttons', JSON.stringify(documentData));
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

        // ✅ Garment images - always files
        productGarmentImages.forEach((file, index) => {
          formData.append(`garment_${index}`, file);
        });

        // ✅ Result images - could be file or URL
        productResultImages.forEach((item, index) => {
          if (item instanceof File) {
            formData.append(`result_file_${index}`, item); // File
          } else if (typeof item === 'string') {
            formData.append(`result_url_${index}`, item); // URL
          }
        });

        try {
          const response = await fetch('/add-products/', {
              method: 'POST',
              body: formData
          });
  
          const contentType = response.headers.get("content-type");

          if (contentType && contentType.includes("application/json")) {
            const result = await response.json();
            console.log(result);
  
            if (result.uploaded_urls === 'uploaded') {
              alert('Product added successfully!');

              // Save submitted data to localStorage
              localStorage.setItem('lastSubmittedData', JSON.stringify(productData));

              // Reset form
              document.getElementById('brand-name').value = '';
              document.getElementById('product-name').value = '';
              document.getElementById('product-fabric').value = '';
              document.getElementById('product-color').value = '';
              document.getElementById('product-quantity').value = '';
              document.getElementById('product-price').value = '';
              document.getElementById('selling-price').value = '';
              document.getElementById("scanned-items").innerHTML = '';
              
              document.querySelectorAll('input[name="size"]:checked').forEach(checkbox => {
                  checkbox.checked = false;
              });
              scannedIds.clear();
              
              // Reset image preview
              previewImage.src = 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png';

              // Reset other fields
              productData = {
                qrcode_ids: [],
                brand_name: '',
                product_name: '',
                product_fabric: '',
                product_sizes: [],
                product_quantity: 0,
                product_price: 0,
                product_selling_price: 0,
                product_colors: []
              };
              
              document.getElementById('resultImage').src = '';
              document.getElementById('resultImage').style.display = 'none';
              document.querySelector('.selected-value-color').textContent = 'Select Color';
              document.getElementById('manual-color-input').value = '';
              document.getElementById('product-color').value = '';

              showSubCategories("None");
              
              updateVariantsTable();
            } else {
              alert('Error: ' + (result.error || 'Something went wrong.'));
            }

          } else {
            const text = await response.text();
            console.error("❌ Not JSON. Response was:", text);
            alert("Server returned an unexpected response.");
          }

        } catch (error) {
            console.error('Submission error:', error);
            alert('Network or server error occurred.');

        } finally {
          btnText.textContent = "Submit Form";
          btnSpinner.style.display = 'none';
        }

    });
  }
// });
