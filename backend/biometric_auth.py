import touchid
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
        
    @staticmethod
    def touchID():
        success = touchid.authenticate()
        if success:
            return True
        else:
            return False
    
    @staticmethod
    def wpf():
        pass