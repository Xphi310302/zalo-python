import time
import pyautogui


def vietnamese_to_telex(text):
    telex_map = {
        "ă": "aw",
        "â": "aa",
        "ê": "ee",
        "ô": "oo",
        "ơ": "ow",
        "ư": "uw",
        "đ": "dd",
        "á": "as",
        "à": "af",
        "ả": "ar",
        "ã": "ax",
        "ạ": "aj",
        "ắ": "aws",
        "ằ": "awf",
        "ẳ": "awr",
        "ẵ": "awx",
        "ặ": "awj",
        "ấ": "aas",
        "ầ": "aaf",
        "ẩ": "aar",
        "ẫ": "aax",
        "ậ": "aaj",
        "é": "es",
        "è": "ef",
        "ẻ": "er",
        "ẽ": "ex",
        "ẹ": "ej",
        "ế": "ees",
        "ề": "eef",
        "ể": "eer",
        "ễ": "eex",
        "ệ": "eej",
        "í": "is",
        "ì": "if",
        "ỉ": "ir",
        "ĩ": "ix",
        "ị": "ij",
        "ó": "os",
        "ò": "of",
        "ỏ": "or",
        "õ": "ox",
        "ọ": "oj",
        "ố": "oos",
        "ồ": "oof",
        "ổ": "oor",
        "ỗ": "oox",
        "ộ": "ooj",
        "ớ": "ows",
        "ờ": "owf",
        "ở": "owr",
        "ỡ": "owx",
        "ợ": "owj",
        "ú": "us",
        "ù": "uf",
        "ủ": "ur",
        "ũ": "ux",
        "ụ": "uj",
        "ứ": "uws",
        "ừ": "uwf",
        "ử": "uwr",
        "ữ": "uwx",
        "ự": "uwj",
        "ý": "ys",
        "ỳ": "yf",
        "ỷ": "yr",
        "ỹ": "yx",
        "ỵ": "yj",
        "Á": "As",
        "À": "Af",
        "Ả": "Ar",
        "Ã": "Ax",
        "Ạ": "Aj",
        "Ắ": "Aws",
        "Ằ": "Awf",
        "Ẳ": "Awr",
        "Ẵ": "Awx",
        "Ặ": "Awj",
        "Ấ": "Aas",
        "Ầ": "Aaf",
        "Ẩ": "Aar",
        "Ẫ": "Aax",
        "Ậ": "Aaj",
        "É": "Es",
        "È": "Ef",
        "Ẻ": "Er",
        "Ẽ": "Ex",
        "Ẹ": "Ej",
        "Ế": "Ees",
        "Ề": "Eef",
        "Ể": "Eer",
        "Ễ": "Eex",
        "Ệ": "Eej",
        "Í": "Is",
        "Ì": "If",
        "Ỉ": "Ir",
        "Ĩ": "Ix",
        "Ị": "Ij",
        "Ó": "Os",
        "Ò": "Of",
        "Ỏ": "Or",
        "Õ": "Ox",
        "Ọ": "Oj",
        "Ố": "Oos",
        "Ồ": "Oof",
        "Ổ": "Oor",
        "Ỗ": "Oox",
        "Ộ": "Ooj",
        "Ớ": "Ows",
        "Ờ": "Owf",
        "Ở": "Owr",
        "Ỡ": "Owx",
        "Ợ": "Owj",
        "Ú": "Us",
        "Ù": "Uf",
        "Ủ": "Ur",
        "Ũ": "Ux",
        "Ụ": "Uj",
        "Ứ": "Uws",
        "Ừ": "Uwf",
        "Ử": "Uwr",
        "Ữ": "Uwx",
        "Ự": "Uwj",
        "Ý": "Ys",
        "Ỳ": "Yf",
        "Ỷ": "Yr",
        "Ỹ": "Yx",
        "Ỵ": "Yj",
        "Ă": "Aw",
        "Â": "Aa",
        "Ê": "Ee",
        "Ô": "Oo",
        "Ơ": "Ow",
        "Ư": "Uw",
        "Đ": "Dd",
    }
    result = ""
    for char in text:
        result += telex_map.get(char, char)
    return result


def type_vietnamese_text(text):
    """
    Type Vietnamese text using pyautogui by converting to Telex input method
    """
    telex_text = vietnamese_to_telex(text)
    # Add a small delay to ensure the application is ready
    time.sleep(1)
    pyautogui.write(telex_text)


# Example usage
if __name__ == "__main__":
    # Give user time to focus on the desired text field
    print("Focus on the text field where you want to type (you have 3 seconds)...")
    time.sleep(3)

    # Example Vietnamese text
    vietnamese_text = "Xin chào, tôi đang sử dụng tiếng Việt"

    # Convert and type
    print(f"Converting and typing: {vietnamese_text}")
    telex_text = vietnamese_to_telex(vietnamese_text)
    print(f"Telex equivalent: {telex_text}")

    # Type the text
    type_vietnamese_text(telex_text)
