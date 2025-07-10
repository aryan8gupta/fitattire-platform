// // Data for components
// const statsData = {
//     'Last 24 hour': {
//       revenue: { value: '$42', change: 8 },
//       customers: { value: '15', change: 12 },
//       transactions: { value: '8', change: 5 },
//       products: { value: '25', change: 3 },
//     },
//     'Last week': {
//       revenue: { value: '$152', change: 16 },
//       customers: { value: '80', change: -0.45 },
//       transactions: { value: '37', change: 8 },
//       products: { value: '120', change: 2 },
//     },
//     'Last month': {
//       revenue: { value: '$612', change: 24 },
//       customers: { value: '300', change: 15 },
//       transactions: { value: '150', change: 12 },
//       products: { value: '350', change: 5 },
//     },
//     'Last year': {
//       revenue: { value: '$5,612', change: 45 },
//       customers: { value: '7,513', change: 32 },
//       transactions: { value: '4,637', change: 28 },
//       products: { value: '1530', change: 15 },
//     },
// };

  
// // Populate StatCard

// function updateStats(range) {
//     const data = statsData[range];
//     if (!data) return;

//     const arrowUpSVG = `
//         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgb(14, 207, 14)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up-right">
//         <path d="M7 7h10v10"></path>
//         <path d="M7 17 17 7"></path>
//         </svg>`;
//     const arrowDownSVG = `
//         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-down-right">
//         <path d="m7 7 10 10"></path>
//         <path d="M17 7v10H7"></path>
//         </svg>`;
  
//     const update = (id, value, change, label = '') => {
//         const valueEl = document.getElementById(id + 'Value');
//         const changeEl = document.getElementById(id + 'Change');
    
//         valueEl.textContent = value;
//         valueEl.style.fontSize = '1.25rem';  // Set the font size
//         valueEl.style.fontWeight = 'bold';   // Make the font bold

//         const isPositive = change >= 0;
//         const arrowSVG = isPositive ? arrowUpSVG : arrowDownSVG;
//         const colorClass = isPositive ? 'positive' : 'negative';

//         // changeEl.innerHTML = `${arrowSVG} <span>${Math.abs(change)}%${label}</span>`;
//         // changeEl.className = colorClass;
//         changeEl.className = `change ${colorClass}`;
//         changeEl.innerHTML = `
//             ${arrowSVG}
//             <span class="change-value">${Math.abs(change)}%</span>
//             <span class="period-label">${label}</span>`;
//     };
  
//     update('revenue', data.revenue.value, data.revenue.change, ` vs ${range}`);
//     update('customers', data.customers.value, data.customers.change, ` vs ${range}`);
//     update('transactions', data.transactions.value, data.transactions.change, ` vs ${range}`);
//     update('products', data.products.value, data.products.change, ` vs ${range}`);
//   }
  
// // Initial load
// updateStats('Last 24 hour');
  


// //Top Transactions:-

// const transactions = [
//     {
//       customer: { id: '#23492', name: 'Jenny Wilson' },
//       item: 'Leather case bag & wallet',
//       date: '12 Jan',
//       purchase: '$2,548',
//       status: 'live order',
//     },
//     {
//       customer: { id: '#23492', name: 'Jenny Wilson' },
//       item: 'Simple Tote Bag',
//       date: '3 Jan',
//       purchase: '$548',
//       status: 'completed',
//     },
// ];
  
// function createTransactionCard(transaction) {
//     const div = document.createElement('div');
//     div.className = 'transaction';
  
//     div.innerHTML = `
//       <div class="avatar">
//         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
//           <circle cx="12" cy="7" r="4" />
//           <path d="M5.5 21a7.5 7.5 0 0 1 13 0" />
//         </svg>
//       </div>
//       <div class="transaction-details">
//         <div class="transaction-row">
//           <div>
//             <p class="customer-name">${transaction.customer.name}</p>
//             <p class="item-name">${transaction.item}</p>
//           </div>
//           <div class="purchase">
//             <p class="customer-name">${transaction.purchase}</p>
//             <p class="item-name">${transaction.date}</p>
//           </div>
//         </div>
//         ${
//           transaction.status === 'live order'
//             ? `<span class="live-badge">Live Order</span>`
//             : ''
//         }
//       </div>
//     `;
  
//     return div;
// }
  
// const container = document.getElementById('transactions');
// transactions.forEach(tx => container.appendChild(createTransactionCard(tx)));
  


// // Top Products

// const products = [
//     {
//       name: 'Denim Jacket with White Feathers',
//       image: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=200&h=200',
//       sales: '240+',
//     },
//     {
//       name: 'Black Leather Jacket',
//       image: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=200&h=200',
//       sales: '180+',
//     },
//   ];

//   const productGrid = document.getElementById('productGrid');

//   products.forEach((product) => {
//     const card = document.createElement('div');
//     card.className = 'product-card';

//     card.innerHTML = `
//       <img src="${product.image}" alt="${product.name}" />
//       <div class="product-overlay">
//         <div class="product-info">
//           <p class="name">${product.name}</p>
//           <p class="sales">Sales: ${product.sales}</p>
//         </div>
//       </div>
//     `;

//     productGrid.appendChild(card);
// });


// // Revenue Chart (Simple Bar Chart Example)

// const revenueChartData = {
//     'Last 24 hour': [
//     { name: '12 AM', revenue: 400, ecommerce: 240 },
//     { name: '4 AM', revenue: 300, ecommerce: 139 },
//     { name: '8 AM', revenue: 500, ecommerce: 380 },
//     { name: '12 PM', revenue: 280, ecommerce: 190 },
//     { name: '4 PM', revenue: 590, ecommerce: 390 },
//     { name: '8 PM', revenue: 350, ecommerce: 300 },
//     { name: 'Now', revenue: 400, ecommerce: 380 },
//     ],
//     'Last week': [
//     { name: 'Sun', revenue: 400, ecommerce: 240 },
//     { name: 'Mon', revenue: 300, ecommerce: 139 },
//     { name: 'Tue', revenue: 500, ecommerce: 380 },
//     { name: 'Wed', revenue: 280, ecommerce: 190 },
//     { name: 'Thu', revenue: 590, ecommerce: 390 },
//     { name: 'Fri', revenue: 350, ecommerce: 300 },
//     { name: 'Sat', revenue: 400, ecommerce: 380 },
//     ],
//     'Last month': [
//     { name: 'Week 1', revenue: 1500, ecommerce: 1000 },
//     { name: 'Week 2', revenue: 2000, ecommerce: 1500 },
//     { name: 'Week 3', revenue: 1800, ecommerce: 1200 },
//     { name: 'Week 4', revenue: 2400, ecommerce: 1800 },
//     ],
//     'Last year': [
//     { name: 'Jan', revenue: 4000, ecommerce: 2400 },
//     { name: 'Mar', revenue: 3000, ecommerce: 1398 },
//     { name: 'May', revenue: 5000, ecommerce: 3800 },
//     { name: 'Jul', revenue: 2800, ecommerce: 1908 },
//     { name: 'Sep', revenue: 5900, ecommerce: 3800 },
//     { name: 'Nov', revenue: 3500, ecommerce: 3000 },
//     { name: 'Dec', revenue: 4000, ecommerce: 3800 },
//     ]
// };

// function renderRevenueChart(timeRange) {
//     const ctx = document.getElementById('revenueChartCanvas').getContext('2d');
//     const data = revenueChartData[timeRange];

//     if (!data) return;

//     document.getElementById("chart-period").textContent = `${timeRange} revenue growth with in percentage`;

//     if (window.revenueChartInstance) window.revenueChartInstance.destroy();

//     window.revenueChartInstance = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: data.map(d => d.name),
//         datasets: [
//         {
//             label: 'Revenue',
//             data: data.map(d => d.revenue),
//             backgroundColor: '#3B82F6',
//             borderRadius: 4
//         },
//         {
//             label: 'Ecommerce',
//             data: data.map(d => d.ecommerce),
//             backgroundColor: '#93C5FD',
//             borderRadius: 4
//         }
//         ]
//     },
//     options: {
//         responsive: true,
//         scales: {
//         x: { grid: { display: false } },
//         y: { grid: { display: true } }
//         },
//         plugins: {
//         tooltip: {
//             backgroundColor: '#fff',
//             titleColor: '#000',
//             bodyColor: '#000',
//             borderColor: '#ddd',
//             borderWidth: 1,
//             cornerRadius: 8
//         },
//         legend: { display: false }
//         }
//     }
//     });
// }


// // Customer Growth

// const instagramInsightsData = {
//     "Last 24 hour": {
//       profileVisits: 140,
//       videoViews: 320,
//       postLikes: 230,
//       followersGained: 22
//     },
//     "Last week": {
//       profileVisits: 1240,
//       videoViews: 2780,
//       postLikes: 1980,
//       followersGained: 155
//     },
//     "Last month": {
//       profileVisits: 4850,
//       videoViews: 11230,
//       postLikes: 8890,
//       followersGained: 410
//     },
//     "Last year": {
//       profileVisits: 52100,
//       videoViews: 138000,
//       postLikes: 101200,
//       followersGained: 6100
//     }
// };
  
// let instagramChart;

// function updateDonutChart(range) {
//     const data = instagramInsightsData[range];
//     if (!data || !instagramChart) return;

//     document.getElementById("customerGrowth-period").textContent = `${range} customer growth with in percentage`;

//     instagramChart.data.datasets[0].data = [
//         data.profileVisits,
//         data.videoViews,
//         data.postLikes,
//         data.followersGained
//     ];
//     instagramChart.update();
// }

// const ctx = document.getElementById('instagramDonutChart').getContext('2d');
// instagramChart = new Chart(ctx, {
// type: 'doughnut',
// data: {
//     labels: ['Profile Visits', 'Video Views', 'Post Likes', 'Followers Gained'],
//     datasets: [{
//     data: Object.values(instagramInsightsData["Last 24 hour"]),
//     backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC']
//     }]
// },
// options: {
//     plugins: {
//     legend: { position: 'bottom' }
//     },
//     cutout: '70%'
// }
// });



// // Add event listeners to time range buttons
// document.querySelectorAll('.time-button').forEach(button => {
//     button.addEventListener('click', () => {
//     document.querySelectorAll('.time-button').forEach(btn => btn.classList.remove('active'));
//     button.classList.add('active');
//     renderRevenueChart(button.dataset.range);
//     updateStats(button.dataset.range);
//     updateDonutChart(button.dataset.range);
//     });
// });

// renderRevenueChart('Last 24 hour'); // Default
// updateStats("Last 24 hour");
// updateDonutChart("Last 24 hour")




// // New js code 2 ------------------------------------------------------->
// // analytics.js (Frontend)
// async function fetchAnalyticsData(range) {
//   const res = await fetch(`/api/analytics?range=${encodeURIComponent(range)}`);
//   const data = await res.json();

//   updateStats(data.stats);
//   renderTopTransactions(data.top_transactions);
//   renderTopProducts(data.top_products);
//   updateDonutChart(range, data.instagram_data);
//   renderRevenueChart(range, data.revenue_chart);
// }

// function updateStats(statsData) {
//   const arrowUpSVG = `<svg ...></svg>`; // Add correct SVG
//   const arrowDownSVG = `<svg ...></svg>`; // Add correct SVG

//   const update = (id, value, change, label = '') => {
//     const valueEl = document.getElementById(id + 'Value');
//     const changeEl = document.getElementById(id + 'Change');

//     valueEl.textContent = value;
//     valueEl.style.fontSize = '1.25rem';
//     valueEl.style.fontWeight = 'bold';

//     const isPositive = change >= 0;
//     const arrowSVG = isPositive ? arrowUpSVG : arrowDownSVG;
//     const colorClass = isPositive ? 'positive' : 'negative';

//     changeEl.className = `change ${colorClass}`;
//     changeEl.innerHTML = `
//       ${arrowSVG}
//       <span class="change-value">${Math.abs(change)}%</span>
//       <span class="period-label">${label}</span>`;
//   };

//   update('revenue', statsData.revenue.value, statsData.revenue.change);
//   update('customers', statsData.customers.value, statsData.customers.change);
//   update('transactions', statsData.transactions.value, statsData.transactions.change);
//   update('products', statsData.products.value, statsData.products.change);
// }

// function renderTopTransactions(transactions) {
//   const container = document.getElementById('transactions');
//   container.innerHTML = '';
//   transactions.forEach(tx => {
//     const div = document.createElement('div');
//     div.className = 'transaction';
//     div.innerHTML = `
//       <div class="avatar">...</div>
//       <div class="transaction-details">
//         <div class="transaction-row">
//           <div>
//             <p class="customer-name">${tx.customer.name}</p>
//             <p class="item-name">${tx.item}</p>
//           </div>
//           <div class="purchase">
//             <p class="customer-name">${tx.purchase}</p>
//             <p class="item-name">${tx.date}</p>
//           </div>
//         </div>
//         ${tx.status === 'live order' ? `<span class="live-badge">Live Order</span>` : ''}
//       </div>`;
//     container.appendChild(div);
//   });
// }

// function renderTopProducts(products) {
//   const grid = document.getElementById('productGrid');
//   grid.innerHTML = '';
//   products.forEach(product => {
//     const card = document.createElement('div');
//     card.className = 'product-card';
//     card.innerHTML = `
//       <img src="${product.image}" alt="${product.name}" />
//       <div class="product-overlay">
//         <div class="product-info">
//           <p class="name">${product.name}</p>
//           <p class="sales">Sales: ${product.sales}</p>
//         </div>
//       </div>`;
//     grid.appendChild(card);
//   });
// }

// function updateDonutChart(range, data) {
//   document.getElementById("customerGrowth-period").textContent = `${range} customer growth with in percentage`;
//   if (!window.instagramChart) return;
//   instagramChart.data.datasets[0].data = [
//     data.profileVisits,
//     data.videoViews,
//     data.postLikes,
//     data.followersGained
//   ];
//   instagramChart.update();
// }

// function renderRevenueChart(timeRange, chartData) {
//   const ctx = document.getElementById('revenueChartCanvas').getContext('2d');
//   if (!chartData || chartData.length === 0) return;
//   document.getElementById("chart-period").textContent = `${timeRange} revenue growth with in percentage`;
//   if (window.revenueChartInstance) window.revenueChartInstance.destroy();
//   window.revenueChartInstance = new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: chartData.map(d => d.name),
//       datasets: [
//         {
//           label: 'Revenue',
//           data: chartData.map(d => d.revenue),
//           backgroundColor: '#3B82F6',
//           borderRadius: 4
//         },
//         {
//           label: 'Ecommerce',
//           data: chartData.map(d => d.ecommerce),
//           backgroundColor: '#93C5FD',
//           borderRadius: 4
//         }
//       ]
//     },
//     options: {
//       responsive: true,
//       scales: {
//         x: { grid: { display: false } },
//         y: { grid: { display: true } }
//       },
//       plugins: {
//         tooltip: {
//           backgroundColor: '#fff',
//           titleColor: '#000',
//           bodyColor: '#000',
//           borderColor: '#ddd',
//           borderWidth: 1,
//           cornerRadius: 8
//         },
//         legend: { display: false }
//       }
//     }
//   });
// }

// // Event Listeners

// document.querySelectorAll('.time-button').forEach(button => {
//   button.addEventListener('click', () => {
//     document.querySelectorAll('.time-button').forEach(btn => btn.classList.remove('active'));
//     button.classList.add('active');
//     fetchAnalyticsData(button.dataset.range);
//   });
// });

// // Donut Chart Init
// const ctx = document.getElementById('instagramDonutChart').getContext('2d');
// window.instagramChart = new Chart(ctx, {
//   type: 'doughnut',
//   data: {
//     labels: ['Profile Visits', 'Video Views', 'Post Likes', 'Followers Gained'],
//     datasets: [{
//       data: [140, 320, 230, 22],
//       backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC']
//     }]
//   },
//   options: {
//     plugins: { legend: { position: 'bottom' } },
//     cutout: '70%'
//   }
// });

// // Initial Load
// fetchAnalyticsData('Last 24 hour');




// New code js - 3 -------------------------->
// analytics.js (Updated)

async function fetchAnalyticsData(range) {
  const res = await fetch("/analytics/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "range": range })
  })

  const data = await res.json();

  updateStats(data.stats, range);
  renderTopTransactions(data.top_transactions);
  renderTopProducts(data.top_products);
  updateDonutChart(range, data.instagram);
  renderRevenueChart(range, data.revenue_chart);
}

function updateStats(statsData, range) {
  const arrowUpSVG = `<svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>`;
  const arrowDownSVG = `<svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>`;

  const update = (id, value, change) => {
    const valueEl = document.getElementById(id + 'Value');
    const changeEl = document.getElementById(id + 'Change');

    if (valueEl.id === "revenueValue") {
      valueEl.textContent = `₹${value}`;
    }
    else {
      valueEl.textContent = `${value}`;
    }

    
    valueEl.style.fontSize = '1.25rem';
    valueEl.style.fontWeight = 'bold';

    const isPositive = change >= 0;
    const arrowSVG = isPositive ? arrowUpSVG : arrowDownSVG;
    const colorClass = isPositive ? 'positive' : 'negative';

    changeEl.className = `change ${colorClass}`;
    changeEl.innerHTML = `
      ${arrowSVG}
      <span class="change-value">${Math.abs(change)}%</span>
      <span class="period-label">vs ${range}</span>`;
  };

  update('revenue', statsData.revenue.value, statsData.revenue.change);
  update('customers', statsData.customers.value, statsData.customers.change);
  update('transactions', statsData.transactions.value, statsData.transactions.change);
  update('products', statsData.products.value, statsData.products.change);
}

function renderTopTransactions(transactions) {
  const container = document.getElementById('transactions');
  container.innerHTML = '';
  transactions.forEach(tx => {
    const div = document.createElement('div');
    div.className = 'transaction';
    div.innerHTML = `
      <div class="avatar">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="12" cy="7" r="4" />
          <path d="M5.5 21a7.5 7.5 0 0 1 13 0" />
        </svg>
      </div>
      <div class="transaction-details">
        <div class="transaction-row">
          <div>
            <p class="customer-name">${tx.customer.name}</p>
            <p class="item-name">${tx.item}</p>
          </div>
          <div class="purchase">
            <p class="customer-name">₹${tx.purchase}</p>
            <p class="item-name">${tx.date}</p>
          </div>
        </div>
        ${tx.status === 'live order' ? `<span class="live-badge">Live Order</span>` : ''}
      </div>`;
    container.appendChild(div);
  });
}

function renderTopProducts(products) {
  const grid = document.getElementById('productGrid');
  grid.innerHTML = '';
  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${product.image}" alt="${product.name}" />
      <div class="product-overlay">
        <div class="product-info">
          <p class="name">${product.name}</p>
          <p class="sales">Sales: ${product.sales}</p>
        </div>
      </div>`;
    grid.appendChild(card);
  });
}

function updateDonutChart(range, data) {
  document.getElementById("customerGrowth-period").textContent = `${range} customer growth with in percentage`;
  if (!window.instagramChart) return;
  instagramChart.data.datasets[0].data = [
    data.profileVisits,
    data.videoViews,
    data.postLikes,
    data.followersGained
  ];
  instagramChart.update();
}

function renderRevenueChart(timeRange, chartData) {
  const ctx = document.getElementById('revenueChartCanvas').getContext('2d');
  if (!chartData || chartData.length === 0) return;
  document.getElementById("chart-period").textContent = `${timeRange} revenue growth with in percentage`;
  if (window.revenueChartInstance) window.revenueChartInstance.destroy();
  window.revenueChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.map(d => d.name),
      datasets: [
        {
          label: 'Revenue',
          data: chartData.map(d => d.revenue),
          backgroundColor: '#3B82F6',
          borderRadius: 4
        },
        {
          label: 'Ecommerce',
          data: chartData.map(d => d.ecommerce),
          backgroundColor: '#93C5FD',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { grid: { display: false } },
        y: { grid: { display: true } }
      },
      plugins: {
        tooltip: {
          backgroundColor: '#fff',
          titleColor: '#000',
          bodyColor: '#000',
          borderColor: '#ddd',
          borderWidth: 1,
          cornerRadius: 8
        },
        legend: { display: false }
      }
    }
  });
}

// Event Listeners
document.querySelectorAll('.time-button').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.time-button').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    fetchAnalyticsData(button.dataset.range);
  });
});

// Donut Chart Init
const ctx = document.getElementById('instagramDonutChart').getContext('2d');
window.instagramChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Profile Visits', 'Video Views', 'Post Likes', 'Followers Gained'],
    datasets: [{
      data: [140, 320, 230, 22],
      backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC']
    }]
  },
  options: {
    plugins: { legend: { position: 'bottom' } },
    cutout: '70%'
  }
});

// Initial Load
fetchAnalyticsData('Last 24 hour');
