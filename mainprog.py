import streamlit as st

# --- Inicjalizacja stanu magazynu ---
# Używamy st.session_state do przechowywania listy towarów.
# Jest to kluczowe dla zachowania danych podczas interakcji.
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

# Tworzenie listy opcji do usunięcia
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
        # Wymuszenie odświeżenia, aby poprawnie zaktualizować listę selectbox
        st.experimental_rerun() 

else:
    st.info("Magazyn jest pusty. Nie ma nic do usunięcia.")

# --- Sekcja Aktualnego Magazynu ---
st.header("📝 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Wyświetlanie listy towarów jako listę punktową
    for towar in st.session_state.magazyn:
        st.write(f"* {towar}")
    
    # Opcjonalnie: Wyświetlanie jako DataFrame
    # st.dataframe({"Nazwa Towaru": st.session_state.magazyn})
    
    st.info(f"Łączna liczba towarów: **{len(st.session_state.magazyn)}**")
else:
    st.warning("Magazyn jest obecnie pusty.")

# --- Instrukcja dla Streamlit ---
st.markdown("---")
st.caption("Aby uruchomić tę aplikację lokalnie, zapisz kod jako `app.py` i uruchom w terminalu komendę: `streamlit run app.py`")
