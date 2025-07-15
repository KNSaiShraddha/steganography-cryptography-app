from PIL import Image

def _text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def _bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def encode(image, text):
    binary = _text_to_bin(text) + '1111111111111110'  # EOF marker
    encoded = image.copy()
    pixels = encoded.load()
    width, height = encoded.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index >= len(binary):
                return encoded
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary[data_index])
            data_index += 1
            if data_index < len(binary):
                g = (g & ~1) | int(binary[data_index])
                data_index += 1
            if data_index < len(binary):
                b = (b & ~1) | int(binary[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
    return encoded

def decode(image):
    binary = ''
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)
            binary += str(g & 1)
            binary += str(b & 1)
            if binary[-16:] == '1111111111111110':  # EOF marker
                return _bin_to_text(binary[:-16])
    return _bin_to_text(binary)
