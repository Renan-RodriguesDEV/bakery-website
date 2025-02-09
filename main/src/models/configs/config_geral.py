from streamlit import secrets

configs = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "acess_token": secrets["ACESS_TOKEN"],
    "pix_key": secrets["PIX_KEY"],
    "token_telegram": secrets["TOKEN_TELEGRAM"],
}
