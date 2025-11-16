# 📋 Tally Form Integration Guide

## ✅ Successfully Integrated!

Your Tally form is now embedded in your Health Care website on the **Consult a Doctor** page.

---

## 🔗 Your Tally Form Details

**Form URL:** https://tally.so/r/WOOzOR

**Embedded Location:** `/consult` page (templates/consult.html)

---

## 📍 Where to Find It

1. **Run your Flask app:**
   ```bash
   python app.py
   ```

2. **Navigate to:**
   - Login to your website
   - Click on **"Consult a Doctor"** from the home page
   - Or go directly to: `http://localhost:5000/consult`

3. **You'll see:**
   - Your Tally form embedded beautifully
   - Users can fill it out directly on your website
   - No need to leave your site!

---

## 🎨 What Was Added

### In `templates/consult.html`:
```html
<iframe 
  src="https://tally.so/r/WOOzOR" 
  width="100%" 
  height="600" 
  frameborder="0" 
  title="Consult a Doctor - Appointment Form">
</iframe>
```

### Features:
- ✅ Fully responsive (works on mobile & desktop)
- ✅ Seamlessly integrated into your design
- ✅ Info box explaining the form
- ✅ Fallback link to open in new tab
- ✅ Professional styling matching your website

---

## 🔧 How to Customize

### Change Form Height:
In `consult.html`, find this line:
```html
height="600"
```
Change `600` to any number (e.g., `800` for taller form)

### Change Form URL:
If you create a new Tally form, replace:
```html
src="https://tally.so/r/WOOzOR"
```
With your new form URL

### Add to Other Pages:
Copy the iframe code and paste it anywhere you want the form to appear!

---

## 📊 Viewing Form Submissions

1. Go to: https://tally.so
2. Login to your Tally account
3. Click on your form
4. View all submissions in the dashboard
5. Export to Excel/CSV if needed

---

## 💡 Pro Tips

### 1. **Email Notifications:**
   - In Tally dashboard, go to form settings
   - Enable email notifications
   - Get notified when someone books an appointment

### 2. **Customize Thank You Message:**
   - In Tally, edit your form
   - Customize the success message
   - Add redirect URL if needed

### 3. **Add More Fields:**
   - Edit your Tally form
   - Add fields like:
     - Preferred date/time
     - Phone number
     - Medical history
     - Insurance details

### 4. **Integrate with Other Tools:**
   - Tally works with Make.com (formerly Integromat)
   - Connect to Google Sheets
   - Send to email
   - Add to calendar

---

## 🚀 Alternative Embedding Methods

### Method 1: Popup (Modal)
```html
<button onclick="window.open('https://tally.so/r/WOOzOR', '_blank', 'width=600,height=800')">
  Book Appointment
</button>
```

### Method 2: Full Page Redirect
```html
<a href="https://tally.so/r/WOOzOR" target="_blank">
  Book Appointment
</a>
```

### Method 3: Tally Widget (Advanced)
```html
<script src="https://tally.so/widgets/embed.js"></script>
<button data-tally-open="WOOzOR" data-tally-emoji-text="👋" data-tally-emoji-animation="wave">
  Book Now
</button>
```

---

## ✅ Testing Checklist

- [ ] Form loads properly on consult page
- [ ] Form is responsive on mobile
- [ ] Can submit test appointment
- [ ] Receives submission in Tally dashboard
- [ ] Email notification works (if enabled)
- [ ] Thank you message displays correctly

---

## 🆘 Troubleshooting

**Form not loading?**
- Check internet connection
- Verify Tally form URL is correct
- Check if form is published in Tally

**Form too small/large?**
- Adjust `height="600"` in iframe
- Add `min-height` in CSS

**Want different styling?**
- Edit `.tally-container` class in consult.html
- Customize colors, borders, shadows

---

## 📞 Need Help?

- Tally Documentation: https://tally.so/help
- Your form dashboard: https://tally.so/forms
- Edit your form: https://tally.so/r/WOOzOR/edit

---

**🎉 Your consultation form is now live and ready to accept appointments!**
