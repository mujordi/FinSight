# Authentication System - FinSight

## Overview
FinSight now includes a secure authentication system to protect access to financial data and models.

## Features

### 1. Login System
- **Login Page**: Beautiful, modern login interface at `/login`
- **Session-based Authentication**: Secure token-based sessions with 24-hour expiration
- **Password Hashing**: SHA-256 password hashing for security
- **Cookie Management**: HttpOnly cookies for secure token storage

### 2. User Management
- **Default Users**:
  - **Admin**: 
    - Username: `admin`
    - Password: `finsight2026`
  - **Demo**: 
    - Username: `demo`
    - Password: `demo123`

### 3. Protected Routes
All application routes and API endpoints are now protected:
- Main dashboard (`/`)
- All market data endpoints (`/api/market-data/*`)

Unauthenticated users are automatically redirected to the login page.

### 4. Session Management
- **Session Duration**: 24 hours
- **Automatic Cleanup**: Expired sessions are automatically removed
- **Logout Functionality**: Users can logout via the logout button in the header

## Technical Implementation

### Files Created/Modified

1. **`auth.py`**: Authentication manager
   - User credential storage (in-memory, can be extended to database)
   - Password hashing
   - Session token generation and validation
   - Session cleanup

2. **`templates/login.html`**: Login page
   - Modern, responsive design
   - Error handling
   - Loading states
   - Demo credentials display

3. **`main.py`**: Updated with authentication
   - Login/logout endpoints
   - Authentication middleware
   - Protected routes
   - Cookie management

4. **`templates/base.html`**: Added logout button
   - User display in header
   - Logout button with styling

## API Endpoints

### Authentication Endpoints

#### `GET /login`
Display login page

#### `POST /api/login`
Authenticate user and create session
- **Request Body**: `{ "username": "string", "password": "string" }`
- **Response**: `{ "success": true, "token": "string", "message": "string" }`

#### `GET /api/logout`
Logout user and destroy session
- **Response**: Redirect to `/login`

### Protected Endpoints
All existing market data endpoints now require authentication:
- `/api/market-data/all`
- `/api/market-data/macro`
- `/api/market-data/gold`
- `/api/market-data/equities`
- `/api/market-data/crypto`
- `/api/market-data/fixed-income`
- `/api/market-data/thematic`
- `/api/market-data/growth`
- `/api/market-data/highbeta`

## Security Considerations

### Current Implementation (Development)
- In-memory user storage
- SHA-256 password hashing
- HttpOnly cookies
- 24-hour session expiration

### Production Recommendations
1. **Database Storage**: Move user credentials to a secure database
2. **Password Hashing**: Upgrade to bcrypt or Argon2 for password hashing
3. **HTTPS**: Always use HTTPS in production
4. **Environment Variables**: Store credentials in environment variables
5. **Rate Limiting**: Implement rate limiting for login attempts
6. **Two-Factor Authentication**: Consider adding 2FA for enhanced security
7. **Session Storage**: Use Redis or similar for session storage in production
8. **CSRF Protection**: Add CSRF tokens for form submissions

## Usage

### For Users
1. Navigate to the application URL
2. You'll be redirected to `/login` if not authenticated
3. Enter username and password
4. Click "Login"
5. Access the dashboard
6. Click "Logout" button in the header to logout

### For Developers
To add new users, modify the `users` dictionary in `auth.py`:

```python
self.users = {
    "username": self._hash_password("password"),
    # Add more users here
}
```

To change session duration, modify `session_duration` in `auth.py`:

```python
self.session_duration = timedelta(hours=24)  # Change as needed
```

## Testing
1. Start the server: `uvicorn main:app --reload --port 8000`
2. Navigate to `http://localhost:8000`
3. You should be redirected to login
4. Login with demo credentials
5. Verify access to dashboard
6. Test logout functionality

## Future Enhancements
- User registration
- Password reset functionality
- Email verification
- Role-based access control (RBAC)
- Activity logging
- Multi-factor authentication
- OAuth integration (Google, GitHub, etc.)



