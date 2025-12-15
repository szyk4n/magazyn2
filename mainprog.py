import streamlit as st

# --- Inicjalizacja stanu magazynu ---
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Kawa", "Herbata", "Cukier", "Mąka"]

def dodaj_towar(nazwa):
    """Dodaje towar do listy, jeśli nie jest pusty."""
    if nazwa:
        st.session_state.magazyn.append(nazwa)

def usun_towar(nazwa):
    """Usuwa pierwsze wystąpienie towaru z listy."""
    try:
        st.session_state.magazyn.remove(nazwa)
    except ValueError:
        st.warning(f"Towar '{nazwa}' nie został znaleziony w magazynie.")

# --- Interfejs Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("Dane przechowywane są w sesji (listy). Nie są zapisywane na stałe.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")
nowy_towar = st.text_input("Nazwa nowego towaru:", key="input_dodaj")

if st.button("Dodaj do Magazynu"):
    dodaj_towar(nowy_towar.strip())
    st.success(f"Dodano towar: {nowy_towar.strip()}")
    # Wyczyść pole tekstowe po dodaniu
    st.session_state.input_dodaj = "" 

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

towary_do_usuniecia = st.session_state.magazyn

if towary_do_usuniecia:
    # Używamy st.selectbox, aby wybrać towar z listy
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia:",
        towary_do_usuniecia
    )

    if st.button("Usuń wybrany towar"):
        usun_towar(wybrany_do_usuniecia)
        st.success(f"Usunięto towar: {wybrany_do_usuniecia}")
        
        # 🟢 POPRAWKA: Zmiana st.experimental_rerun() na st.rerun()
        st.rerun() 
        # Jest to konieczne, aby natychmiast odświeżyć listę opcji w st.selectbox po usunięciu.

else:
    st.info("Magazyn jest pusty. Nie ma nic do usunięcia.")

# --- Sekcja Aktualnego Magazynu ---
st.header("📝 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Wyświetlanie listy towarów jako listę punktową
    for towar in st.session_state.magazyn:
        st.write(f"* {towar}")
    
    st.info(f"Łączna liczba towarów: **{len(st.session_state.magazyn)}**")
else:
    st.warning("Magazyn jest obecnie pusty.")

st.markdown("---")
st.caption("Użyto `st.rerun()` zamiast przestarzałego `st.experimental_rerun()`.")
