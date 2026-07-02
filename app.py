import streamlit as st
import time
from pathlib import Path
from main import create_file, read_file, rename_file, append_file, overwrite_file, delete_file

st.set_page_config(page_title="Smart File Manager", page_icon="📁", layout="centered")

if "tab" not in st.session_state:
    st.session_state.tab = "Create"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background:#000;}
.block-container{padding:3rem 1rem 5rem!important;max-width:620px!important;margin:0 auto!important;}

.top-badge{text-align:center;margin-bottom:1.4rem;}
.top-badge span{display:inline-flex;align-items:center;gap:.4rem;border:1px solid #C8F135;
border-radius:999px;padding:.28rem .9rem;font-size:.6rem;font-weight:700;color:#C8F135;
letter-spacing:2px;text-transform:uppercase;}

.main-title{text-align:center;font-size:3rem;font-weight:800;color:#fff;
letter-spacing:-1.5px;line-height:1;margin-bottom:.4rem;}
.main-sub{text-align:center;font-size:.8rem;color:#444;letter-spacing:.5px;margin-bottom:2.4rem;}
.main-sub b{color:#C8F135;}

.panel{background:#111;border:1px solid #1e1e1e;border-radius:12px;
padding:1.5rem 1.7rem 1rem;margin-top:.3rem;}
.panel-ttl{font-size:.95rem;font-weight:700;color:#fff;margin-bottom:1.2rem;
display:flex;align-items:center;gap:.45rem;}
.panel-ttl b{color:#C8F135;}

.stTextInput>div>div>input,.stTextArea>div>div>textarea{
background:#0a0a0a!important;border:1px solid #2a2a2a!important;
border-radius:7px!important;color:#e0e0e0!important;font-size:.87rem!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
border-color:#C8F135!important;box-shadow:0 0 0 2px rgba(200,241,53,.12)!important;}
[data-baseweb="select"]>div{background:#0a0a0a!important;border:1px solid #2a2a2a!important;
border-radius:7px!important;}
[data-baseweb="select"] *{color:#e0e0e0!important;}
label{color:#555!important;font-size:.62rem!important;font-weight:700!important;
letter-spacing:1.4px!important;text-transform:uppercase!important;}

/* Secondary = inactive tab */
button[kind="secondary"]{
    background:#111!important;color:#555!important;
    border:1px solid #2a2a2a!important;font-size:.72rem!important;
    font-weight:700!important;letter-spacing:1px!important;
    padding:.55rem .4rem!important;border-radius:7px!important;
    box-shadow:none!important;transition:all .15s ease!important;}
button[kind="secondary"]:hover{
    border-color:#4311ee!important;color:#4311ee!important;
    background:#111!important;box-shadow:none!important;}

/* Primary = active tab + action buttons — lime */
.stButton>button{background:#C8F135!important;color:#000!important;font-weight:700!important;
font-size:.85rem!important;border:none!important;border-radius:7px!important;
padding:.6rem 1.4rem!important;width:100%!important;
transition:all .15s ease!important;box-shadow:none!important;}
.stButton>button:hover{background:#d4f547!important;transform:translateY(-1px)!important;
box-shadow:0 4px 14px rgba(55, 14, 202, 22)!important;}

.stDownloadButton>button{background:#1a1a1a!important;color:#C8F135!important;
border:1px solid #C8F135!important;font-weight:700!important;font-size:.85rem!important;
border-radius:7px!important;padding:.6rem 1.4rem!important;width:100%!important;
transition:all .15s ease!important;}
.stDownloadButton>button:hover{background:rgba(200,241,53,.1)!important;
transform:translateY(-1px)!important;}

div[data-testid="stAlert"]{border-radius:7px!important;font-size:.82rem!important;}
.stCodeBlock>div{border-radius:7px!important;border:1px solid #1e1e1e!important;
background:#0a0a0a!important;font-size:.81rem!important;}
details{background:#0a0a0a!important;border:1px solid #1e1e1e!important;
border-radius:7px!important;overflow:hidden!important;}
details summary{color:#555!important;font-size:.79rem!important;padding:.55rem .9rem!important;}
.stCheckbox label{color:#666!important;font-size:.82rem!important;
font-weight:500!important;letter-spacing:0!important;text-transform:none!important;}

.dnote{font-size:.79rem;color:#666;margin:.4rem 0 .9rem;line-height:1.6;}
.dnote code{background:#1a1a1a;color:#C8F135;padding:.1rem .35rem;
border-radius:4px;font-size:.79rem;}
.meta{font-size:.7rem;color:#444;margin-bottom:.6rem;font-family:monospace;}

.site-footer{text-align:center;margin-top:3rem;font-size:.62rem;color:#ffffff;
letter-spacing:1.4px;text-transform:uppercase;}
.site-footer b{color:#C8F135;}
</style>
""", unsafe_allow_html=True)



def show(r, balloon=False):
    if r["success"]:
        st.success(f"✅  {r['message']}")
        if balloon:
            st.balloons()
    else:
        st.error(f"❌  {r['message']}")


def project_files():
    exts = {".txt",".csv",".md",".py",".json",".yaml",".yml",
            ".ini",".cfg",".log",".html",".xml",".js",".ts",
            ".css",".sh",".toml",".rst",".env",".bat"}
    try:
        return sorted(e.name for e in Path(".").iterdir()
                      if e.is_file() and e.suffix.lower() in exts)
    except Exception:
        return []


# ── Header ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-badge"><span>📁 &nbsp; File Management System</span></div>
<div class="main-title">Smart File Manager</div>
<div class="main-sub">&ndash; <b>create</b> &nbsp;·&nbsp; read &nbsp;·&nbsp;
<b>update</b> &nbsp;·&nbsp; delete &ndash;</div>
""", unsafe_allow_html=True)

# ── Tab navigation ────────────────────────────────────────────────────────────────
TABS = [
    ("Create", "+ CREATE"),
    ("Read",   "◎ READ"),
    ("Update", "○ UPDATE"),
    ("Delete", "✕ DELETE"),
]

cols = st.columns(4, gap="small")
for col, (name, icon) in zip(cols, TABS):
    with col:
        active = st.session_state.tab == name
        btn_type = "primary" if active else "secondary"
        if st.button(icon, key=f"t_{name}", use_container_width=True,
                     type=btn_type):
            st.session_state.tab = name
            st.rerun()

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

# ── CREATE ────────────────────────────────────────────────────────────────────────
if st.session_state.tab == "Create":
    st.markdown('<div class="panel"><div class="panel-ttl"><b>+</b> Create File</div></div>',
                unsafe_allow_html=True)
    name    = st.text_input("FILE NAME", placeholder="e.g. notes.txt")
    content = st.text_area("CONTENT", placeholder="Type file content here…", height=180)
    with st.expander("📎  Upload a file instead"):
        up = st.file_uploader("Upload", type=None, label_visibility="collapsed")
        if up:
            content = up.read().decode("utf-8", errors="replace")
            st.caption(f"Loaded {up.name} — {len(content):,} chars")
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    if st.button("Create File", key="do_create", use_container_width=True):
        if not name.strip():
            st.error("Enter a file name.")
        else:
            with st.spinner("Creating…"):
                time.sleep(0.2)
            show(create_file(name.strip(), content), balloon=True)

# ── READ ──────────────────────────────────────────────────────────────────────────
elif st.session_state.tab == "Read":
    st.markdown('<div class="panel"><div class="panel-ttl"><b>◎</b> Read File</div></div>',
                unsafe_allow_html=True)
    files = project_files()
    name  = st.selectbox("SELECT FILE", files) if files else \
            st.text_input("FILE NAME", placeholder="e.g. notes.txt")
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    if st.button("Read File", key="do_read", use_container_width=True):
        n = str(name).strip() if name else ""
        if not n:
            st.error("Select or enter a file name.")
        else:
            with st.spinner("Reading…"):
                r = read_file(n)
            if r["success"]:
                c = r["content"]
                st.success(f"✅  {r['message']}")
                st.markdown(
                    f"<div class='meta'>{n} &nbsp;·&nbsp; "
                    f"{len(c):,} chars &nbsp;·&nbsp; {len(c.splitlines())} lines</div>",
                    unsafe_allow_html=True)
                st.code(c, language="text")
                st.download_button("⬇️  Download", c, file_name=n,
                                   mime="text/plain", use_container_width=True)
            else:
                st.error(f"❌  {r['message']}")

# ── UPDATE ────────────────────────────────────────────────────────────────────────
elif st.session_state.tab == "Update":
    st.markdown('<div class="panel"><div class="panel-ttl"><b>○</b> Update File</div></div>',
                unsafe_allow_html=True)
    op    = st.selectbox("OPERATION", ["Rename", "Append Content", "Overwrite Content"])
    files = project_files()
    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

    if op == "Rename":
        old = st.selectbox("CURRENT FILE", files, key="ren_s") if files else \
              st.text_input("CURRENT FILE NAME", placeholder="old.txt", key="ren_t")
        new = st.text_input("NEW FILE NAME", placeholder="new.txt")
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        if st.button("Rename File", key="do_rename", use_container_width=True):
            o, n = str(old).strip() if old else "", new.strip()
            if not o or not n:
                st.error("Fill in both filenames.")
            else:
                show(rename_file(o, n), balloon=True)

    elif op == "Append Content":
        name = st.selectbox("SELECT FILE", files, key="app_s") if files else \
               st.text_input("FILE NAME", placeholder="notes.txt", key="app_t")
        data = st.text_area("CONTENT TO APPEND",
                             placeholder="Content to add at the end…", height=160)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        if st.button("Append Content", key="do_append", use_container_width=True):
            n = str(name).strip() if name else ""
            if not n:
                st.error("Select or enter a file name.")
            else:
                show(append_file(n, data), balloon=True)

    elif op == "Overwrite Content":
        name = st.selectbox("SELECT FILE", files, key="ow_s") if files else \
               st.text_input("FILE NAME", placeholder="notes.txt", key="ow_t")
        data = st.text_area("NEW CONTENT",
                             placeholder="Replaces all existing content…", height=160)
        with st.expander("⚠️  About overwrite"):
            st.warning("Permanently replaces ALL content. Cannot be undone.")
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        if st.button("Overwrite File", key="do_overwrite", use_container_width=True):
            n = str(name).strip() if name else ""
            if not n:
                st.error("Select or enter a file name.")
            else:
                show(overwrite_file(n, data), balloon=True)

# ── DELETE ────────────────────────────────────────────────────────────────────────
elif st.session_state.tab == "Delete":
    st.markdown('<div class="panel"><div class="panel-ttl"><b>✕</b> Delete File</div></div>',
                unsafe_allow_html=True)
    files = project_files()
    name  = st.selectbox("SELECT FILE", files, key="del_s") if files else \
            st.text_input("FILE NAME", placeholder="old_report.txt", key="del_t")
    if name:
        st.markdown(
            f"<div class='dnote'>You are about to permanently delete "
            f"<code>{name}</code>. This action cannot be undone.</div>",
            unsafe_allow_html=True)
        confirmed = st.checkbox(f"I understand — permanently delete {name}",
                                key="del_confirm")
    else:
        confirmed = False
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    if st.button("Delete File", key="do_delete", use_container_width=True):
        n = str(name).strip() if name else ""
        if not n:
            st.error("Select or enter a file name.")
        elif not confirmed:
            st.warning("Check the confirmation box first.")
        else:
            with st.spinner("Deleting…"):
                time.sleep(0.2)
            show(delete_file(n), balloon=True)

# ── Footer ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    Built with <b>♥</b> Streamlit and Python&nbsp;·&nbsp; <br>Developed by Shubham S Shivarayakar
</div>
""", unsafe_allow_html=True)
