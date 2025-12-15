import streamlit as st

# --- Inicjalizacja stanu magazynu (teraz jako słownik) ---
# Klucz: nazwa towaru, Wartość: ilość (int)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = {
        "Kawa": 150, 
        "Herbata": 75, 
        "Mąka": 200
    }
if 'input_dodaj_nazwa' not in st.session_state:
    st.session_state.input_dodaj_nazwa = ""
if 'input_dodaj_ilosc' not in st.session_state:
    st.session_state.input_dodaj_ilosc = 0

# --- Funkcje modyfikujące magazyn ---

def dodaj_towar():
    """Dodaje lub aktualizuje towar wraz z ilością."""
    nazwa = st.session_state.input_dodaj_nazwa.strip()
    ilosc = st.session_state.input_dodaj_ilosc
    
    if nazwa and ilosc > 0:
        if nazwa in st.session_state.magazyn:
            st.session_state.magazyn[nazwa] += ilosc
            st.success(f"Zaktualizowano stan towaru '{nazwa}'. Dodano: {ilosc} szt.")
        else:
            st.session_state.magazyn[nazwa] = ilosc
            st.success(f"Dodano nowy towar: {nazwa} ({ilosc} szt.)")
            
        # Resetujemy pola tekstowe i numeryczne po dodaniu
        st.session_state.input_dodaj_nazwa = ""
        st.session_state.input_dodaj_ilosc = 0
    elif not nazwa:
        st.warning("Nazwa towaru nie może być pusta.")
    elif ilosc <= 0:
        st.warning("Ilość musi być większa niż zero.")

def usun_towar(nazwa):
    """Usuwa towar całkowicie z magazynu i wymusza odświeżenie."""
    if nazwa in st.session_state.magazyn:
        del st.session_state.magazyn[nazwa]
        st.success(f"Usunięto towar: {nazwa}")
        # Wymuszenie odświeżenia, aby poprawnie zaktualizować listę 'selectbox'
        st.rerun() 
    else:
        st.warning(f"Towar '{nazwa}' nie został znaleziony w magazynie.")


# --- Interfejs Streamlit ---

st.title("🦇 Magazyn Gotham (Streamlit)")
st.markdown("### 🌃 System kontroli zapasów Mrocznego Rycerza")
st.caption("Stan magazynu przechowywany jest w sesji (słownik).")


# --- Sekcja Dodawania Towaru ---
st.header("➕ Przyjęcie Towaru")
col1, col2 = st.columns(2)

with col1:
    st.text_input("Nazwa Towaru:", 
                  key="input_dodaj_nazwa", 
                  placeholder="Np. Batarang, Lina")

with col2:
    st.number_input("Ilość:", 
                    min_value=0, 
                    step=1, 
                    key="input_dodaj_ilosc")

# Przycisk wykorzystuje callback (on_click) do wywołania funkcji dodaj_towar.
st.button("Zapisz w Jaskini Batmana", on_click=dodaj_towar, use_container_width=True)


# --- Sekcja Usuwania Towaru ---
st.header("➖ Wydanie Towaru (Usunięcie)")

towary_do_usuniecia = list(st.session_state.magazyn.keys())

if towary_do_usuniecia:
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia:",
        towary_do_usuniecia,
        key="wybor_do_usuniecia"
    )

    # Przycisk usuwania wywołuje funkcję z argumentem
    if st.button(f"Usuń {wybrany_do_usuniecia}", use_container_width=True):
        usun_towar(wybrany_do_usuniecia)
else:
    st.info("Magazyn jest pusty. Nie ma nic do usunięcia.")


# --- Sekcja Aktualnego Magazynu ---
st.header("📝 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Tworzymy listę krotek (nazwa, ilość) do wyświetlenia
    dane = [(k, v) for k, v in st.session_state.magazyn.items()]
    
    # Wyświetlanie stanu magazynu w formie tabeli dla lepszej czytelności
    st.dataframe(dane, 
                 column_config={0: "Nazwa Towaru", 1: "Ilość"}, 
                 hide_index=True, 
                 use_container_width=True)
    
    total_items = sum(st.session_state.magazyn.values())
    st.info(f"Całkowita liczba jednostek w magazynie: **{total_items}**")
else:
    st.warning("Magazyn jest obecnie pusty.")
