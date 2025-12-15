import streamlit as st
import pandas as pd # Dodano pandas do lepszego wyświetlania tabeli

# --- Inicjalizacja stanu magazynu (słownik) ---
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = {
        "Batarang": 150, 
        "Lina z hakiem": 75, 
        "Granat dymny": 200
    }
# Stany dla pól wejściowych
if 'input_dodaj_nazwa' not in st.session_state:
    st.session_state.input_dodaj_nazwa = ""
if 'input_dodaj_ilosc' not in st.session_state:
    st.session_state.input_dodaj_ilosc = 0
if 'input_usun_ilosc' not in st.session_state:
    st.session_state.input_usun_ilosc = 1

# --- Funkcje modyfikujące magazyn ---

def dodaj_towar():
    """Dodaje lub aktualizuje towar wraz z ilością."""
    nazwa = st.session_state.input_dodaj_nazwa.strip()
    ilosc = st.session_state.input_dodaj_ilosc
    
    if nazwa and ilosc > 0:
        if nazwa in st.session_state.magazyn:
            st.session_state.magazyn[nazwa] += ilosc
            st.success(f"Zaktualizowano stan '{nazwa}'. Dodano: {ilosc} szt.")
        else:
            st.session_state.magazyn[nazwa] = ilosc
            st.success(f"Dodano nowy towar: {nazwa} ({ilosc} szt.)")
            
        # Resetujemy pola
        st.session_state.input_dodaj_nazwa = ""
        st.session_state.input_dodaj_ilosc = 0
    elif not nazwa:
        st.warning("Nazwa towaru nie może być pusta.")
    elif ilosc <= 0:
        st.warning("Ilość musi być większa niż zero.")

def wydaj_ilosc(nazwa, ilosc_do_usuniecia):
    """Usuwa określoną ilość towaru."""
    if nazwa not in st.session_state.magazyn:
        st.warning(f"Błąd: Towar '{nazwa}' nie istnieje w magazynie.")
        return

    aktualny_stan = st.session_state.magazyn[nazwa]

    if ilosc_do_usuniecia <= 0:
        st.warning("Ilość do usunięcia musi być większa niż zero.")
    elif ilosc_do_usuniecia > aktualny_stan:
        st.error(f"Błąd: Nie można usunąć {ilosc_do_usuniecia} sztuk. Dostępny stan: {aktualny_stan}.")
    else:
        st.session_state.magazyn[nazwa] -= ilosc_do_usuniecia
        st.success(f"Wydano {ilosc_do_usuniecia} sztuk towaru '{nazwa}'. Pozostało: {st.session_state.magazyn[nazwa]} szt.")
        
        # Usuń towar, jeśli stan spadnie do zera
        if st.session_state.magazyn[nazwa] == 0:
             del st.session_state.magazyn[nazwa]
             st.info(f"Towar '{nazwa}' został całkowicie wyczerpany i usunięty z listy.")
             st.rerun() # Wymuszenie odświeżenia, aby zaktualizować selectboxy

def usun_calkowicie(nazwa):
    """Usuwa towar całkowicie z magazynu (cała pozycja)."""
    if nazwa in st.session_state.magazyn:
        del st.session_state.magazyn[nazwa]
        st.success(f"Całkowicie usunięto towar: {nazwa}")
        st.rerun() 
    else:
        st.warning(f"Towar '{nazwa}' nie został znaleziony w magazynie.")


# --- Interfejs Streamlit ---

# 🦇 LOGO BATMANA (Wyśrodkowane i na całą szerokość kolumny)
col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    st.image("batman_logo.png", use_column_width=True) 
    
    st.title("🦇 Magazyn Gotham (Streamlit)")
    st.markdown("### 🌃 System kontroli zapasów Mrocznego Rycerza")

st.caption("Stan magazynu przechowywany jest w sesji. Wymaga pliku `config.toml` dla ciemnego motywu.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Przyjęcie Towaru")
col_add_1, col_add_2 = st.columns(2)

with col_add_1:
    st.text_input("Nazwa Towaru:", 
                  key="input_dodaj_nazwa", 
                  placeholder="Np. Batarang, Lina")

with col_add_2:
    st.number_input("Ilość:", 
                    min_value=0, 
                    step=1, 
                    key="input_dodaj_ilosc")

st.button("Zapisz w Jaskini Batmana", on_click=dodaj_towar, use_container_width=True)

st.markdown("---")

# --- Sekcja Wydawania (Usuwanie Ilości) ---
st.header("🛒 Wydanie Towaru (Usuwanie Ilości)")

towary_do_wydania = list(st.session_state.magazyn.keys())

if towary_do_wydania:
    col_wydanie_1, col_wydanie_2 = st.columns(2)
    
    with col_wydanie_1:
        wybrany_do_wydania = st.selectbox(
            "Wybierz towar:",
            towary_do_wydania,
            key="wybor_do_wydania"
        )
    
    with col_wydanie_2:
        max_ilosc = st.session_state.magazyn.get(wybrany_do_wydania, 0)
        # Upewniamy się, że towarem nie jest pusta nazwa z magazynu
        if wybrany_do_wydania in st.session_state.magazyn:
            ilosc_do_wydania = st.number_input(
                f"Ilość do wydania (Max: {max_ilosc})",
                min_value=1,
                max_value=max_ilosc,
                step=1,
                key="input_usun_ilosc"
            )
        else:
             ilosc_do_wydania = 0 # Zapobieganie błędom, gdy lista jest pusta

    if st.button(f"Wydaj {ilosc_do_wydania} sztuk", use_container_width=True, key="btn_wydaj"):
        wydaj_ilosc(wybrany_do_wydania, ilosc_do_wydania)
        
else:
    st.info("Brak towarów do wydania w magazynie.")

st.markdown("---")

# --- Sekcja Usuwania Całkowitego ---
st.header("❌ Usuń Pozycję Całkowicie")

towary_do_usuniecia = list(st.session_state.magazyn.keys())

if towary_do_usuniecia:
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia:",
        towary_do_usuniecia,
        key="wybor_do_usuniecia_calkowitego"
    )

    if st.button(f"Usuń Całkowicie {wybrany_do_usuniecia}", use_container_width=True, key="btn_usun_calkowicie"):
        usun_calkowicie(wybrany_do_usuniecia)
else:
    st.info("Brak pozycji do usunięcia.")

st.markdown("---")

# --- Sekcja Aktualnego Magazynu ---
st.header("📝 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Używamy Pandas DataFrame do eleganckiego wyświetlania danych
    dane_df = pd.DataFrame(st.session_state.magazyn.items(), columns=['Nazwa Towaru', 'Ilość'])
    
    st.dataframe(dane_df, hide_index=True, use_container_width=True)
    
    total_items = sum(st.session_state.magazyn.values())
    st.info(f"Całkowita liczba jednostek w magazynie: **{total_items}**")
else:
    st.warning("Magazyn jest obecnie pusty.")

st.markdown("---")
