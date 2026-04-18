import uuid
from fastapi import APIRouter, HTTPException, Header
from app.data.mock_db import db
from app.schemas.payloads import (
    UserRegisterRequest, 
    UserLoginRequest, 
    GoogleAuthRequest, 
    ForgotPasswordRequest
)

router = APIRouter()

@router.post("/register", status_code=201)
def register_user(payload: UserRegisterRequest):
    """Handles the 'Create Account' form from the Sign Up UI"""
    
    # 1. Check if email already exists
    existing_user = next((u for u in db["users"] if u["email"] == payload.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # 2. Create new user (Role is 'User' by default per your UI note)
    new_user_id = f"u-{str(uuid.uuid4())[:8]}"
    new_user = {
        "id": new_user_id,
        "name": payload.full_name,
        "email": payload.email,
        "organization": payload.organization,
        "role": "User", 
        "password": payload.password # In a real app, ALWAYS hash this! (e.g., bcrypt)
    }
    
    db["users"].append(new_user)
    
    # 3. Return a fake JWT token and user info
    return {
        "message": "Account created successfully",
        "token": f"fake-jwt-token-for-{new_user_id}",
        "user": {k: v for k, v in new_user.items() if k != "password"} # Don't send password back!
    }


@router.post("/login")
def login_user(payload: UserLoginRequest):
    """Handles standard Email/Password login"""
    user = next((u for u in db["users"] if u["email"] == payload.email), None)
    
    # For our mock DB, existing users don't have passwords, so we bypass password check for them.
    # But for newly registered users, we check the password.
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    if "password" in user and user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {
        "token": f"fake-jwt-token-for-{user['id']}", 
        "user": {k: v for k, v in user.items() if k != "password"}
    }


@router.post("/google")
def login_with_google(payload: GoogleAuthRequest):
    """
    Handles the 'Continue with Google' button. 
    Frontend sends the Google OAuth Token, backend verifies it.
    """
    # In a real app: Verify payload.google_token with Google's API here.
    # For now, we simulate a successful Google login.
    
    simulated_google_email = "jane@acmecorp.com" # Pretend we got this from the token
    
    # Check if user exists, if not, auto-register them
    user = next((u for u in db["users"] if u["email"] == simulated_google_email), None)
    if not user:
        new_user_id = f"u-{str(uuid.uuid4())[:8]}"
        user = {
            "id": new_user_id,
            "name": "Jane Doe",
            "email": simulated_google_email,
            "role": "User"
        }
        db["users"].append(user)

    return {
        "token": f"fake-jwt-google-token-for-{user['id']}", 
        "user": user
    }


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest):
    """Handles the Forgot Password link"""
    # Security Best Practice: Never reveal if the email actually exists in the DB
    # Always return a generic success message to prevent user enumeration attacks.
    return {
        "message": f"If {payload.email} is registered, a password reset link has been sent."
    }


@router.get("/me")
def get_current_user(user_id: str = Header(default="u1", alias="x-user-id")):
    """Fetches logged-in user details to populate the profile and dashboard UI"""
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {k: v for k, v in user.items() if k != "password"}