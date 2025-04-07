
import streamlit as st
import os
from PIL import Image

# ========== SETUP ==========
st.set_page_config(page_title="Mentorship Intersectional Dashboard", layout="wide")

BASE_DIR = "race_gender_parenteducation_careerstage"
SECTIONS = ["Overview", "1-Way Analysis", "2-Way Analysis", "3-Way Analysis", "4-Way Analysis", "Visualizations"]

st.title("📊 Mentorship Analysis Dashboard")
st.markdown("Explore 1-way to 4-way intersectional analyses of mentorship hours using race, gender, parent education, career stage, and major categories.")

section = st.sidebar.radio("📁 Choose Section", SECTIONS)

# ========== HELPERS ==========
def load_text(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def display_folder(folder_path):
    text_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".png") or f.endswith(".jpg")]

    for txt in sorted(text_files):
        st.subheader(f"📄 {txt}")
        st.code(load_text(os.path.join(folder_path, txt)), language='text')
        if "effect_size" in txt:
            st.markdown("> ℹ️ **Interpretation**: Higher eta squared values suggest stronger effects of the factor or interaction.")

    for img in sorted(image_files):
        st.subheader(f"🖼 {img}")
        st.image(Image.open(os.path.join(folder_path, img)), use_column_width=True)

# ========== SECTIONS ==========
if section == "Overview":
    st.header("Overview")
    st.markdown("""
    This dashboard summarizes the statistical analyses performed on mentorship hour data across various demographic intersections. 
    Use the sidebar to view:
    - **1-Way Analysis**: Each factor individually
    - **2-Way Analysis**: Pairs of factors
    - **3-Way & 4-Way**: Combined factor interactions
    - **Visuals**: Distributions and boxplots
    """)

elif section == "1-Way Analysis":
    st.header("1-Way Analysis Results")
    one_way_path = os.path.join(BASE_DIR, "1-way")
    if os.path.exists(one_way_path):
        folders = sorted(os.listdir(one_way_path))
        selected = st.selectbox("Select a variable", folders)
        display_folder(os.path.join(one_way_path, selected))
    else:
        st.warning("No 1-Way results found.")

elif section == "2-Way Analysis":
    st.header("2-Way Intersectional Analysis")
    path = os.path.join(BASE_DIR, "2-way")
    if os.path.exists(path):
        folders = sorted(os.listdir(path))
        selected = st.selectbox("Select 2-Way Combination", folders)
        display_folder(os.path.join(path, selected))
    else:
        st.warning("No 2-Way folders found.")

elif section == "3-Way Analysis":
    st.header("3-Way Intersectional Analysis")
    path = os.path.join(BASE_DIR, "3-way")
    if os.path.exists(path):
        folders = sorted(os.listdir(path))
        selected = st.selectbox("Select 3-Way Combination", folders)
        display_folder(os.path.join(path, selected))
    else:
        st.warning("No 3-Way folders found.")

elif section == "4-Way Analysis":
    st.header("4-Way Intersectional Analysis")
    path = os.path.join(BASE_DIR, "4-way")
    if os.path.exists(path):
        folders = sorted(os.listdir(path))
        selected = st.selectbox("Select 4-Way Combination", folders)
        display_folder(os.path.join(path, selected))
    else:
        st.warning("No 4-Way folders found.")

elif section == "Visualizations":
    st.header("Visualizations")
    images = []
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                images.append(os.path.join(root, file))

    selected = st.selectbox("Select Visualization", images)
    st.image(Image.open(selected), use_column_width=True)
    st.text_area("📝 Notes or Interpretation", "")
