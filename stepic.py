from PIL import Image

def _int_to_bin(rgb):
    return tuple(format(c, '08b') for c in rgb)

def _bin_to_int(rgb):
    return tuple(int(c, 2) for c in rgb)

def _merge_rgb(rgb, bits):
    r, g, b = _int_to_bin(rgb)
    new_rgb = r[:-1] + bits[0], g[:-1] + bits[1], b[:-1] + bits[2]
    return _bin_to_int(new_rgb)

def encode(img, data):
    img = img.convert('RGB')
    encoded = img.copy()
    width, height = img.size
    data += chr(0)  # Null char to indicate end of message
    data_bits = ''.join(format(ord(c), '08b') for c in data)
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index + 3 <= len(data_bits):
                rgb = img.getpixel((x, y))
                bits = data_bits[data_index:data_index+3]
                data_index += 3
                encoded.putpixel((x, y), _merge_rgb(rgb, bits))
            else:
                return encoded
    return encoded

def decode(img):
    img = img.convert('RGB')
    width, height = img.size
    bits = ''

    for y in range(height):
        for x in range(width):
            r, g, b = _int_to_bin(img.getpixel((x, y)))
            bits += r[-1] + g[-1] + b[-1]

    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''
    for c in chars:
        if int(c, 2) == 0:
            break
        message += chr(int(c, 2))
    return message
