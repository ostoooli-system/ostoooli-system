import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام أسطولي لإدارة النقل | Ostooooli System",
    page_icon="🚛",
    layout="wide"
)

# تفعيل التحديث التلقائي كل 10 ثواني (10000 ميللي ثانية)
st_autorefresh(interval=10000, key="datarefresh")

# القاموس متعدد اللغات
translations = {
    "العربية": {
        "title": "🚛 نظام أسطولي لإدارة النقل والتوصيل",
        "settings": "إعدادات النظام",
        "lang_select": "اختر اللغة / Select Language",
        "uploader_title": "رفع بيانات الأسطول",
        "uploader_help": "اختر ملف الإكسل الخاص بك (.xlsx أو .csv)",
        "menu_title": "قائمة التحكم",
        "menu_1": "لوحة القيادة الرئيسية",
        "menu_2": "البحث عن السائقين",
        "menu_3": "إدارة محفظة الكاش",
        "menu_4": "متابعة الإقامات والرخص",
        "total_drivers": "إجمالي السائقين",
        "accepted_orders": "إجمالي الطلبات المقبولة",
        "rejected_orders": "إجمالي الطلبات المرفوضة",
        "total_cash": "إجمالي محفظة الكاش",
        "dashboard_summary": "📊 ملخص حالة الأسطول (يتم التحديث تلقائياً)",
        "search_title": "🔍 البحث المتقدم عن السائقين",
        "search_input": "أدخل اسم السائق أو رقم الإقامة للبحث:",
        "search_success": "تم العثور على {count} نتيجة مطابقة:",
        "search_error": "عذراً، لم يتم العثور على أي سائق بهذا الاسم أو رقم الإقامة.",
        "search_info": "الرجاء كتابة اسم السائق أو رقم الإقامة في خانة البحث أعلاه.",
        "cash_title": "💰 إدارة أرصدة محفظة الكاش للسائقين",
        "cash_desc": "مراجعة الأرصدة النقدية ومحفظة الكاش لكل سائق:",
        "residency_title": "📋 متابعة صلاحية الإقامات والرخص السارية",
        "residency_desc": "متابعة حالة الإقامات وتواريخ انتهاء الرخص لضمان الالتزام القانوني:",
        "filter_status": "تصفية حسب حالة الرخصة:",
        "filter_all": "الكل",
        "filter_valid": "الرخص السارية فقط 🟢",
        "filter_invalid": "الرخص المنتهية فقط 🔴",
        "footer": "نظام أسطولي لإدارة النقل والتوصيل © 2026 - إعداد بشمهندسة بسملة عبد الستار 🚀",
        "success_upload": "تم رفع ملف الإكسل بنجاح! 🟢",
        "demo_info": "💡 من فضلك ارفع ملف الإكسل الخاص بأسطولك لعرض بياناتك الحقيقية، ويتم عرض بيانات تجريبية توضيحية حالياً."
    },
    "English": {
        "title": "🚛 Ostooooli Transport Management System",
        "settings": "System Settings",
        "lang_select": "Select Language",
        "uploader_title": "Upload Fleet Data",
        "uploader_help": "Choose your Excel file (.xlsx or .csv)",
        "menu_title": "Control Panel",
        "menu_1": "Main Dashboard",
        "menu_2": "Search Drivers",
        "menu_3": "Cash Wallet Management",
        "menu_4": "Residency & License Tracking",
        "total_drivers": "Total Drivers",
        "accepted_orders": "Total Accepted Orders",
        "rejected_orders": "Total Rejected Orders",
        "total_cash": "Total Cash Wallet",
        "dashboard_summary": "📊 Fleet Status Summary (Auto-refreshed)",
        "search_title": "🔍 Advanced Driver Search",
        "search_input": "Enter driver name or residency ID to search:",
        "search_success": "Found {count} matching result(s):",
        "search_error": "Sorry, no driver found with this name or ID.",
        "search_info": "Please enter a driver name or residency ID in the search box above.",
        "cash_title": "💰 Driver Cash Wallet Management",
        "cash_desc": "Review cash balances and wallets for each driver:",
        "residency_title": "📋 Residency & Active License Tracking",
        "residency_desc": "Monitor residency status and license expiration dates:",
        "filter_status": "Filter by license status:",
        "filter_all": "All",
        "filter_valid": "Valid Licenses Only 🟢",
        "filter_invalid": "Expired Licenses Only 🔴",
        "footer": "Ostooooli Transport System © 2026 - Developed by Eng. Basmala Abdelstar 🚀",
        "success_upload": "Excel file uploaded successfully! 🟢",
        "demo_info": "💡 Please upload your fleet Excel file to view your real data. Showing demo data for now."
    },
    "اردو / پاکستان": {
        "title": "🚛 استولی ٹرانسپورٹ مینجمنٹ سسٹم",
        "settings": "سسٹم کی ترتیبات",
        "lang_select": "زبان منتخب کریں",
        "uploader_title": "فلیٹ ڈیٹا اپ لوڈ کریں",
        "uploader_help": "اپنی ایکسل فائل منتخب کریں (.xlsx یا .csv)",
        "menu_title": "کنٹرول پینل",
        "menu_1": "مین ڈیش بورڈ",
        "menu_2": "ڈرائیور تلاش کریں",
        "menu_3": "کیش والٹ مینجمنٹ",
        "menu_4": "اقامہ اور لائسنس ٹریکنگ",
        "total_drivers": "کل ڈرائیورز",
        "accepted_orders": "کل قبول شدہ آرڈرز",
        "rejected_orders": "کل مسترد شدہ آرڈرز",
        "total_cash": "کل کیش والٹ",
        "dashboard_summary": "📊 فلیٹ کی حیثیت کا خلاصہ",
        "search_title": "🔍 ایڈوانسڈ ڈرائیور تلاش",
        "search_input": "تلاش کے لیے ڈرائیور کا نام یا اقامہ نمبر درج کریں:",
        "search_success": "{count} مماثل نتائج ملے:",
        "search_error": "معذرت، اس نام یا اقامہ نمبر سے کوئی ڈرائیور نہیں ملا۔",
        "search_info": "براہ کرم اوپر تلاش کے خانے میں ڈرائیور کا نام یا اقامہ نمبر درج کریں۔",
        "cash_title": "💰 ڈرائیور کیش والٹ مینجمنٹ",
        "cash_desc": "ہر ڈرائیور کے نقد توازن اور کیش والٹ کا جائزہ لیں:",
        "residency_title": "📋 اقامہ اور فعال لائسنس کی نگرانی",
        "residency_desc": "قانونی تعمیل کو یقینی بنانے کے لیے اقامہ اور لائسنس کی تاریخوں کی نگرانی کریں:",
        "filter_status": "لائسنس کی حیثیت سے فلٹر کریں:",
        "filter_all": "سب",
        "filter_valid": "صرف درست لائسنس 🟢",
        "filter_invalid": "صرف منسوخ شدہ لائسنس 🔴",
        "footer": "استولی ٹرانسپورٹ سسٹم © 2026 - انجینئر بسملہ عبد الستار 🚀",
        "success_upload": "ایکسل فائل کامیابی سے اپ لوڈ ہو گئی! 🟢",
        "demo_info": "💡 براہ کرم اپنا اصل ڈیٹا دیکھنے کے لیے فلیٹ کی ایکسل فائل اپ لوڈ کریں۔"
    },
    "हिन्दी / भारत": {
        "title": "🚛 ओस्टूली परिवहन प्रबंधन प्रणाली",
        "settings": "सिस्टम सेटिंग्स",
        "lang_select": "भाषा चुनें",
        "uploader_title": "फ्लीट डेटा अपलोड करें",
        "uploader_help": "अपनी एक्सेल फ़ाइल चुनें (.xlsx या .csv)",
        "menu_title": "कंट्रोल पैनल",
        "menu_1": "मुख्य डैशबोर्ड",
        "menu_2": "ड्राइवर खोजें",
        "menu_3": "कैश वॉलेट प्रबंधन",
        "menu_4": "आवास और लाइसेंस ट्रैकिंग",
        "total_drivers": "कुल ड्राइवर",
        "accepted_orders": "कुल स्वीकृत ऑर्डर",
        "rejected_orders": "कुल अस्वीकृत ऑर्डर",
        "total_cash": "कुल कैश वॉलेट",
        "dashboard_summary": "📊 फ़्लीट स्थिति सारांश",
        "search_title": "🔍 उन्नत ड्राइवर खोज",
        "search_input": "खोजने के लिए ड्राइवर का नाम या निवास आईडी दर्ज करें:",
        "search_success": "{count} मिलान परिणाम मिले:",
        "search_error": "क्षमा करें, इस नाम या आईडी से कोई ड्राइवर नहीं मिला।",
        "search_info": "कृपया ऊपर खोज बॉक्स में ड्राइवर का नाम या आईडी दर्ज करें।",
        "cash_title": "💰 ड्राइवर कैश वॉलेट प्रबंधन",
        "cash_desc": "प्रत्येक ड्राइवर के नकद शेष और वॉलेट की समीक्षा करें:",
        "residency_title": "📋 निवास और सक्रिय लाइसेंस ट्रैकिंग",
        "residency_desc": "कानूनी अनुपालन सुनिश्चित करने के लिए निवास और लाइसेंस की समाप्ति तिथियों की निगरानी करें:",
        "filter_status": "लाइसेंस स्थिति के अनुसार फ़िल्टर करें:",
        "filter_all": "सभी",
        "filter_valid": "केवल वैध लाइसेंस 🟢",
        "filter_invalid": "केवल समाप्त लाइसेंस 🔴",
        "footer": "ओस्टूली ट्रांसपोर्ट सिस्टम © 2026 - इंजीनियर बसमला अब्देलस्टार 🚀",
        "success_upload": "एक्सेल फ़ाइल सफलतापूर्वक अपलोड हो गई! 🟢",
        "demo_info": "💡 कृपया अपना वास्तविक डेटा देखने के लिए अपनी फ्लीट एक्सेल फ़ाइल अपलोड करें।"
    }
}

# شريط إعدادات القائمة الجانبية
st.sidebar.title("⚙️ Settings / إعدادات")
selected_lang = st.sidebar.selectbox("Language / اللغة", list(translations.keys()))
t = translations[selected_lang]

st.sidebar.markdown("---")
st.sidebar.title(t["uploader_title"])
uploaded_file = st.sidebar.file_uploader(t["uploader_help"], type=["xlsx", "csv"])

# معالجة ملف الإكسل المرفوع أو عرض البيانات التجريبية التوضيحية
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success(t["success_upload"])
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
        df = None
else:
    df = pd.DataFrame([
        {
            "اسم السائق": "أحمد محمد",
            "رقم الإقامة": "2458963214",
            "رقم المركبة": "أ ب ج 1234",
            "حالة الإقامة": "سارية",
            "تاريخ انتهاء الرخصة": "2026-12-15",
            "رخصة سارية؟": "نعم 🟢",
            "محفظة الكاش (ج.م)": 1250.00,
            "الطلبات المقبولة": 45,
            "الطلبات المرفوضة": 3
        },
        {
            "اسم السائق": "محمود علي",
            "رقم الإقامة": "2398741236",
            "رقم المركبة": "س ص ع 5678",
            "حالة الإقامة": "منتهية",
            "تاريخ انتهاء الرخصة": "2026-04-10",
            "رخصة سارية؟": "لا (منتهية) 🔴",
            "محفظة الكاش (ج.م)": 840.50,
            "الطلبات المقبولة": 30,
            "الطلبات المرفوضة": 7
        }
    ])
    st.sidebar.info(t["demo_info"])

if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.title(t["menu_title"])
    menu = st.sidebar.selectbox(
        "Navigation", 
        [t["menu_1"], t["menu_2"], t["menu_3"], t["menu_4"]]
    )

    # 1. لوحة القيادة الرئيسية
    if menu == t["menu_1"]:
        st.title(t["title"])
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t["total_drivers"], len(df))
        with col2:
            acc_col = "الطلبات المقبولة" if "الطلبات المقبولة" in df.columns else df.columns[0]
            acc_val = int(df[acc_col].sum()) if pd.api.types.is_numeric_dtype(df[acc_col]) else 0
            st.metric(t["accepted_orders"], acc_val)
        with col3:
            rej_col = "الطلبات المرفوضة" if "الطلبات المرفوضة" in df.columns else df.columns[0]
            rej_val = int(df[rej_col].sum()) if pd.api.types.is_numeric_dtype(df[rej_col]) else 0
            st.metric(t["rejected_orders"], rej_val)
        with col4:
            cash_col = "محفظة الكاش (ج.م)" if "محفظة الكاش (ج.م)" in df.columns else df.columns[-1]
            cash_val = df[cash_col].sum() if pd.api.types.is_numeric_dtype(df[cash_col]) else 0.0
            st.metric(t["total_cash"], f"{cash_val:,.2f}")
        
        st.markdown("---")
        st.subheader(t["dashboard_summary"])
        st.dataframe(df, use_container_width=True)

    # 2. البحث عن السائقين بالاسم أو رقم الإقامة
    elif menu == t["menu_2"]:
        st.title(t["search_title"])
        st.markdown("---")
        
        search_query = st.text_input(t["search_input"])
        
        name_col = "اسم السائق" if "اسم السائق" in df.columns else df.columns[0]
        id_col = "رقم الإقامة" if "رقم الإقامة" in df.columns else df.columns[1]
        
        if search_query:
            result_df = df[
                df[name_col].astype(str).str.contains(search_query, case=False, na=False) |
                df[id_col].astype(str).str.contains(search_query, case=False, na=False)
            ]
            
            if not result_df.empty:
                st.success(t["search_success"].format(count=len(result_df)))
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning(t["search_error"])
        else:
            st.info(t["search_info"])
            st.dataframe(df, use_container_width=True)

    # 3. إدارة محفظة الكاش
    elif menu == t["menu_3"]:
        st.title(t["cash_title"])
        st.markdown("---")
        
        st.write(t["cash_desc"])
        st.dataframe(df, use_container_width=True)

    # 4. متابعة الإقامات والرخص
    elif menu == t["menu_4"]:
        st.title(t["residency_title"])
        st.markdown("---")
        
        st.write(t["residency_desc"])
        
        status_filter = st.radio(t["filter_status"], [t["filter_all"], t["filter_valid"], t["filter_invalid"]])
        
        license_col = "رخصة سارية؟" if "رخصة سارية؟" in df.columns else None
        
        if license_col and status_filter == t["filter_valid"]:
            filtered_df = df[df[license_col].astype(str).str.contains("نعم|Valid", case=False)]
        elif license_col and status_filter == t["filter_invalid"]:
            filtered_df = df[df[license_col].astype(str).str.contains("لا|Expired|منتهية", case=False)]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True)

# تذييل الصفحة
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{t['footer']}</p>", unsafe_allow_html=True)
