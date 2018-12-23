from presets import USER_DATA_FILE


def new_file():
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as outfile:
        user_data = ""
        outfile.write(user_data)


def to_file(user_data):
    with open(USER_DATA_FILE, 'a', encoding='utf-8') as outfile:
        outfile.write(user_data)
