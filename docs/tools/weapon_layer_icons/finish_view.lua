-- Hide only our diagnostic overlay, retain its text/logs for inspection.
-- Invoke after all capture batches are done; no inventory/map/camera changes.
ShowConsoleLog(false)
return "Diagnostic overlay hidden; log retained"
