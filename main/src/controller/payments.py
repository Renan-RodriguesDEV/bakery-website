import mercadopago
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv("ACESS_TOKEN")
sdk = mercadopago.SDK(access_token)


def payment(name_product: str, price: float, quantity: int):
    payment_data = {
        "items": [
            {
                "title": name_product,
                "quantity": quantity,
                "currency_id": "BRL",
                "unit_price": price,
            }
        ],
        "back_urls": {
            "success": "http://localhost:8501/",
            "failure": "http://localhost:8501/",
            "pending": "http://localhost:8501/",
        },
        "auto_return": "all",
    }
    result = sdk.preference().create(payment_data)
    # print(result["response"])
    return result["response"]["init_point"]


link_payment = payment("nome", 1, 1)


print(link_payment)
# d ={'status': 201, 'response': {'additional_info': '', 'auto_return': 'all', 'back_urls': {'failure': 'http://localhost:8501/', 'pending': 'http://
# localhost:8501/', 'success': 'http://localhost:8501/'}, 'binary_mode': False, 'client_id': '8665552835003051', 'collector_id': 446242375, 'coupon_code': None, 'coupon_labels': None, 'date_created': '2024-11-05T13:16:41.155-04:00', 'date_of_expiration': None, 'expiration_date_from': None, 'expiration_date_to': None, 'expires': False, 'external_reference': '', 'id': '446242375-63c321c2-a3ea-4c5d-91b6-176ce0fcf530', 'init_point': 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=446242375-63c321c2-a3ea-4c5d-91b6-176ce0fcf530', 'internal_metadata': None, 'items': [{'id': '', 'category_id': '', 'currency_id': 'BRL', 'description': '', 'title': 'nome', 'quantity': 1, 'unit_price': 1}], 'marketplace': 'MP-MKT-8665552835003051', 'marketplace_fee': 0, 'metadata': {}, 'notification_url': None, 'operation_type': 'regular_payment', 'payer': {'phone': {'area_code': '', 'number': ''}, 'address': {'zip_code': '', 'street_name': '', 'street_number': None}, 'email': '', 'identification': {'number':
# '', 'type': ''}, 'name': '', 'surname': '', 'date_created': None, 'last_purchase': None}, 'payment_methods': {'default_card_id': None, 'default_payment_method_id': None, 'excluded_payment_methods': [{'id': ''}], 'excluded_payment_types': [{'id': ''}], 'installments': None, 'default_installments': None}, 'processing_modes': None, 'product_id': None, 'redirect_urls': {'failure': '', 'pending': '', 'success': ''}, 'sandbox_init_point': 'https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id=446242375-63c321c2-a3ea-4c5d-91b6-176ce0fcf530', 'site_id': 'MLB', 'shipments': {'default_shipping_method': None, 'receiver_address': {'zip_code': '', 'street_name': '', 'street_number': None, 'floor': '', 'apartment': '', 'city_name': None, 'state_name': None, 'country_name': None}}, 'total_amount': None, 'last_updated': None, 'financing_group': ''}}
