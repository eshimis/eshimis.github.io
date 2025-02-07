from js import document
from collections import defaultdict

def dp_sequential_extraction_probabilities(items, probabilities, num_select):
    """
    DP を用いて、重複なく非復元抽出で num_select 個を選ぶ場合の、
    各組み合わせ（frozenset状態）の確率を計算する関数
    """
    n = len(items)
    dp = [defaultdict(float) for _ in range(num_select + 1)]
    dp[0][frozenset()] = 1.0
    for k in range(num_select):
        for selected_set, prob_so_far in list(dp[k].items()):
            remaining_total = sum(probabilities[i] for i in range(n) if items[i] not in selected_set)
            if remaining_total == 0:
                continue
            for i in range(n):
                if items[i] in selected_set:
                    continue
                new_set = selected_set | frozenset([items[i]])
                dp[k + 1][new_set] += prob_so_far * (probabilities[i] / remaining_total)
    return dp[num_select]

# CSVから取得したアイテムと正規化済み確率（既に正規化済み）
items = ["Shiny", "Radiant", "Silver", "Gold", "Platinum", "Copper", "Weapon Parts", 
         "Flower", "Colorful", "Mystic", "Diamond", "Abundance", "Hyakkiyako", 
         "Red Winter", "Trinity", "Gehenna", "Abydos", "Millennium", "Shanhaijing", 
         "Valkyrie", "Arius"]

probabilities = [0.3619492909141521, 0.09976807370069578, 0.09048732272853803,
                 0.06032488181902535, 0.05336431883990704, 0.01392112695823662,
                 0.018561501944315495, 0.09280751072157747, 0.12529013862412958,
                 0.006960562979118311, 0.002320187993039436, 0.002320187993039436,
                 0.007991654976025036, 0.007991654976025036, 0.007991654976025036,
                 0.007991654976025036, 0.007991654976025036, 0.007991654976025036,
                 0.007991654976025036, 0.007991654976025036, 0.007991654976025036]

def run_calculation(event):
    # 入力欄から num_select を取得
    num_select_str = document.getElementById("num_select").value
    try:
        num_select = int(num_select_str)
    except Exception as e:
        num_select = 5

    # 出力エリアを初期化
    output_div = document.getElementById("output")
    output_div.innerHTML = "<p>計算中…</p>"

    dp_result = dp_sequential_extraction_probabilities(items, probabilities, num_select)
    total_probability = sum(dp_result.values())
    
    total_flower = 0      # "Flower" を含む組み合わせ
    total_radiant = 0     # "Flower" を含まないが "Radiant" を含む組み合わせ
    total_shiny = 0       # "Flower" も "Radiant" も含まないが "Shiny" を含む組み合わせ

    for comb, prob in dp_result.items():
        if "Flower" in comb:
            total_flower += prob
        elif "Radiant" in comb:
            total_radiant += prob
        elif "Shiny" in comb:
            total_shiny += prob

    # 結果をHTMLで整形して出力エリアに表示
    result_html = f"""
    <p><strong>Total probability (should be 1.0):</strong> {total_probability:.6f}</p>
    <p><strong>Probability including 'Flower':</strong> {total_flower:.6f}</p>
    <p><strong>Probability including 'Radiant' (without 'Flower'):</strong> {total_radiant:.6f}</p>
    <p><strong>Probability including 'Shiny' (without 'Flower' and 'Radiant'):</strong> {total_shiny:.6f}</p>
    """
    output_div.innerHTML = result_html

# ボタンにイベントリスナーを設定
document.getElementById("run-btn").addEventListener("click", run_calculation)
