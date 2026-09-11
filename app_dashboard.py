import os
import requests
import streamlit as st

# تحديد رابط الـ Backend تلقائياً (سحابياً أو محلياً)
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# إعدادات صفحة Streamlit
st.set_page_config(
    page_title="أسطولي | Ostoooli Fleet Management",
    page_icon="🚛",
    layout="wide",
)

# اختيار اللغة (العربية، الإنجليزية، الإسبانية، الفرنسية، الهندية، الباكستانية/الأوردو)
language = st.sidebar.selectbox(
    "Choose Language / اختر اللغة / Langue / भाषा / زبان",
    ["العربية", "English", "Español", "Français", "हिन्दी", "اردو"],
)

# قواميس اللغات المتعددة لنظام أسطولي (Ostoooli)
if language == "العربية":
  title_text = "🚛 منصة أسطولي (Ostoooli) لإدارة الأساطير"
  desc_text = (
      "منصة سحابية ذكية لمتابعة السائقين، رخصهم، المستندات، والامتثال بشكل"
      " أوتوماتيكي."
  )
  upload_header = "اختر شيت Excel الخاص بالسائقين"
  status_title = "حالة الاتصال بالخادم الخلفي (FastAPI)"
  success_msg = "تم رفع ومعالجة البيانات بنجاح!"
  error_conn = (
      "تعذر الاتصال بالخادم الخلفي (FastAPI). تأكد من تشغيل السيرفر."
  )
  spinner_text = "جاري معالجة البيانات وتحليل الامتثال..."
elif language == "English":
  title_text = "🚛 Ostoooli Fleet Management Platform"
  desc_text = (
      "Smart cloud platform to track drivers, licenses, documents, and"
      " compliance automatically."
  )
  upload_header = "Choose Drivers Excel Sheet"
  status_title = "FastAPI Backend Connection Status"
  success_msg = "Data uploaded and processed successfully!"
  error_conn = (
      "Failed to connect to FastAPI backend. Make sure the server is running."
  )
  spinner_text = "Processing data and compliance analysis..."
elif language == "Español":
  title_text = "🚛 Ostoooli: Plataforma de Gestión de Flotas"
  desc_text = (
      "Plataforma inteligente en la nube para rastrear conductores, licencias y"
      " cumplimiento automáticamente."
  )
  upload_header = "Elija la hoja de Excel de conductores"
  status_title = "Estado de conexión del backend (FastAPI)"
  success_msg = "¡Datos subidos y procesados con éxito!"
  error_conn = (
      "Error al conectar con el backend (FastAPI). Asegúrese de que el servidor"
      " esté encendido."
  )
  spinner_text = "Procesando datos..."
elif language == "Français":
  title_text = "🚛 Ostoooli : Plateforme de Gestion de Flotte"
  desc_text = (
      "Plateforme cloud intelligente pour suivre automatiquement les"
      " conducteurs et la conformité."
  )
  upload_header = "Choisissez la feuille Excel des conducteurs"
  status_title = "État de la connexion du backend (FastAPI)"
  success_msg = "Données téléchargées et traitées avec succès !"
  error_conn = (
      "Échec de la connexion au backend (FastAPI). Assurez-vous que le serveur"
      " est démarré."
  )
  spinner_text = "Traitement des données en cours..."
elif language == "हिन्दी":
  title_text = "🚛 ओस्टूली (Ostoooli) फ्लीट मैनेजमेंट प्लेटफॉर्म"
  desc_text = (
      "ड्राइवरों, लाइसेंस और दस्तावेजों को स्वचालित रूप से ट्रैक करने के लिए"
      " स्मार्ट क्लाउड प्लेटफॉर्म।"
  )
  upload_header = "ड्राइवरों की एक्सेल शीट चुनें"
  status_title = "FastAPI बैकएंड कनेक्शन स्थिति"
  success_msg = "डेटा सफलतापूर्वक अपलोड और प्रोसेस किया गया!"
  error_conn = (
      "FastAPI बैकएंड से कनेक्ट करने में विफल। सुनिश्चित करें कि सर्वर चल"
      " रहा है।"
  )
  spinner_text = "डेटा प्रोसेस किया जा रहा है..."
else:
  title_text = "🚛 اوستولی (Ostoooli) فلیٹ مینجمنٹ پلیٹ فارم"
  desc_text = (
      "ڈرائیوروں، لائسنسوں اور دستاویزات کو خودکار طریقے سے ٹریک کرنے کے لیے ایک"
      " سمارٹ کلاؤڈ پلیٹ فارم۔"
  )
  upload_header = "ڈرائیوروں کی ایکسل شیٹ منتخب کریں"
  status_title = "FastAPI بیک اینڈ کنکشن کی حیثیت"
  success_msg = "ڈیٹا کامیابی کے ساتھ اپ لوڈ اور پروسیس ہو گیا!"
  error_conn = (
      "FastAPI بیک اینڈ سے جڑنے میں ناکام۔ یقینی بنائیں کہ سرور چل رہا ہے۔"
  )
  spinner_text = "ڈیٹا پروسیس کیا جا رہا ہے۔۔۔"

# عرض العناوين والوصف
st.title(title_text)
st.markdown(desc_text)

# فحص الاتصال بالـ Backend
st.sidebar.divider()
st.sidebar.subheader(status_title)
try:
  response = requests.get(f"{API_BASE_URL}/")
  if response.status_code == 200:
    st.sidebar.success("متصل / Connected / Conectado / Connecté / जुड़ा हुआ ✅")
  else:
    st.sidebar.warning("استجابة غير متوقعة / Unexpected response")
except requests.exceptions.ConnectionError:
  st.sidebar.error(error_conn)

# واجهة رفع الملفات
st.divider()
uploaded_file = st.file_uploader(
    upload_header, type=["xlsx", "csv"], accept_multiple_files=False
)

if uploaded_file is not None:
  with st.spinner(spinner_text):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
      res = requests.post(f"{API_BASE_URL}/upload/", files=files)
      if res.status_code == 200:
        st.success(success_msg)
        data = res.json()
        st.json(data)
      else:
        st.error(f"خطأ / Error: {res.text}")
    except Exception as e:
      st.error(f"فشل الاتصال / Connection failed: {e}")