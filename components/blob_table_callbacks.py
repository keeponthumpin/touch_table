

def onTableChange(dat):
    ext = parent.blobtrack.extensions[0]
    
    if not ext:
        debug('Blob tracking extension not found')
        return
    """Just send all current active blobs"""
    
    
    # Skip header row, send all active blobs
    for i in range(1, dat.numRows):
        blob_id = int(dat[i, 'id'].val)
        u = float(dat[i, 'u'].val)
        v = float(dat[i, 'v'].val)
        active = int(dat[i, 'active'].val)
        
        # Only send active blobs
        if active:
            ext.SendOSC('/touch/move', blob_id, u, v)

def onRowChange(dat, row):
    pass

def onColChange(dat, col):
    pass

def onCellChange(dat, row, col, prev):
    pass