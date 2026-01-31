 so tb  
 # 📅 Complete Appointment Automation Setup Guide
## No-Code Solution with Make.com + Google Calendar + WhatsApp

---

## ✅ STEP 1 — COMPLETED!

Your Tally form is already embedded on your website at `/consult` page.

**Form Link:** https://tally.so/r/WOOzOR

**Embedded Code:**
```html
<iframe src="https://tally.so/r/WOOzOR" width="100%" height="600px"></iframe>
```

---

## 📆 STEP 2 — Create Google Calendar for Appointments

### Instructions:

1. **Go to Google Calendar:**
   - Visit: https://calendar.google.com

2. **Create New Calendar:**
   - On the left sidebar, click the **+** next to "Other calendars"
   - Select **"Create new calendar"**

3. **Configure Calendar:**
   - **Name:** `Health Care Appointments` or `Bookings Calendar`
   - **Description:** `Patient consultation appointments`
   - **Time zone:** Select your timezone
   - Click **"Create calendar"**

4. **Get Calendar ID:**
   - Click on your new calendar → Settings
   - Scroll down to **"Integrate calendar"**
   - Copy the **Calendar ID** (looks like: `abc123@group.calendar.google.com`)
   - **Save this ID** - you'll need it for Make.com!

---

## 🔗 STEP 3 — Create Make.com Automation (NO CODE)

### 3.1 Setup Make.com Account

1. Go to: https://www.make.com
2. Click **"Sign up for free"**
3. Verify your email
4. Login to dashboard

### 3.2 Create New Scenario

1. Click **"Create a new scenario"**
2. Name it: `Health Care Appointment Booking`

### 3.3 Add Modules (Step-by-Step)

#### MODULE 1: Tally Webhook Trigger

1. Click **+** to add first module
2. Search for **"Tally"**
3. Select **"Watch Form Responses"**
4. Click **"Create a connection"**
5. Connect your Tally account
6. Select your form: `WOOzOR`
7. Click **"OK"**

**Alternative if Tally module not available:**
1. Search **"Webhooks"**
2. Select **"Custom webhook"**
3. Click **"Add"**
4. Name it: `Tally Form Webhook`
5. Copy the webhook URL (e.g., `https://hook.eu1.make.com/xxxxx`)
6. Go to Tally.so → Your form → Settings → Integrations → Webhooks
7. Paste the webhook URL
8. Save

#### MODULE 2: Google Calendar - Check Availability

1. Click **+** after webhook module
2. Search **"Google Calendar"**
3. Select **"Search Events"**
4. Connect your Google account
5. Select your **"Health Care Appointments"** calendar
6. Configure:
   - **Calendar ID:** Your calendar ID from Step 2
   - **Start Date:** `{{1.date}}` (from form)
   - **End Date:** `{{1.date}}` (same day)
7. Click **"OK"**

#### MODULE 3: Router (for availability check)

1. Click **+** after Search Events
2. Search **"Router"**
3. Add Router module
4. This will create two paths:
   - Path 1: If slot is available
   - Path 2: If slot is taken

#### MODULE 4A: Create Calendar Event (If Available)

**On Path 1:**
1. Add filter: `Total number of bundles = 0` (no existing events)
2. Click **+** on Path 1
3. Search **"Google Calendar"**
4. Select **"Create an Event"**
5. Configure:
   - **Calendar ID:** Your calendar ID
   - **Summary:** `Appointment - {{1.name}}`
   - **Description:** 
     ```
     Patient: {{1.name}}
     Email: {{1.email}}
     Phone: {{1.phone}}
     Service: {{1.service}}
     Notes: {{1.notes}}
     ```
   - **Start Date:** `{{1.date}} {{1.time}}`
   - **End Date:** Add 30 minutes to start time
   - **Attendees:** `{{1.email}}`
   - **Send Notifications:** Yes
6. Click **"OK"**

#### MODULE 5A: Send Confirmation Email (Patient)

1. Click **+** after Create Event
2. Search **"Gmail"** or **"Email"**
3. Select **"Send an Email"**
4. Configure:
   - **To:** `{{1.email}}`
   - **Subject:** `✅ Appointment Confirmed - Health Care`
   - **Content:**
     ```
     Dear {{1.name}},

     Your appointment has been confirmed!

     📅 Date: {{1.date}}
     ⏰ Time: {{1.time}}
     🏥 Service: {{1.service}}
     
     We look forward to seeing you!
     
     If you need to reschedule, please contact us at:
     📧 Email: your-email@example.com
     📱 Phone: +1234567890
     
     Best regards,
     Health Care Team
     ```
5. Click **"OK"**

#### MODULE 6A: Send Admin Notification

1. Click **+** after patient email
2. Search **"Gmail"**
3. Select **"Send an Email"**
4. Configure:
   - **To:** `your-admin-email@example.com`
   - **Subject:** `🔔 New Appointment Booked`
   - **Content:**
     ```
     New appointment booked:
     
     Patient: {{1.name}}
     Email: {{1.email}}
     Phone: {{1.phone}}
     Date: {{1.date}}
     Time: {{1.time}}
     Service: {{1.service}}
     Notes: {{1.notes}}
     
     Check Google Calendar for details.
     ```
5. Click **"OK"**

#### MODULE 7A: Save to Google Sheets (Optional)

1. Click **+** after admin email
2. Search **"Google Sheets"**
3. Select **"Add a Row"**
4. Connect Google account
5. Select your spreadsheet (create one first)
6. Map columns:
   - Column A: `{{1.name}}`
   - Column B: `{{1.email}}`
   - Column C: `{{1.phone}}`
   - Column D: `{{1.date}}`
   - Column E: `{{1.time}}`
   - Column F: `{{1.service}}`
   - Column G: `{{1.notes}}`
   - Column H: `{{now}}`
7. Click **"OK"**

#### MODULE 4B: Send "Slot Not Available" Email

**On Path 2:**
1. Add filter: `Total number of bundles > 0` (slot taken)
2. Click **+** on Path 2
3. Search **"Gmail"**
4. Select **"Send an Email"**
5. Configure:
   - **To:** `{{1.email}}`
   - **Subject:** `❌ Time Slot Not Available`
   - **Content:**
     ```
     Dear {{1.name}},

     Unfortunately, the time slot you selected is no longer available.

     Requested: {{1.date}} at {{1.time}}

     Please visit our website to choose another time:
     http://localhost:5000/consult

     We apologize for the inconvenience.

     Best regards,
     Health Care Team
     ```
6. Click **"OK"**

### 3.4 Save and Activate

1. Click **"Save"** (bottom right)
2. Toggle **"Scheduling"** to **ON**
3. Set to run: **Immediately** (real-time)
4. Click **"Run once"** to test

---

## 📱 STEP 4 — Add WhatsApp Notifications (Optional)

### Option A: Using WhatsApp Cloud API (Free - 1000 messages/month)

1. Go to: https://developers.facebook.com
2. Create a Meta Business account
3. Create an app → Select **"Business"**
4. Add **WhatsApp** product
5. Get your:
   - Phone Number ID
   - Access Token
6. In Make.com:
   - Add **"HTTP"** module after email
   - Method: **POST**
   - URL: `https://graph.facebook.com/v17.0/YOUR_PHONE_ID/messages`
   - Headers:
     - `Authorization: Bearer YOUR_ACCESS_TOKEN`
     - `Content-Type: application/json`
   - Body:
     ```json
     {
       "messaging_product": "whatsapp",
       "to": "{{1.phone}}",
       "type": "template",
       "template": {
         "name": "appointment_confirmation",
         "language": { "code": "en" },
         "components": [
           {
             "type": "body",
             "parameters": [
               { "type": "text", "text": "{{1.name}}" },
               { "type": "text", "text": "{{1.date}}" },
               { "type": "text", "text": "{{1.time}}" }
             ]
           }
         ]
       }
     }
     ```

### Option B: Using Twilio WhatsApp (Easier)

1. Go to: https://www.twilio.com
2. Sign up for free account
3. Get WhatsApp sandbox number
4. In Make.com:
   - Add **"Twilio"** module
   - Select **"Send WhatsApp Message"**
   - Configure:
     - **From:** Twilio WhatsApp number
     - **To:** `{{1.phone}}`
     - **Message:**
       ```
       ✅ Appointment Confirmed!
       
       Hi {{1.name}},
       Your appointment is booked for:
       📅 {{1.date}} at ⏰ {{1.time}}
       
       See you soon!
       - Health Care Team
       ```

### Option C: Using UltraMsg (Simplest)

1. Go to: https://ultramsg.com
2. Create free account
3. Connect your WhatsApp
4. Get API token
5. In Make.com:
   - Add **"HTTP"** module
   - Method: **POST**
   - URL: `https://api.ultramsg.com/instance_id/messages/chat`
   - Body:
     ```json
     {
       "token": "YOUR_TOKEN",
       "to": "{{1.phone}}",
       "body": "✅ Appointment Confirmed!\n\nHi {{1.name}},\nYour appointment: {{1.date}} at {{1.time}}"
     }
     ```

---

## 🎯 COMPLETE AUTOMATION FLOW

```
VISITOR fills Tally form
    ↓
Make.com receives webhook
    ↓
Check Google Calendar for availability
    ↓
    ├─→ SLOT AVAILABLE:
    │   ├─→ Create calendar event
    │   ├─→ Send confirmation email to patient
    │   ├─→ Send notification email to admin
    │   ├─→ Send WhatsApp to patient
    │   └─→ Save to Google Sheets
    │
    └─→ SLOT TAKEN:
        └─→ Send "not available" email
```

---

## 🧪 TESTING YOUR AUTOMATION

### Test Checklist:

1. **Fill out your Tally form** with test data
2. **Check Make.com** - scenario should run automatically
3. **Check Google Calendar** - event should appear
4. **Check email** - confirmation should arrive
5. **Check Google Sheets** - row should be added
6. **Check WhatsApp** - message should be sent

### Troubleshooting:

**Webhook not triggering?**
- Check Tally webhook URL is correct
- Make sure scenario is "ON"
- Click "Run once" manually

**Calendar event not creating?**
- Verify calendar ID is correct
- Check date/time format from form
- Ensure Google Calendar is connected

**Email not sending?**
- Verify Gmail connection
- Check spam folder
- Ensure "Less secure app access" is enabled

---

## 📊 MONITORING & ANALYTICS

### In Make.com:
- View **History** tab to see all runs
- Check for errors
- Monitor execution time
- View data processed

### In Google Calendar:
- All appointments visible
- Color-code by service type
- Set reminders

### In Google Sheets:
- Track all bookings
- Create charts/reports
- Export data

---

## 💰 PRICING (All Free Tier)

- **Tally:** Free (unlimited forms)
- **Make.com:** Free (1,000 operations/month)
- **Google Calendar:** Free
- **Google Sheets:** Free
- **Gmail:** Free
- **WhatsApp Cloud API:** Free (1,000 messages/month)

**Total Cost: $0/month** for small to medium usage!

---

## 🚀 NEXT STEPS

1. ✅ Complete Step 2 (Google Calendar)
2. ✅ Complete Step 3 (Make.com automation)
3. ✅ Test the full flow
4. ✅ Add WhatsApp (optional)
5. ✅ Monitor and optimize

---

## 📞 SUPPORT RESOURCES

- **Make.com Help:** https://www.make.com/en/help
- **Tally Support:** https://tally.so/help
- **Google Calendar API:** https://developers.google.com/calendar
- **WhatsApp Business API:** https://developers.facebook.com/docs/whatsapp

---

**🎉 Once set up, your appointment system will be 100% automated!**
