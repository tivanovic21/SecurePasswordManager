import pyotp

class TwoFactorAuth:
    @staticmethod
    def generateSecret():
        return pyotp.random_base32() # time based secret
    
    @staticmethod
    def getTOTPuri(user, secret):
        return pyotp.totp.TOTP(secret).provisioning_uri(user, issuer_name="Password Manager")
    
    @staticmethod
    def verifyToken(secret, token):
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @staticmethod
    def generateToken(secret):
        totp = pyotp.TOTP(secret)
        return totp.now()