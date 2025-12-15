import streamlit as st

# --- Inicjalizacja stanu magazynu ---
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Kawa", "Herbata", "Cukier", "Mąka"]
if 'input_dodaj' not in st.session_state:
    st.session_state.input_dodaj = ""

# --- Funkcje modyfikujące magazyn ---

def dodaj_towar():
    """Dodaje towar do listy i czyści pole tekstowe."""
    # Pobieramy wartość z pola tekstowego poprzez klucz 'input_dodaj'
    nazwa = st.session_state.input_dodaj.strip()
    
    if nazwa:
        st.session_state.magazyn.append(nazwa)
        st.success(f"Dodano towar: {nazwa}")
        # Resetujemy pole tekstowe po dodaniu (to rozwiązuje Błąd 2)
        st.session_state.input_dodaj = ""
    else:
        st.warning("Nazwa towaru nie może być pusta.")

def usun_towar(nazwa):
    """Usuwa pierwsze wystąpienie towaru z listy i wymusza odświeżenie."""
    try:
        st.session_state.magazyn.remove(nazwa)
        st.success(f"Usunięto towar: {nazwa}")
        # Wymuszenie odświeżenia, aby poprawnie zaktualizować listę 'selectbox'
        # POPRAWKA BŁĘDU 1: Zastąpienie st.experimental_rerun() przez st.rerun()
        st.rerun() 
    except ValueError:
        st.warning(f"Towar '{nazwa}' nie został znaleziony w magazynie.")


# --- Interfejs Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("Dane przechowywane są w sesji. Aplikacja naprawiona, błędy 'st.experimental_rerun' i 'APIException' rozwiązane.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

# st.text_input używa teraz klucza 'input_dodaj' do pobierania i ustawiania wartości.
st.text_input("Nazwa nowego towaru:", 
              key="input_dodaj", 
              placeholder="Wprowadź nazwę towaru")

# Przycisk wykorzystuje callback (on_click) do wywołania funkcji dodaj_towar.
st.button("Dodaj do Magazynu", on_click=dodaj_towar)


# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

towary_do_usuniecia = st.session_state.magazyn

if towary_do_usuniecia:
    # Używamy st.selectbox, aby wybrać towar z listy
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia:",
        towary_do_usuniecia,
        key="wybor_do_usuniecia" # Dodatkowy klucz dla unikalności
    )

    # Przycisk usuwania wywołuje funkcję z argumentem, używając lambda
    if st.button("Usuń wybrany towar"):
        usun_towar(wybrany_do_usuniecia)
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
st.caption("Uruchomienie lokalne: `streamlit run app.py`")
