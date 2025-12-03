import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# スマホ最適化：横幅いっぱい使う設定
st.set_page_config(layout="wide")

# ダークテーマ（オシロ風）
plt.style.use("dark_background")

# スマホ最適化 CSS
st.markdown("""
    <style>
    /* 全体の余白を調整 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* スマホ向けフォント調整 */
    @media (max-width: 640px) {
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        .stSlider { font-size: 0.9rem !important; }
    }

    /* グラフがスマホで潰れないように中央寄せ */
    .plot-container {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.title("📱 トランジスタ特性ジェネレーター（クール版・スマホ最適化）")

# モード切り替え
mode = st.selectbox(
    "モードを選んでください",
    ["BJT（NPN）", "BJT（PNP）", "MOSFET（N-ch）", "MOSFET（P-ch）", "マニアックモード（BJT）"]
)

# 蛍光カラー
colors = ["#00FFAA", "#00AFFF", "#FF00FF", "#00FF44", "#FF8844", "#33CCFF", "#FF22AA"]

# ⭐ グラフをスマホ読みやすく描く関数
def render_plot():
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.pyplot(plt)
    st.markdown('</div>', unsafe_allow_html=True)


# =======================
# ① BJT NPN
# =======================
if mode == "BJT（NPN）":
    st.subheader("BJT NPN：Ic–Vce 特性")

    beta = st.slider("β（電流増幅率）", 50, 300, 150)
    Ib_min = st.slider("最小Ib [mA]", 0.01, 0.2, 0.02)
    Ib_max = st.slider("最大Ib [mA]", 0.05, 1.0, 0.1)
    num_curves = st.slider("曲線の数", 2, 8, 5)

    Vce = np.linspace(0, 10, 300)
    Ib_values = np.linspace(Ib_min, Ib_max, num_curves)

    plt.figure(figsize=(8, 5))  # スマホで潰れにくい比率
    for i, Ib in enumerate(Ib_values):
        Ic = beta * Ib
        Ic_curve = Ic * (1 - np.exp(-Vce))
        plt.plot(Vce, Ic_curve, color=colors[i % len(colors)], linewidth=2,
                 label=f"Ib={Ib:.2f} mA")

    plt.title("Ic–Vce（NPN）", color="#00FFAA")
    plt.xlabel("Vce [V]")
    plt.ylabel("Ic [mA]")
    plt.grid(color="#444")
    plt.legend(facecolor="#222")
    render_plot()


# =======================
# ② BJT PNP
# =======================
elif mode == "BJT（PNP）":
    st.subheader("BJT PNP：Ic–Vce 特性")

    beta = st.slider("β（電流増幅率）", 50, 300, 150)
    Ib_min = st.slider("最小|Ib| [mA]", 0.01, 0.2, 0.02)
    Ib_max = st.slider("最大|Ib| [mA]", 0.05, 1.0, 0.1)
    num_curves = st.slider("曲線の数", 2, 8, 5)

    Vce = np.linspace(0, -10, 300)
    Ib_values = np.linspace(Ib_min, Ib_max, num_curves)

    plt.figure(figsize=(8, 5))
    for i, Ib in enumerate(Ib_values):
        Ic = -(beta * Ib)
        Ic_curve = Ic * (1 - np.exp(Vce))
        plt.plot(Vce, Ic_curve, color=colors[i % len(colors)], linewidth=2,
                 label=f"|Ib|={Ib:.2f} mA")

    plt.title("Ic–Vce（PNP）", color="#FF00FF")
    plt.xlabel("Vce [V]")
    plt.ylabel("Ic [mA]")
    plt.grid(color="#444")
    plt.legend(facecolor="#222")
    render_plot()


# =======================
# ③ MOSFET N-ch
# =======================
elif mode == "MOSFET（N-ch）":
    st.subheader("MOSFET N-ch：Id–Vds 特性")

    Vth = st.slider("Vth [V]", 0.5, 3.0, 1.0)
    k = st.slider("k（トランスコンダクタンス）", 0.1, 5.0, 1.0)
    Vgs_min = st.slider("最小Vgs [V]", 1.0, 5.0, 2.0)
    Vgs_max = st.slider("最大Vgs [V]", 2.0, 10.0, 6.0)
    num_curves = st.slider("曲線の数", 2, 8, 5)

    Vds = np.linspace(0, 10, 300)
    Vgs_values = np.linspace(Vgs_min, Vgs_max, num_curves)

    plt.figure(figsize=(8, 5))
    for i, Vgs in enumerate(Vgs_values):
        Id = []
        for v in Vds:
            if Vgs < Vth:
                Id.append(0)
            else:
                Id.append(k * (Vgs - Vth) ** 2 * (1 - np.exp(-v)))
        plt.plot(Vds, Id, color=colors[i % len(colors)], linewidth=2,
                 label=f"Vgs={Vgs:.1f} V")

    plt.title("Id–Vds（N-ch）", color="#00AFFF")
    plt.xlabel("Vds [V]")
    plt.ylabel("Id")
    plt.grid(color="#444")
    plt.legend(facecolor="#222")
    render_plot()


# =======================
# ④ MOSFET P-ch
# =======================
elif mode == "MOSFET（P-ch）":
    st.subheader("MOSFET P-ch：Id–Vds 特性")

    Vth = st.slider("Vth（負）[V]", -3.0, -0.5, -1.0)
    k = st.slider("k（P-ch）", 0.1, 5.0, 1.0)
    Vgs_min = st.slider("最小Vgs（負）[V]", -10.0, -2.0, -6.0)
    Vgs_max = st.slider("最大Vgs（負）[V]", -5.0, -1.0, -2.0)
    num_curves = st.slider("曲線の数", 2, 8, 5)

    Vds = np.linspace(0, -10, 300)
    Vgs_values = np.linspace(Vgs_min, Vgs_max, num_curves)

    plt.figure(figsize=(8, 5))
    for i, Vgs in enumerate(Vgs_values):
        Id = []
        for v in Vds:
            if Vgs > Vth:
                Id.append(0)
            else:
                Id.append(-k * (Vgs - Vth) ** 2 * (1 - np.exp(v)))
        plt.plot(Vds, Id, color=colors[i % len(colors)], linewidth=2,
                 label=f"Vgs={Vgs:.1f} V")

    plt.title("Id–Vds（P-ch）", color="#FF8844")
    plt.xlabel("Vds [V]")
    plt.ylabel("Id")
    plt.grid(color="#444")
    plt.legend(facecolor="#222")
    render_plot()


# =======================
# ⑤ マニアック（Early効果入りBJT）
# =======================
else:
    st.subheader("マニアック：BJT + Early効果")

    beta = st.slider("β", 50, 500, 200)
    Ib_min = st.slider("最小Ib [mA]", 0.01, 0.2, 0.02)
    Ib_max = st.slider("最大Ib [mA]", 0.05, 2.0, 0.5)
    num_curves = st.slider("曲線の数", 2, 10, 6)
    Va = st.slider("Early電圧 Va（大きいほど直線に近い）", 20, 200, 100)

    Vce = np.linspace(0, 15, 300)
    Ib_values = np.linspace(Ib_min, Ib_max, num_curves)

    plt.figure(figsize=(8, 5))
    for i, Ib in enumerate(Ib_values):
        Ic0 = beta * Ib
        lambda_val = 1.0 / Va
        Ic_curve = Ic0 * (1 + lambda_val * Vce)
        Ic_curve = Ic_curve * (1 - np.exp(-Vce))
        plt.plot(Vce, Ic_curve, color=colors[i % len(colors)], linewidth=2,
                 label=f"Ib={Ib:.2f} mA")

    plt.title("Ic–Vce（Early効果）", color="#FF22AA")
    plt.xlabel("Vce [V]")
    plt.ylabel("Ic")
    plt.grid(color="#444")
    plt.legend(facecolor="#222")
    render_plot()
