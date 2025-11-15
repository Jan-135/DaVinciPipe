# ui/style.py

appStyle = """
#Root { background: #0f1115; }
* { 
    color: #eaeaea; 
    font-family: Inter, Segoe UI, Arial; 
    font-size: 14px; 
}
QLabel { background: transparent; }

#Card { 
    background: #1b1f2a; 
    border-radius: 14px; 
}
QLabel#Title { 
    font-size: 20px; 
    font-weight: 700; 
}
QLabel#Subtitle { 
    color: #a0a7b3; 
    font-size: 12px; 
}
QLabel#Error { 
    color: #ff6b6b; 
    background: rgba(255,107,107,0.08); 
    border: 1px solid rgba(255,107,107,0.35); 
    padding: 6px 8px; 
    border-radius: 8px; 
}

/* Inputs */
QLineEdit#LineEdit { 
    background: #0f1320; 
    border:1px solid #2a3142; 
    border-radius:10px; 
    padding:10px 12px; 
}
QLineEdit#LineEdit:focus { 
    border-color:#3a7afe; 
}

/* Buttons allgemein */
QPushButton { 
    border-radius: 10px; 
    padding: 9px 12px; 
}

/* Primary Buttons – früher "Sign In" */
QPushButton[role="primary"] {
    background:#3a7afe; 
    color:white; 
    border:none; 
}
QPushButton[role="primary"]:hover { 
    background:#2f67d6; 
}

/* Secondary Buttons – früher "Cancel" / "Browse" */
QPushButton[role="secondary"] {
    background:transparent; 
    border:1px solid #2a3142; 
}
QPushButton[role="secondary"]:hover {
    background:#0f1320; 
}
"""
