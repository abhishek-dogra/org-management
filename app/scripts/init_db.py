from app.utils.startup import wait_for_database, create_tables_if_not_exist, check_database_health

wait_for_database()
create_tables_if_not_exist()
check_database_health()
