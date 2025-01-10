import uuid

def generate_uuid() -> str:
    """
    تولید یک شناسه یکتای جدید (UUID).
    
    Returns:
        str: یک رشته متنی شامل UUID نسخه 4.
    """
    return str(uuid.uuid4())
