from uuid import UUID

# Funciones auxiliares

def parse_uuid(value: str):
    try:
        return UUID(value)
    except ValueError:
        return None
