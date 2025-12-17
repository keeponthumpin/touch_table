def onTableChange(dat):
    """Called when the blob tracking table changes"""
    ext = parent.blobtrack.extensions[0]
    
    if not ext:
        return
    
    current_blob_ids = set()
    
    for i in range(1, dat.numRows):
        blob_id = int(dat[i, 'id'].val)
        u = float(dat[i, 'u'].val)
        v = float(dat[i, 'v'].val)
        width = float(dat[i, 'width'].val)
        height = float(dat[i, 'height'].val)
        active = int(dat[i, 'active'].val)
        revived = int(dat[i, 'revived'].val)
        lost = int(dat[i, 'lost'].val)
        expired = int(dat[i, 'expired'].val)
        
        current_blob_ids.add(blob_id)
        
        if blob_id not in ext.ActiveBlobs:
            if active or revived:
                ext.Debug(f"[DAT] BEGIN Blob {blob_id} at ({u:.4f}, {v:.4f})")
                ext.SendOSC('/touch/begin', blob_id, u, v, width, height)
                ext.active_blobs.val[blob_id] = ext.Blob(blob_id, u, v, 'active')
                ext.active_blobs.modified()
        else:
            if active:
                ext.SendOSC('/touch/move', blob_id, u, v, width, height)
                ext.active_blobs.val[blob_id].u = u
                ext.active_blobs.val[blob_id].v = v
                ext.active_blobs.modified()
            
            if lost or expired:
                ext.Debug(f"[DAT] END Blob {blob_id} ({'lost' if lost else 'expired'}) at ({u:.4f}, {v:.4f})")
                ext.SendOSC('/touch/end', blob_id, u, v, width, height)
                if blob_id in ext.active_blobs.val:
                    del ext.active_blobs.val[blob_id]
                    ext.active_blobs.modified()
    
    tracked_ids = set(ext.active_blobs.val.keys())
    missing_ids = tracked_ids - current_blob_ids
    
    for missing_id in missing_ids:
        stored_blob = ext.active_blobs.val[missing_id]
        ext.Debug(f"[DAT] END Blob {missing_id} (removed from table) at ({stored_blob.u:.4f}, {stored_blob.v:.4f})")
        ext.SendOSC('/touch/end', missing_id, stored_blob.u, stored_blob.v, 0.1, 0.1)
        del ext.active_blobs.val[missing_id]
        ext.active_blobs.modified()

def onRowChange(dat, row):
    pass

def onColChange(dat, col):
    pass

def onCellChange(dat, row, col, prev):
    pass