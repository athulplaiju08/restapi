from flask import Flask, jsonify, request
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Credentials & Sheet Info
CREDENTIALS_FILE = "flask-sheet-api-d0de2646fb83.json"
SHEET_ID = "1y9w0M7w3IRidYKb2gJzhJK6_g5sPbvkCtS87n73JNs0"
WORKSHEET_NAME = "orders" 

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)


@app.route('/action', methods=['PATCH'])
def change_action():
    try:
        data = request.get_json()
        if not data or 'Order ID' not in data:
            return jsonify({"error": "Order ID is required"}), 400

        order_id = str(data['Order ID'])
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        if order_id not in df['Order ID'].astype(str).values:
            return jsonify({"error": "Order not found"}), 404

        row_index = df[df['Order ID'].astype(str) == order_id].index[0] + 2  # header + 0-index
        action_col_index = df.columns.get_loc("Action") + 1  # 1-based index

        sheet.update_cell(row_index, action_col_index, "Cancel")

        updated_row = sheet.row_values(row_index)
        return jsonify({
            "message": f"Action updated to 'Cancel' for Order ID {order_id}",
            "updated_row": updated_row
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
