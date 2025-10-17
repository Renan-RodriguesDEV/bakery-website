import os

import streamlit as st


def load_css(filename):
    with open(
        os.path.join(os.getcwd(), "main", "src", "style", "components", filename),
        "r",
        encoding="utf-8",
    ) as f:
        st.html(f"<style>{f.read()}</style>")


def get_config_map(latitude, longitude):
    return f"""
        <style>
        :root {{
            --accent: #DAA520;
            --card-bg: rgba(255,255,255,0.04);
            --text: #ffffff;
            --muted: rgba(255,255,255,0.75);
        }}
        .location-card {{
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--card-bg);
            padding: 12px;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
            transition: transform 0.12s ease, box-shadow 0.12s ease;
            color: var(--text);
            max-width: 100%;
        }}
        .location-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 24px rgba(0,0,0,0.18);
        }}
        .location-icon {{
            font-size: 28px;
            line-height: 1;
            padding: 8px;
            border-radius: 8px;
            background: rgba(218,165,32,0.12);
            color: var(--accent);
            display:flex;
            align-items:center;
            justify-content:center;
            min-width:44px;
            min-height:44px;
        }}
        .location-content {{
            flex: 1;
            min-width: 0;
        }}
        .location-title {{
            margin: 0;
            font-weight: 700;
            font-size: 16px;
            color: var(--text);
        }}
        .location-sub {{
            margin: 2px 0 0 0;
            font-size: 13px;
            color: var(--muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .map-btn {{
            background: var(--accent);
            color: #fff;
            padding: 8px 10px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            transition: filter 0.12s ease, transform 0.12s ease;
            border: none;
        }}
        .map-btn:hover {{
            filter: brightness(0.95);
            transform: translateY(-1px);
        }}
        @media (max-width:420px) {{
            .location-card {{ gap: 8px; padding: 10px; }}
            .location-icon {{ font-size: 24px; min-width:40px; min-height:40px; }}
            .location-title {{ font-size: 15px; }}
        }}
        </style>
        <div class="location-card" role="region" aria-label="Localização da loja">
            <div class="location-icon" aria-hidden="true">📍</div>
            <div class="location-content">
                <p class="location-title">Estamos localizados em</p>
                <p  class="location-sub">Clique em "maps" para abrir a localização no Google Maps</p>
            </div>
            <a style="text-decoration:none; color:#fff" class="map-btn" href="https://www.google.com/maps/search/?api=1&query={latitude},{longitude}" target="_blank" rel="noopener noreferrer">maps</a>
        </div>
"""
