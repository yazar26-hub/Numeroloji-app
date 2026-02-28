import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Numeroloji Analiz", page_icon="🔮", layout="centered")

# --- HESAPLAMA FONKSİYONLARI ---
def rakam_topla(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

harf_tablosu = {
    'A':1, 'J':1, 'S':1, 'Ş':1, 'B':2, 'K':2, 'T':2, 'C':3, 'L':3, 'U':3, 'Ü':3,
    'D':4, 'M':4, 'V':4, 'E':5, 'N':5, 'W':5, 'F':6, 'O':6, 'Ö':6, 'X':6,
    'G':7, 'Ğ':7, 'P':7, 'Y':7, 'H':8, 'Q':8, 'Z':8, 'I':9, 'İ':9, 'R':9
}
sesli_harfler = "AEIİOÖUÜ"

# --- ARAYÜZ ---
st.title("🔮 Numeroloji & Pin Kodu Analizi")
st.markdown("---")

with st.form("analiz_form"):
    ad_soyad = st.text_input("Ad Soyad Giriniz")
    dogum_tarihi = st.date_input("Doğum Tarihinizi Seçiniz", min_value=pd.to_datetime("1900-01-01"))
    submit = st.form_submit_button("Hesapla")

if submit and ad_soyad:
    # İsim Analizi
    temiz_ad = ad_soyad.replace(" ", "").upper()
    sesli_top = sum(harf_tablosu.get(h, 0) for h in temiz_ad if h in sesli_harfler)
    sessiz_top = sum(harf_tablosu.get(h, 0) for h in temiz_ad if h not in sesli_harfler)
    
    # Pin Kodu
    gun, ay, yil = dogum_tarihi.day, dogum_tarihi.month, dogum_tarihi.year
    h1 = rakam_topla(gun)
    h2 = rakam_topla(ay)
    h3 = rakam_topla(sum(int(d) for d in str(yil)))
    h4 = rakam_topla(h1 + h2 + h3)
    h5 = rakam_topla(h1 + h4)
    h6 = rakam_topla(h1 + h2)
    h7 = rakam_topla(h2 + h3)
    h8 = rakam_topla(h6 + h7)
    h9 = rakam_topla(h1+h2+h3+h4+h5+h6+h7+h8)
    
    hayat_yolu = rakam_topla(int(dogum_tarihi.strftime("%Y%m%d")))

    # SONUÇ EKRANI
    st.balloons()
    st.subheader(f"📊 {ad_soyad.upper()} İçin Analiz Sonuçları")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Sesli Harf", sesli_top)
    col2.metric("Sessiz Harf", sessiz_top)
    col3.metric("Hayat Yolu", hayat_yolu)

    st.markdown("### 📍 PİN KODU")
    pin_kodu_stili = f"""
    <div style="background-color: #1e1e1e; color: #00ff00; padding: 20px; border-radius: 10px; text-align: center; font-family: monospace; font-size: 30px;">
        {h1}{h2}{h3}{h4}{h5}<br>
        {h6}{h7}<br>
        {h8}<br>
        {h9}
    </div>
    """
    st.markdown(pin_kodu_stili, unsafe_allow_html=True)
