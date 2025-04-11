from flask import Flask, jsonify, request
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API Scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Embed service account credentials directly (REMOVE THIS in production and use env/secure store)
service_account_info = {
  "type": "service_account",
  "project_id": "flask-sheet-api",
  "private_key_id": "69e575b52a66b9616eaf58f9378734e845c9304f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCPmoXg78OI+OtV\nFGqtQHs8Phfh2G8FvzIF5DqWkOwTNfkQueeC75+ck4r9SoFXZJVVjtIZD/Qf0uLN\nUyBlDrJ0ReNLK2QoQWkeU5X/ywJr9756TYZaclSiK7UX+z/DVR3KZOtho0vXnGTj\nCSVbgB7FWSGLNHjZEktnwexb2g33oSOHx5W4xNtvis2hL6LHLT42byhbtXynNpb3\niQ2rBShG3WMsqoSnH2IUIOuCGjT3X8pcpn5baoLU3Vs1hGN5dRt4HFfSRFjZWwy8\nj5pytKDAwiJzSJvhQBrAIfT/EFFMLvNVdEBsD8CP7+FGZ9BUSXMF/OCmePd2qzV6\n9L3wgNhTAgMBAAECggEAKI9V+fruiQz5dx3dpZKdXB4To8P8U6y1hcl5LNbA/woT\nD4DanXZt6A0aSEFXd+Yecbx1pgOGCckIK0Mr1q9IgyPMN4qJbv9On/Su3MErrXAb\nmjK0XG6HbgiXTS83SsYLNIO9oeW8AamYKzIFnar5xfbPTSCkc3dB2gwBZM4ZfNPX\nubCfNdfx687I1oHVZ2jFGkAgLcvA8M72ePEl/zsjqq1pM0AUxky7ZnBtMAbxuBN/\nZ5t5nVSFUNccHP5a8pxdmtrt29mhMCKesu/dZgoYW9bM3X4JzAkv2CsO8nukWOEd\nW7faE8AChY+mnfnbnVswGJ78VJizWdEq2NndF69MVQKBgQDFGKj8Mt/LX4Y2GIc1\nft2GdhmhFDzDsZmLwLHiIL1+T/I0zkMwYOVHWsAZwyFIzN8xyaTustJD5YYVzmMD\nUhyhqapCkjb7mXdV42HuV3exPUYqaiNEed8gOedUqO/vCWKsL+Kvhu/1WEWTjAPY\nYFL74SfwgJC142W6WzCnggiXDwKBgQC6hUU241W+7q9Qb82VFrbzma0WSg1CnYgW\nZadBxgYKw13HMd/EbiWq9i1euP0zEnS1mhh7NrBl3IFnoXHojzDO9GF9sL77dgJH\n47rUkT4T9qT1SVNETbeuMtlvOb8CXQ4CMVeJxzAfjwNYdVn+8q+rnE7UUGgIOp71\nbejOmQ+KfQKBgGPjUZEvP1hUuzIjUDL+bsq8g9Ss6vbKxWScbgqKST8AyWGVv1t/\nX/O/vGfSCsZYfi0/YoVOv12Fr2TRykBelwAfephufcsZRe+TY4hlb9W1lh/c1q7X\njQtKDUFMtPzSJt3ZDuuiWW5gJDLY3QIGH0hkHde3cJ+d9Wpy2L+sGSplAoGAKmCh\nKylXj/vW5SWhxd/VTV97DfdhL+Nuyffqmm0NbmCY6+sO9ig4crFf+Yd6L6Jf1ere\n6Q+x4FLLK+poYPg3lK29gLspiSR0vDSnfChLvGlrbTdtrbUiqHdxI24xUa4mwqTH\nSMxyyJjLn8t52Qz2kL0AxAhIuqXm+8gu/tGT0FkCgYEAugbgNeDL7gux/Br5V1RS\nXwuvwzN4KSsIGLa+84Dj9LhaLmEuotYIwUxSmYfKIx2NjNcwpxXLwbAa6geTN9Df\ngpsSD1unF7VXb9qUWUybW1qZRmScLx1vq2SJH1KaQFeZgqBzvm0/fTA1IwVxIt/D\nZvm/NkAJQAY5grA/0ynqWRw=\n-----END PRIVATE KEY-----\n",
  "client_email": "flask-service-account@flask-sheet-api.iam.gserviceaccount.com",
  "client_id": "112439755545531505913",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/flask-service-account%40flask-sheet-api.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}



# Authorize using dict
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(credentials)

# Google Sheet details
SHEET_ID = "1y9w0M7w3IRidYKb2gJzhJK6_g5sPbvkCtS87n73JNs0"
WORKSHEET_NAME = "orders"
sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        records = sheet.get_all_records()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orderstatus/<order_id>', methods=['GET'])
def order_status(order_id):
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
    try:
        data = request.get_json()
        if not data or 'Order ID' not in data:
            return jsonify({"error": "Order ID is required"}), 400

        order_id = str(data['Order ID'])
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        if order_id not in df['Order ID'].astype(str).values:
            return jsonify({"error": "Order not found"}), 404

        row_index = df[df['Order ID'].astype(str) == order_id].index[0] + 2
        action_col_index = df.columns.get_loc("Action") + 1

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
        expected_fields = ['Order ID', 'Customer Name', 'Medicine', 'Quantity',
                           'Order Date', 'Delivery Date', 'Status', 'Action']

        data = request.get_json()
        missing_fields = [field for field in expected_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        new_row = [data[field] for field in expected_fields]
        sheet.append_row(new_row)

        return jsonify({
            "message": "New order added successfully",
            "order": dict(zip(expected_fields, new_row))
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
