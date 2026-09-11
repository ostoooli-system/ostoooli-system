import datetime
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام أسطولي لإدارة النقل والتوصيل | Ostooooli Fleet System",
    page_icon="🚚",
    layout="wide",
)

# تفعيل التحديث التلقائي
st_autorefresh(interval=10000, key="datarefresh")

# القاموس متعدد اللغات (عربي، إنجليزي، هندي، أوردو)
translations = {
    "العربية": {
        "title": "🚚 نظام أسطولي لإدارة النقل والتوصيل",
        "settings": "إعدادات النظام",
        "total_drivers": "إجمالي السائقين",
        "active_orders": "إجمالي الطلبات المقبولة",
        "rejected_orders": "إجمالي الطلبات المرفوضة",
        "total_cash": "إجمالي محفظة الكاش",
        "fleet_status": "ملخص حالة الأسطول (يتم التحديث تلقائياً)",
        "upload_section": "رفع بيانات الأسطول",
        "upload_label": "ارفع ملفات (XLSX أو CSV)",
        "upload_help": "رفع ملفات أسطولك الخاص لتظهر لك بياناتك وحدك.",
        "search_label": "🔍 بحث عن سائق (بالاسم أو رقم الإقامة)",
        "filter_label": "🏷️ فلترة حالة الإقامة",
        "all_residences": "عرض الكل",
        "valid_residences": "الإقامات السارية فقط",
        "expired_residences": "الإقامات المنتهية / المعطلة",
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
        "upload_section": "Upload Fleet Data",
        "upload_label": "Upload files (XLSX or CSV)",
        "upload_help": "Upload your company fleet files to view your data.",
        "search_label": "🔍 Search driver (Name or Residence ID)",
        "filter_label": "🏷️ Filter by Residence Status",
        "all_residences": "All",
        "valid_residences": "Valid Residences Only",
        "expired_residences": "Expired / Critical Residences",
        "footer": "Ostooooli Fleet Management System © 2026 - Prepared by Eng. Basmala Abdelstar",
        "days_remaining": "Days Remaining for Residency",
    },
    "हिन्दी (Hindi)": {
        "title": "🚚 ओस्टूलि बेड़ा प्रबंधन प्रणाली",
        "settings": "सिस्टम सेटिंग्स",
        "total_drivers": "कुल ड्राइवर",
        "active_orders": "स्वीकृत ऑर्डर",
        "rejected_orders": "अस्वीकृत ऑर्डर",
        "total_cash": "कुल नकद वॉलेट",
        "fleet_status": "बेड़े की स्थिति सारांश (स्वचालित अपडेट)",
        "upload_section": "बेड़ा डेटा अपलोड करें",
        "upload_label": "फ़ाइलें अपलोड करें (XLSX या CSV)",
        "upload_help": "अपना डेटा देखने के लिए अपनी कंपनी की फ़ाइलें अपलोड करें।",
        "search_label": "🔍 ड्राइवर खोजें (नाम या इकामा आईडी)",
        "filter_label": "🏷️ निवास स्थिति फ़िल्टर करें",
        "all_residences": "सभी",
        "valid_residences": "केवल वैध निवास",
        "expired_residences": "समाप्त / महत्वपूर्ण निवास",
        "footer": "Ostooooli Fleet System © 2026 - Eng. Basmala Abdelstar",
        "days_remaining": "निवास के लिए शेष दिन",
    },
    "اردو (Urdu)": {
        "title": "🚚 استولی فلیٹ مینجمنٹ سسٹم",
        "settings": "سسٹم کی ترتیبات",
        "total_drivers": "کل ڈرائیورز",
        "active_orders": "قبول شدہ آرڈرز",
        "rejected_orders": "مسترد شدہ آرڈرز",
        "total_cash": "کل کیش والٹ",
        "fleet_status": "فلیٹ کی صورتحال (خودکار اپ ڈیٹ)",
        "upload_section": "فلیٹ کا ڈیٹا اپ لوڈ کریں",
        "upload_label": "فائلیں اپ لوڈ کریں (XLSX یا CSV)",
        "upload_help": "اپنا ڈیٹا دیکھنے کے لیے اپنی کمپنی کی فائلیں اپ لوڈ کریں۔",
        "search_label": "🔍 ڈرائیور تلاش کریں (نام یا اقامہ نمبر)",
        "filter_label": "🏷️ اقامہ کی حیثیت کے لحاظ سے فلٹر کریں",
        "all_residences": "تمام",
        "valid_residences": "صرف درست اقامے",
        "expired_residences": "خارج شدہ / معطل اقامے",
        "footer": "Ostooooli Fleet System © 2026 - Eng. Basmala Abdelstar",
        "days_remaining": "اقامہ کے بقیہ دن",
    },
}

# --- نظام تسجيل الدخول ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.company_name = ""

if not st.session_state.logged_in:
  st.title("🔐 تسجيل الدخول - نظام أسطولي")
  st.markdown("الرجاء إدخال اسم شركتك وكود الاشتراك أو كلمة المرور.")

  with st.form("login_form"):
    company_input = st.text_input("اسم شركتك (الذي سيظهر في لوحة التحكم)")
    code_input = st.text_input("كلمة المرور أو كود الاشتراك", type="password")
    submit_button = st.form_submit_button("دخول المنصة")

    if submit_button:
      clean_code = code_input.strip().lower()
      admin_pass = "ahmed khaled 1998"
      valid_codes = ["ninja-2026-vip", "toyou-2026-pro", "fleet-9988-2026"]

      if clean_code == admin_pass:
        st.session_state.logged_in = True
        st.session_state.company_name = (
            company_input if company_input else "لوحة الإدارة الرئيسية (الأدمن)"
        )
        st.success("مرحباً بكِ يا بشمهندسة بسملة! يتم فتح المنصة...")
        st.rerun()
      elif clean_code in valid_codes:
        if company_input.strip() == "":
          st.error("الرجاء كتابة اسم شركتك بشكل صحيح.")
        else:
          st.session_state.logged_in = True
          st.session_state.company_name = company_input
          st.success(f"مرحباً بكِ في لوحة تحكم شركة {company_input}!")
          st.rerun()
      else:
        st.error("كلمة المرور غير صحيحة. تأكد من البيانات.")

  st.stop()

# --- لوحة التحكم الجانبية ---
st.sidebar.title("⚙️ الإعدادات والتحكم")

if st.sidebar.button("🚪 تسجيل الخروج"):
  st.session_state.logged_in = False
  st.session_state.company_name = ""
  st.rerun()

st.sidebar.success(f"👤 الشركة: {st.session_state.company_name}")

selected_lang = st.sidebar.selectbox(
    "Language / زبان / भाषा",
    ["العربية", "English", "हिन्दी (Hindi)", "اردو (Urdu)"],
)
t = translations[selected_lang]

st.title(f"{t['title']} - [{st.session_state.company_name}]")

# قسم رفع الملفات
st.sidebar.markdown("---")
st.sidebar.subheader(t["upload_section"])
uploaded_files = st.sidebar.file_uploader(
    t["upload_label"], type=["csv", "xlsx"], accept_multiple_files=True
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
  df = pd.concat(dfs, ignore_index=True) if dfs else None
else:
  data = {
      "اسم السائق": ["قم برفع ملفات الأسطول الخاصة بك"],
      "رقم الإقامة": ["100200300"],
      "رقم المركبة": ["ABC-1234"],
      "حالة الإقامة": ["سارية"],
      "تاريخ انتهاء الإقامة": ["2026-12-31"],
      "رخصة سارية؟": ["نعم"],
      "الطلبات المقبولة": [15],
      "الطلبات المرفوضة": [2],
      "محفظة الكاش (ج.م)": [1250.50],
      "منصة التوصيل": ["مثال_الشركة"],
  }
  df = pd.DataFrame(data)
  st.sidebar.info("💡 برجاء رفع ملفات الإكسل الخاصة بالأسطول لعرض البيانات.")

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

  st.markdown("---")
  col_s1, col_s2 = st.columns(2)
  with col_s1:
    search_query = st.text_input(t["search_label"], "")
  with col_s2:
    filter_status = st.selectbox(
        t["filter_label"],
        [
            t["all_residences"],
            t["valid_residences"],
            t["expired_residences"],
        ],
    )

  if search_query:
    q = search_query.lower()
    name_col = (
        "اسم السائق" if "اسم السائق" in df.columns else df.columns[0]
    )
    res_col = "رقم الإقامة" if "رقم الإقامة" in df.columns else None
    if res_col and res_col in df.columns:
      df = df[
          df[name_col].astype(str).str.lower().str.contains(q)
          | df[res_col].astype(str).str.lower().str.contains(q)
      ]
    else:
      df = df[df[name_col].astype(str).str.lower().str.contains(q)]

  if filter_status == t["valid_residences"] and t["days_remaining"] in df.columns:
    df = df[df[t["days_remaining"]].str.contains("متبقي", na=False)]
  elif (
      filter_status == t["expired_residences"] and t["days_remaining"] in df.columns
  ):
    df = df[
        df[t["days_remaining"]].str.contains("منتهية|تنتهي", na=False)
    ]

  st.markdown("---")
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
