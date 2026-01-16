# FinSight - Changelog

## Latest Changes (2026-01-16)

### ✅ Sentiment Indicators Completed
- **Added sentiment semaphores** to all tabs:
  - ✅ Macro (already had it)
  - ✅ Crypto (already had it)
  - ✅ Equities (already had it)
  - ✅ Growth (already had it)
  - ✅ High Beta (already had it)
  - ✅ **Gold (NEW)**
  - ✅ **Fixed Income (NEW)**
  - ✅ **Thematic (NEW)**

All tabs now display a "BULLISH/NEUTRAL/BEARISH" indicator above the tables.

### 🔒 Authentication System Implemented

#### New Files Created:
1. **`auth.py`**: Complete authentication manager
   - SHA-256 password hashing
   - Session token generation
   - 24-hour session expiration
   - Automatic session cleanup

2. **`templates/login.html`**: Modern login page
   - Beautiful, responsive design
   - Error handling with animations
   - Loading states
   - Demo credentials displayed

3. **`AUTHENTICATION.md`**: Complete documentation

#### Modified Files:
1. **`main.py`**: 
   - Added authentication middleware
   - New endpoints: `/login`, `/api/login`, `/api/logout`
   - Protected all existing endpoints
   - Cookie-based session management

2. **`templates/base.html`**:
   - Added username display in header
   - Added logout button with styling

3. **`requirements.txt`**:
   - Added `pydantic`
   - Added `python-multipart`

### 🔑 Default Credentials

**Admin User:**
- Username: `admin`
- Password: `finsight2026`

**Demo User:**
- Username: `demo`
- Password: `demo123`

### 🛡️ Security Features

- **Protected Routes**: All pages require authentication
- **Protected APIs**: All `/api/market-data/*` endpoints require authentication
- **HttpOnly Cookies**: Secure token storage
- **Session Expiration**: 24-hour automatic expiration
- **Password Hashing**: SHA-256 for stored passwords
- **Redirect Logic**: Unauthenticated users redirected to login

### 🚀 How to Test

1. **Server is running** on `http://localhost:8000`
2. **Navigate** to `http://localhost:8000` in your browser
3. You'll be **redirected** to `/login`
4. **Login** with demo credentials (demo/demo123)
5. Access the **full dashboard**
6. Click **Logout** button to exit

### 📊 All Sentiment Indicators Working

Every model tab now calculates and displays sentiment based on:
- Individual factor signals (positive/neutral/negative)
- Factor weights (high/medium/low)
- Aggregated sentiment score
- Visual color coding (green/yellow/red)

### 🎯 Summary

**Completed:**
- ✅ Added missing sentiment indicators (Gold, Fixed Income, Thematic)
- ✅ Implemented complete authentication system
- ✅ Protected all routes and API endpoints
- ✅ Created beautiful login page
- ✅ Added logout functionality
- ✅ Full documentation

**Ready to Use:**
- Open browser → `http://localhost:8000`
- Login → Access dashboard
- All features working with authentication

