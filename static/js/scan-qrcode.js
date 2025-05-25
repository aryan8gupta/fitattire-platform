const scanBtn = document.getElementById("scan-btn");
const cancelBtn = document.getElementById("cancel-btn");
const readerDiv = document.getElementById("reader");
const html5QrCode = new Html5Qrcode("reader");

let isScanning = false;

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

    // 🔄 Choose rear camera if available
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
        html5QrCode.stop().then(() => {
          isScanning = false;
          cancelBtn.style.display = "none";
          readerDiv.style.display = "none";
          scanBtn.style.display = "block";

          // ✅ Extract last 6 characters from the scanned URL
          const shortCode = decodedText.slice(-6);

          // ✅ Navigate to the backend route
          window.location.href = `/product-display/${shortCode}`;


          // try {
          //   const url = new URL(decodedText);
          //   window.location.href = url.href;
          // } catch {
          //   alert("Scanned: " + decodedText);
          //   window.location.reload();
          // }
        });
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
