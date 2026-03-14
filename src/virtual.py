# as i mostly run in a VM enviroment i want to make it show somthing a little cheeky
# basucally going to add:
'''
class VirtualProvider:
    def get_thermals(self):
        return {
            "cpu": "I can't see that...",
            "mb": "You're in a VM!",
            "nvme": "Likely hot? ¯\_(ツ)_/¯"
        }

    def get_os_metadata(self):
        # can still pull the real OS version, 
        # but maybe append a " (Virtual)" tag
        return "Windows 11 (Sandboxed)"
'''
# makes it a little less boring when running in a VM.
# also gives me a chance to test the UI with some fun data.