from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import requests
from datetime import datetime

app = Dash(__name__, title="Dashboard Cuaca Indonesia")
server = app.server

KOTA_DEFAULT = "Bojonegoro"

KOORDINAT_KOTA = {
    "Surabaya": {"lat": -7.2575, "lon": 112.7521, "negara": "Indonesia"},
    "Jakarta": {"lat": -6.2088, "lon": 106.8456, "negara": "Indonesia"},
    "Bandung": {"lat": -6.9175, "lon": 107.6191, "negara": "Indonesia"},
    "Yogyakarta": {"lat": -7.7956, "lon": 110.3695, "negara": "Indonesia"},
    "Malang": {"lat": -7.9666, "lon": 112.6326, "negara": "Indonesia"},
    "Bali": {"lat": -8.4095, "lon": 115.1889, "negara": "Indonesia"},
    "Makassar": {"lat": -5.1477, "lon": 119.4327, "negara": "Indonesia"},
    "Medan": {"lat": 3.5952, "lon": 98.6722, "negara": "Indonesia"},
    "Semarang": {"lat": -6.9667, "lon": 110.4167, "negara": "Indonesia"},
    "Palembang": {"lat": -2.9761, "lon": 104.7754, "negara": "Indonesia"},
    "Bojonegoro": {"lat": -7.1502, "lon": 111.8817, "negara": "Indonesia"},
}

CSS = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: "Segoe UI", Arial, sans-serif;
}
body {
    background: linear-gradient(135deg, #c5dcf3 0%, #b6d3ef 50%, #cfe4f8 100%);
    min-height: 100vh;
}
.page-bg {
    min-height: 100vh;
    padding: 32px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.main-shell {
    width: 100%;
    max-width: 1400px;
    min-height: 820px;
    background: #05070b;
    border-radius: 28px;
    padding: 18px;
    display: grid;
    grid-template-columns: 82px 1fr;
    gap: 18px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
    border: 1px solid rgba(255,255,255,0.06);
}
.sidebar {
    background: linear-gradient(180deg, #091120 0%, #0b1120 100%);
    border-radius: 22px;
    padding: 18px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    border: 1px solid rgba(255,255,255,0.05);
}
.sidebar-logo {
    width: 52px;
    height: 52px;
    border-radius: 18px;
    background: linear-gradient(135deg, #4fa4ff, #6a8cff);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: 700;
    font-size: 20px;
    margin-bottom: 8px;
}
.sidebar-icon {
    width: 52px;
    height: 52px;
    border-radius: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #a4afc3;
    background: rgba(255,255,255,0.02);
    cursor: pointer;
    transition: 0.2s ease;
    font-size: 22px;
}
.sidebar-icon.active,
.sidebar-icon:hover {
    background: linear-gradient(135deg, #4f9cff, #6fa5ff);
    color: white;
}
.dashboard-content {
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.topbar {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 16px;
}
.search-box {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(90deg, #0d1526 0%, #0d1524 100%);
    border-radius: 22px;
    padding: 10px 12px;
    min-width: 450px;
    border: 1px solid rgba(255,255,255,0.05);
}
.search-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: #ffffff;
    font-size: 18px;
    padding: 10px 14px;
}
.search-input::placeholder {
    color: #8b94a7;
}
.search-btn {
    background: linear-gradient(135deg, #4ea3ff, #648fff);
    color: white;
    border: none;
    border-radius: 18px;
    padding: 16px 28px;
    cursor: pointer;
    font-weight: 700;
    font-size: 16px;
}
.search-btn:hover {
    transform: translateY(-1px);
}
.content-grid {
    display: grid;
    grid-template-columns: 0.95fr 1.15fr 1fr;
    gap: 18px;
    flex: 1;
}
.left-column, .center-column, .right-column {
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.hero-weather-card {
    min-height: 490px;
    border-radius: 30px;
    padding: 28px;
    background: linear-gradient(180deg, #75b4f8 0%, #619eea 60%, #4d7ee2 100%);
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-weather-card::after {
    content: "";
    position: absolute;
    right: -40px;
    bottom: -40px;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.hero-date {
    font-size: 16px;
    opacity: 0.95;
    position: relative;
    z-index: 5;
}
.hero-location {
    margin-top: 16px;
    font-size: 18px;
    font-weight: 700;
    position: relative;
    z-index: 5;
}
.hero-animation {
    position: relative;
    height: 150px;
    margin-top: 20px;
    z-index: 2;
}
.hero-temp {
    margin-top: 4px;
    font-size: 84px;
    font-weight: 800;
    line-height: 1;
    position: relative;
    z-index: 5;
}
.hero-desc {
    margin-top: 10px;
    font-size: 24px;
    position: relative;
    z-index: 5;
}
.hero-stats {
    margin-top: 34px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    position: relative;
    z-index: 5;
}
.stat-box {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 22px;
    padding: 16px;
    backdrop-filter: blur(8px);
}
.stat-label {
    font-size: 14px;
    opacity: 0.95;
}
.stat-value {
    margin-top: 10px;
    font-size: 18px;
    font-weight: 800;
}
.mini-cities-wrapper {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.mini-city-card {
    background: linear-gradient(90deg, #0d1526 0%, #0d1524 100%);
    border-radius: 24px;
    padding: 20px 22px;
    border: 1px solid rgba(255,255,255,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.mini-city-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.mini-icon {
    font-size: 28px;
}
.mini-city-name {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
}
.mini-city-desc {
    color: #9ba8c5;
    font-size: 14px;
    margin-top: 4px;
}
.mini-temp {
    color: white;
    font-size: 48px;
    font-weight: 800;
}
.forecast-card, .chart-card, .map-card, .details-card, .map-info-card {
    background: linear-gradient(90deg, #0d1526 0%, #0d1524 100%);
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.05);
}
.forecast-card {
    padding: 26px;
    min-height: 490px;
}
.card-header-row {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}
.card-title {
    color: #ffffff;
    font-size: 26px;
    font-weight: 800;
}
.see-all {
    color: #8ab8ff;
    font-size: 16px;
    cursor: pointer;
    margin-left: auto;
}
.forecast-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.forecast-row {
    display: grid;
    grid-template-columns: 120px 60px 1fr 120px;
    align-items: center;
    gap: 8px;
    padding: 16px 16px;
    border-radius: 20px;
    background: rgba(255,255,255,0.02);
}
.forecast-day {
    color: #ffffff;
    font-weight: 700;
    font-size: 17px;
}
.forecast-icon {
    font-size: 28px;
}
.forecast-desc {
    color: #aeb9d0;
    font-size: 15px;
}
.forecast-temp {
    color: #ffffff;
    text-align: right;
    font-weight: 800;
    font-size: 18px;
}
.chart-card {
    padding: 20px;
    min-height: 320px;
}
.chart-graph {
    height: 250px;
}
.map-card {
    overflow: hidden;
    min-height: 430px;
}
.map-graph {
    height: 430px;
}
.map-info-card {
    padding: 16px 20px;
    color: #dbe5f7;
    font-size: 15px;
}
.details-card {
    padding: 20px;
    min-height: 260px;
}
.details-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
}
.detail-item {
    background: rgba(255,255,255,0.03);
    border-radius: 22px;
    padding: 24px 20px;
}
.detail-label {
    color: #9fb0cc;
    font-size: 16px;
}
.detail-value {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    margin-top: 12px;
}
.error-box {
    background: #141923;
    border-radius: 24px;
    padding: 24px;
    color: #f4f7fd;
    border: 1px solid rgba(255,255,255,0.06);
}

/* ANIMASI CUACA */
.sun {
    position: absolute;
    left: 38px;
    top: 15px;
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #fff6b1, #ffd348 65%, #ffbe27 100%);
    box-shadow: 0 0 35px rgba(255, 214, 82, 0.55);
    animation: putarMatahari 12s linear infinite;
}
.sun-rays {
    position: absolute;
    left: 13px;
    top: 13px;
    width: 112px;
    height: 112px;
    border-radius: 50%;
    border: 3px dashed rgba(255, 221, 116, 0.55);
    animation: putarMatahari 18s linear infinite reverse;
}
.cloud {
    position: absolute;
    width: 118px;
    height: 52px;
    border-radius: 35px;
    background: linear-gradient(180deg, #ffffff, #d9d8ef);
    box-shadow: inset -8px -8px 18px rgba(124, 109, 210, 0.10);
    animation: awanJalan 6s ease-in-out infinite;
}
.cloud::before {
    content: "";
    position: absolute;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(180deg, #ffffff, #d9d8ef);
    left: 16px;
    top: -24px;
}
.cloud::after {
    content: "";
    position: absolute;
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: linear-gradient(180deg, #ffffff, #d9d8ef);
    left: 42px;
    top: -34px;
}
.cloud.dark {
    background: linear-gradient(180deg, #4f5d7e, #2b3550);
}
.cloud.dark::before,
.cloud.dark::after {
    background: linear-gradient(180deg, #4f5d7e, #2b3550);
}
.rain-drop {
    position: absolute;
    width: 8px;
    height: 26px;
    border-radius: 10px;
    background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(86, 93, 255, 0.9));
    animation: hujanTurun 1s linear infinite;
}
.lightning {
    position: absolute;
    left: 80px;
    top: 54px;
    font-size: 54px;
    animation: kilatKedip 1.2s infinite;
}
.fog-layer {
    position: absolute;
    width: 150px;
    height: 18px;
    border-radius: 20px;
    background: rgba(255,255,255,0.25);
    filter: blur(2px);
    animation: kabutGeser 5s ease-in-out infinite;
}
@keyframes putarMatahari {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes awanJalan {
    0%, 100% { transform: translateX(0px) translateY(0px); }
    50% { transform: translateX(10px) translateY(-5px); }
}
@keyframes hujanTurun {
    0% { transform: translateY(0px); opacity: 1; }
    100% { transform: translateY(34px); opacity: 0; }
}
@keyframes kilatKedip {
    0%, 100% { opacity: 0.15; transform: scale(0.95); }
    30% { opacity: 1; transform: scale(1.1); }
    60% { opacity: 0.35; transform: scale(1); }
}
@keyframes kabutGeser {
    0%, 100% { transform: translateX(0px); opacity: 0.35; }
    50% { transform: translateX(18px); opacity: 0.6; }
}

@media (max-width: 1280px) {
    .content-grid { grid-template-columns: 1fr; }
    .main-shell { grid-template-columns: 1fr; }
    .sidebar {
        flex-direction: row;
        justify-content: center;
    }
}
@media (max-width: 768px) {
    .page-bg { padding: 14px; }
    .search-box {
        min-width: unset;
        width: 100%;
    }
    .topbar {
        flex-direction: column;
        align-items: stretch;
    }
    .forecast-row {
        grid-template-columns: 1fr;
        text-align: left;
    }
    .details-grid { grid-template-columns: 1fr; }
    .hero-stats { grid-template-columns: 1fr; }
}
"""

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{CSS}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

def kode_cuaca_ke_teks(kode):
    mapping = {
        0: "Cerah",
        1: "Cerah Berawan",
        2: "Berawan Sebagian",
        3: "Mendung",
        45: "Berkabut",
        48: "Kabut Tebal",
        51: "Gerimis Ringan",
        53: "Gerimis Sedang",
        55: "Gerimis Lebat",
        56: "Gerimis Beku Ringan",
        57: "Gerimis Beku Lebat",
        61: "Hujan Ringan",
        63: "Hujan Sedang",
        65: "Hujan Lebat",
        66: "Hujan Beku Ringan",
        67: "Hujan Beku Lebat",
        71: "Salju Ringan",
        73: "Salju Sedang",
        75: "Salju Lebat",
        77: "Butiran Salju",
        80: "Hujan Lokal",
        81: "Hujan Deras",
        82: "Hujan Sangat Deras",
        85: "Salju Lokal",
        86: "Salju Lebat",
        95: "Badai Petir",
        96: "Badai + Hujan Es",
        99: "Badai Hebat",
    }
    return mapping.get(kode, "Tidak Diketahui")

def kode_cuaca_ke_icon(kode):
    if kode == 0:
        return "☀️"
    elif kode in [1, 2]:
        return "⛅"
    elif kode == 3:
        return "☁️"
    elif kode in [45, 48]:
        return "🌫️"
    elif kode in [51, 53, 55, 56, 57]:
        return "🌦️"
    elif kode in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"
    elif kode in [71, 73, 75, 77, 85, 86]:
        return "❄️"
    elif kode in [95, 96, 99]:
        return "⛈️"
    return "🌤️"

def format_hari_indonesia(tanggal_str):
    dt = datetime.strptime(tanggal_str, "%Y-%m-%d")
    hari_en = dt.strftime("%A")
    mapping = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return mapping.get(hari_en, hari_en)

def format_tanggal_indonesia(dt):
    nama_hari = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    nama_bulan = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
        7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
    }
    hari = nama_hari.get(dt.strftime("%A"), dt.strftime("%A"))
    return f"{hari}, {dt.day} {nama_bulan[dt.month]} {dt.year}"

def ambil_koordinat(nama_kota):
    if nama_kota in KOORDINAT_KOTA:
        return {
            "nama": nama_kota,
            "lat": KOORDINAT_KOTA[nama_kota]["lat"],
            "lon": KOORDINAT_KOTA[nama_kota]["lon"],
            "negara": KOORDINAT_KOTA[nama_kota]["negara"]
        }

    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": nama_kota, "count": 1, "language": "id", "format": "json"}
        res = requests.get(url, params=params, timeout=15)
        data = res.json()
        if "results" in data and len(data["results"]) > 0:
            hasil = data["results"][0]
            return {
                "nama": hasil.get("name", nama_kota),
                "lat": hasil["latitude"],
                "lon": hasil["longitude"],
                "negara": hasil.get("country", "Indonesia")
            }
    except Exception:
        pass

    return {
        "nama": KOTA_DEFAULT,
        "lat": KOORDINAT_KOTA[KOTA_DEFAULT]["lat"],
        "lon": KOORDINAT_KOTA[KOTA_DEFAULT]["lon"],
        "negara": KOORDINAT_KOTA[KOTA_DEFAULT]["negara"]
    }

def ambil_data_cuaca(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m",
        "hourly": "temperature_2m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max",
        "forecast_days": 7,
        "timezone": "auto"
    }
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json()

def buat_grafik_suhu(data_per_jam):
    waktu = data_per_jam["time"][:24]
    suhu = data_per_jam["temperature_2m"][:24]
    waktu_format = [datetime.fromisoformat(t).strftime("%H:%M") for t in waktu]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=waktu_format,
            y=suhu,
            mode="lines+markers",
            line=dict(width=3, color="#6a7cff"),
            marker=dict(size=6, color="#6a7cff"),
            fill="tozeroy",
            fillcolor="rgba(106, 124, 255, 0.14)",
            hovertemplate="Jam %{x}<br>Suhu %{y}°C<extra></extra>"
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#A7B0C0")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zeroline=False, tickfont=dict(color="#A7B0C0")),
        font=dict(color="#EAEFF7")
    )
    return fig

def buat_peta_interaktif(lat, lon, nama_kota, suhu, deskripsi):
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode="markers+text",
            text=[f"{nama_kota}<br>{suhu}°C · {deskripsi}"],
            textposition="top right",
            marker=dict(size=18, color="#695cff"),
            hovertemplate=f"<b>{nama_kota}</b><br>Suhu: {suhu}°C<br>Kondisi: {deskripsi}<extra></extra>",
            name="Lokasi"
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=lat, lon=lon),
            zoom=8
        ),
        clickmode="event+select",
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff")
    )
    return fig

def animasi_cuaca(kode):
    if kode == 0:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="sun-rays"),
                html.Div(className="sun")
            ]
        )

    if kode in [1, 2]:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="sun-rays"),
                html.Div(className="sun"),
                html.Div(className="cloud", style={"left": "65px", "top": "56px"})
            ]
        )

    if kode == 3:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="cloud dark", style={"left": "30px", "top": "48px"}),
                html.Div(className="cloud dark", style={"left": "85px", "top": "60px", "transform": "scale(0.85)"})
            ]
        )

    if kode in [45, 48]:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="cloud", style={"left": "36px", "top": "30px"}),
                html.Div(className="fog-layer", style={"left": "10px", "top": "95px"}),
                html.Div(className="fog-layer", style={"left": "28px", "top": "118px"}),
                html.Div(className="fog-layer", style={"left": "0px", "top": "138px"})
            ]
        )

    if kode in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="cloud", style={"left": "42px", "top": "28px"}),
                html.Div(className="rain-drop", style={"left": "58px", "top": "88px", "animationDelay": "0s"}),
                html.Div(className="rain-drop", style={"left": "82px", "top": "95px", "animationDelay": "0.2s"}),
                html.Div(className="rain-drop", style={"left": "106px", "top": "88px", "animationDelay": "0.4s"}),
                html.Div(className="rain-drop", style={"left": "130px", "top": "95px", "animationDelay": "0.1s"})
            ]
        )

    if kode in [95, 96, 99]:
        return html.Div(
            className="hero-animation",
            children=[
                html.Div(className="cloud dark", style={"left": "42px", "top": "22px"}),
                html.Div("⚡", className="lightning"),
                html.Div(className="rain-drop", style={"left": "50px", "top": "96px", "animationDelay": "0.1s"}),
                html.Div(className="rain-drop", style={"left": "75px", "top": "104px", "animationDelay": "0.3s"}),
                html.Div(className="rain-drop", style={"left": "108px", "top": "100px", "animationDelay": "0.0s"}),
                html.Div(className="rain-drop", style={"left": "135px", "top": "106px", "animationDelay": "0.4s"})
            ]
        )

    return html.Div(
        className="hero-animation",
        children=[
            html.Div(className="cloud", style={"left": "42px", "top": "28px"})
        ]
    )

def kartu_kota_kecil(nama_kota):
    coords = ambil_koordinat(nama_kota)
    try:
        data = ambil_data_cuaca(coords["lat"], coords["lon"])
        current = data["current"]
        icon = kode_cuaca_ke_icon(current["weather_code"])
        return html.Div(
            className="mini-city-card",
            children=[
                html.Div(
                    className="mini-city-left",
                    children=[
                        html.Div(icon, className="mini-icon"),
                        html.Div([
                            html.Div(nama_kota, className="mini-city-name"),
                            html.Div(kode_cuaca_ke_teks(current["weather_code"]), className="mini-city-desc")
                        ])
                    ]
                ),
                html.Div(f"{round(current['temperature_2m'])}°", className="mini-temp")
            ]
        )
    except Exception:
        return html.Div(
            className="mini-city-card",
            children=[
                html.Div(
                    className="mini-city-left",
                    children=[
                        html.Div("🌥️", className="mini-icon"),
                        html.Div([
                            html.Div(nama_kota, className="mini-city-name"),
                            html.Div("Data tidak tersedia", className="mini-city-desc")
                        ])
                    ]
                ),
                html.Div("--°", className="mini-temp")
            ]
        )

def bangun_dashboard(nama_kota):
    coords = ambil_koordinat(nama_kota)
    cuaca = ambil_data_cuaca(coords["lat"], coords["lon"])
    current = cuaca["current"]
    daily = cuaca["daily"]
    hourly = cuaca["hourly"]

    teks_cuaca = kode_cuaca_ke_teks(current["weather_code"])

    kartu_forecast = []
    for i in range(7):
        hari = format_hari_indonesia(daily["time"][i])
        kode = daily["weather_code"][i]
        icon = kode_cuaca_ke_icon(kode)
        kartu_forecast.append(
            html.Div(
                className="forecast-row",
                children=[
                    html.Div(hari, className="forecast-day"),
                    html.Div(icon, className="forecast-icon"),
                    html.Div(kode_cuaca_ke_teks(kode), className="forecast-desc"),
                    html.Div(
                        f"{round(daily['temperature_2m_max'][i])}° / {round(daily['temperature_2m_min'][i])}°",
                        className="forecast-temp"
                    ),
                ]
            )
        )

    kartu_utama = html.Div(
        className="hero-weather-card",
        children=[
            html.Div(format_tanggal_indonesia(datetime.now()), className="hero-date"),
            html.Div(f"{coords['nama']}, {coords['negara']}", className="hero-location"),
            animasi_cuaca(current["weather_code"]),
            html.Div(f"{round(current['temperature_2m'])}°", className="hero-temp"),
            html.Div(teks_cuaca, className="hero-desc"),
            html.Div(
                className="hero-stats",
                children=[
                    html.Div([
                        html.Div("Angin", className="stat-label"),
                        html.Div(f"{current['wind_speed_10m']} km/j", className="stat-value")
                    ], className="stat-box"),
                    html.Div([
                        html.Div("Kelembapan", className="stat-label"),
                        html.Div(f"{current['relative_humidity_2m']}%", className="stat-value")
                    ], className="stat-box"),
                    html.Div([
                        html.Div("Curah", className="stat-label"),
                        html.Div(f"{current['precipitation']} mm", className="stat-value")
                    ], className="stat-box"),
                ]
            )
        ]
    )

    kartu_7_hari = html.Div(
        className="forecast-card",
        children=[
            html.Div(
                className="card-header-row",
                children=[
                    html.H3("Prakiraan 7 Hari", className="card-title"),
                    html.Div("Lihat semua", className="see-all")
                ]
            ),
            html.Div(className="forecast-list", children=kartu_forecast)
        ]
    )

    detail = html.Div(
        className="details-grid",
        children=[
            html.Div([
                html.Div("Terasa Seperti", className="detail-label"),
                html.Div(f"{round(current['apparent_temperature'])}°C", className="detail-value")
            ], className="detail-item"),
            html.Div([
                html.Div("Kelembapan", className="detail-label"),
                html.Div(f"{current['relative_humidity_2m']}%", className="detail-value")
            ], className="detail-item"),
            html.Div([
                html.Div("Peluang Hujan", className="detail-label"),
                html.Div(f"{daily['precipitation_probability_max'][0]}%", className="detail-value")
            ], className="detail-item"),
            html.Div([
                html.Div("Matahari Terbit", className="detail-label"),
                html.Div(daily["sunrise"][0][-5:], className="detail-value")
            ], className="detail-item"),
            html.Div([
                html.Div("Matahari Terbenam", className="detail-label"),
                html.Div(daily["sunset"][0][-5:], className="detail-value")
            ], className="detail-item"),
            html.Div([
                html.Div("Kondisi", className="detail-label"),
                html.Div(teks_cuaca, className="detail-value")
            ], className="detail-item"),
        ]
    )

    fig_peta = buat_peta_interaktif(
        coords["lat"], coords["lon"], coords["nama"], round(current["temperature_2m"]), teks_cuaca
    )

    return kartu_utama, kartu_7_hari, buat_grafik_suhu(hourly), fig_peta, detail

app.layout = html.Div(
    className="page-bg",
    children=[
        dcc.Interval(id="refresh-interval", interval=10 * 60 * 1000, n_intervals=0),
        dcc.Store(id="selected-city", data=KOTA_DEFAULT),

        html.Div(
            className="main-shell",
            children=[
                html.Div(
                    className="sidebar",
                    children=[
                        html.Div("W", className="sidebar-logo"),
                        html.Div("⌂", className="sidebar-icon active"),
                    ]
                ),

                html.Div(
                    className="dashboard-content",
                    children=[
                        html.Div(
                            className="topbar",
                            children=[
                                html.Div(
                                    className="search-box",
                                    children=[
                                        dcc.Input(
                                            id="city-input",
                                            type="text",
                                            placeholder="Cari kota...",
                                            value=KOTA_DEFAULT,
                                            className="search-input"
                                        ),
                                        html.Button("Cari", id="search-btn", className="search-btn")
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className="content-grid",
                            children=[
                                html.Div(
                                    className="left-column",
                                    children=[
                                        html.Div(id="main-weather-card"),
                                        html.Div(
                                            className="mini-cities-wrapper",
                                            children=[
                                                kartu_kota_kecil("Jakarta"),
                                                kartu_kota_kecil("Bandung"),
                                                kartu_kota_kecil("Yogyakarta"),
                                            ]
                                        )
                                    ]
                                ),

                                html.Div(
                                    className="center-column",
                                    children=[
                                        html.Div(id="forecast-card"),
                                        html.Div(
                                            className="chart-card",
                                            children=[
                                                html.Div(
                                                    className="card-header-row",
                                                    children=[
                                                        html.H3("Ringkasan", className="card-title")
                                                    ]
                                                ),
                                                dcc.Graph(
                                                    id="temp-chart",
                                                    config={
                                                        "displayModeBar": False,
                                                        "scrollZoom": True
                                                    },
                                                    className="chart-graph"
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                html.Div(
                                    className="right-column",
                                    children=[
                                        html.Div(
                                            className="map-card",
                                            children=[
                                                dcc.Graph(
                                                    id="weather-map",
                                                    config={
                                                        "displayModeBar": False,
                                                        "scrollZoom": True
                                                    },
                                                    className="map-graph"
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            "Peta bisa di-drag, di-zoom, dan marker bisa diklik.",
                                            className="map-info-card"
                                        ),
                                        html.Div(
                                            className="details-card",
                                            id="details-card"
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output("selected-city", "data"),
    Input("search-btn", "n_clicks"),
    State("city-input", "value"),
    prevent_initial_call=True
)
def update_kota(_, city_input):
    if city_input and city_input.strip():
        return city_input.strip()
    return KOTA_DEFAULT

@app.callback(
    Output("main-weather-card", "children"),
    Output("forecast-card", "children"),
    Output("temp-chart", "figure"),
    Output("weather-map", "figure"),
    Output("details-card", "children"),
    Input("selected-city", "data"),
    Input("refresh-interval", "n_intervals")
)
def refresh_dashboard(nama_kota, _):
    try:
        return bangun_dashboard(nama_kota)
    except Exception as e:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        error_box = html.Div(
            className="error-box",
            children=[
                html.H3("Data gagal dimuat"),
                html.P(str(e))
            ]
        )
        return error_box, error_box, empty_fig, empty_fig, error_box

if __name__ == "__main__":
    app.run(debug=True)