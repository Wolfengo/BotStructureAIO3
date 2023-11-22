TEST = True

# Токен бота
TEST_TOKEN = ""
REALISE_TOKEN = ""

BOT_TOKEN = TEST_TOKEN if TEST is True else REALISE_TOKEN

# Токен оплаты
PAYMENTS_TOKEN = ""

# Имя пользователя, пароль, хост, порт в PostgreSQL
db_user = "postgres"
db_password = "password"
db_password_postgres = 'password'
db_host = 'localhost'
db_port = 5432

# Имя базы данных
db_name = "telegram"
