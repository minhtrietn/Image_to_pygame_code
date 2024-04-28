def show_image(image_path, x=0, y=0, resize=None, rotate=0):
    """
    :param image_path: path of image
    :param x: int
    :param y: int
    :param resize: tuple (width, height)
    :param rotate: Should be 0 - 3
    """

    image = Image.open(image_path)

    if resize is not None:
        image = image.resize(resize)

    width, height = image.size

    pixels = image.load()

    pixel = []
    matrix = []

    for i in range(height):
        for j in range(width):
            r, g, b, a = pixels[i, j]
            if a != 0:
                pixel.append((r, g, b, a))
            else:
                pixel.append((0, 0, 0, 0))
        matrix.append(pixel)
        pixel = []

    for i in range(rotate):
        matrix = np.rot90(np.array(matrix))

    single = {}
    vertical = {}
    horizontal = {}
    check_pos = set()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (i, j) not in check_pos and not np.array_equal(matrix[i][j], (0, 0, 0, 0)):
                current = matrix[i][j]
                horizontal_count = 1
                k = j + 1
                while k < len(matrix[0]) and np.array_equal(matrix[i][k], current):
                    horizontal_count += 1
                    k += 1

                # Kiểm tra hàng dọc
                vertical_count = 1
                l = i + 1
                while l < len(matrix) and np.array_equal(matrix[l][j], current):
                    vertical_count += 1
                    l += 1

                if horizontal_count == 1 and vertical_count == 1:
                    single[(i, j)] = current

                if vertical_count > 1:
                    vertical[(i, j, vertical_count, 1)] = current
                    for p in range(i, i + vertical_count):
                        check_pos.add((p, j))
                if horizontal_count > 1:
                    horizontal[(i, j, 1, horizontal_count)] = current
                    for q in range(j, j + horizontal_count):
                        check_pos.add((i, q))

    code = ""

    for i in single.keys():
        code += f"pygame.draw.rect(screen, {tuple(single[i][:3])}, {(i[0] + x, i[1] + y, 1, 1)})\n"
    for i in vertical.keys():
        code += f"pygame.draw.rect(screen, {tuple(vertical[i][:3])}, {i[0] + x, i[1] + y, *i[2:]})\n"
    for i in horizontal.keys():
        code += f"pygame.draw.rect(screen, {tuple(horizontal[i][:3])}, {i[0] + x, i[1] + y, *i[2:]})\n"

    return code


code = show_image("bishop1.png", x=100, y=100, rotate=0)

print(code)
