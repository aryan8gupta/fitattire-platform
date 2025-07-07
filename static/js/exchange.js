// Exchange Page JavaScript

    // Delete Button Functionality
    // const deleteButtons = document.querySelectorAll('.delete-btn, .delete-icon');
    // const deleteModal = document.getElementById('delete-modal');
    // const closeModalBtn = document.querySelector('.close-modal');
    // const cancelDeleteBtn = document.getElementById('cancel-delete');
    // const confirmDeleteBtn = document.getElementById('confirm-delete');
    // let currentDeleteId = null;

    // // Show delete confirmation modal
    // deleteButtons.forEach(button => {
    //     button.addEventListener('click', function() {
    //         currentDeleteId = this.getAttribute('data-id');
    //         deleteModal.classList.remove('hidden');
    //     });
    // });

    // // Close modal when clicking the X button
    // if (closeModalBtn) {
    //     closeModalBtn.addEventListener('click', function() {
    //         deleteModal.classList.add('hidden');
    //     });
    // }

    // // Close modal when clicking Cancel
    // if (cancelDeleteBtn) {
    //     cancelDeleteBtn.addEventListener('click', function() {
    //         deleteModal.classList.add('hidden');
    //     });
    // }

    // // Handle delete confirmation
    // if (confirmDeleteBtn) {
    //     confirmDeleteBtn.addEventListener('click', function() {
    //         if (currentDeleteId) {
    //             // In a real app, this would send a request to delete the item
    //             // For now, we'll just remove the row from the table
    //             let row = document.querySelector(`.delete-btn[data-id="${currentDeleteId}"]`);
    //             if (!row) {
    //                 row = document.querySelector(`.delete-icon[data-id="${currentDeleteId}"]`);
    //             }

    //             if (row) {
    //                 row.closest('tr').remove();
    //             }

    //             // Close the modal
    //             deleteModal.classList.add('hidden');
    //             currentDeleteId = null;
    //         }
    //     });
    // }

    // // Tab Navigation
    // const tabButtons = document.querySelectorAll('.tab-btn');
    // const exchangeTableBody = document.getElementById('exchange-table-body');

    // // Sample data for exchange history
    // const exchangeData = [
    //     { id: 'P001', name: 'Watch', status: 'Returned', date: '12/05/2023', user: 'John Doe' },
    //     { id: 'P002', name: 'Chain', status: 'Deleted', date: '11/05/2023', user: 'Jane Smith' },
    //     { id: 'P003', name: 'Ring', status: 'Returned', date: '10/05/2023', user: 'John Doe' },
    //     { id: 'P004', name: 'Earrings', status: 'Deleted', date: '09/05/2023', user: 'Jane Smith' },
    //     { id: 'P005', name: 'Bracelet', status: 'Returned', date: '08/05/2023', user: 'John Doe' },
    //     { id: 'P006', name: 'Necklace', status: 'Deleted', date: '07/05/2023', user: 'Jane Smith' },
    //     { id: 'P007', name: 'Pendant', status: 'Returned', date: '06/05/2023', user: 'John Doe' },
    //     { id: 'P008', name: 'Anklet', status: 'Deleted', date: '05/05/2023', user: 'Jane Smith' },
    //     { id: 'P009', name: 'Bangle', status: 'Returned', date: '04/05/2023', user: 'John Doe' },
    //     { id: 'P010', name: 'Cufflinks', status: 'Deleted', date: '03/05/2023', user: 'Jane Smith' }
    // ];

    // // Pagination variables
    // let currentPage = 1;
    // const itemsPerPage = 5;
    // let filteredData = [...exchangeData];

    // // Initialize exchange history table
    // function updateExchangeTable() {
    //     if (!exchangeTableBody) return;

    //     // Clear the table
    //     exchangeTableBody.innerHTML = '';

    //     // Calculate start and end indices for current page
    //     const startIndex = (currentPage - 1) * itemsPerPage;
    //     const endIndex = Math.min(startIndex + itemsPerPage, filteredData.length);

    //     // Add rows for current page
    //     for (let i = startIndex; i < endIndex; i++) {
    //         const item = filteredData[i];
    //         const row = document.createElement('tr');
    //         row.innerHTML = `
    //             <td>${item.id}</td>
    //             <td>${item.name}</td>
    //             <td>${item.status}</td>
    //             <td>${item.date}</td>
    //             <td>${item.user}</td>
    //         `;
    //         exchangeTableBody.appendChild(row);
    //     }

    //     // Update pagination info
    //     const pageInfo = document.getElementById('page-info');
    //     if (pageInfo) {
    //         pageInfo.textContent = ` ${startIndex + 1}-${endIndex} of ${filteredData.length}`;
    //     }

    //     // Update pagination buttons
    //     const prevPageBtn = document.getElementById('prev-page');
    //     const nextPageBtn = document.getElementById('next-page');

    //     if (prevPageBtn) {
    //         prevPageBtn.disabled = currentPage === 1;
    //     }

    //     if (nextPageBtn) {
    //         nextPageBtn.disabled = endIndex >= filteredData.length;
    //     }
    // }

    // // Handle tab clicks
    // tabButtons.forEach(button => {
    //     button.addEventListener('click', function() {
    //         // Remove active class from all tabs
    //         tabButtons.forEach(btn => btn.classList.remove('active'));

    //         // Add active class to clicked tab
    //         this.classList.add('active');

    //         // Filter data based on selected tab
    //         const tabType = this.getAttribute('data-tab');

    //         if (tabType === 'all') {
    //             filteredData = [...exchangeData];
    //         } else if (tabType === 'returned') {
    //             filteredData = exchangeData.filter(item => item.status === 'Returned');
    //         } else if (tabType === 'deleted') {
    //             filteredData = exchangeData.filter(item => item.status === 'Deleted');
    //         }

    //         // Reset to first page and update table
    //         currentPage = 1;
    //         updateExchangeTable();
    //     });
    // });

    // Handle pagination
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');

    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                updateExchangeTable();
            }
        });
    }

    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', function() {
            if (currentPage * itemsPerPage < filteredData.length) {
                currentPage++;
                updateExchangeTable();
            }
        });
    }

    // Product Search Functionality
    const productSearchInput = document.getElementById('product-search');

    if (productSearchInput) {
        productSearchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                const searchTerm = this.value.trim().toLowerCase();

                // In a real app, this would send a request to search for products
                // For now, we'll just log the search term
                console.log('Searching for:', searchTerm);

                // Clear the search input
                this.value = '';
            }
        });
    }

    // Initialize the exchange table
    // updateExchangeTable();

    /*--------------------------------------------------------------
    # Multiple QR Code Scanner Section
    --------------------------------------------------------------*/
    const returnhtml5QrCode = new Html5Qrcode("return-reader");
    const deletehtml5QrCode = new Html5Qrcode("delete-reader");
    let isScanning = false;
    const scannedProductData = {};
    const qrcodeidsarray = [];
    let qrId = "";
    let currentMode = ""; 
    let scanner = "";

    // QR Code Start Buttons Starts  -------------------------------->
    document.getElementById("return-scan-btn").addEventListener("click", async () => {
        document.getElementById("return-reader").style.display = "block";
        document.getElementById("return-cancel-btn").style.display = "block";
        document.getElementById("return-scan-btn").style.display = "none";
        currentMode = "Returned";
        disableOtherButton("return");
        startQrScanner();
    });

    document.getElementById("delete-scan-btn").addEventListener("click", async () => {
        document.getElementById("delete-reader").style.display = "block";
        document.getElementById("delete-cancel-btn").style.display = "block";
        document.getElementById("delete-scan-btn").style.display = "none";
        currentMode = "Deleted";
        disableOtherButton("delete");
        startQrScanner();
    });
    // QR Code Start Buttons Ends  ------------------------------->

    // QR Code Cancel Buttons Starts ------------------------------->
    document.getElementById("return-cancel-btn").addEventListener("click", async () => {
        if (isScanning) {
            returnhtml5QrCode.stop().then(() => {
                isScanning = false;
                document.getElementById("return-reader").style.display = "none";
                document.getElementById("return-cancel-btn").style.display = "none";
                document.getElementById("return-scan-btn").style.display = "block";
            });
        }
    });

    document.getElementById("delete-cancel-btn").addEventListener("click", async () => {
        if (isScanning) {
            deletehtml5QrCode.stop().then(() => {
                isScanning = false;
                document.getElementById("delete-reader").style.display = "none";
                document.getElementById("delete-cancel-btn").style.display = "none";
                document.getElementById("delete-scan-btn").style.display = "block";
            });
        }
    });

    function return_cancel_btn() {
        if (isScanning) {
            console.log("5")
            returnhtml5QrCode.stop().then(() => {
                isScanning = false;
                console.log("6")
                document.getElementById("return-reader").style.display = "none";
                document.getElementById("return-cancel-btn").style.display = "none";
                document.getElementById("return-scan-btn").style.display = "block";
            });
        }
        console.log("8")
    }

    function delete_cancel_btn() {
        if (isScanning) {
            deletehtml5QrCode.stop().then(() => {
                isScanning = false;
                document.getElementById("delete-reader").style.display = "none";
                document.getElementById("delete-cancel-btn").style.display = "none";
                document.getElementById("delete-scan-btn").style.display = "block";
            });
        }
    }
    // QR Code Cancel Buttons Ends  ------------------------------->


    // --- Helper Functions ---

    function disableOtherButton(mode) {
        const returnBtn = document.getElementById("return-scan-btn");
        const deleteBtn = document.getElementById("delete-scan-btn");

        if (mode === "return") {
            deleteBtn.disabled = true;
        } else if (mode === "delete") {
            returnBtn.disabled = true;
        }
    }

    function enableBothButtons() {
        document.getElementById("return-scan-btn").disabled = false;
        document.getElementById("delete-scan-btn").disabled = false;
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
            scanner = currentMode === "Returned" ? returnhtml5QrCode : deletehtml5QrCode;

            await scanner.start(
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

        if (currentMode === "Returned") {
            return_cancel_btn();

            fetch("/get-product-sold/", {
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

        } else {
            delete_cancel_btn();

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
    }

    function displayAllRowsFromDataStore() {
        const tableBody = document.getElementById("tableBody");
        tableBody.innerHTML = "";
    
        for (const qrId in scannedProductData) {
            const dataWrapper = scannedProductData[qrId];
            const data = dataWrapper.data || dataWrapper; // handles both nested and flat cases
            
            const variants = data.variants || [];
    
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
    
                    const returnedTd = document.createElement("td");
                    returnedTd.rowSpan = rowSpan;
                    returnedTd.textContent = currentMode;
    
                    const stockTd = document.createElement("td");
                    stockTd.rowSpan = rowSpan;
                    stockTd.textContent = data.product_quantity || 0;

                    const productNameTd = document.createElement("td");
                    productNameTd.rowSpan = rowSpan;
                    productNameTd.textContent = data.product_name || 0;
    
                    const priceTd = document.createElement("td");
                    priceTd.rowSpan = rowSpan;
                    priceTd.textContent = data.product_price ? `₹${data.product_price * variants.length}` : "N/A";
    
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
                    row.appendChild(returnedTd);
                    row.appendChild(stockTd);
                    row.appendChild(priceTd);
                    row.appendChild(actionTd);
                }
    
                tableBody.appendChild(row);
            });
        }
    }

    document.getElementById("submit-btn").addEventListener("click", async () => {
        exchangepostdata = {
            'qr_ids': qrcodeidsarray,
            'status': currentMode,
        }
        try {
            const response = await fetch("/exchange/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ data: exchangepostdata }),
            });
            console.log("100")
    
            const result = await response.json();
            console.log(result.exchange_data)

            document.getElementById("tableBody").innerHTML = "";
            qrcodeidsarray.length = 0;
            enableBothButtons();

            updateExchangeTable(result.exchange_data);  // update bottom table
        } catch (error) {
            console.error("Submit failed:", error);
        }

    });
    
    function updateExchangeTable(data) {
        const tableBody = document.getElementById("exchangeTableBody");
        tableBody.innerHTML = "";
        
        console.log("200")
        console.log(data)
        // Sort by date ascending
        data.sort((a, b) => new Date(b.date) - new Date(a.date));
        console.log("300")
    
        data.forEach(entry => {
            const row = document.createElement("tr");
    
            // const variants = entry.variants.map(v => v.color).join(", ");
    
            row.innerHTML = `
                <td>${entry.qr_id}</td>
                <td>${entry.product_name}</td>
                <td>${entry.status}</td>
                <td>${entry.date}</td>
            `;
            tableBody.appendChild(row);
        });
    }
    

    document.addEventListener("DOMContentLoaded", () => {
        updateExchangeTable(exchangeFirstData);
    });
