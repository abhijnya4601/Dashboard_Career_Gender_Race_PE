
import streamlit as st
import os
from PIL import Image

# ========== SETUP ==========
st.set_page_config(page_title="Mentorship Intersectional Dashboard", layout="wide")

BASE_DIR = "race_gender_parenteducation_careerstage"
SECTIONS = ["Overview", "1-Way Analysis", "2-Way Analysis", "3-Way Analysis", "4-Way Analysis", "Visualizations"]

st.title("📊 Mentorship Analysis Dashboard")
st.markdown("Explore intersectional analyses of mentorship hours using race, gender, parent education, career stage, and major categories.")

section = st.sidebar.radio("📁 Choose Section", SECTIONS)

# ========== HELPERS ==========
def load_text(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def display_folder(folder_path):
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg'))])
    text_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

    for img in image_files:
        st.subheader(f"🖼 {img}")
        st.image(Image.open(os.path.join(folder_path, img)), use_column_width=True)

    for txt in text_files:
        st.subheader(f"📄 {txt}")
        st.code(load_text(os.path.join(folder_path, txt)), language='text')

        # Basic interpretation hints
        if "anova" in txt:
            st.markdown("> 📌 **Interpretation:** ANOVA results show whether there are statistically significant differences in mentorship hours based on this combination of factors.")
        elif "effect_size" in txt:
            st.markdown("> 📏 **Interpretation:** Higher eta squared values indicate a stronger impact of the corresponding variable on mentorship hours.")
        elif "counts" in txt:
            st.markdown("> 🔢 **Interpretation:** These are the participant counts in each demographic group combination.")
        elif "descriptive_stats" in txt:
            st.markdown("> 📊 **Interpretation:** Shows distribution of mentorship hours (mean, std, min, max) for each subgroup.")
        elif "correlation" in txt:
            st.markdown("> 🔗 **Interpretation:** Correlation values closer to ±1 show stronger relationships between variables or with mentorship hours.")

# ========== SECTION ROUTES ==========
def analysis_section(name, subdir):
    st.header(name)
    path = os.path.join(BASE_DIR, subdir)
    if os.path.exists(path):
        folders = sorted(os.listdir(path))
        selected = st.selectbox(f"Select {name} Combination", folders)
        display_folder(os.path.join(path, selected))
    else:
        st.warning(f"No {name} results found.")

if section == "Overview":
    st.header("Overview")
    st.markdown("""
    This dashboard summarizes statistical results from a multi-dimensional analysis of mentorship hours.

    Use the sidebar to explore:
    - **1-Way Analysis**: Effect of individual factors
    - **2-Way Analysis**: Paired factor effects
    - **3-Way & 4-Way**: Combined factor effects and interactions
    - **Visualizations**: All boxplots and distributions
    """)

elif section == "1-Way Analysis":
    analysis_section("1-Way", "1-way")

elif section == "2-Way Analysis":
    analysis_section("2-Way", "2-way")

elif section == "3-Way Analysis":
    analysis_section("3-Way", "3-way")

elif section == "4-Way Analysis":
    analysis_section("4-Way", "4-way")

elif section == "Visualizations":
    st.header("Visualizations")
    images = []
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith((".png", ".jpg")):
                images.append(os.path.join(root, file))
    selected = st.selectbox("Select Image", images)
    st.image(Image.open(selected), use_column_width=True)
    st.text_area("📝 Notes", "")
