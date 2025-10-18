from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

users = []
otp_store = {}
profile_data = {}
waste_contributions = []
pickup_schedules = []
pickup_tracking = []
farmers = []
farmer_deliveries = []

LANG_TEXTS = {
    "en": {
        "dashboard": "Green Cycle Dashboard",
        "welcome": "Welcome to Green Cycle!",
        "subtitle": "Join our mission to turn kitchen waste into organic compost for a cleaner planet.",
        "profile": "Your Profile",
        "name": "Name",
        "email": "E-mail",
        "phone": "Phone Number",
        "address": "Address",
        "save": "Save",
        "waste_contribution": "Waste Contribution",
        "waste_name": "Your Name",
        "waste_amount": "Waste Amount (kg)",
        "submit_contribution": "Submit Contribution",
        "schedule_pickup": "Schedule Waste Pickup",
        "pickup_name": "Name",
        "pickup_phone": "Phone Number",
        "pickup_address": "Address",
        "pickup_district": "District",
        "pickup_pincode": "Pincode",
        "pickup_state": "State",
        "pickup_submit": "Schedule Pickup",
        "pickup_tracking": "Pickup Tracking",
        "track_phone": "Enter Phone Number",
        "track_submit": "Track Pickup",
        "farmer_section": "Farmer Compost Management",
        "farmer_details": "Farmer Details",
        "add_farmer": "Add Farmer",
        "farmer_name": "Farmer Name",
        "farmer_phone": "Contact Number",
        "farmer_address": "Farm Address",
        "composted_kg": "Composted (kg)",
        "compost_btn": "Add Compost",
        "waste_delivery": "Waste Delivery to Farmer",
        "delivery_section": "Assign/Track Waste Delivery",
        "assign_delivery": "Assign Delivery",
        "deliver_to_farmer": "Deliver to Farmer",
        "delivery_farmer": "Farmer",
        "delivery_amount": "Delivered (kg)",
        "delivery_status": "Delivery Status",
        "logout": "Logout",
        "profile_saved": "Profile saved successfully!",
        "pickup_scheduled": "Pickup scheduled successfully!",
        "otp_alert": "Your OTP is: ",
        "thank_you": "Thank you",
        "points_earned": "You earned",
        "points": "points",
        "contribution_failed": "Contribution failed:",
        "failed": "Failed:",
        "tracking_failed": "Tracking failed:"
    },
    "te": {
        "dashboard": "గ్రీన్ సైకిల్ డాష్‌బోర్డ్",
        "welcome": "గ్రీన్ సైకిల్‌కు స్వాగతం!",
        "subtitle": "పరిశుభ్రమైన గ్రహం కోసం వంటగది వ్యర్థాలను సేంద్రీయ కంపోస్టుగా మార్చడంలో మాతో కలిసి భాగమవ్వండి.",
        "profile": "మీ వివరాలు",
        "name": "పేరు",
        "email": "ఈ-మెయిల్",
        "phone": "ఫోన్ నంబర్",
        "address": "చిరునామా",
        "save": "సేవ్ చేయండి",
        "waste_contribution": "వ్యర్థం అందించడం",
        "waste_name": "మీ పేరు",
        "waste_amount": "వ్యర్థం (కిలోలు)",
        "submit_contribution": "అందించండి",
        "schedule_pickup": "వ్యర్థం పికప్‌ను షెడ్యూల్ చేయండి",
        "pickup_name": "పేరు",
        "pickup_phone": "ఫోన్ నంబర్",
        "pickup_address": "చిరునామా",
        "pickup_district": "జిల్లా",
        "pickup_pincode": "పిన్ కోడ్",
        "pickup_state": "రాష్ట్రం",
        "pickup_submit": "పికప్‌ను షెడ్యూల్ చేయండి",
        "pickup_tracking": "పికప్ ట్రాకింగ్",
        "track_phone": "ఫోన్ నంబర్ ఇవ్వండి",
        "track_submit": "ట్రాక్ చేయండి",
        "farmer_section": "రైతు కంపోస్ట్ నిర్వహణ",
        "farmer_details": "రైతు వివరాలు",
        "add_farmer": "రైతును జోడించండి",
        "farmer_name": "రైతు పేరు",
        "farmer_phone": "సంప్రదింపు సంఖ్య",
        "farmer_address": "ఫార్మ్ చిరునామా",
        "composted_kg": "కంపోస్టు (కిలోలలో)",
        "compost_btn": "కంపోస్టు జోడించండి",
        "waste_delivery": "వ్యర్థాన్ని రైతుకు పంపు",
        "delivery_section": "డెలివరీ అప్పగింత/ట్రాకింగ్",
        "assign_delivery": "డెలివరీ అప్పగించు",
        "deliver_to_farmer": "రైతుకు డెలివరీ చేయండి",
        "delivery_farmer": "రైతు",
        "delivery_amount": "డెలివరీ (కిలోలు)",
        "delivery_status": "స్టేటస్",
        "logout": "లాగౌట్",
        "profile_saved": "వివరాలు సేవ్‌య్యాయి!",
        "pickup_scheduled": "పికప్ షెడ్యూల్ అయింది!",
        "otp_alert": "మీ OTP:",
        "thank_you": "ధన్యవాదాలు",
        "points_earned": "మీకు లభించిన పాయింట్లు",
        "points": "పాయింట్లు",
        "contribution_failed": "అందించడం విఫలమైంది:",
        "failed": "విఫలమైంది:",
        "tracking_failed": "ట్రాకింగ్ విఫలమైంది:"
    },
    "hi": {
        "dashboard": "ग्रीन साइकिल डैशबोर्ड",
        "welcome": "ग्रीन साइकिल में आपका स्वागत है!",
        "subtitle": "एक स्वच्छ पृथ्वी के लिए किचन वेस्ट को ऑर्गेनिक कम्पोस्ट में बदलने के हमारे मिशन से जुड़ें।",
        "profile": "आपकी प्रोफ़ाइल",
        "name": "नाम",
        "email": "ईमेल",
        "phone": "फोन नंबर",
        "address": "पता",
        "save": "सेव करें",
        "waste_contribution": "कचरा योगदान",
        "waste_name": "आपका नाम",
        "waste_amount": "कचरा (किलो)",
        "submit_contribution": "योगदान भेजें",
        "schedule_pickup": "कचरा पिकअप शेड्यूल करें",
        "pickup_name": "नाम",
        "pickup_phone": "फोन नंबर",
        "pickup_address": "पता",
        "pickup_district": "जिला",
        "pickup_pincode": "पिनकोड",
        "pickup_state": "राज्य",
        "pickup_submit": "शेड्यूल करें",
        "pickup_tracking": "पिकअप ट्रैकिंग",
        "track_phone": "फोन नंबर दर्ज करें",
        "track_submit": "ट्रैक करें",
        "farmer_section": "किसान कम्पोस्ट प्रबंधन",
        "farmer_details": "किसान विवरण",
        "add_farmer": "किसान जोड़ें",
        "farmer_name": "किसान का नाम",
        "farmer_phone": "संपर्क नंबर",
        "farmer_address": "फॉर्म का पता",
        "composted_kg": "कम्पोस्ट (किलो)",
        "compost_btn": "कम्पोस्ट जोड़े",
        "waste_delivery": "कचरा किसान तक डेलिवरी",
        "delivery_section": "डेलिवरी असाइन/ट्रैकिंग",
        "assign_delivery": "डेलिवरी असाइन करें",
        "deliver_to_farmer": "किसान को पहुंचाएं",
        "delivery_farmer": "किसान",
        "delivery_amount": "कितना डेलिवर हुआ (किलो)",
        "delivery_status": "डेलिवरी स्थिति",
        "logout": "लॉगआउट",
        "profile_saved": "प्रोफाइल सेव हो गई!",
        "pickup_scheduled": "पिकअप शेड्यूल हुआ!",
        "otp_alert": "आपका OTP है:",
        "thank_you": "धन्यवाद",
        "points_earned": "आपको मिले",
        "points": "पॉइंट्स",
        "contribution_failed": "योगदान असफल:",
        "failed": "असफल:",
        "tracking_failed": "ट्रैकिंग असफल रही:"
    }
}

@app.route('/lang_texts/<lang>')
def get_lang_texts(lang):
    return jsonify(LANG_TEXTS.get(lang, LANG_TEXTS["en"]))

@app.route('/farmers', methods=['GET', 'POST'])
def farmer_list():
    if request.method == 'GET':
        return jsonify(farmers)
    data = request.json
    required = ['name', 'phone', 'address']
    if not all(k in data and data[k] for k in required):
        return jsonify({"success": False, "error": "Missing required fields"})
    farmer = {
        "id": len(farmers) + 1,
        "name": data['name'],
        "phone": data['phone'],
        "address": data['address'],
        "composted_kg": data.get('composted_kg', 0)
    }
    farmers.append(farmer)
    return jsonify({"success": True, "farmer": farmer})

@app.route('/farmers/<int:fid>', methods=['GET'])
def single_farmer(fid):
    f = next((farmer for farmer in farmers if farmer['id']==fid), None)
    return jsonify(f) if f else jsonify({"error": "Not found"}), 404 if not f else 200

@app.route('/farmer_compost/<int:fid>', methods=['POST'])
def update_farmer_compost(fid):
    data = request.json
    amount = data.get('composted_kg')
    for farmer in farmers:
        if farmer["id"] == fid:
            farmer["composted_kg"] = farmer.get("composted_kg", 0) + float(amount)
            return jsonify({"success": True, "farmer": farmer})
    return jsonify({"success": False, "error": "Farmer not found"})

@app.route('/assign_delivery', methods=['POST'])
def assign_delivery():
    data = request.json
    required = ['waste_amount_kg', 'farmer_id']
    if not all(k in data and data[k] for k in required):
        return jsonify({"success": False, "error": "Missing required fields"})
    delivery = {
        "id": len(farmer_deliveries) + 1,
        "farmer_id": data['farmer_id'],
        "waste_amount_kg": data['waste_amount_kg'],
        "status": "Assigned"
    }
    farmer_deliveries.append(delivery)
    return jsonify({"success": True, "delivery": delivery})

@app.route('/farmer_deliveries', methods=['GET'])
def get_deliveries():
    res = []
    for d in farmer_deliveries:
        farmer = next((f for f in farmers if f['id'] == d['farmer_id']), None)
        entry = {**d, "farmer_name": farmer["name"] if farmer else "?"}
        res.append(entry)
    return jsonify(res)

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    data = request.json
    phone = data.get('phone')
    if not phone or len(phone) != 10 or not phone.isdigit():
        return jsonify({"success": False, "error": "Invalid phone number"})
    otp = str(random.randint(100000, 999999))
    otp_store[phone] = otp
    return jsonify({"success": True, "otp": otp, "message": f"OTP generated for {phone}"})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone = data.get('phone')
    otp = data.get('otp')
    if otp_store.get(phone) == otp:
        otp_store.pop(phone, None)
        return jsonify({"success": True, "message": "OTP verified"})
    else:
        return jsonify({"success": False, "error": "Invalid OTP"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    required = ['name', 'username', 'email', 'password', 'phone', 'otp']
    if not all(field in data for field in required):
        return jsonify({"success": False, "error": "Missing required fields"})
    phone = data['phone']
    otp = data['otp']
    if otp_store.get(phone) != otp:
        return jsonify({"success": False, "error": "OTP not verified or invalid"})
    for u in users:
        if u['email'] == data['email']:
            return jsonify({"success": False, "error": "Email already registered"})
        if u['username'] == data['username']:
            return jsonify({"success": False, "error": "Username already taken"})
    user = {
        "name": data['name'],
        "username": data['username'],
        "email": data['email'],
        "password": data['password'],
        "phone": data['phone']
    }
    users.append(user)
    profile_data.update({
        "name": user['name'],
        "email": user['email'],
        "phone": user['phone'],
        "address": ""
    })
    pickup_tracking.append({
        "name": user['name'],
        "phone": user['phone'],
        "address": "",
        "status": "No pickups yet"
    })
    otp_store.pop(phone, None)
    return jsonify({"success": True, "message": "Registration successful"})

@app.route('/profileData.json', methods=['GET'])
def get_profile():
    return jsonify(profile_data)

@app.route('/profile', methods=['POST'])
def save_profile():
    data = request.json
    profile_data.update(data)
    for pickup in pickup_tracking:
        if pickup['phone'] == data.get('phone'):
            pickup['name'] = data.get('name', pickup['name'])
            pickup['address'] = data.get('address', pickup['address'])
    return jsonify({"success": True, "message": "Profile updated!"})

@app.route('/waste', methods=['POST'])
def add_waste():
    data = request.json
    name = data.get('name')
    amount = data.get('amount')
    if not name or not amount or amount <= 0:
        return jsonify({"success": False, "error": "Invalid name or amount"})
    points = int(amount * 10)
    entry = {"name": name, "amount": amount, "points": points}
    waste_contributions.append(entry)
    return jsonify({"success": True, "entry": entry})

@app.route('/pickup', methods=['POST'])
def schedule_pickup():
    data = request.json
    required_fields = ['name', 'phone', 'address', 'district', 'pincode', 'state']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "error": f"Missing field: {field}"})
    data["status"] = "Scheduled"
    pickup_schedules.append(data)
    updated = False
    for pickup in pickup_tracking:
        if pickup['phone'] == data['phone']:
            pickup.update({
                "name": data['name'],
                "address": data['address'],
                "status": "Scheduled"
            })
            updated = True
            break
    if not updated:
        pickup_tracking.append({
            "name": data['name'],
            "phone": data['phone'],
            "address": data['address'],
            "status": "Scheduled"
        })
    return jsonify({"success": True, "message": "Pickup scheduled successfully!"})

@app.route('/pickup/tracking', methods=['POST'])
def get_tracking():
    data = request.json
    phone = data.get('phone')
    if not phone:
        return jsonify({"success": False, "error": "Phone number required for tracking"})
    user_pickups = [p for p in pickup_tracking if p["phone"] == phone]
    if not user_pickups:
        return jsonify({"success": False, "error": "No pickup found for this phone"})
    return jsonify({"success": True, "tracking": user_pickups})

if __name__ == '__main__':
    app.run(debug=True, port=3000)