class blobtrackingextension:
    """
    Simple blob tracking - just send current positions
    """
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.debug_mode = False
        
    @property
    def OscOut(self):
        return op('oscout1')
    
    def Debug(self, message):
        if self.debug_mode:
            debug(message)
    
    def ToggleDebug(self):
        self.debug_mode = not self.debug_mode
        debug(f"[BLOB DEBUG] Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def SetDebug(self, enabled):
        self.debug_mode = enabled
        debug(f"[BLOB DEBUG] Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def SendOSC(self, address, blob_id, u, v):
        """Send OSC message"""
        if self.OscOut:
            self.OscOut.sendOSC(address, [blob_id, u, v])
            self.Debug(f"[OSC] {address} {blob_id} {u:.7f} {v:.7f}")