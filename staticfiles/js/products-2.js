// Product data
const products = [
    { id: 1, name: "Round-Mock T-Shirt", image: "Hoodie.png" },
    { id: 2, name: "Up-Mock T-Shirt", image: "Coat.png"},
    { id: 3, name: "V-Mock T-Shirt", image: "tea.png" },
    { id: 4, name: "Polo T-Shirt", image: "Coat.png" },
    
];

// Load initial products
function generateProductData(count) {
    const generatedProducts = [];

    for (let i = 0; i < count; i++) {
        const baseProduct = products[i % products.length];

        generatedProducts.push({
            ...baseProduct,
            id: Date.now() + i
        });
    }

    return generatedProducts;
}

// Create product card element
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'category-item';

    card.innerHTML = `
        <img src="../static/img/home/${product.image}" alt="${product.name}" class="category-image">
    <div class="shine"></div>
  </div>
        <div class="category-details">
            <div class="item">
                <h3 class="item-title">${product.name}</h3>
                <a href="#" class="explore-link">Explore Now!</a>
            </div>
            <img src="./assets/img/arrow-1.svg" alt="Arrow" class="explore-arrow">
        </div>
    `;

    return card;
}

// Load more products
function loadMoreProducts() {
    const productGrid = document.getElementById('productGrid');
    const moreProducts = generateProductData(12); // Load 12 more products each time

    moreProducts.forEach(product => {
        productGrid.appendChild(createProductCard(product));
    });

    // Smooth scroll to the newly added products
    const cards = productGrid.children;
    cards[cards.length - 1].scrollIntoView({ behavior: 'smooth' });
}

// Initialize the main
document.addEventListener('DOMContentLoaded', () => {
    // Don't call loadInitialProducts() here, let the user click the button to load products.

    // Add click event to load more button
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    loadMoreBtn.addEventListener('click', loadMoreProducts);
});
