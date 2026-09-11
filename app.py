import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام أسطولي لإدارة النقل",
    page_icon="🚛",
    layout="wide"
)

st.sidebar.title("إعدادات النظام")
language = st.sidebar.selectbox("اختر اللغة / Language", ["العربية", "English"])

st.sidebar.markdown("---")
st.sidebar.title("رفع بيانات العملاء")
# زرار يخلي كل عميل يرفع ملف الإكسل الخاص به
uploaded_file = st.sidebar.file_uploader("اختر ملف الإكسل الخاص بك (.xlsx أو .csv)", type=["xlsx", "csv"])

# لو العميل لسه ما رفعش ملف، نعرض له نموذج تجريبي أو رسالة توجيهية
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("تم رفع ملف الإكسل بنجاح! 🟢")
    except Exception as e:
        st.sidebar.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        df = None
else:
    # بيانات افتراضية توضيحية لو مفيش ملف مرفوع حالياً
    df = pd.DataFrame([
        {
            "اسم السائق": "مثال: أحمد محمد",
            "رقم الإقامة": "2458963214",
            "رقم المركبة": "أ ب ج 1234",
            "حالة الإقامة": "سارية",
            "تاريخ انتهاء الرخصة": "2026-12-15",
            "رخصة سارية؟": "نعم 🟢",
            "محفظة الكاش (ج.م)": 1250.00,
            "الطلبات المقبولة": 45,
            "الطلبات المرفوضة": 3
        }
    ])
    st.sidebar.info("💡 من فضلك ارفع ملف الإكسل الخاص بأسطولك من هنا لعرض بياناتك الحقيقية.")

if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.title("قائمة التحكم")
    menu = st.sidebar.selectbox(
        "اختر القسم", 
        ["لوحة القيادة الرئيسية", "البحث عن السائقين", "إدارة محفظة الكاش", "متابعة الإقامات والرخص"]
    )

    # واحة لوحة القيادة الرئيسية
    if menu == "لوحة القيادة الرئيسية":
        st.title("🚛 نظام أسطولي لإدارة النقل والتوصيل")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("إجمالي السائقين", len(df))
        with col2:
            accepted_col = "الطلبات المقبولة" if "الطلبات المقبولة" in df.columns else df.columns[0]
            st.metric("إجمالي الطلبات المقبولة", int(df[accepted_col].sum()) if pd.api.types.is_numeric_dtype(df[accepted_col]) else 0)
        with col3:
            rejected_col = "الطلبات المرفوضة" if "الطلبات المرفوضة" in df.columns else df.columns[0]
            st.metric("إجمالي الطلبات المرفوضة", int(df[rejected_col].sum()) if pd.api.types.is_numeric_dtype(df[rejected_col]) else 0)
        with col4:
            cash_col = "محفظة الكاش (ج.م)" if "محفظة الكاش (ج.م)" in df.columns else df.columns[-1]
            total_cash = df[cash_col].sum() if pd.api.types.is_numeric_dtype(df[cash_col]) else 0.0
            st.metric("إجمالي محفظة الكاش", f"{total_cash:,.2f} ج.م")
        
        st.markdown("---")
        st.subheader("📊 ملخص حالة الأسطول من ملف الإكسل")
        st.dataframe(df, use_container_width=True)

    # قسم البحث عن السائق بالاسم أو رقم الإقامة
    elif menu == "البحث عن السائقين":
        st.title("🔍 البحث المتقدم عن السائقين")
        st.markdown("---")
        
        search_query = st.text_input("أدخل اسم السائق أو رقم الإقامة للبحث:")
        
        name_col = "اسم السائق" if "اسم السائق" in df.columns else df.columns[0]
        id_col = "رقم الإقامة" if "رقم الإقامة" in df.columns else df.columns[1]
        
        if search_query:
            result_df = df[
                df[name_col].astype(str).str.contains(search_query, case=False, na=False) |
                df[id_col].astype(str).str.contains(search_query, case=False, na=False)
            ]
            
            if not result_df.empty:
                st.success(f"تم العثور على {len(result_df)} نتيجة مطابقة:")
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning("عذراً، لم يتم العثور على أي سائق بهذا الاسم أو رقم الإقامة.")
        else:
            st.info("الرجاء كتابة اسم السائق أو رقم الإقامة في خانة البحث أعلاه.")
            st.dataframe(df, use_container_width=True)

    # قسم إدارة محفظة الكاش
    elif menu == "إدارة محفظة الكاش":
        st.title("💰 إدارة أرصدة محفظة الكاش للسائقين")
        st.markdown("---")
        
        st.write("مراجعة الأرصدة النقدية ومحفظة الكاش لكل سائق:")
        st.dataframe(df, use_container_width=True)

    # قسم متابعة الإقامات ورخص القيادة
    elif menu == "متابعة الإقامات والرخص":
        st.title("📋 متابعة صلاحية الإقامات والرخص السارية")
        st.markdown("---")
        
        st.write("متابعة حالة الإقامات وتواريخ انتهاء الرخص لضمان الالتزام القانوني:")
        st.dataframe(df, use_container_width=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>نظام أسطولي لإدارة النقل والتوصيل © 2026 - إعداد بشمهندسة بسملة عبد الستار 🚀</p>", unsafe_allow_html=True)
