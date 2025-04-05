import math

TARGET = int(input("請輸入目標："))
TOTAL_ROUNDS = 10
initial_money = 8888
options_first5 = [10, 30, 60]
options_last5 = [10, 30, 60, 100]
rate_table = [2.00, 2.03, 2.22, 2.33, 3.14, 3.14, 5.55, 5.55, 6.18, 8.88]

def discretize(money, round_index):
    resolution = 1 if round_index < 5 else 10
    return (money // resolution) * resolution

dp = {(0, 0, initial_money): (initial_money, 0, [])}

for round_index in range(TOTAL_ROUNDS):
    if round_index > 0:
        print("\033[F\033[K", end="")
    new_dp = {}
    choices = options_first5 if round_index < 5 else options_last5
    dp_items = list(dp.items())
    total_steps = len(dp_items) * len(choices)
    current_step = 0
    last_percent = -1
    for (r, ws, dmoney), (money, win_streak, path) in dp_items:
        if r != round_index or money <= 0:
            current_step += len(choices)
            continue
        for pct in choices:
            bet = math.ceil(money * pct / 100)
            bet = min(bet, money)
            current_rate = rate_table[win_streak] if win_streak < len(rate_table) else rate_table[-1]
            bonus = math.ceil(current_rate * bet)
            new_money_win = money + bonus
            new_win_streak = win_streak + 1
            new_path_win = path + [f"第{round_index+1}輪贏{pct}%"]
            new_dmoney = discretize(new_money_win, round_index)
            key_win = (round_index+1, new_win_streak, new_dmoney)
            if key_win not in new_dp or abs(new_dp[key_win][0] - TARGET) > abs(new_money_win - TARGET):
                new_dp[key_win] = (new_money_win, new_win_streak, new_path_win)
            new_money_loss = money - bet
            if new_money_loss > 0:
                new_path_loss = path + [f"第{round_index+1}輪輸{pct}%"]
                new_dmoney_loss = discretize(new_money_loss, round_index)
                key_loss = (round_index+1, 0, new_dmoney_loss)
                if key_loss not in new_dp or abs(new_dp[key_loss][0] - TARGET) > abs(new_money_loss - TARGET):
                    new_dp[key_loss] = (new_money_loss, 0, new_path_loss)
            current_step += 1
            progress = current_step / total_steps
            percent = progress * 100
            if int(percent) != last_percent:
                last_percent = int(percent)
                current_best = min(new_dp.values(), key=lambda x: abs(x[0]-TARGET))[0] if new_dp else dp_items[0][1][0]
                print(f"\r{round_index+1}/{TOTAL_ROUNDS} 輪，最佳本金：{current_best:,}，進度 {percent:5.1f}%，狀態數 {len(new_dp)}/{total_steps}", end='')
    dp = new_dp
    best = min(dp.values(), key=lambda x: abs(x[0]-TARGET))
    print(f"\r{round_index+1}/{TOTAL_ROUNDS} 輪，最佳本金：{best[0]:,}，進度 100.0%，狀態數 {len(dp)}/{total_steps}")

best_money, best_ws, best_path = min(dp.values(), key=lambda x: abs(x[0]-TARGET))
if best_money == TARGET:
    print("\n目標", TARGET, "的解存在")
    print("\n==== 路徑 ====")
    for move in best_path:
        print(move)
else:
    print("\n目標", TARGET, "的解不存在，距離", TARGET, "最近的解為", best_money, "，差距", abs(best_money - TARGET))
    print("\n===== 路徑 =====")
    for move in best_path:
        print(move)
