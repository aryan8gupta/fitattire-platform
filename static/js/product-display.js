console.log("JS loaded");
function scrollImages(direction) {
  const container = document.getElementById("imageContainer");
  const scrollAmount = 260; 

  if (direction === "left") {
    container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  } else {
    container.scrollBy({ left: scrollAmount, behavior: "smooth" });
  }
}
// navigation menu-mobile view
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

// hamburger.addEventListener("click", () => {
//   navLinks.classList.toggle("active");
// });

const scrollBox = document.getElementById("relatedScroll");

function scrollLeftCarousel() {
  scrollBox.scrollBy({ left: -300, behavior: "smooth" });
}

function scrollRightCarousel() {
  scrollBox.scrollBy({ left: 300, behavior: "smooth" });
}


// Switch Images & Color Name Dynamically
function updateDisplay(resultImage, garmentImage, color, clickedThumb, index) {
  // Update large images
  document.getElementById('mainResultImage').src = resultImage;
  document.getElementById('mainGarmentImage').src = garmentImage;

  // Update color text
  document.getElementById('selectedColor').textContent = color;

  // Update active thumbnail
  const thumbs = document.querySelectorAll('.result-thumb');
  thumbs.forEach(thumb => thumb.classList.remove('active'));
  clickedThumb.classList.add('active');

  // Optional: Use the index value if needed
  console.log("Selected variant index:", index);
}