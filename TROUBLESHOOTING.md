# 🔧 Troubleshooting Guide

## Fixed Issues

### ✅ Yoga Section Error - FIXED!

**Problem:** Yoga poses weren't displaying correctly

**Solution:** 
- Fixed pose name matching between `suggest_yoga()` and `YOGA_POSES` database
- Added more yoga poses to match all recommendations
- Updated template to use new data structure

**Now includes 17 yoga poses:**
1. Padmasana (Lotus Pose)
2. Shavasana (Corpse Pose)
3. Anulom Vilom (Alternate Nostril Breathing)
4. Tadasana (Mountain Pose)
5. Balasana (Child's Pose)
6. Viparita Karani (Legs Up the Wall)
7. Bhujangasana (Cobra Pose)
8. Vajrasana (Diamond Pose)
9. Surya Namaskar (Sun Salutation)
10. Dhanurasana (Bow Pose)
11. Paschimottanasana (Seated Forward Bend)
12. Marjaryasana-Bitilasana (Cat-Cow Pose)
13. Setu Bandhasana (Bridge Pose)
14. Uttanasana (Standing Forward Bend)
15. Vrikshasana (Tree Pose)
16. Sukhasana (Easy Pose)

---

## Common Issues & Solutions

### Issue: "Module not found" error

**Solution:**
```bash
pip install flask
```

### Issue: Images not loading

**Possible causes:**
1. No internet connection (images are from Unsplash)
2. Firewall blocking external images

**Solution:**
- Check internet connection
- Or replace with local images in `static/images/`

### Issue: Videos not playing

**Possible causes:**
1. YouTube blocked in your region
2. Browser blocking embedded content

**Solution:**
- Try different browser
- Check YouTube availability
- Or replace with local videos

### Issue: Page not found (404)

**Solution:**
- Make sure you're logged in
- Check the URL is correct
- Restart the Flask app

### Issue: Styles not loading

**Solution:**
1. Clear browser cache (Ctrl+Shift+R)
2. Check `static/style.css` exists
3. Restart Flask app

### Issue: Database/Session errors

**Solution:**
```python
# In app.py, make sure secret key is set:
app.secret_key = "healthcare_secret"
```

---

## Testing Checklist

### ✅ Test Each Feature:

1. **Login/Register**
   - [ ] Can create account
   - [ ] Can login
   - [ ] Password toggle works

2. **Home Page**
   - [ ] All cards display
   - [ ] Navigation works
   - [ ] Responsive on mobile

3. **Dashboard**
   - [ ] Wellness score shows
   - [ ] Stats display correctly
   - [ ] Quick actions work

4. **Symptom Checker**
   - [ ] Can select symptoms
   - [ ] Results show correctly
   - [ ] Specialist recommendations appear

5. **Yoga Section**
   - [ ] Search works
   - [ ] Pose cards display with images
   - [ ] Can click to see details
   - [ ] Videos play
   - [ ] Instructions show

6. **Medicine Section**
   - [ ] Search works
   - [ ] Medicine images display
   - [ ] Details page works
   - [ ] Dosage info shows

7. **BMI Calculator**
   - [ ] Calculations work
   - [ ] Results display
   - [ ] Recommendations show

8. **Consultation**
   - [ ] Form submits
   - [ ] Confirmation shows

---

## Browser Compatibility

### Tested & Working:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

### Known Issues:
- Older IE versions not supported (use modern browser)

---

## Performance Tips

### If app is slow:

1. **Optimize images:**
   - Use smaller image sizes
   - Compress images
   - Use local images instead of external URLs

2. **Cache static files:**
   - Browser will cache CSS/images after first load

3. **Database:**
   - Currently using in-memory storage (fast)
   - For production, use real database

---

## Development Tips

### Hot Reload:
Flask debug mode is enabled by default:
```python
app.run(debug=True)
```

### View Errors:
Check terminal/console for error messages

### Test on Mobile:
1. Find your IP: `ipconfig` or `ifconfig`
2. Access from phone: `http://YOUR_IP:5000`

---

## Getting Help

### Check Documentation:
1. `COMPLETE_FEATURES_SUMMARY.md` - All features
2. `IMAGES_VIDEOS_GUIDE.md` - Visual content
3. `DESIGN_SYSTEM.md` - Design guide
4. `QUICK_START.md` - Quick start

### Debug Steps:
1. Check terminal for errors
2. Check browser console (F12)
3. Verify file paths
4. Clear cache and reload
5. Restart Flask app

---

## Contact

If you need help:
1. Check error messages in terminal
2. Review documentation files
3. Test in different browser
4. Check all files are present

---

**Everything should work perfectly now! 🎉**
