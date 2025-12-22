def onTableChange(dat):
    """
    ULTIMATE TABLE CHANGE HANDLER
    Processes blob tracking table with full begin/move/end lifecycle
    """
    ext = parent.blobtrack.extensions[0]
    
    if not ext:
        debug("[ERROR] Extension not found!")
        return
    
    # Increment frame counter
    ext.current_frame += 1
    
    ext.Debug("=" * 80)
    ext.Debug(f"[FRAME {ext.current_frame}] Processing {dat.numRows - 1} rows")
    
    # Get current blob IDs from table
    current_blob_ids = set()
    
    # Process all rows
    for i in range(1, dat.numRows):
        try:
            blob_id = int(dat[i, 'id'].val)
            u = float(dat[i, 'u'].val)
            v = float(dat[i, 'v'].val)
            width = float(dat[i, 'width'].val)
            height = float(dat[i, 'height'].val)
            active = int(dat[i, 'active'].val)
            lost = int(dat[i, 'lost'].val)
            expired = int(dat[i, 'expired'].val)
            
            # Only process active blobs
            if active:
                current_blob_ids.add(blob_id)
                
                # Check if this is a new blob
                if blob_id not in ext.ActiveBlobs:
                    ext.ProcessBlobBegin(blob_id, u, v, width, height)
                else:
                    ext.ProcessBlobMove(blob_id, u, v, width, height)
            
            # Handle lost/expired blobs
            elif (lost or expired) and blob_id in ext.ActiveBlobs:
                ext.ProcessBlobEnd(blob_id)
        
        except Exception as e:
            ext.Debug(f"[ERROR] Processing row {i}: {e}")
    
    # Clean up blobs that disappeared from table entirely
    tracked_ids = set(ext.ActiveBlobs.keys())
    missing_ids = tracked_ids - current_blob_ids
    
    for missing_id in missing_ids:
        ext.Debug(f"[CLEANUP] Blob {missing_id} disappeared from table")
        ext.ProcessBlobEnd(missing_id)
    
    ext.Debug(f"[FRAME {ext.current_frame}] Complete - {ext.GetActiveBlobCount()} active blobs")

def onRowChange(dat, row):
    pass

def onColChange(dat, col):
    pass

def onCellChange(dat, row, col, prev):
    pass