from dataclasses import dataclass

@dataclass
class Blob:
    id: int
    u: float
    v: float
    state: str

class blobtrackingextension:
    """
    Blob tracking extension with OSC output
    """
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.active_blobs = tdu.Dependency({})
        self.debug_mode = True
        
    @property
    def ActiveBlobs(self):
        return self.active_blobs.val
    
    @property
    def OscOut(self):
        return op('oscout1')
    
    @property
    def Blob(self):
        return Blob
    
    def Debug(self, message):
        if self.debug_mode:
            debug(message)
    
    def ToggleDebug(self):
        self.debug_mode = not self.debug_mode
        debug(f"[BLOB DEBUG] Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        return self.debug_mode
    
    def SetDebug(self, enabled):
        self.debug_mode = enabled
        debug(f"[BLOB DEBUG] Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def SendOSC(self, address, blob_id, u, v, width, height):
        """Send OSC message with numeric values"""
        if self.OscOut:
            self.OscOut.sendOSC(address, [blob_id, u, v, width, height])
            self.Debug(f"[OSC] {address} id:{blob_id} u:{u:.4f} v:{v:.4f} w:{width:.4f} h:{height:.4f}")
        else:
            self.Debug(f"[OSC] ERROR - OSC Out not found!")
    
    def ClearAllBlobs(self):
        """Manually clear all tracked blobs"""
        self.Debug(f"[CLEAR] Clearing {len(self.active_blobs.val)} blobs")
        self.active_blobs.val = {}
        self.active_blobs.modified()
    
    def GetActiveBlobs(self):
        return list(self.active_blobs.val.values())
    
    def GetActiveBlobCount(self):
        return len(self.active_blobs.val)