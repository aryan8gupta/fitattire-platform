/*--------------------------------------------------------------
# Script-1
--------------------------------------------------------------*/


// === CATEGORY & IMAGE DATA ===

const data = {
  "Men": {
    "T-Shirts": {
      "Half Sleeve T-Shirts": [
        "Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts",
        "Raglan T-Shirts", "Oversized T-Shirts", "Tank Tops", "Muscle Fit T-Shirts",
        "Printed T-Shirts", "Color Block T-Shirts", "Graphic T-Shirts", "Running T-Shirts", "Gym T-Shirts"
      ],
      "Full Sleeve T-Shirts": [
        "Plain T-Shirts", "Striped T-Shirts", "Graphic T-Shirts", "Thermal T-Shirts", "Compression T-Shirts"
      ]
    },
    "Shirts": {
      "Half Sleeve Shirts": ["Casual Shirts", "Printed Shirts"],
      "Full Sleeve Shirts": ["Formal Shirts", "Casual Shirts", "Denim Shirts", "Printed Shirts", "Checkered Shirts", "Linen Shirts"]
    },
    "Jackets": {
      "Half Jackets": ["Sleeveless Jackets", "Puffer Vests", "Half Bomber Jackets"],
      "Full Jackets": [
        "Bomber Jackets", "Denim Jackets", "Leather Jackets", "Puffer Jackets", "Windcheaters",
        "Rain Jackets", "Winter Jackets", "Varsity Jackets", "Fleece Jackets", "Motorbike Jackets"
      ]
    },
    "Sweaters": {
      "Full Sleeve Sweaters": ["Crew Neck Sweater", "V-Neck Sweater", "Turtleneck Sweater", "Zipper Sweater", "Woolen Sweater"]
    },
    "Hoodies": {
      "Zip-up Hoodies": ["Basic Zip-up Hoodie", "Graphic Zip-up Hoodie"],
      "Pullover Hoodies": ["Plain Pullover Hoodie", "Printed Pullover Hoodie"]
    },
    "Jeans": ["Slim Fit Jeans", "Regular Fit Jeans", "Tapered Jeans", "Skinny Jeans", "Ripped Jeans", "Baggy Jeans"],
    "Lowers": ["Track Pants", "Joggers", "Pyjamas", "Cargos", "Shorts", "Boxers"],
    "Shorts": ["Casual Shorts", "Sports Shorts", "Denim Shorts", "Cotton Shorts"],
    "Tank Tops": ["Gym Tank Tops", "Casual Tank Tops"],
    "Suits": ["Business Suits", "Office Wear Suits", "3-Piece Suits"],
    "Rain Wear": ["Rain Suits", "Rain Jackets", "Ponchos"],
    "Wedding Wear": ["Sherwani", "Kurta Pajama", "Kurta Pajama with Jacket", "Indo-Western", "Jodhpuri Suits", "Tuxedo", "3-Piece Wedding Suit"]
  },

  "Women": {
    "T-Shirts": {
      "Half Sleeve T-Shirts": [
        "Over Sized T-Shirts", "Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts", 
        "Raglan T-Shirts", "Crop T-Shirts", "Graphic T-Shirts", "Gym T-Shirts"
      ],
      "Full Sleeve T-Shirts": ["Striped T-Shirts", "Plain T-Shirts", "Graphic T-Shirts", "Thermal T-Shirts"]
    },
    "Shirts": {
      "Half Sleeve Shirts": ["Over Sized Shirts", "Crop Shirts"],
      "Full Sleeve Shirts": ["Formal Shirts", "Casual Shirts", "Printed Shirts", "Denim Shirts"]
    },
    "Tops": ["Crop Tops", "Blouse Tops", "Off-Shoulder Tops", "Wrap Tops", "Peplum Tops", "Halter Tops", "Tube Tops"],
    "Kurtis": ["Anarkali Kurtis", "Straight Kurtis", "A-line Kurtis", "Flared Kurtis", "Kaftan Kurtis", "Shirt Kurtis"],
    "Suits": ["Salwar Suits", "Anarkali Suits", "Straight Suits", "A-line Suits", "Churidar Suits", "Sharara Suits", "Palazzo Suits"],
    "Dresses": ["Maxi Dresses", "Bodycon Dresses", "A-Line Dresses", "Wrap Dresses", "Skater Dresses", "Slip Dresses"],
    "Sarees": ["Silk Sarees", "Cotton Sarees", "Designer Sarees", "Partywear Sarees", "Chiffon Sarees", "Georgette Sarees"],
    "Lehenga": ["Bridal Lehenga", "Designer Lehenga", "Simple Lehenga", "Sharara Lehenga"],
    "Gowns": ["Wedding Gowns", "Evening Gowns", "Party Gowns", "Anarkali Gowns"],
    "Coord Sets": ["Top & Skirt Set", "Top & Pant Set", "Crop Top & Palazzo", "Shirt & Short Set", "Kurta & Pant Coord Set"],
    "Jeans": ["Skinny Jeans", "Boyfriend Jeans", "High-waist Jeans", "Straight Fit Jeans", "Flared Jeans", "Mom Jeans"],
    "Skirts": ["Mini Skirts", "Pencil Skirts", "A-line Skirts", "Wrap Skirts", "Pleated Skirts"],
    "Jackets": {
      "Half Jackets": ["Sleeveless Jackets", "Cropped Jackets", "Denim Vests"],
      "Full Jackets": ["Denim Jackets", "Blazers", "Puffer Jackets", "Bomber Jackets", "Trench Coats", "Leather Jackets"]
    },
    "Sweaters": {
      "Full Sleeve Sweaters": ["Pullover Sweaters", "Cardigans", "Turtleneck Sweaters", "Shrugs", "Woolen Sweaters"]
    },
    "Hoodies": {
      "Zip-up Hoodies": ["Basic Zip-up Hoodie", "Graphic Zip-up Hoodie"],
      "Pullover Hoodies": ["Plain Pullover Hoodie", "Printed Pullover Hoodie"]
    },
    "Rain Wear": ["Rain Suits", "Rain Coats", "Ponchos"],
  }
};


const azureBaseUrl = "https://fitattirestorage.blob.core.windows.net/fitattire-assets";
const images = {};
Object.keys(data).forEach(gender => {
  Object.keys(data[gender]).forEach(category => {
    const sub = data[gender][category];
    if (typeof sub === 'object' && !Array.isArray(sub)) {
      Object.keys(sub).forEach(subCategory => {
        sub[subCategory].forEach(final => {
          // const key = `${gender}:${final}`;
          const key = `${gender}:${category}:${subCategory}:${final}`;
          images[key] = Array.from({ length: 5 }, (_, i) => `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${subCategory.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
        });
      });
    } else {
      sub.forEach(final => {
        // const key = `${gender}:${final}`;
        const key = `${gender}:${category}:${final}`;
        images[key] = Array.from({ length: 5 }, (_, i) => `${azureBaseUrl}/${gender.toLowerCase()}:${category.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}:${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
      });
    }
  });
});


let selectedGender = "";
let selectedCategory = "";
let selectedSubCategory = "";
let selectedFinalCategory = "";
let selectedImagePath = "";
let currentMode = "";


let mainImages = [];
let secondImages = [];

let showMainImages = [];
let showSecondImages = [];

document.getElementById("mainImageInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const imageUrl = URL.createObjectURL(file);
    document.getElementById("mainImagePreview").src = imageUrl;
    mainImages.push(file); // store image URL in array
    showMainImages.push(imageUrl)
  }
});

document.getElementById("secondImageInput").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const imageUrl = URL.createObjectURL(file);
    document.getElementById("secondImagePreview").src = imageUrl;
    secondImages.push(file); // store image URL in array
    showSecondImages.push(imageUrl)
  }
});

document.getElementById("modelConversionBtn").addEventListener("click", () => {
  currentMode = "model";
  document.getElementById("modelConversionWrapper").style.display = "block";
  document.getElementById("nomodelConversionWrapper").style.display = "none";
});

document.getElementById("noModelConversionBtn").addEventListener("click", () => {
  currentMode = "nomodel";
  document.getElementById("modelConversionWrapper").style.display = "none";
  document.getElementById("nomodelConversionWrapper").style.display = "block";
});


// === MULTI-BLOCK LOGIC ===

const resetCategorySections = []; // store reset handlers

document.querySelectorAll('.category-section').forEach(section => {
  const categoryGrid = section.querySelector('.category-grid');
  const subCategoryGrid = section.querySelector('.sub-category-grid');
  const finalCategoryGrid = section.querySelector('.final-category-grid');
  const finalSubCategoryGrid = section.querySelector('.final-sub-category-grid');
  const imagesSection = section.querySelector('.images-section');
  const heading = section.querySelector('.image-section-heading');
  const detailBox = document.getElementById("result-image-box");
  const productDetailsSection = document.getElementById("product-details");

  function clearGrid(grid) {
    if (grid) grid.innerHTML = '';
  }

  function createCategoryItem(name, icon = 'fas fa-tshirt') {
    const div = document.createElement('div');
    div.className = 'category-item';
    div.innerHTML = `<i class="${icon}"></i><span>${name}</span>`;
    return div;
  }

  function showSubCategories(gender) {
    if (gender === "None") {
      [subCategoryGrid, finalCategoryGrid, finalSubCategoryGrid, imagesSection].forEach(clearGrid);
      if (heading) heading.style.display = 'none';
      if (detailBox) detailBox.style.display = "none";
      return;
    }

    [subCategoryGrid, finalCategoryGrid, finalSubCategoryGrid, imagesSection].forEach(clearGrid);
    if (heading) heading.style.display = 'none';
    if (detailBox) detailBox.style.display = "none";

    if (!gender || !data[gender]) return;

    Object.keys(data[gender]).forEach(category => {
      const item = createCategoryItem(category);
      item.addEventListener('click', () => {
        selectedCategory = category;
        showFinalCategories(gender, category);
      });
      subCategoryGrid.appendChild(item);
    });
  }

  function showFinalCategories(gender, category) {
    [finalCategoryGrid, finalSubCategoryGrid, imagesSection].forEach(clearGrid);
    if (heading) heading.style.display = 'none';
    if (detailBox) detailBox.style.display = "none";

    const sub = data[gender][category];
    if (Array.isArray(sub)) {
      sub.forEach(subCat => {
        const item = createCategoryItem(subCat);
        item.addEventListener('click', () => {
          selectedSubCategory = subCat;
          if (currentMode === "model") {
            // showImages(gender, subCat);
            showImages(gender, category, '', subCat);

          } else {
            if (heading) heading.style.display = 'none';
            if (detailBox) detailBox.style.display = 'none';
            clearGrid(imagesSection);
            productDetailsSection.style.display = "block";
          }
        });
        finalCategoryGrid.appendChild(item);
      });
    } else {
      Object.keys(sub).forEach(subCat => {
        const item = createCategoryItem(subCat);
        item.addEventListener('click', () => {
          selectedSubCategory = subCat;
          showFinalSubCategories(gender, category, subCat);
        });
        finalCategoryGrid.appendChild(item);
      });
    }
  }

  function showFinalSubCategories(gender, category, subCat) {
    [finalSubCategoryGrid, imagesSection].forEach(clearGrid);
    if (heading) heading.style.display = 'none';
    if (detailBox) detailBox.style.display = "none";

    data[gender][category][subCat].forEach(final => {
      const item = createCategoryItem(final);
      item.addEventListener('click', () => {
        selectedFinalCategory = final;
        if (currentMode === "model") {
          // showImages(gender, final);
          showImages(gender, category, subCat, final);

        } else {
          if (heading) heading.style.display = 'none';
          if (detailBox) detailBox.style.display = 'none';
          clearGrid(imagesSection);
          productDetailsSection.style.display = "block";
        }
      });
      finalSubCategoryGrid.appendChild(item);
    });
  }


  function showImages(gender, category, subCategory, final) {
    clearGrid(imagesSection);
    if (heading) {
      heading.style.display = 'block';
      heading.textContent = `Choose Models`;
    }
  
    // const key = `${gender}:${category}:${subCategory}:${final}`;
    const key = [gender, category, subCategory, final].filter(Boolean).join(':');

    const imageList = images[key];
    if (!imageList) {
      return;
    }
      

    imageList.forEach(src => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = final;
      img.loading = "lazy";
      img.style = "width: 200px; height: 250px; object-fit: contain; margin: 10px;";
      img.className = 'image-item';
  
      img.addEventListener('click', () => {
        imagesSection.querySelectorAll('img').forEach(i => i.classList.remove('active'));
        img.classList.add('active');
        if (detailBox) detailBox.style.display = "block";
        selectedImagePath = img.src;
      });
      imagesSection.appendChild(img);
    });
  }
  

  categoryGrid.addEventListener('click', function (e) {
    const target = e.target.closest('[data-gender]');
    if (!target) return;
    selectedGender = target.dataset.gender;
    categoryGrid.querySelectorAll('.category-item').forEach(item => item.classList.remove('active'));
    target.classList.add('active');
    showSubCategories(selectedGender);
  });

  // ✅ Save this section's reset function
  resetCategorySections.push(() => showSubCategories("None"));
});


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
const clothes_swap_category = document.getElementById("swap_category")?.value || "Not Provided";


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
  const colorBtn = document.getElementById("color-select");
  colorBtn.addEventListener("click", handleColorDropDownBtn);

  const colorBtn2 = document.getElementById("color-select-2");
  colorBtn2.addEventListener("click", handleColorDropDownBtn);

  function handleColorDropDownBtn() {
    if (currentMode === "model") {
      const dropdown = document.getElementById("color-select");
      const optionsContainer = dropdown.nextElementSibling;
      const hiddenInput1 = document.getElementById("product-color");
      const selectedValue1 = dropdown.querySelector(".selected-value-color");

      dropdown.classList.toggle("open");

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

    } else if (currentMode === "nomodel") {
      const dropdown = document.getElementById("color-select-2");
      const optionsContainer = dropdown.nextElementSibling;
      const hiddenInput1 = document.getElementById("product-color-2");
      const selectedValue1 = dropdown.querySelector(".selected-value-color");

      dropdown.classList.toggle("open");

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
    }
  }

  function getSelectedColor() {
    if (currentMode === "nomodel") {
      const manualColor = document.getElementById("manual-color-input-2").value.trim();
      const dropdownColor = document.getElementById("product-color-2").value.trim();

      // Priority: manual color
      if (manualColor !== "") {
        return manualColor;
      }
      return dropdownColor;

    } else if  (currentMode === "model") {
      const manualColor = document.getElementById("manual-color-input").value.trim();
      const dropdownColor = document.getElementById("product-color").value.trim();

      // Priority: manual color
      if (manualColor !== "") {
        return manualColor;
      }
      return dropdownColor;
    }
  }

  /*--------------------------------------------------------------
  # Handle Variant Button Section
  --------------------------------------------------------------*/

  const btn5 = document.getElementById("submit-variant-btn");
  btn5.addEventListener("click", handleSubmitVariant);

  const btn6 = document.getElementById("submit-variant-btn-2");
  btn6.addEventListener("click", handleSubmitVariant2);

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

  function handleSubmitVariant2() {
    // If brand etc not set, read them once
    if (!productData.brand_name) {
      productData.brand_name = document.getElementById('brand-name-2').value;
      productData.product_name = document.getElementById('product-name-2').value;
      productData.product_fabric = document.getElementById('product-fabric-2').value;
      productData.product_quantity = document.getElementById('product-quantity-2').value;
      productData.product_price = document.getElementById('product-price-2').value;
      productData.product_selling_price = document.getElementById('selling-price-2').value;
      productData.product_sizes = Array.from(document.querySelectorAll('input[name="size"]:checked')).map(cb => cb.value);

      if (!productData.brand_name || !productData.product_name || !productData.product_fabric || !productData.product_quantity || !productData.product_price || !productData.product_selling_price || productData.product_sizes.length === 0) {
        alert("Please fill all the main product fields before adding variants.");
        return;
      }
    }

    const productColor = getSelectedColor();
    productData.product_colors.push(productColor);

    documentData = {
      gender: selectedGender,
      category: selectedCategory,
      subCategory: selectedSubCategory,
      finalCategory: selectedFinalCategory,
      modelImagePath: selectedImagePath,
      swapCategory: clothes_swap_category
    };

    // Update the table with the new variant added
    updateVariantsTable();

    // Reset variant-specific fields (images, color)
    resetVariantFields();
  }

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

    // Append variant data to arrays

    productData.product_colors.push(productColor);
    
    // To show Images in Result Table Starts  ----------------------------------------->
    if (productResult && typeof productResult === 'string' && 
      (productResult.startsWith('http') || productResult.startsWith('/'))) {

      // It's likely a URL (absolute or relative)
      showResultImages.push(productResult);

    } else if (productResult instanceof File) {
      // Not a valid URL or empty
      const resultImageURL = URL.createObjectURL(productResult);
      showResultImages.push(resultImageURL);
    }

    const garmentImageURL = URL.createObjectURL(garmentImages2);
    showGarmentImages.push(garmentImageURL)

    // To show Images in Result Table Ends  ----------------------------------------->


    productGarmentImages.push(garmentImages2);

    productResultImages.push(productResult);

    documentData = {
      gender: selectedGender,
      category: selectedCategory,
      subCategory: selectedSubCategory,
      finalCategory: selectedFinalCategory,
      modelImagePath: selectedImagePath,
      swapCategory: clothes_swap_category
    };

    // Update the table with the new variant added
    updateVariantsTable();

    // Reset variant-specific fields (images, color)
    resetVariantFields();
  }


  function resetVariantFields() {
    document.getElementById('preview-image').src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    document.getElementById("mainImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    document.getElementById("secondImagePreview").src = "https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png";
    document.getElementById('resultImage').src = "";
    document.getElementById('resultImage').style.display = "none";
    document.getElementById('product-color').value = "";
    document.querySelector('.selected-value-color').textContent = "Select Color";

    // Reset file inputs
    document.getElementById('manual-color-input').value = "";
    document.getElementById('product-image-upload').value = "";
    document.getElementById('product-result-image-upload').value = "";
    document.getElementById('resultImageURL').value = "";
    selectedImagePath = "";
  }

  function updateVariantsTable() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = ""; // clear existing rows
    const tableBody2 = document.getElementById("tableBody-2");
    tableBody2.innerHTML = ""; // clear existing rows


    if (currentMode === "nomodel") {
      for (let i = 0; i < productData.product_colors.length; i++) {

        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${i + 1}</td>
          <td><img src="${showMainImages[i]}" alt="Result Image" width="60" height="95"></td>
          <td><img src="${showSecondImages[i]}" alt="Garment Image" width="60" height="90"></td>
          <td>${productData.product_colors[i]}</td>
          <td style="padding: 0;">
            <div style="display: flex; justify-content: center; align-items: center; height: 100%; width: 100%; padding: 10px;">
              <svg class="delete-icon" viewBox="0 0 24 24" data-index="${i}" style="cursor: pointer; width: 24px; height: 24px;">
                <path d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-4.5l-1-1z"/>
              </svg>
            </div>
          </td>
        `;
        tableBody2.appendChild(row);
      }
      // Attach event listeners to all delete icons
      const deleteIcons = document.querySelectorAll(".delete-icon");
      deleteIcons.forEach(icon => {
        icon.addEventListener("click", (event) => {
          const index = parseInt(event.currentTarget.getAttribute("data-index"));
          deleteVariant(index);
        });
      });

    } else if (currentMode === "model") {
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
  }

  function deleteVariant(index) {
    if (currentMode === "model") {

      productData.product_colors.splice(index, 1);

      showResultImages.splice(index, 1);
      showGarmentImages.splice(index, 1);

      productResultImages.splice(index, 1);
      productGarmentImages.splice(index, 1);
    
      updateVariantsTable(); // Re-render the table

    } else if (currentMode === "nomodel") {
      productData.product_colors.splice(index, 1);

      mainImages.splice(index, 1);
      secondImages.splice(index, 1);
    
      updateVariantsTable(); // Re-render the table
    }

  }
  

  /*--------------------------------------------------------------
  # Multiple QR Code Scanner Section
  --------------------------------------------------------------*/
  const scanBtn = document.getElementById("scan-btn");
  scanBtn.addEventListener("click", handleScanBtn);

  const scanBtn2 = document.getElementById("scan-btn-2");
  scanBtn2.addEventListener("click", handleScanBtn);

  const scannedIds = new Set(); // to avoid duplicates

  async function handleScanBtn() {
    if (currentMode === "model") {
      const scanBtn = document.getElementById("scan-btn");
      const cancelBtn = document.getElementById("cancel-btn");
      const readerDiv = document.getElementById("reader");
      const scannedItemsDiv = document.getElementById("scanned-items");
      const html5QrCode = new Html5Qrcode("reader");

      let isScanning = false;

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
          
          }
        );

        isScanning = true;

      } catch (err) {
        alert("Error accessing the camera. Please allow permission.");
        console.error(err);
        cancelBtn.style.display = "none";
        scanBtn.style.display = "block";
      }

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

    } else if (currentMode === "nomodel") {
      const scanBtn = document.getElementById("scan-btn-2");
      const cancelBtn = document.getElementById("cancel-btn-2");
      const readerDiv = document.getElementById("reader-2");
      const scannedItemsDiv = document.getElementById("scanned-items-2");
      const html5QrCode = new Html5Qrcode("reader-2");

      let isScanning = false;

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
              div.className = "scanned-item-2";
              div.innerText = shortId; // ✅ show only shortId
              scannedItemsDiv.appendChild(div);
            }
          
          }
        );

        isScanning = true;

      } catch (err) {
        alert("Error accessing the camera. Please allow permission.");
        console.error(err);
        cancelBtn.style.display = "none";
        scanBtn.style.display = "block";
      }

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
    }
  }

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

  productForm1 = document.querySelector('.product-form-model');
  productForm2 = document.querySelector('.product-form-nomodel');

  const submitBtn1 = productForm1.querySelector('.submit-add-products-btn');
  submitBtn1.addEventListener("click", handleSubmitBtn);

  const submitBtn2 = productForm2.querySelector('.submit-add-products-btn');
  submitBtn2.addEventListener("click", handleSubmitBtn);

  // Utility to get key from sessionStorage
  // async function getEncryptionKey() {
  //   const base64Key = sessionStorage.getItem("encryptionKey");
  //   if (!base64Key) {
  //     console.error("Encryption key not found in sessionStorage.");
  //     throw new Error("Encryption key not found. User might not be logged in or session expired.");
  //   }

  //   const rawKey = Uint8Array.from(atob(base64Key), c => c.charCodeAt(0));
  //   return await crypto.subtle.importKey(
  //     "raw",
  //     rawKey,
  //     "AES-GCM",
  //     false,
  //     ["encrypt", "decrypt"]
  //   );
  // }

  // Encrypt a single string field using AES-GCM
  // async function encryptField(text, key) {
  //   const encoder = new TextEncoder();
  //   const iv = crypto.getRandomValues(new Uint8Array(12)); // 96-bit IV for GCM

  //   const encryptedBuffer = await crypto.subtle.encrypt(
  //     {
  //       name: "AES-GCM",
  //       iv: iv
  //     },
  //     key,
  //     encoder.encode(text)
  //   );

  //   // Combine IV and encrypted text
  //   const combined = new Uint8Array(iv.length + encryptedBuffer.byteLength);
  //   combined.set(iv);
  //   combined.set(new Uint8Array(encryptedBuffer), iv.length);

  //   // Convert to base64 string for safe transmission/storage
  //   return btoa(String.fromCharCode(...combined));
  // }


  // Encrypt a single string field using AES-GCM
  // async function encryptField(text, key) {
  //   if (text === null || text === undefined || text === '') {
  //       if (text === '') return await _performEncryption('', key);
  //       return text;
  //   }
  //   return await _performEncryption(text, key);
  // }

  // // Helper to encapsulate actual encryption logic
  // async function _performEncryption(text, key) {
  //   const encoder = new TextEncoder();
  //   const iv = crypto.getRandomValues(new Uint8Array(12)); // 96-bit IV for GCM

  //   const encryptedBuffer = await crypto.subtle.encrypt(
  //     {
  //       name: "AES-GCM",
  //       iv: iv
  //     },
  //     key,
  //     encoder.encode(text)
  //   );

  //   // Combine IV and encrypted text
  //   const combined = new Uint8Array(iv.length + encryptedBuffer.byteLength);
  //   combined.set(iv);
  //   combined.set(new Uint8Array(encryptedBuffer), iv.length);

  //   // Convert to base64 string for safe transmission/storage
  //   return btoa(String.fromCharCode(...combined));
  // }


  // // Decrypt a single Base64-encoded field using AES-GCM (useful for display later)
  // async function decryptField(base64Ciphertext, key) {
  //     if (base64Ciphertext === null || base64Ciphertext === undefined || base64Ciphertext === '') {
  //         return base64Ciphertext; // If nothing was encrypted, return as is
  //     }
  //     try {
  //         const decoder = new TextDecoder();
  //         const combined = Uint8Array.from(atob(base64Ciphertext), c => c.charCodeAt(0));
  //         const iv = combined.slice(0, 12);
  //         const ciphertext = combined.slice(12);

  //         const decryptedBuffer = await crypto.subtle.decrypt(
  //             {
  //                 name: "AES-GCM",
  //                 iv: iv
  //             },
  //             key,
  //             ciphertext
  //         );

  //         return decoder.decode(decryptedBuffer);
  //     } catch (e) {
  //         console.error("Decryption failed:", e);
  //         // Handle decryption failure (e.g., corrupted data, wrong key)
  //         return null; // Or throw error, depending on desired behavior
  //     }
  // }


  async function handleSubmitBtn() {
    let productForm = null;
    let submitButton = null;
    let btnText = null;
    let btnSpinner = null;
  
    if (currentMode === "model") {
      productForm = document.querySelector('.product-form-model');
    } else if (currentMode === "nomodel") {
      productForm = document.querySelector('.product-form-nomodel');
    }
  
    if (productForm) {
      submitButton = productForm.querySelector('.submit-add-products-btn');
      btnText = submitButton.querySelector('.btn-text');
      btnSpinner = submitButton.querySelector('.btn-spinner');
    }
  
    if (!submitButton) return;
    
    const idsArray = Array.from(scannedIds);
    productData.qrcode_ids = [...idsArray];
  
    btnText.textContent = "Submitting";
    btnSpinner.style.display = 'inline-block';
  
    try {

      // if (!sessionStorage.getItem("encryptionKey")) {
      //   alert("Encryption key missing. Please log in again.");
      //   window.location.href = "/login/"; // or your actual login URL
      //   return;
      // }

      // // 🔐 Get AES Key
      // const key = await getEncryptionKey();
      // console.log("key:-", key)
  
      // // 🔐 Encrypt product fields
      // const encryptedProduct = { ...productData };
  
      // encryptedProduct.product_name = await encryptField(productData.product_name, key);
      // encryptedProduct.product_fabric = await encryptField(productData.product_fabric, key);
      // encryptedProduct.product_price = await encryptField(productData.product_price, key);  
      // encryptedProduct.product_selling_price = await encryptField(productData.product_selling_price, key);
  
      // encryptedProduct.product_sizes = await Promise.all(
      //   (productData.product_sizes || []).map(size => encryptField(size, key))
      // );
  
      // encryptedProduct.product_colors = await Promise.all(
      //   (productData.product_colors || []).map(color => encryptField(color, key))
      // );
  
      // console.log("Selling price encrypted:", encryptedProduct.product_selling_price);

  
      const formData = new FormData();
      formData.append('document', JSON.stringify(productData));
      formData.append('selectedmiddlebuttons', JSON.stringify(documentData));
      formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
  
      // 🖼️ Add images
      if (currentMode === "model") {
        productGarmentImages.forEach((file, index) => {
          formData.append(`garment_${index}`, file);
        });
  
        productResultImages.forEach((item, index) => {
          if (item instanceof File) {
            formData.append(`result_file_${index}`, item);
          } else if (typeof item === 'string') {
            formData.append(`result_url_${index}`, item);
          }
        });
  
      } else if (currentMode === "nomodel") {
        if (secondImages.length > 0) {
          secondImages.forEach((file, index) => {
            formData.append(`garment_${index}`, file);
          });
        }
  
        if (mainImages.length > 0) {
          mainImages.forEach((item, index) => {
            formData.append(`result_file_${index}`, item);
          });
        }
      }
  
      const response = await fetch('/add-products/', {
        method: 'POST',
        body: formData
      });
  
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const result = await response.json();
  
        if (result.uploaded_urls === 'uploaded') {
          alert('Product added successfully!');
          localStorage.setItem('lastSubmittedData', JSON.stringify(productData));
  
          const suffix = currentMode === 'model' ? '' : '-2';
          document.getElementById(`brand-name${suffix}`).value = '';
          document.getElementById(`product-name${suffix}`).value = '';
          document.getElementById(`product-fabric${suffix}`).value = '';
          document.getElementById(`product-color${suffix}`).value = '';
          document.getElementById(`product-quantity${suffix}`).value = '';
          document.getElementById(`product-price${suffix}`).value = '';
          document.getElementById(`selling-price${suffix}`).value = '';
          document.getElementById(`scanned-items${suffix}`).innerHTML = '';
  
          document.querySelectorAll('input[name="size"]:checked').forEach(c => c.checked = false);
          showResultImages = []; showGarmentImages = [];
          showMainImages = []; showSecondImages = [];
          scannedIds.clear();
  
          previewImage.src = 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/add-product_placeholder-image.png';
  
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
  
          if (currentMode === "model") {
            document.getElementById('resultImage').src = '';
            document.getElementById('resultImage').style.display = 'none';
            document.querySelector('.selected-value-color').textContent = 'Select Color';
            document.getElementById('manual-color-input').value = '';
            document.getElementById('product-color').value = '';
          } else {
            document.querySelector('.selected-value-color').textContent = 'Select Color';
            document.getElementById('manual-color-input-2').value = '';
            document.getElementById('product-color-2').value = '';
          }
  
          resetCategorySections.forEach(reset => reset());
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
      alert('Encryption or network/server error occurred.');
    } finally {
      btnText.textContent = "Submit Form";
      btnSpinner.style.display = 'none';
    }
  }
