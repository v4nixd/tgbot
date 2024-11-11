import segno
import io

def generate(content: str) -> bytes:
    img = segno.make(content)
    buffer = io.BytesIO()
    img.save(buffer, kind="png", scale=10)
    img_bytes = buffer.getvalue()
    buffer.close()
    return img_bytes
