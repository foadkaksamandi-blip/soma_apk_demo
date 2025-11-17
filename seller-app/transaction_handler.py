# seller-app/transaction_handler.py
import qrcode
import json
import uuid
import time

# --- Seller's Wallet and Information ---
# In a real app, this would be loaded securely.
SELLER_DATA = {
    "id": "SELLER_12345",
    "name": "My Awesome Store"
}

def generate_payment_request(amount):
    """
    Generates the data structure for a payment request.
    """
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number.")

    transaction_data = {
        "type": "PAYMENT_REQUEST",
        "seller_info": SELLER_DATA,
        "transaction_details": {
            "amount": amount,
            "currency": "IRR",
            "transaction_id": str(uuid.uuid4()),
            "timestamp": int(time.time())
        }
    }
    return transaction_data

def create_qr_code(data, file_path="payment_qr.png"):
    """
    Creates a QR code from the given data and saves it as an image file.
    """
    try:
        json_data = json.dumps(data, indent=4)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)
        print(f"QR code successfully generated and saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

if __name__ == '__main__':
    # --- Demo: Seller creates a payment request ---
    payment_amount = 50000  # 50,000 IRR
    print(f"Seller '{SELLER_DATA['name']}' is requesting a payment of {payment_amount} IRR.")

    # 1. Generate the transaction data
    request_data = generate_payment_request(payment_amount)
    print("\nGenerated Transaction Data:")
    print(json.dumps(request_data, indent=4))

    # 2. Create a QR code from the data
    create_qr_code(request_data)
