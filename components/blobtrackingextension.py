from dataclasses import dataclass
from TDStoreTools import StorageManager
import TDFunctions as TDF

@dataclass
class Blob:
    id: int
    u: float
    v: float
    state: str  # 'new', 'active', 'lost', 'expired'

class blobtrackingextension:
    """
    Blob tracking extension with OSC output
    """
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.active_blobs = tdu.Dependency({})  # id: Blob
        self.debug_mode = False  # Toggle this on/off
        
    @property
    def ActiveBlobs(self):
        return self.active_blobs.val
    @property
    def OscOut(self):
        return op('oscout1')  
    
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
    
    def SendOSC(self, address, blob_id, u, v):
        """Send OSC message"""
        if self.OscOut:
            self.OscOut.sendOSC(address, [blob_id, u, v])
            self.Debug(f"[BLOB OSC] {address} {blob_id} {u:.7f} {v:.7f}")
        else:
            self.Debug(f"[BLOB OSC] ERROR - OSC Out not found!")
    
    def OnBlobTrack(self, blobTrackTop, blobs):
        for blob in blobs:
            blob_id = blob.id
            u = blob.u
            v = blob.v
            
            # Send move message
            self.SendOSC('/touch/move', blob_id, u, v)
            
            # Update stored blob
            if blob_id in self.active_blobs.val:
                self.active_blobs.val[blob_id].u = u
                self.active_blobs.val[blob_id].v = v
                self.active_blobs.modified()
            else:
                # Shouldn't happen, but safety check
                self.active_blobs.val[blob_id] = Blob(blob_id, u, v, 'active')
                self.active_blobs.modified()
    
    def OnBlobStateChange(self, blobTrackTop, blobs):
        self.Debug("[BLOB STATE] " + "=" * 60)
        self.Debug(f"[BLOB STATE] Processing {len(blobs)} blob(s)")
        
        for blob in blobs:
            blob_id = blob.id
            u = blob.u
            v = blob.v
            state = blob.state
            
            self.Debug(f"[BLOB STATE] Blob {blob_id} - State: {state} - Tracked: {blob_id in self.active_blobs.val}")
            
            if state == 'new' or state == 'revived':
                # BEGIN
                self.Debug(f"[BLOB STATE]   -> BEGIN Blob {blob_id} at ({u:.4f}, {v:.4f})")
                self.SendOSC('/touch/begin', blob_id, u, v)
                self.active_blobs.val[blob_id] = Blob(blob_id, u, v, state)
                self.active_blobs.modified()
                
            elif state == 'lost' or state == 'expired':
                # END
                if blob_id in self.active_blobs.val:
                    stored_blob = self.active_blobs.val[blob_id]
                    self.Debug(f"[BLOB STATE]   -> END Blob {blob_id} ({state}) at ({stored_blob.u:.4f}, {stored_blob.v:.4f})")
                    self.SendOSC('/touch/end', blob_id, stored_blob.u, stored_blob.v)
                    del self.active_blobs.val[blob_id]
                    self.active_blobs.modified()
                else:
                    self.Debug(f"[BLOB STATE]   -> ERROR: Blob {blob_id} {state} but not tracked!")
        
        # Summary
        self.Debug(f"[BLOB STATE] Active blobs: {len(self.active_blobs.val)}")
        if self.active_blobs.val:
            self.Debug(f"[BLOB STATE]   IDs: {list(self.active_blobs.val.keys())}")
        self.Debug("[BLOB STATE] " + "=" * 60)
    
    def GetActiveBlobs(self):
        """Return list of currently active blobs"""
        return list(self.active_blobs.val)
    
    def GetActiveBlobCount(self):
        """Return count of active blobs"""
        return len(self.active_blobs.val)