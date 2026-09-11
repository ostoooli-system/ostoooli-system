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

# --- نظام تسجيل الدخول الديناميكي (أكواد شهرية + إدخال اسم الشركة للعميل) ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.company_name = ""

if not st.session_state.logged_in:
  st.title("🔐 تسجيل الدخول - نظام أسطولي")
  st.markdown("الرجاء إدخال اسم شركتك وكود الاشتراك الشهري الخاص بك.")

  with st.form("login_form"):
    company_input = st.text_input("اسم شركتك (الذي سيظهر في لوحة التحكم)")
    code_input = st.text_input("كود الاشتراك الشهري", type="password")
    submit_button = st.form_submit_button("دخول المنصة")

    if submit_button:
      # كلمة مرور الإدارة بالإنجليزية للأمان التام
      ADMIN_PASSWORD = "Ahmed Khaled 1998"

      # أكواد الاشتراكات الشهرية الصالحة التي تقومي ببيعها للعملاء
      valid_subscription_codes = [
          "NINJA-2026-VIP",
          "TOYOU-2026-PRO",
          "FLEET-9988-2026",
      ]

      if code_input == ADMIN_PASSWORD:
        st.session_state.logged_in = True
        st.session_state.company_name = (
            company_input if company_input else "لوحة الإدارة الرئيسية (الأدمن)"
        )
        st.success("مرحباً بكِ يا بشمهندسة بسملة! يتم فتح المنصة...")
        st.rerun()
      elif code_input in valid_subscription_codes:
        if company_input.strip() == "":
          st.error("الرجاء كتابة اسم شركتك بشكل صحيح.")
        else:
          st.session_state.logged_in = True
          st.session_state.company_name = company_input
          st.success(f"مرحباً بكِ في لوحة تحكم شركة {company_input}!")
          st.rerun()
      else:
        st.error("كود الاشتراك الشهري غير صحيح أو منتهي الصلاحية.")

  st.stop()

# لو تم تسجيل الدخول بنجاح
st.sidebar.title("⚙️ الإعدادات والتحكم")

if st.sidebar.button("🚪 تسجيل الخروج"):
  st.session_state.logged_in = False
  st.session_state.company_name = ""
  st.rerun()

st.sidebar.success(f"👤 الشركة: {st.session_state.company_name}")

selected_lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
t = translations[selected_lang]

st.title(f"{t['title']} - [{st.session_state.company_name}]")

# قسم رفع الملفات
st.sidebar.markdown("---")
st.sidebar.subheader(t["upload_section"])
uploaded_files = st.sidebar.file_uploader(
    t["upload_label"],
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    help=t["upload_help"],
)

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
  data = {
      "اسم السائق": ["قم برفع ملفات الأسطول الخاصة بك"],
      "رقم الإقامة": ["---"],
      "رقم المركبة": ["---"],
      "حالة الإقامة": ["---"],
      "تاريخ انتهاء الإقامة": ["2026-12-31"],
      "رخصة سارية؟": ["---"],
      "الطلبات المقبولة": [0],
      "الطلبات المرفوضة": [0],
      "محفظة الكاش (ج.م)": [0.0],
      "منصة التوصيل": ["---"],
  }
  df = pd.DataFrame(data)
  st.sidebar.info("💡 برجاء رفع ملفات الإكسل الخاصة بالأسطول لعرض البيانات وتحليلها.")

if df is not None:
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

  col1, col2, col3, col4 = st.columns(4)
  total_drivers = len(df)
  active_orders_sum = (
      df["الطلبات المقبولة"].sum() if "الطلبات المقبولة" in df.columns else 0
  )
  rejected_orders_sum = (
      df["الطلبات المرفوضة"].sum() if "الطلبات المرفوضة" in df.columns else 0
  )
  total_cash_sum = (
      df["محفظة الكاش (ج.م)"].sum() if "محفظة الكاش (ج.م)" in df.columns else 0.0
  )

  col1.metric(t["total_drivers"], f"{total_drivers}")
  col2.metric(t["active_orders"], f"{active_orders_sum}")
  col3.metric(t["rejected_orders"], f"{rejected_orders_sum}")
  col4.metric(t["total_cash"], f"{total_cash_sum:,.2f}")

  st.markdown("---")

  st.subheader(t["fleet_status"])
  st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown(
    f"<p style='text-align: center;'>{t['footer']}</p>", unsafe_allow_html=True
)
