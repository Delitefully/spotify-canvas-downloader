import requests
import time
import hashlib
import hmac
import base64
import struct
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class SpotifyAuth:
    def __init__(self):
        self.access_token = None
        self.expires_at = 0
        self.sp_dc_cookie = os.getenv('SP_DC')
        
    def set_sp_dc_cookie(self, sp_dc: str):
        """Set the sp_dc cookie required for authentication"""
        self.sp_dc_cookie = sp_dc
        
    def base32_from_bytes(self, data: bytes, secret_sauce: str) -> str:
        """Convert bytes to base32 using custom alphabet"""
        t = 0
        n = 0
        r = ""
        
        for byte in data:
            n = (n << 8) | byte
            t += 8
            while t >= 5:
                r += secret_sauce[(n >> (t - 5)) & 31]
                t -= 5
                
        if t > 0:
            r += secret_sauce[(n << (5 - t)) & 31]
            
        return r
    
    def generate_totp(self) -> str:
        """Generate TOTP for Spotify authentication"""
        secret_sauce = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        
        # Secret cipher bytes from Spotify's implementation
        secret_cipher_bytes = [12, 56, 76, 33, 88, 44, 88, 33, 78, 78, 11, 66, 22, 22, 55, 69, 54]
        
        # Apply the XOR transformation
        transformed_bytes = [byte ^ (i % 33 + 9) for i, byte in enumerate(secret_cipher_bytes)]
        
        # Process the secret according to Spotify's algorithm
        joined_string = "".join(str(byte) for byte in transformed_bytes)
        utf8_bytes = joined_string.encode('utf-8')
        hex_string = "".join(f"{byte:02x}" for byte in utf8_bytes)
        secret_bytes = bytes.fromhex(hex_string)
        
        # Convert to base32
        secret = self.base32_from_bytes(secret_bytes, secret_sauce)
        
        # Get server time from Spotify
        try:
            server_time_response = requests.get("https://open.spotify.com/server-time")
            server_time_seconds = server_time_response.json()["serverTime"]
        except:
            server_time_seconds = int(time.time())
        
        # Generate TOTP
        time_counter = server_time_seconds // 30
        
        # Add padding to secret if needed
        missing_padding = len(secret) % 8
        if missing_padding:
            secret += '=' * (8 - missing_padding)
        
        try:
            secret_bytes = base64.b32decode(secret.upper())
        except Exception as e:
            raise Exception(f"Failed to decode TOTP secret: {e}")
        
        # Generate HMAC-SHA1
        time_bytes = struct.pack('>Q', time_counter)
        hmac_digest = hmac.new(secret_bytes, time_bytes, hashlib.sha1).digest()
        
        # Dynamic truncation
        offset = hmac_digest[-1] & 0x0F
        truncated = struct.unpack('>I', hmac_digest[offset:offset + 4])[0]
        truncated &= 0x7FFFFFFF
        
        # Generate 6-digit code
        totp_value = truncated % (10 ** 6)
        
        return f"{totp_value:06d}"
    
    def get_access_token(self) -> str:
        """Get access token using Spotify's authentication scheme"""
        if not self.sp_dc_cookie:
            raise Exception("sp_dc cookie is required. Set SP_DC environment variable or use set_sp_dc_cookie()")
        
        # Check if current token is still valid
        if self.access_token and time.time() < self.expires_at:
            return self.access_token
        
        try:
            # Generate TOTP
            totp = self.generate_totp()
            timestamp = int(time.time())
            
            url = (
                f"https://open.spotify.com/get_access_token"
                f"?reason=transport"
                f"&productType=web_player"
                f"&totp={totp}"
                f"&totpVer=5"
                f"&ts={timestamp}"
            )
            
            headers = {
                "Cookie": f"sp_dc={self.sp_dc_cookie}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            self.access_token = data["accessToken"]
            self.expires_at = data["accessTokenExpirationTimestampMs"] / 1000
            
            return self.access_token
            
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    def is_authenticated(self) -> bool:
        """Check if we have a valid access token"""
        return self.access_token is not None and time.time() < self.expires_at


_spotify_auth = SpotifyAuth()


def get_access_token() -> str:
    """Get access token - compatible with existing code"""
    return _spotify_auth.get_access_token() 