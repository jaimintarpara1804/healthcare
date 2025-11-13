# How to Use Forgot Password Feature 🔑

## ✅ Yes, the Forgot Password button is fully functional!

Your forgot password feature is now working perfectly with the database. Here's how to use it:

## Step-by-Step Guide:

### 1. **Access Forgot Password**
   - Go to the login page: `http://localhost:5000/login_register`
   - Click on **"Forgot your password?"** link at the bottom

### 2. **Generate Reset Code**
   - Enter your registered email address
   - Click **"Generate Reset Code"**
   - A 6-digit code will appear on screen (valid for 15 minutes)
   - Example code: `123456`

### 3. **Reset Your Password**
   - Click **"Reset Password Now"** button (or go to `/reset`)
   - Enter:
     - Your email address
     - The 6-digit reset code
     - New password (minimum 6 characters)
     - Confirm new password
   - Click **"Reset Password"**

### 4. **Login with New Password**
   - You'll see a success message
   - Click **"Go to Login"**
   - Login with your email and new password

## Features:

✅ **Secure** - Passwords are hashed using werkzeug security
✅ **Time-limited** - Reset codes expire after 15 minutes
✅ **Database-backed** - All changes are saved permanently
✅ **User-friendly** - Clean, modern interface with helpful messages
✅ **Validation** - Checks if email exists before generating code

## Test Account Available:

You can test with this account:
- **Email:** testuser@example.com
- **Password:** oldpassword123

Try resetting the password and logging in with the new one!

## Important Notes:

- Reset codes are shown on screen (demo mode - in production, these would be sent via email)
- Codes expire after 15 minutes for security
- You must use the same email for both generating the code and resetting the password
- Old password won't work after reset
