import itertools


def calculation_rtp(bet_size: int) -> float:
    symbols_on_reel = ['R', 'B', 'L', 'B', 'L']

    symbol_combination = []
    # Количество барабанов
    num_reels = 5

    # Генерация всех возможных комбинаций
    symbol_combinations = [''.join(combination) for combination in
                           itertools.product(symbols_on_reel, repeat=num_reels)]

    # Вывод всех комбинаций
    for combination in symbol_combinations:
        symbol_combination.append(combination)

    num_combinations = len(symbol_combination)
    uniform_probability = 1 / num_combinations
    probabilities = [uniform_probability] * num_combinations

    payouts = [
        bet_size * 9.7 if 'LLLLL' in combination or 'BBBBB' in combination else
        0 for combination in symbol_combinations
    ]

    expected_income = sum(prob * payout for prob, payout in zip(probabilities, payouts))
    total_bet = sum(prob * bet_size for prob in probabilities)
    rtp = ((expected_income / total_bet) * 100) * 5

    print(f"RTP: {rtp}%")


calculation_rtp(10) # расчитываем процент RTP от выбранной ставки