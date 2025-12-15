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
    st.markdown("### 🌃 System kontroli zapasów Mrocznego Ry
