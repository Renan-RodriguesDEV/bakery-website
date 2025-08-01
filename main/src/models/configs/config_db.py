from streamlit import secrets

configs_db = {
    "username": secrets["TEST_USER_DB"],
    "password": secrets["TEST_PASSWORD_DB"],
    "host": secrets["TEST_HOST_DB"],
    "database": secrets["TEST_DATABASE_NAME"],
    "connection_url": secrets["DATABASE_URL"],
}
