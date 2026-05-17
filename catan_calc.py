import streamlit as st

st.set_page_config(page_title="Catan Calc", page_icon="🎲", layout="centered")

DOTS = {0: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
HOT = [6, 8]
WARM = [5, 9, 4, 10]
LAYOUT = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, None, None, None, None, 0]

def dot_str(n):
    return "—" if n == 0 else "●" * DOTS.get(n, 0)

if "history" not in st.session_state:
    st.session_state.history = []
if "current" not in st.session_state:
    st.session_state.current = []

st.title("🎲 Catan Calc")

# --- 履歴エリア ---
with st.container(border=True):
    for i in range(5):
        if i < len(st.session_state.history):
            entry = st.session_state.history[i]
            total = sum(DOTS.get(x, 0) for x in entry)
            formula = " + ".join(str(x) for x in entry)
            col1, col2 = st.columns([9, 1])
            col1.write(f"{formula} = {total}")
            if col2.button("✕", key=f"del_{i}"):
                st.session_state.history.pop(i)
                st.rerun()
        elif i == len(st.session_state.history) and len(st.session_state.history) < 5:
            cur = st.session_state.current
            if cur:
                total = sum(DOTS.get(x, 0) for x in cur)
                formula = " + ".join(str(x) for x in cur)
                st.markdown(f":blue[{formula} = {total}]")
            else:
                st.caption("← 数字を選んでください")
        else:
            st.write(" ")

# --- キーパッド ---
cols = st.columns(3)
for i, n in enumerate(LAYOUT):
    col = cols[i % 3]
    if n is None:
        col.write("")
        continue

    dots = dot_str(n)
    if n in HOT:
        label = f"🔴 {n}\n\n{dots}"
    elif n in WARM:
        label = f"🟡 {n}\n\n{dots}"
    else:
        label = f"{n}\n\n{dots}"

    if col.button(label, key=f"key_{n}", use_container_width=True):
        if len(st.session_state.history) < 5:
            st.session_state.current.append(n)
            if len(st.session_state.current) >= 3:
                st.session_state.history.insert(0, st.session_state.current[:])
                if len(st.session_state.history) > 5:
                    st.session_state.history.pop()
                st.session_state.current = []
            st.rerun()

# --- 操作ボタン ---
c1, c2 = st.columns(2)
if c1.button("クリア", use_container_width=True):
    st.session_state.current = []
    st.rerun()
if c2.button("AC", use_container_width=True, type="primary"):
    st.session_state.history = []
    st.session_state.current = []
    st.rerun()
