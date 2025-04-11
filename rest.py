from flask import Flask, jsonify, request
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API Scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Embed service account credentials directly
service_account_info = {
    "type": "service_account",
    "project_id": "flask-sheet-api",
    "private_key_id": "50b71c6651ab53d541deb7c8f9f60bceff433322",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCUxpskt7yBLvdi\\nEzjUAWkn1ef7zM+g5cwtxZCwbBVj/TPDkgLgPf73dcZRmO9z3PLZllyYNHs6n1cP\\nTMldX1GZLfk7V/EQBfTk2hPStcNKhLRMtQCXYjza/xVslZsTE/4sjR4980HIh/D/\\nfpA9v7mXHTDJofLQvCxZuiVq7rmL7CYUwpyg20xdQ5cNTss4E+wPPlCeSq0LLUnu\\nnSrsmdm4yRp3pycKIzSUCNiGDrJew8ZADzUESipM5oyMKdX7PaD4EFE+vSSswN/V\\nvshVaPN5DIBF7E52LPPMSzEYsIsVI9MIyci+2WrYgBJ0w2dQOQugegEau0LIHJ4U\\nG5RHtutJAgMBAAECggEAMzLj6i9m6kgY70HxMRhpMUHOS1uw6kyaxvex8tzHQbk9\\nyqRhY/1B1LRNswAAC63yTwoNRH3vGH4ETmoc9AqdAKuPFSqO9XYvUGByKPXPRsJD\\ncBBsKyyuB6l4HH2ht9+N/ZP039nqfhG2UJ6kEfP8cPIlO4aFkurnElvai6Gq7eko\\ny4Hjmo4q3HD47/SkhlLuuIe/ceIpV4+gPbZt34Nb+sBhJw2jw+bdT1V7SBojeuMU\\ngFGRp6vitdov6f6g15gesXiiKUsLIzlFojhnm4Weg5tOSYnUTgGJ8NvLSbXdzOM6\\nQZqMcm9tBUKMUuZoUyHY8yGwPGxn+4HctCIW1DHhJwKBgQDKMpxniFvHz/ND3mE4\\njNVZGtJ0xIrNrTgjjKaUkcovr4FyZTOitx+NsqkObg+A18aTiCiVf4ONoYpBSzNU\\nDWHCgWiY6S5x+4QRGyJ9KYUKOT9H4HbtEqtBj8ZWd4iawNknWZu4eEZfplKSYwig\\ndeYhabLRQcorP+8QjcOgXBlB8wKBgQC8XPrOcJaoRY5UemYEMEPKCmKtIRaHDixc\\nxwjN6uDgtMCPf5XzmevRiMz4qkIiQSiH8PRugNNGb0sWvL4nGPySsinjrwcV07vN\\nQODpPkx2fAlhdDI5qyHCjeg5C5oZZjJ96JJdPtzrvDVNkIPpAcQTXdK+VplbaR+7\\nGSa97Vgw0wKBgF2j6Lkt9ktoK+H/iAjXeCrG+DZpm1q7YOddyPu/NOK2pf1jjvFJ\\nW4yU9CQhpn5l76n9gcYSgstBx7SLbh77/41DvzwpqX/SGoyNg4BxjRJ6Bqtz8b/D\\nSJqZSiJbQ2Ff9HF711ksInNDpLP0t1cQot5QhCbTEBzNhBqnfLS0UmIvAoGAQgWp\\nF1DZTbPLloqsVU2BhUCso5hUaBQssnxE9sAcAEb6s5F5wr+xq2jyxzoOIimKhlOL\\nqWvYIfkCbb7MO7IDXXu7OQXxStJDIkdaTga7EFCbjSAINrRoCeRpgA0z/zEWA5HQ\\nM4TENJBscnpz8ejfjBY3tuVtrV+kcpT3Qlz9q2cCgYApzbkmde7nLDQCcG/FlU+/\\nR3B0dTLtBbCc5Sz+o7TKnfUshKN5NrLz/8XTX/elaZsfQlvA0EzAfaSemuSUVmM2\\nfnl/Aq+2o07K1n308ANnUZvm2DM2BOyqQ50WrALcvYCqiT19qp0UpBlwni6yA7EY\\nICRD5bjVumgO/NdoQBabIA==\\n-----END PRIVATE KEY-----\\n",
    "client_email": "flask-service-account@flask-sheet-api.iam.gserviceaccount.com",
    "client_id": "112439755545531505913",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/flask-service-account%40flask-sheet-api.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(credentials)

# Google Sheet details
SHEET_ID = "1y9w0M7w3IRidYKb2gJzhJK6_g5sPbvkCtS87n73JNs0"
WORKSHEET_NAME = "orders"
sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)


@app.route('/data', methods=['GET'])
def get_data():
    """Fetch all order data from Google Sheets."""
    try:
        records = sheet.get_all_records()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/orderstatus/<order_id>', methods=['GET'])
def order_status(order_id):
    """Fetch the status of an order by Order ID."""
    try:
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        order = df[df['Order ID'].astype(str) == order_id]
        if not order.empty:
            status = order.iloc[0]['Status']
            return jsonify({"Order ID": order_id, "Status": status})
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/action', methods=['PATCH'])
def change_action():
    """Update the Action column to 'Cancel' for a given Order ID."""
    try:
        data = request.get_json()
        if not data or 'Order ID' not in data:
            return jsonify({"error": "Order ID is required"}), 400

        order_id = str(data['Order ID'])
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        if order_id not in df['Order ID'].astype(str).values:
            return jsonify({"error": "Order not found"}), 404

        row_index = df[df['Order ID'].astype(str) == order_id].index[0] + 2  # +2 for header row + 1-based index
        action_col_index = df.columns.get_loc("Action") + 1  # 1-based index

        sheet.update_cell(row_index, action_col_index, "Cancel")
        updated_row = sheet.row_values(row_index)

        return jsonify({
            "message": f"Action updated to 'Cancel' for Order ID {order_id}",
            "updated_row": updated_row
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/addorder', methods=['POST'])
def add_order():
    try:
        # Expected fields
        expected_fields = ['Order ID', 'Customer Name', 'Medicine', 'Quantity',
                           'Order Date', 'Delivery Date', 'Status', 'Action']

        data = request.get_json()

        # Ensure all fields are present
        missing_fields = [field for field in expected_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Prepare row data in correct order
        new_row = [data[field] for field in expected_fields]
        sheet.append_row(new_row)

        return jsonify({
            "message": "New order added successfully",
            "order": dict(zip(expected_fields, new_row))
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True, port=6000)
