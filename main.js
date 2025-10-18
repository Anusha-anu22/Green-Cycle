let LANG_DATA = {};
let currentLang = "en";

// Initial texts update
document.addEventListener('DOMContentLoaded', () => setLanguage(currentLang));

// Multi-language loader
function setLanguage(lang) {
  currentLang = lang;
  fetch('http://localhost:3000/lang_texts/' + lang)
    .then(res => res.json())
    .then(t => {
      LANG_DATA = t;
      setLangUI();
      reloadFarmers();
    });
}

function setLangUI() {
  document.getElementById('dashboard').innerText = LANG_DATA.dashboard;
  document.getElementById('subtitle').innerText = LANG_DATA.subtitle;
  document.getElementById('welcome').innerText = LANG_DATA.welcome;
  document.getElementById('subtitle2').innerText = LANG_DATA.subtitle;
  document.getElementById('profile_title').innerText = LANG_DATA.profile;
  document.getElementById('label_name').innerText = LANG_DATA.name;
  document.getElementById('label_email').innerText = LANG_DATA.email;
  document.getElementById('label_phone').innerText = LANG_DATA.phone;
  document.getElementById('label_address').innerText = LANG_DATA.address;
  document.getElementById('saveBtn').innerText = LANG_DATA.save;
  document.getElementById('logoutNav').innerText = LANG_DATA.logout;

  document.getElementById('waste_contribution_title').innerText = LANG_DATA.waste_contribution;
  document.getElementById('waste_name').placeholder = LANG_DATA.waste_name;
  document.getElementById('waste_amount').placeholder = LANG_DATA.waste_amount;
  document.getElementById('submit_contribution').innerText = LANG_DATA.submit_contribution;

  document.getElementById('schedule_pickup_title').innerText = LANG_DATA.schedule_pickup;
  document.getElementById('pickup_name').placeholder = LANG_DATA.pickup_name;
  document.getElementById('pickup_phone').placeholder = LANG_DATA.pickup_phone;
  document.getElementById('pickup_address').placeholder = LANG_DATA.pickup_address;
  document.getElementById('pickup_district').placeholder = LANG_DATA.pickup_district;
  document.getElementById('pickup_pincode').placeholder = LANG_DATA.pickup_pincode;
  document.getElementById('pickup_state').placeholder = LANG_DATA.pickup_state;
  document.getElementById('pickup_submit').innerText = LANG_DATA.pickup_submit;

  document.getElementById('pickup_tracking_title').innerText = LANG_DATA.pickup_tracking;
  document.getElementById('tracking_phone').placeholder = LANG_DATA.track_phone;
  document.getElementById('track_submit').innerText = LANG_DATA.track_submit;
  document.getElementById('track_name').innerText = LANG_DATA.name;
  document.getElementById('track_phone_title').innerText = LANG_DATA.phone;
  document.getElementById('track_address').innerText = LANG_DATA.address;
  document.getElementById('track_status').innerText = LANG_DATA.delivery_status;

  // Farmer UI
  document.getElementById('farmer_section').innerText = LANG_DATA.farmer_section;
  document.getElementById('farmer_name').placeholder = LANG_DATA.farmer_name;
  document.getElementById('farmer_phone').placeholder = LANG_DATA.farmer_phone;
  document.getElementById('farmer_address').placeholder = LANG_DATA.farmer_address;
  document.getElementById('add_farmer').innerText = LANG_DATA.add_farmer;
  document.getElementById('farmer_details').innerText = LANG_DATA.farmer_details;
  document.getElementById('farmer_name_title').innerText = LANG_DATA.farmer_name;
  document.getElementById('farmer_phone_title').innerText = LANG_DATA.farmer_phone;
  document.getElementById('farmer_address_title').innerText = LANG_DATA.farmer_address;
  document.getElementById('composted_kg').innerText = LANG_DATA.composted_kg;
  document.getElementById('compost_btn_title').innerText = LANG_DATA.compost_btn;
  document.getElementById('delivery_section').innerText = LANG_DATA.delivery_section;
  document.getElementById('assign_delivery').innerText = LANG_DATA.assign_delivery;
  document.getElementById('delivery_farmer_title').innerText = LANG_DATA.farmer_name;
  document.getElementById('delivery_amount_title').innerText = LANG_DATA.delivery_amount;
  document.getElementById('delivery_status_title').innerText = LANG_DATA.delivery_status;
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
function showSection(sectionId) {
  closeNav();
  const sections = document.querySelectorAll('.section');
  sections.forEach(s => s.style.display = 'none');
  const section = document.getElementById(sectionId);
  if (section) section.style.display = 'block';
  if (sectionId === 'profile') loadProfile();
  if (sectionId === 'farmerSection') reloadFarmers();
}

// Profile
function loadProfile() {
  fetch('http://localhost:3000/profileData.json')
    .then(res => res.json())
    .then(data => {
      document.getElementById('name').value = data.name || '';
      document.getElementById('email').value = data.email || '';
      document.getElementById('phone').value = data.phone || '';
      document.getElementById('address').value = data.address || '';
    }).catch(() => alert('Error loading profile'));
}
function saveProfile() {
  const profileData = {
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    address: document.getElementById('address').value.trim(),
  };
  fetch('http://localhost:3000/profile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData)
  }).then(res => res.json())
    .then(data => {
      document.getElementById('msg').textContent = data.success
        ? LANG_DATA.profile_saved
        : LANG_DATA.failed + " " + data.error;
      document.getElementById('msg').style.color = data.success ? 'green' : 'red';
    }).catch(() => alert('Error saving profile'));
}

// Waste
document.getElementById('wasteForm').addEventListener('submit', async e => {
  e.preventDefault();
  const name = document.getElementById('waste_name').value.trim();
  const amount = Number(document.getElementById('waste_amount').value);
  const res = await fetch('http://localhost:3000/waste', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, amount })
  });
  const data = await res.json();
  const waste_msg = document.getElementById('waste_msg');
  if (data.success) {
    waste_msg.textContent =
      `${LANG_DATA.thank_you}, ${name}! ${LANG_DATA.points_earned} ${data.entry.points} ${LANG_DATA.points}.`;
    waste_msg.classList.remove('error');
    e.target.reset();
  } else {
    waste_msg.textContent = `${LANG_DATA.contribution_failed} ` + (data.error || '');
    waste_msg.classList.add('error');
  }
});

// Pickup
document.getElementById('pickupForm').addEventListener('submit', async e => {
  e.preventDefault();
  const payload = {
    name: document.getElementById('pickup_name').value.trim(),
    phone: document.getElementById('pickup_phone').value.trim(),
    address: document.getElementById('pickup_address').value.trim(),
    district: document.getElementById('pickup_district').value.trim(),
    pincode: document.getElementById('pickup_pincode').value.trim(),
    state: document.getElementById('pickup_state').value.trim()
  };
  const res = await fetch('http://localhost:3000/pickup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  const pickup_msg = document.getElementById('pickup_msg');
  pickup_msg.textContent = data.success
    ? LANG_DATA.pickup_scheduled
    : LANG_DATA.failed + " " + (data.error || '');
  pickup_msg.classList.toggle('error', !data.success);
  if (data.success) e.target.reset();
});

// Pickup tracking
document.getElementById('trackingForm').addEventListener('submit', async e => {
  e.preventDefault();
  const phone = document.getElementById('tracking_phone').value.trim();
  const res = await fetch('http://localhost:3000/pickup/tracking', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone })
  });
  const data = await res.json();
  const tracking_msg = document.getElementById('tracking_msg');
  const table = document.getElementById('tracking_table');
  const tbody = table.querySelector('tbody');
  tbody.innerHTML = '';
  if (data.success) {
    tracking_msg.textContent = '';
    table.style.display = 'table';
    data.tracking.forEach(pickup => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${pickup.name}</td><td>${pickup.phone}</td><td>${pickup.address}</td><td>${pickup.status}</td>`;
      tbody.appendChild(tr);
    });
  } else {
    tracking_msg.textContent = `${LANG_DATA.tracking_failed} ` + (data.error || '');
    tracking_msg.classList.add('error');
    table.style.display = 'none';
  }
});

function logout() {
  alert('You have been logged out.');
}

// Farmer section
document.getElementById('addFarmerForm').addEventListener('submit', async e => {
  e.preventDefault();
  const name = document.getElementById('farmer_name').value.trim();
  const phone = document.getElementById('farmer_phone').value.trim();
  const address = document.getElementById('farmer_address').value.trim();
  let res = await fetch('http://localhost:3000/farmers', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name, phone, address})
  });
  let data = await res.json();
  document.getElementById('add_farmer_msg').textContent =
    data.success ? LANG_DATA.add_farmer + " successful!" : data.error || LANG_DATA.failed;
  if(data.success) reloadFarmers();
});

async function reloadFarmers() {
  let res = await fetch('http://localhost:3000/farmers');
  let farmers = await res.json();
  let tbody = document.querySelector('#farmersTable tbody');
  let dropdown = document.getElementById('farmers_dropdown');
  tbody.innerHTML = '';
  dropdown.innerHTML = '';
  farmers.forEach(f => {
    let tr = document.createElement('tr');
    tr.innerHTML = `<td>${f.name}</td><td>${f.phone}</td><td>${f.address}</td>
      <td>${f.composted_kg}</td>
      <td><button onclick="compostFarmer(${f.id})">${LANG_DATA.compost_btn || 'Compost'}</button></td>`;
    tbody.appendChild(tr);
    let opt = document.createElement('option');
    opt.value = f.id;
    opt.textContent = f.name;
    dropdown.appendChild(opt);
  });
  reloadDeliveries();
}

window.compostFarmer = async function(fid) {
  let amount = prompt(LANG_DATA.composted_kg + "?");
  if(!amount || isNaN(amount)) return;
  await fetch(`http://localhost:3000/farmer_compost/${fid}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({composted_kg: parseFloat(amount)})
  });
  reloadFarmers();
};

document.getElementById('assignDeliveryForm').addEventListener('submit', async e => {
  e.preventDefault();
  let fid = document.getElementById('farmers_dropdown').value;
  let kg = document.getElementById('delivery_amount').value;
  let res = await fetch('http://localhost:3000/assign_delivery', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({farmer_id: fid, waste_amount_kg: kg})
  });
  let data = await res.json();
  document.getElementById('assign_delivery_msg').textContent =
    data.success ? "Delivery assigned" : data.error || LANG_DATA.failed;
  if(data.success) reloadDeliveries();
});

async function reloadDeliveries() {
  let res = await fetch('http://localhost:3000/farmer_deliveries');
  let deliveries = await res.json();
  let tbody = document.querySelector('#deliveryTable tbody');
  tbody.innerHTML = '';
  deliveries.forEach(d => {
    let tr = document.createElement('tr');
    tr.innerHTML = `<td>${d.farmer_name}</td><td>${d.waste_amount_kg}</td><td>${d.status}</td>`;
    tbody.appendChild(tr);
  });
}

// ----- Image Slider -----
const slides = document.getElementById('slides');
const leftArrow = document.querySelector('.nav-left');
const rightArrow = document.querySelector('.nav-right');
const totalImages = slides ? slides.children.length : 0;
const slideWidth = 600;
let currentIndex = 0;
function updateSlidePosition() {
  slides.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}
if(leftArrow && rightArrow && slides) {
  leftArrow.addEventListener('click', () => {
    currentIndex = currentIndex === 0 ? totalImages - 1 : currentIndex - 1;
    updateSlidePosition();
    resetAutoSlide();
  });
  rightArrow.addEventListener('click', () => {
    currentIndex = currentIndex === totalImages - 1 ? 0 : currentIndex + 1;
    updateSlidePosition();
    resetAutoSlide();
  });
  let autoSlide = setInterval(() => {
    currentIndex = (currentIndex + 1) % totalImages;
    updateSlidePosition();
  }, 3000);
  function resetAutoSlide() {
    clearInterval(autoSlide);
    autoSlide = setInterval(() => {
      currentIndex = (currentIndex + 1) % totalImages;
      updateSlidePosition();
    }, 3000);
  }
}