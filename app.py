import datetime
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام أسطولي لإدارة النقل والتوصيل | Ostooooli System",
    page_icon="🚚",
    layout="wide",
)

# تفعيل التحديث التلقائي كل 10 ثواني
st_autorefresh(interval=10000, key="datarefresh")

# القاموس متعدد اللغات
translations = {
    "العربية": {
        "title": "🚚 نظام أسطولي لإدارة النقل والتوصيل",
        "settings": "إعدادات النظام",
        "total_drivers": "إجمالي السائقين",
        "active_orders": "إجمالي الطلبات المقبولة",
        "rejected_orders": "إجمالي الطلبات المرفوضة",
        "total_cash": "إجمالي محفظة الكاش",
        "fleet_status": "ملخص حالة الأسطول (يتم التحديث تلقائياً)",
        "upload_section": "رفع بيانات الأسطول (يدعم عدة ملفات)",
        "upload_label": "ارفع ملفات (XLSX أو CSV) للشركة الخاصة بك",
        "upload_help": "يمكنك رفع ملفات أسطولك الخاص لتظهر لك بياناتك وحدك.",
        "footer": "نظام أسطولي لإدارة النقل والتوصيل © 2026 - إعداد بشمهندسة بسملة عبد الستار",
        "days_remaining": "الأيام المتبقية للإقامة",
    },
    "English": {
        "title": "🚚 Ostooooli Fleet Management System",
        "settings": "System Settings",
        "total_drivers": "Total Drivers",
        "active_orders": "Accepted Orders",
        "rejected_orders": "Rejected Orders",
        "total_cash": "Total Cash Wallet",
        "fleet_status": "Fleet Status Summary (Auto-updating)",
        "upload_section": "Upload Fleet Data (Multi-files)",
        "upload_label": "Upload files (XLSX or CSV) for your company",
        "upload_help": "Upload your company fleet files to view your data exclusively.",
        "footer": "Ostooooli Fleet Management System © 2026 - Prepared by Eng. Basmala Abdelstar",
        "days_remaining": "Days Remaining for Residency",
    },
}

# --- نظام تسجيل الدخول وعزل العملاء (SaaS Multi-Tenant Authentication) ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.company_name = ""

if not st.session_state.logged_in:
  st.title("🔐 تسجيل دخول الشركات - نظام أسطولي")
  st.markdown("الرجاء إدخال بيانات الاشتراك الخاصة بشركتك للوصول إلى لوحة التحكم المعزولة.")

  with st.form("login_form"):
    company_input = st.text_input("اسم الشركة أو كود العميل")
    password_input = st.text_input("كلمة المرور (Password)", type="password")
    submit_button = st.form_submit_button("دخول المنصة")

    if submit_button:
      # قاعدة بيانات تجريبية للشركات المشتركة (يمكن توسيعها لاحقاً أو ربطها بقاعدة بيانات)
      valid_companies = {
          "محمد": "mohamed123",
          "أحمد": "ahmed456",
          "شركة الفرسان": "forsan2026",
      }

      if company_input in valid_companies and valid_companies[company_input] == password_input:
        st.session_state.logged_in = True
        st.session_state.company_name = company_input
        st.success(f"مرحباً بك يا {company_input}! يتم تحميل لوحة التحكم الخاصة بشركتك...")
        st.rerun()
      else:
        st.error("خطأ في اسم الشركة أو كلمة المرور. تأكد من البيانات.")

  st.stop()  # إيقاف عرض باقي الصفحة لو لم يتم تسجيل الدخول

# لو المستخدم مسجل دخول، نقدر نكمل عرض الداشبورد الخاصة به فقط
st.sidebar.title("⚙️ الإعدادات والتحكم")

# زر تسجيل الخروج
if st.sidebar.button("🚪 تسجيل الخروج"):
  st.session_state.logged_in = False
  st.session_state.company_name = ""
  st.rerun()

st.sidebar.success(f"👤 الشركة الحالية: {st.session_state.company_name}")

selected_lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
t = translations[selected_lang]

# عنوان النظام الرئيسي مخصص باسم الشركة الحالية
st.title(f"{t['title']} - [{st.session_state.company_name}]")

# قسم رفع الملفات الخاصة بالشركات
st.sidebar.markdown("---")
st.sidebar.subheader(t["upload_section"])
uploaded_files = st.sidebar.file_uploader(
    t["upload_label"],
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    help=t["upload_help"],
)

# معالجة ودمج الملفات المرفوعة للشركة الحالية
if uploaded_files:
  dfs = []
  for file in uploaded_files:
    try:
      if file.name.endswith(".csv"):
        temp_df = pd.read_csv(file)
      else:
        temp_df = pd.read_excel(file)

      platform_name = file.name.rsplit(".", 1)[0]
      temp_df["منصة التوصيل"] = platform_name
      dfs.append(temp_df)
    except Exception as e:
      st.error(f"Error reading {file.name}: {e}")

  if dfs:
    df = pd.concat(dfs, ignore_index=True)
  else:
    df = None
else:
  # داتا افتراضية توضيحية خاصة بالشركات
  data = {
      "اسم السائق": [f"سائق تبع {st.session_state.company_name} 1", f"سائق تبع {st.session_state.company_name} 2"],
      "رقم الإقامة": ["2458963214", "2398741236"],
      "رقم المركبة": ["أ ب ج 1234", "س ص ع 5678"],
      "حالة الإقامة": ["سارية", "منتهية"],
      "تاريخ انتهاء الإقامة": ["2026-12-15", "2026-04-10"],
      "رخصة سارية؟": ["نعم", "لا (منتهية)"],
      "الطلبات المقبولة": [45, 30],
      "الطلبات المرفوضة": [3, 7],
      "محفظة الكاش (ج.م)": [1250.0, 840.5],
      "منصة التوصيل": ["نينجا (Ninja)", "توي (ToYou)"],
  }
  df = pd.DataFrame(data)
  st.sidebar.info(f"💡 يتم عرض بيانات تجريبية خاصة بشركة {st.session_state.company_name}. ارفع ملفاتك لعرض داتائك الحقيقية.")

if df is not None:
  # حساب الأيام المتبقية لانتهاء الإقامة توماتيكياً
  if "تاريخ انتهاء الإقامة" in df.columns:
    df["تاريخ انتهاء الإقامة ديت"] = pd.to_datetime(
        df["تاريخ انتهاء الإقامة"], errors="coerce"
    ).dt.date
    today = datetime.date.today()

    def calc_days(x):
      if pd.isnull(x):
        return "غير متوفر"
      delta = (x - today).days
      if delta < 0:
        return f"منتهية من {-delta} يوم ⚠️"
      elif delta == 0:
        return "تنتهي اليوم! 🚨"
      else:
        return f"متبقي {delta} يوم"

    df[t["days_remaining"]] = df["تاريخ انتهاء الإقامة ديت"].apply(calc_days)
    df = df.drop(columns=["تاريخ انتهاء الإقامة ديت"])

  # المؤشرات الحية (Metrics)
  col1, col2, col3, col4 = st.columns(4)
  total_drivers = len(df)
  active_orders_sum = df["الطلبات المقبولة"].sum() if "الطلبات المقبولة" in df.columns else 0
  rejected_orders_sum = df["الطلبات المرفوضة"].sum() if "الطلبات المرفوضة" in df.columns else 0
  total_cash_sum = df["محفظة الكاش (ج.م)"].sum() if "محفظة الكاش (ج.م)" in df.columns else 0.0

  col1.metric(t["total_drivers"], f"{total_drivers}")
  col2.metric(t["active_orders"], f"{active_orders_sum}")
  col3.metric(t["rejected_orders"], f"{rejected_orders_sum}")
  col4.metric(t["total_cash"], f"{total_cash_sum:,.2f}")

  st.markdown("---")

  # جدول عرض حالة الأسطول الخاص بالشركة فقط
  st.subheader(t["fleet_status"])
  st.dataframe(df, use_container_width=True)

# تذييل الصفحة (Footer)
st.markdown("---")
st.markdown(f"<p style='text-align: center;'>{t['footer']}</p>", unsafe_allow_html=True)
