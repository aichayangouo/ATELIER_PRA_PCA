import os
import glob
import time
from flask import jsonify

@app.route('/status', methods=['GET'])
def get_status():
    try:
        # Récupération du compte (à adapter selon votre fonction SQLite)
        count = get_db_count() 
        
        backup_files = glob.glob("/backup/*")
        if not backup_files:
            return jsonify({"count": count, "last_backup_file": None, "backup_age_seconds": None}), 200
            
        latest_backup = max(backup_files, key=os.path.getmtime)
        return jsonify({
            "count": count,
            "last_backup_file": os.path.basename(latest_backup),
            "backup_age_seconds": int(time.time() - os.path.getmtime(latest_backup))
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500