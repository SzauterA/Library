#regex minták a bekért adatok ellenőrzéséhez
username_pattern = r"^[a-zA-Z][a-zA-Z0-9_-]{2,14}$"
name_pattern = r"^[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
phone_pattern = r"^\+\d{1,19}$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"