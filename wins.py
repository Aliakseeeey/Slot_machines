# Вспомогательные функции для обнаружения побед

def flip_horizontal(result):
    # Переворачиваем результаты по горизонтали, чтобы они были в более читаемом списке
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    # Переворачиваем на 90 градусов, чтобы получить текстовое представление вращения по порядку.
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y]
    hvals3 = [item[::-1] for item in hvals2]
    return hvals3

def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0, 0
    for i in range(len(hit) - 1):
        # Проверьте, являются ли индексы в параметре попадания последовательными
        if hit[i] == hit[i + 1] - 1:
            subSeqLength += 1
            if subSeqLength > longest:
                longest = subSeqLength
                start = i + 2 - subSeqLength
                end = i + 2
        else:
            subSeqLength = 1
    return hit[start:end]