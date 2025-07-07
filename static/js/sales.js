// Sales Page JavaScript

// New Code
function validateInput(value) {
    const errorEl = document.getElementById("phoneError");
    const customerDetails = document.getElementById("customer-details");
    const noDetails = document.getElementById("no-details");

    if (!/^\d{0,10}$/.test(value)) {
        errorEl.textContent = "Invalid Input: Only digits allowed.";
        customerDetails.classList.add("hidden");
        noDetails.classList.add("hidden");
    } else if (value.length !== 10) {
        errorEl.textContent = "Please enter exactly 10 digits.";
        customerDetails.classList.add("hidden");
        noDetails.classList.add("hidden");
    } else {
        errorEl.textContent = "";
    }
}

let customer_name = "";

function searchNumber() {
    const number = document.getElementById("mobile-number").value.trim();
    const errorEl = document.getElementById("phoneError");
    const customerDetails = document.getElementById("customer-details");
    const noDetails = document.getElementById("no-details");
    console.log("1")

    if (!/^\d{10}$/.test(number)) {
        errorEl.textContent = "Invalid Input: Enter a valid 10-digit mobile number.";
        customerDetails.classList.add("hidden");
        noDetails.classList.add("hidden");
        return;
    }

    errorEl.textContent = "";

    fetch('/search-whatsapp-number/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ phone: '+91' + number })
    })
    .then(response => response.json())
    .then(data => {
        console.log("5")
        console.log(data)
        if (data.found) {
            document.getElementById("customer-name").textContent = data.name;
            document.getElementById("phone-number").textContent = data.phone;

            customer_name = data.name;

            // Clear previous rows
            const tableContainer = document.querySelector(".table-container");
            const tbody = document.getElementById("last-purchases");
            tbody.innerHTML = "";
            if (data.purchases && data.purchases.length > 0) {
                (data.purchases || []).forEach(p => {
                    const row = `<tr>
                        <td>${p.product}</td>
                        <td>${p.qty}</td>
                        <td>${p.price}</td>
                    </tr>`;
                    tbody.innerHTML += row;
                });
                tableContainer.style.display = "block";  // Show table
            } else {
                tableContainer.style.display = "none";  // Hide table
                const noPurchaseMsg = document.createElement("p");
                noPurchaseMsg.textContent = "No Purchases Yet!";
                noPurchaseMsg.style.color = "gray";
                noPurchaseMsg.style.marginTop = "10px";
                noPurchaseMsg.id = "no-purchase-msg";
    
                // Remove any previous message
                const prevMsg = document.getElementById("no-purchase-msg");
                if (prevMsg) prevMsg.remove();
    
                document.getElementById("customer-details").appendChild(noPurchaseMsg);
            }

            customerDetails.classList.remove("hidden");
            noDetails.classList.add("hidden");

        } else {
            customerDetails.classList.add("hidden");
            noDetails.classList.remove("hidden");
            document.getElementById("new-customer-phone").value = number;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}


function addNumber() {
    const customer_name2 = document.getElementById("new-customer-name").value.trim();
    const phone = document.getElementById("new-customer-phone").value.trim();

    if (customer_name2 === "" || !/^\d{10}$/.test(phone)) {
        alert("Please enter a valid name and 10-digit mobile number.");
        return;
    }

    fetch('/add-whatsapp-number/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: customer_name2, phone: '+91' + phone })
    })
    .then(response => response.json())
    .then(data => {
        console.log("6")
        console.log(data)
        alert(data.message || "Number added successfully.");
        // Optionally reset form
        document.getElementById("new-customer-name").value = "";
        document.getElementById("new-customer-phone").value = "";
        document.getElementById("mobile-number").value = "";

        document.getElementById("customer-name").textContent = customer_name2;
        document.getElementById("phone-number").textContent = phone;

        customer_name = customer_name2;

        // Clear previous rows
        const tableContainer = document.querySelector(".table-container");
        const tbody = document.getElementById("last-purchases");
        tbody.innerHTML = "";
        if (data.purchases && data.purchases.length > 0) {
            (data.purchases || []).forEach(p => {
                const row = `<tr>
                    <td>${p.product}</td>
                    <td>${p.qty}</td>
                    <td>${p.price}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
            tableContainer.style.display = "block";  // Show table
        } else {
            tableContainer.style.display = "none";  // Hide table
            const noPurchaseMsg = document.createElement("p");
            noPurchaseMsg.textContent = "No Purchases Yet!";
            noPurchaseMsg.style.color = "gray";
            noPurchaseMsg.style.marginTop = "10px";
            noPurchaseMsg.id = "no-purchase-msg";

            // Remove any previous message
            const prevMsg = document.getElementById("no-purchase-msg");
            if (prevMsg) prevMsg.remove();

            document.getElementById("customer-details").appendChild(noPurchaseMsg);
        }

        customerDetails.classList.remove("hidden");
        noDetails.classList.add("hidden");

    })
    .catch(error => {
        console.error("Error:", error);
        alert("Could not add the number. Please try again.");
    });
}

const html5QrCode = new Html5Qrcode("reader");
let isScanning = false;
const scannedProductData = {};
const qrcodeidsarray = [];
let qrId = "";
let total_sum = 0;

document.getElementById("scan-btn").addEventListener("click", async () => {
    document.getElementById("reader").style.display = "block";
    document.getElementById("cancel-btn").style.display = "block";
    document.getElementById("scan-btn").style.display = "none";
    startQrScanner();
});

document.getElementById("cancel-btn").addEventListener("click", () => {
    if (isScanning) {
        html5QrCode.stop().then(() => {
            isScanning = false;
            document.getElementById("reader").style.display = "none";
            document.getElementById("cancel-btn").style.display = "none";
            document.getElementById("scan-btn").style.display = "block";
        });
    }
});

function qr_cancel_btn() {
    if (isScanning) {
        html5QrCode.stop().then(() => {
            isScanning = false;
            document.getElementById("reader").style.display = "none";
            document.getElementById("cancel-btn").style.display = "none";
            document.getElementById("scan-btn").style.display = "block";
        });
    }
}

async function startQrScanner() {
    try {
        const devices = await Html5Qrcode.getCameras();
        console.log("Available devices:", devices); 
        if (devices.length === 0) {
            alert("No cameras found.");
            return;
        }   

        const backCamera = devices.find(d => /back|rear/i.test(d.label)) || devices[0];

        await html5QrCode.start(
            backCamera.id,
            { fps: 10, qrbox: { width: 250, height: 250 } },
            onScanSuccess
        );
        isScanning = true;
        
    } catch (e) {
        alert("Camera access error.");
        console.error(e);
    }
}

function onScanSuccess(decodedText) {
    
    const qrId = decodedText.slice(-10);   
    // qrId = "FiA-75913/"; 

    if (scannedProductData[qrId]) return;
    
    console.log(qrId)
    // scanner.stop(); // Stop scanning after one scan

    qr_cancel_btn();

    // isScanning = false;
    fetch("/get-product/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ qr_id: qrId })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        if (!data.error) {
            scannedProductData[qrId] = data;
            qrcodeidsarray.push(qrId)
            displayAllRowsFromDataStore();
        } else {
            alert(data.error || "Product not found.");
        }
    });
}

function displayAllRowsFromDataStore() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";

    let product_sum = 0;
    total_sum = 0;

    for (const qrId in scannedProductData) {
        const dataWrapper = scannedProductData[qrId];
        const data = dataWrapper.data || dataWrapper; // handles both nested and flat cases
        
        const variants = data.variants || [];

        product_sum = data.selling_price * variants.length
        total_sum = total_sum + product_sum

        variants.forEach((variant, index) => {
            const row = document.createElement("tr");
            row.setAttribute("data-qrid", qrId);

            row.innerHTML = `
                <td><img src="${variant.result_image}" alt="Result" style="height: 60px;" /></td>
                <td>${variant.color || "N/A"}</td>
            `;

            // Only add these columns once, with rowspan
            if (index === 0) {
                const rowSpan = variants.length;

                const stockTd = document.createElement("td");
                stockTd.rowSpan = rowSpan;
                stockTd.textContent = data.product_quantity || 0;

                const productNameTd = document.createElement("td");
                productNameTd.rowSpan = rowSpan;
                productNameTd.textContent = data.product_name || 0;

                const priceTd = document.createElement("td");
                priceTd.rowSpan = rowSpan;
                priceTd.textContent = data.selling_price ? `₹${data.selling_price * variants.length}` : "N/A";

                const actionTd = document.createElement("td");
                actionTd.rowSpan = rowSpan;

                const deleteWrapper = document.createElement("div");
                deleteWrapper.style.cssText = "display: flex; justify-content: center; align-items: center; padding: 10px;";

                const deleteIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                deleteIcon.setAttribute("viewBox", "0 0 24 24");
                deleteIcon.setAttribute("style", "cursor: pointer; width: 24px; height: 24px; fill: red;");
                deleteIcon.classList.add("delete-icon");

                const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                path.setAttribute("d", "M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-4.5l-1-1z");
                deleteIcon.appendChild(path);

                deleteWrapper.appendChild(deleteIcon);
                actionTd.appendChild(deleteWrapper);

                deleteIcon.addEventListener("click", () => {
                    delete scannedProductData[qrId];
                    displayAllRowsFromDataStore();
                });

                // Append extra <td> to current row
                row.appendChild(productNameTd);
                row.appendChild(stockTd);
                row.appendChild(priceTd);
                row.appendChild(actionTd);
            }

            tableBody.appendChild(row);
            document.getElementById("amount").textContent = total_sum;
        });
    }
}

const inputField = document.getElementById('discount-input');
const numpad = document.getElementById('numpad');
let discountPercent;
let discount;

function showDiscountBox() {
    document.getElementById('discount-section').style.display = 'block';

    const discountInput = document.getElementById('discount-input');
    discountInput.focus();

    discountInput.addEventListener('input', function () {
        discountPercent = parseFloat(this.value);

        if (!isNaN(discountPercent) && discountPercent >= 0 && discountPercent <= 100) {
        const discountedAmount = total_sum - (total_sum * (discountPercent / 100));
        document.getElementById('discounted-amount').textContent =
            `New Amount after ${discountPercent}% discount: ₹${discountedAmount.toFixed(2)}`;
        } else {
        document.getElementById('discounted-amount').textContent = '';
        }
    });
}


inputField.addEventListener('focus', () => {
    numpad.style.display = 'flex';
    numpad.style.flexWrap = 'wrap';
});

function appendNumber(num) {
    inputField.value += num;
    updateDiscountedAmount();
}

function backspace() {
    inputField.value = inputField.value.slice(0, -1);
    updateDiscountedAmount();
}

function clearInput() {
    inputField.value = '';
    updateDiscountedAmount();
}

function updateDiscountedAmount() {
    discount = parseFloat(inputField.value);
    if (!isNaN(discount) && discount >= 0 && discount <= 100) {
    const discounted = total_sum - (total_sum * discount / 100);
    document.getElementById('discounted-amount').textContent =
        `New Amount after ${discount}% discount: ₹${discounted.toFixed(2)}`;
    } else {
    document.getElementById('discounted-amount').textContent = '';
    }
}


// Payment Calculation
// Payment Calculation
const customerAmountInput = document.getElementById('customer-amount');
const discountedElement = document.getElementById('discounted-amount');
const originalElement = document.getElementById('amount');
const changeElement = document.getElementById('change-return');
let totalAmount;
let originalAmount;
let discountedAmount;
let customerAmount;
let change;

if (customerAmountInput && discountedElement && originalElement && changeElement) {
    customerAmountInput.addEventListener('input', function () {
        calculateChange();
    });

    function calculateChange() {
        customerAmount = parseFloat(customerAmountInput.value) || 0;

        // Try to extract ₹ amount from discounted text (e.g., "New Amount after 20% discount: ₹240.00")
        const discountMatch = discountedElement.textContent.match(/₹([\d.,]+)/);
        discountedAmount = discountMatch ? parseFloat(discountMatch[1].replace(/,/g, '')) : NaN;

        originalAmount = parseFloat(originalElement.textContent) || 0;

        // Priority to discounted amount if it exists and is valid
        totalAmount = !isNaN(discountedAmount) ? discountedAmount : originalAmount;

        change = customerAmount - totalAmount;

        if (change >= 0) {
            changeElement.textContent = '₹' + change.toFixed(2);
            changeElement.style.color = '#2c3e50';
        } else {
            changeElement.textContent = '-₹' + Math.abs(change).toFixed(2);
            changeElement.style.color = '#e74c3c';
        }
    }
}


// Submit Transaction Button
const submitButton = document.getElementById("submit-btn");
const btnText = submitButton.querySelector('.btn-text');
const btnSpinner = submitButton.querySelector('.btn-spinner');

submitButton.addEventListener("click", async () => {

    btnText.textContent = "Submitting";
    btnSpinner.style.display = 'inline-block';

    let phone = "";


    const phone2El = document.getElementById('phone-number');       // span
    const spanPhone = phone2El?.textContent.trim();

    if (spanPhone) {
        phone = spanPhone;
    }

    console.log("Phone:", phone);
    console.log(totalAmount);
    console.log(originalAmount);
    console.log(discountedAmount);
    console.log(discount);
    console.log(customerAmount);
    console.log(customer_name);
    console.log(qrcodeidsarray);

    const discountedPercentage = discount ? discount : discountPercent;

    const exchangepostdata = {
        qr_ids: qrcodeidsarray ?? [],
        phone: phone ?? "",
        customer_name: customer_name ?? "",
        total_bill: totalAmount ?? 0,
        original_amount: originalAmount ?? 0,
        discounted_amount: discountedAmount ?? 0,
        discount_percentage: discountedPercentage ?? 0,
        customer_amount: customerAmount ?? 0,
        amount_less_more: (change ?? 0).toFixed(2)
    };
    

    try {
        const response = await fetch("/sales/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: exchangepostdata }),
        });
        console.log("100")

        const result = await response.json();
        console.log(result);
  
        if (result.uploaded_urls === 'uploaded') {
            alert('Product Sold successfully!');
            
            // Reset form
            document.getElementById("tableBody").innerHTML = "";
            document.getElementById("last-purchases").innerHTML = "";
            qrcodeidsarray.length = 0;
            document.getElementById('change-return').textContent = '₹0.00';
            document.getElementById('customer-amount').value = '';
            document.getElementById('discounted-amount').innerHTML = '';
            document.getElementById('discount-input').value = '';
            document.getElementById('discount-section').style.display = 'none';
            document.getElementById("amount").textContent = '0';
            document.getElementById('customer-details').style.display = 'none';
            document.getElementById("customer-name").textContent = '';
            document.getElementById("phone-number").textContent = '';
            document.getElementById("mobile-number").value = '';
            document.getElementById('no-details').style.display = 'none';
        }

    } catch (error) {
        console.error("Submit failed:", error);
    } finally {
        btnText.textContent = "Submit Transaction";
        btnSpinner.style.display = 'none';
    }
});
