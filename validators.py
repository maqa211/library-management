def validate_book(book_id, title, author, year, category):
    if not book_id.strip():
        raise ValueError("Book ID cannot be empty.")

    if not title.strip():
        raise ValueError("Book title cannot be empty.")

    if not author.strip():
        raise ValueError("Author cannot be empty.")

    if not category.strip():
        raise ValueError("Category cannot be empty.")

    try:
        year = int(year)
    except ValueError:
        raise ValueError("Year must be a number.")

    if year <= 0:
        raise ValueError("Year must be greater than 0.")

    return year


def validate_member(member_id, name, phone, email):
    if not member_id.strip():
        raise ValueError("Member ID cannot be empty.")

    if not name.strip():
        raise ValueError("Member name cannot be empty.")

    if not phone.strip():
        raise ValueError("Phone cannot be empty.")

    if not email.strip():
        raise ValueError("Email cannot be empty.")

    if "@" not in email:
        raise ValueError("Please enter a valid email.")

    return True
