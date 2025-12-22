from dataclasses import dataclass
import math

@dataclass
class Blob:
    id: int
    u: float
    v: float
    width: float
    height: float
    u_corrected: float
    v_corrected: float

class blobtrackingextension:
    """
    Blob tracking with edge detection for elongated blobs
    """
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.debug_mode = True
        
        # Detection parameters
        self.elongation_threshold = 2.5
        self.large_blob_threshold = 0.15
        self.center_u = 0.5
        self.center_v = 0.5
        self.edge_offset_ratio = 0.4  # How much of blob size to offset
        
    @property
    def OscOut(self):
        return op('oscout1')
    
    @property
    def Blob(self):
        return Blob
    
    def Debug(self, message):
        debug(message)
        
    def SetDebug(self, enabled):
        self.debug_mode = enabled
        debug(f"[BLOB DEBUG] Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def CalculateEdgePoint(self, u, v, width, height):
        """
        Calculate the leading edge point (hand/fingertip) of an elongated blob
        Returns the point closest to center (the reaching hand/fingertip)
        """
        # Calculate blob size
        blob_size = max(width, height)
        
        # Calculate aspect ratio to determine elongation
        if height > 0:
            aspect_ratio = width / height if width > height else height / width
        else:
            aspect_ratio = 1.0
        
        # Check if blob is large and elongated
        is_elongated = aspect_ratio > self.elongation_threshold
        is_large = blob_size > self.large_blob_threshold
        
        if is_elongated and is_large:
            # Calculate vector from blob center TO table center
            # This gives us the direction the hand is reaching
            dx = self.center_u - u
            dy = self.center_v - v
            distance_to_center = math.sqrt(dx*dx + dy*dy)
            
            # Only apply correction if we're not already at center
            if distance_to_center > 0.05:  # Minimum distance threshold
                # Normalize direction vector
                dir_x = dx / distance_to_center
                dir_y = dy / distance_to_center
                
                # Move the tracking point TOWARD center by a portion of blob size
                # This shifts from blob center to the fingertip end
                offset = blob_size * self.edge_offset_ratio
                
                u_corrected = u + (dir_x * offset)
                v_corrected = v + (dir_y * offset)
                
                self.Debug(f"[EDGE] Blob {aspect_ratio:.2f}x elongated, size={blob_size:.3f}")
                self.Debug(f"[EDGE]   Original: ({u:.3f}, {v:.3f})")
                self.Debug(f"[EDGE]   Corrected: ({u_corrected:.3f}, {v_corrected:.3f})")
                self.Debug(f"[EDGE]   Distance to center: {distance_to_center:.3f}")
                
                return u_corrected, v_corrected, True
            else:
                # Very close to center - just use blob center
                self.Debug(f"[EDGE] Blob at center, no correction needed")
                return u, v, False
        
        # Not elongated or not large enough - use blob center as-is
        return u, v, False
    
    def SendOSC(self, address, blob_id, u, v):
        """Send OSC message"""
        if self.OscOut:
            self.OscOut.sendOSC(address, [blob_id, u, v])
            self.Debug(f"[OSC] {address} {blob_id} {u:.7f} {v:.7f}")