import imageio as iio


def main(args):
    import os, math

    in_file = args[1]
    file_content = iio.imread(in_file)
    if args[2] == "auto":
        s = os.get_terminal_size()
        s2 = file_content.shape
        h, w = s2[0], s2[1]
        f1 = math.ceil(h / (s.lines - 1))
        f2 = math.ceil(2 * w / (s.columns - 1))
        f = max(f1, f2)
    else:
        f = int(args[2])
    pixelated = pixelate(file_content, f)
    print("\033[2J")
    if len(args) == 4:
        print_image(pixelated, args[3])
    elif len(args) == 5:
        print_image(pixelated, args[3], args[4])

    else:
        print_image(pixelated)


def print_image(
    image,
    with_ascii="true",
    with_color="true",
):
    for row in image:
        for col in row:
            c = get_ascii_char(col)
            if with_ascii == "false":
                print(
                    f"\033[48;2;{int(col[0])};{int(col[1])};{int(col[2])}m  ",
                    end="",
                )
            else:
                if with_color == "false":
                    print(f"{c}{c}", end="")
                else:
                    c = get_ascii_char([col[0] * 1.5, col[1] * 1.5, col[2] * 1.5])
                    print(
                        f"\033[38;2;{int(col[0])};{int(col[1])};{int(col[2])}m{c}{c}",
                        end="",
                    )

        print("\033[48;5;0;38;5;7m")


def get_ascii_char(color):
    possible_chars = [" ", ".", "-", "*", "+", "x", "%", "#", "8", "@"]
    sum = ((color[0] + color[1] + color[2]) / 3) ** 2
    sum /= 256**2
    sum *= len(possible_chars)
    sum = max(min(sum, len(possible_chars) - 1), 0)
    return possible_chars[int(sum)]


def pixelate(image, amount):
    kernel_size = (amount, amount)
    pixelated = []
    for row in range(0, len(image), kernel_size[1]):
        p_row = []
        for col in range(0, len(image[row]), kernel_size[0]):
            p_pixel = [0, 0, 0]
            norm_count = 0
            for row_off in range(0, kernel_size[1]):
                for col_off in range(0, kernel_size[0]):
                    try:
                        pixel_val = image[row + row_off][col + col_off]
                    except:
                        break
                    norm_count += 1
                    for i in range(0, 3):
                        p_pixel[i] += pixel_val[i]
            for i in range(0, 3):
                p_pixel[i] /= norm_count
            p_row.append(p_pixel)
        pixelated.append(p_row)
    return pixelated


if __name__ == "__main__":
    import sys

    main(sys.argv)
