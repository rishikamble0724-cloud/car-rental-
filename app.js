// ============================================================
//  CAR RENTAL SYSTEM  -  FRONTEND LOGIC (JavaScript)
// ============================================================
//  On Vercel the backend runs on the SAME site under /api,
//  so no link needs to be pasted here. It just works.
// ============================================================

const BACKEND_URL = "/api";

// ---------- load cars + bookings ----------
async function loadData() {
  try {
    const cars = await (await fetch(BACKEND_URL + "/cars")).json();
    document.getElementById("carTable").innerHTML = cars
      .map((c) => `<tr><td>${c.id}</td><td>${c.brand}</td><td>${c.name}</td><td>${c.price}</td></tr>`)
      .join("");

    const books = await (await fetch(BACKEND_URL + "/bookings")).json();
    document.getElementById("bookTable").innerHTML = books
      .map((b) => `<tr><td>${b.id}</td><td>${b.customer}</td><td>${b.car}</td><td>${b.days}</td><td>${b.amount}</td></tr>`)
      .join("");
  } catch (e) {
    document.getElementById("msg").style.color = "red";
    document.getElementById("msg").innerText = "Cannot reach backend.";
  }
}

// ---------- book a car ----------
async function bookCar() {
  const customer = document.getElementById("customer").value;
  const carId = document.getElementById("carId").value;
  const days = document.getElementById("days").value;

  if (!customer || !carId || !days) {
    alert("Please fill all fields");
    return;
  }

  try {
    const res = await fetch(BACKEND_URL + "/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer: customer, car_id: Number(carId), days: Number(days) }),
    });
    const data = await res.json();
    document.getElementById("msg").style.color = "green";
    document.getElementById("msg").innerText = "Booking done! Total Amount = Rs " + data.amount;
    loadData();
  } catch (e) {
    document.getElementById("msg").style.color = "red";
    document.getElementById("msg").innerText = "Error: " + e.message;
  }
}

// load tables when page opens
loadData();
