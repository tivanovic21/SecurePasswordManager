#import touchid
import platform

class BiometricAuth:
    @staticmethod
    def checkPlatform():
        if platform.system() == 'Darwin': #macOS
            return 'macOS'
        elif platform.system() == 'Windows':
            return 'windows'
        else:
            return 'linux'
        
    #@staticmethod
    #def touchID():
    #   success = touchid.authenticate()
    #    if success:
    #        return True
    #    else:
    #        return False
    
    @staticmethod
    def wbf():
        from backend.fingerprint import FingerPrint
        myFP = FingerPrint()
        try:
            myFP.open()
            if myFP.verify():
                return True
            else:
                return False
        except:
            return False
        finally:
            myFP.close()