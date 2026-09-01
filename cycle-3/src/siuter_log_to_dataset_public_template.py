# PUBLIC-SAFE ADAPTER
# This file is a sanitized release template derived from the research converter.
# It is NOT a verbatim copy of the private institutional data-preparation script.
# Raw institutional logs and respondent-sensitive data are excluded from the repository.

"""
ER-CyRIS Siklus 2 — Konversi Log SIUTER ke Dataset
====================================================
Input  : laravel.log dari SIAKAD SIUTER Universitas Sebelas April
Output : siuter_dataset.csv — dataset terstruktur, anonim, siap dipakai
         siuter_anomaly_summary.txt — ringkasan labeling anomali

Catatan privasi:
  - Email    → SHA256 hash (domain dipertahankan terpisah)
  - Nama     → DIHAPUS
  - Token OAuth → DIHAPUS
  - No. HP   → DIHAPUS
  - NIM      → SHA256 hash
  - Google user_id → SHA256 hash
  - IP address     → hashed by default in this public-safe adapter
  - session_id     → use only within controlled research environment

Kolom output (38 kolom):
  timestamp, log_level, event_type, event_category,
  user_email_hash, user_domain, user_domain_type, role,
  session_id, user_id_hash, nim_hash,
  ip_address, id_fakultas, semester_aktif,
  redirect_url, url_path, url_module,
  hour, minute, day_of_week, day_name, is_weekend, is_off_hours,
  is_error, error_class, has_context,
  session_events_per_hour (TOS fitur),
  anomaly_label, anomaly_reason
"""

import re
import json
import hashlib
import pandas as pd
from datetime import datetime
from collections import defaultdict
import sys
import os

# ─── Konfigurasi ─────────────────────────────────────────────────────
LOG_PATH     = os.environ.get("ERCYRIS_LOG_PATH", "")
OUT_DATASET  = os.environ.get("ERCYRIS_OUT_DATASET", "siuter_dataset_public.csv")
OUT_SUMMARY  = os.environ.get("ERCYRIS_OUT_SUMMARY", "siuter_anomaly_summary_public.txt")

# Public release: never hard-code a hashing secret in source control.
SALT = os.environ.get("ERCYRIS_HASH_SALT", "")
STORE_RAW_IP = os.environ.get("ERCYRIS_STORE_RAW_IP", "false").lower() == "true"


# ─── Pola regex ──────────────────────────────────────────────────────
LOG_HEADER = re.compile(
    r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] '
    r'(\w+)\.(\w+): '
    r'(.+?)(?=\s*\{|\s*$)'
)
JSON_BODY  = re.compile(r'(\{.*\})\s*$', re.DOTALL)

# Peta event_type → kategori
EVENT_CATEGORY = {
    "Google OAuth Redirect Initiated":          "auth_attempt",
    "Google OAuth Callback Success - Full User Data": "auth_success",
    "Storing avatar in session":                "auth_success",
    "Login session check":                      "session",
    "Final redirect URL":                       "session",
    "Dashboard session data":                   "session",
    "Avatar data for dashboard":                "session",
    "Avatar key missing from session data and database, using null": "session",
    "getDataAkun called":                       "data_access",
    "KrsService: getPeriodStatus Check":        "academic_access",
    "KRS Period Ad-Hoc Debug":                  "academic_access",
    "SiakadHelper: Raw Riwayat found":          "academic_access",
    "SiakadHelper: Final Active Data":          "academic_access",
    "AkunSiuter count":                         "system_info",
    "Watzap Image Message berhasil":            "notification",
    "WhatsApp message sent successfully":       "notification",
    "Google OAuth Error":                       "auth_error",
    "Login Auth Error":                         "auth_error",
}

# Aturan anomaly labeling — RULE-BASED (tidak ada ground truth)
ANOMALY_RULES = {
    # Level ERROR → suspect
    "ERROR": ("error_event", 1),
    # Event auth error → anomali
    "auth_error": ("auth_failure", 1),
    # Event khusus anomali
    "Google OAuth Error": ("oauth_error", 1),
    "Login Auth Error": ("login_auth_error", 1),
    "Attempt to read property \"nim\" on null": ("null_property_access", 1),
}

# Off-hours: 00:00–05:59
OFF_HOURS = set(range(0, 6))

# ─── Helper functions ─────────────────────────────────────────────────

def sha256(value: str) -> str:
    if not SALT:
        raise RuntimeError("Set ERCYRIS_HASH_SALT in the execution environment before converting institutional identifiers.")
    """Hash nilai PII dengan salt."""
    if not value or value in ("null", "None", ""):
        return ""
    return hashlib.sha256(f"{SALT}:{value}".encode()).hexdigest()[:16]

def extract_domain(email: str) -> tuple:
    """Ekstrak domain dan tipe domain dari email."""
    if not email or "@" not in email:
        return "", "unknown"
    domain = email.split("@")[1].lower()
    if "student.unsap.ac.id" in domain:
        return domain, "student"
    elif "unsap.ac.id" in domain:
        return domain, "staff"
    else:
        return domain, "external"

def extract_url_module(url: str) -> str:
    """Ekstrak modul dari URL SIUTER."""
    if not url:
        return ""
    # Hapus domain, ambil path pertama
    path = re.sub(r"https?://[^/]+", "", url)
    parts = [p for p in path.split("/") if p]
    if not parts:
        return "root"
    # Normalisasi: /mhs/dashboard → module=mhs, /admin/... → admin
    module_map = {
        "mhs": "mahasiswa", "dosen": "dosen", "admin": "admin",
        "auth": "auth", "krs": "krs", "nilai": "nilai",
        "jadwal": "jadwal", "akademik": "akademik",
        "fakultas": "fakultas", "oauth": "oauth",
    }
    first = parts[0].lower()
    return module_map.get(first, first[:20])

def parse_log_entry(line: str, json_lines: str) -> dict | None:
    """Parse satu log entry + baris JSON-nya menjadi dict."""
    m = LOG_HEADER.match(line)
    if not m:
        return None

    ts_str, env, level, msg = m.groups()
    msg = msg.strip()

    # Parse JSON context
    ctx = {}
    full_text = line + " " + json_lines
    jm = JSON_BODY.search(full_text)
    if jm:
        try:
            ctx = json.loads(jm.group(1))
        except json.JSONDecodeError:
            pass

    return {
        "ts_str":  ts_str,
        "env":     env,
        "level":   level,
        "msg":     msg,
        "ctx":     ctx,
    }

def determine_anomaly(level: str, event_type: str,
                      event_category: str, hour: int,
                      is_error: bool) -> tuple:
    """Tentukan label dan alasan anomali berbasis aturan."""
    # Rule 1: ERROR level
    if level == "ERROR":
        # Auth error → anomali
        if "auth_error" in event_category or "auth" in event_type.lower():
            return 1, "auth_error_event"
        # DB error bisa jadi probe
        if "SQLSTATE" in event_type:
            return 1, "db_error_suspicious"
        # Error lain
        return 1, "error_level"

    # Rule 2: Auth failure events
    if event_category == "auth_error":
        return 1, "auth_failure"

    # Rule 3: Off-hours dengan aktivitas tidak normal
    if hour in OFF_HOURS and event_category in ("auth_attempt", "data_access"):
        return 1, "offhours_access"

    # Rule 4: Akses data sensitif di luar jam kerja
    if hour in OFF_HOURS and "admin" in event_type.lower():
        return 1, "offhours_admin"

    # Rule 5: WARNING level
    if level == "WARNING":
        return 1, "warning_level"

    # Normal
    return 0, ""


# ─── MAIN PARSER ──────────────────────────────────────────────────────

def parse_log(log_path: str) -> list:
    """Parse seluruh log file, gabungkan multi-line entries."""
    records = []
    current_line = ""
    current_json_lines = []
    total = 0

    print(f"[INFO] Membaca {log_path} ...")

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            if raw.startswith("[20"):
                # Proses entry sebelumnya
                if current_line:
                    e = parse_log_entry(current_line,
                                        " ".join(current_json_lines))
                    if e:
                        records.append(e)
                        total += 1
                        if total % 50000 == 0:
                            print(f"  ... parsed {total:,} entries")
                current_line = raw.rstrip()
                current_json_lines = []
            else:
                current_json_lines.append(raw.rstrip())

    # Entry terakhir
    if current_line:
        e = parse_log_entry(current_line, " ".join(current_json_lines))
        if e:
            records.append(e)

    print(f"[OK] Total entries parsed: {len(records):,}")
    return records


# ─── FEATURE ENGINEERING ──────────────────────────────────────────────

def build_dataset(records: list) -> pd.DataFrame:
    """Ubah list parsed entries menjadi DataFrame terstruktur + features."""
    rows = []

    # Pre-pass: hitung event per session untuk TOS (sederhana)
    session_hourly = defaultdict(int)
    ip_hour_count  = defaultdict(int)

    print("[INFO] Menghitung pre-pass features ...")
    for e in records:
        ts = None
        try:
            ts = datetime.strptime(e["ts_str"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
        ctx = e["ctx"]
        # Session events per (session_id, tanggal+jam)
        sid = ctx.get("session_id", "")
        ip  = ctx.get("user_ip", "")
        if ts and sid:
            key = (sid, ts.strftime("%Y-%m-%d %H"))
            session_hourly[key] += 1
        if ts and ip:
            key2 = (ip, ts.strftime("%Y-%m-%d %H"))
            ip_hour_count[key2] += 1

    print("[INFO] Membangun dataset ...")
    for e in records:
        ts = None
        try:
            ts = datetime.strptime(e["ts_str"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

        level        = e["level"].upper()
        msg          = e["msg"]
        ctx          = e["ctx"]
        is_error     = (level in ("ERROR", "EMERGENCY"))

        # Normalisasi event_type
        event_type = msg[:100]
        event_category = EVENT_CATEGORY.get(msg, "other")
        if is_error:
            event_category = "error"

        # ── Ekstrak field dari context ───────────────────────────────
        # User info (dari Dashboard session atau OAuth Callback)
        user_data = ctx.get("siuter_user_data", {})
        email_raw  = (user_data.get("email") or
                      ctx.get("user_email") or "")
        role       = (user_data.get("role") or
                      ctx.get("role") or "")
        status     = user_data.get("status", "")
        nim_raw    = (user_data.get("nim") or ctx.get("nim") or "")
        nuptk      = user_data.get("nuptk")  # null untuk mahasiswa
        user_id_raw= ctx.get("user_id", "")
        session_id = ctx.get("session_id", "")
        ip_address = ctx.get("user_ip", "")
        id_fakultas= ctx.get("id_fakultas") or ctx.get("id_fakultas_resolved","")
        semester   = ctx.get("semester_aktif", "")
        period_src = ctx.get("period_source", "")

        # URL
        url_raw   = ctx.get("url", "")
        url_path  = re.sub(r"https?://[^/]+", "", url_raw) if url_raw else ""
        url_module= extract_url_module(url_raw)

        # Error class
        error_cls = ""
        if is_error:
            em = re.search(r'\(([A-Za-z\\]+Exception|[A-Za-z]+Error)[^)]*\)',
                           msg)
            if em:
                error_cls = em.group(1).split("\\")[-1]
            elif "SQLSTATE" in msg:
                error_cls = "SqlStateError"
            else:
                error_cls = "GenericError"

        # ── Anonimisasi PII ──────────────────────────────────────────
        domain, domain_type = extract_domain(email_raw)
        email_hash   = sha256(email_raw)
        nim_hash     = sha256(nim_raw) if nim_raw else ""
        user_id_hash = sha256(user_id_raw) if user_id_raw else ""
        # Token OAuth TIDAK disimpan sama sekali
        # Nama pengguna TIDAK disimpan
        # No. HP TIDAK disimpan

        # ── Temporal features ────────────────────────────────────────
        hour     = ts.hour        if ts else -1
        minute   = ts.minute      if ts else -1
        dow      = ts.weekday()   if ts else -1  # 0=Senin
        day_name = ts.strftime("%A") if ts else ""
        is_weekend  = int(dow in (5, 6)) if ts else -1
        is_off_hours = int(hour in OFF_HOURS) if ts else -1

        # ── TOS features (sederhana) ─────────────────────────────────
        sess_events_hr = 0
        ip_events_hr   = 0
        if ts and session_id:
            sess_events_hr = session_hourly.get(
                (session_id, ts.strftime("%Y-%m-%d %H")), 0)
        if ts and ip_address:
            ip_events_hr = ip_hour_count.get(
                (ip_address, ts.strftime("%Y-%m-%d %H")), 0)

        # ── Anomaly labeling ─────────────────────────────────────────
        anomaly_label, anomaly_reason = determine_anomaly(
            level, event_type, event_category, hour, is_error
        )

        # Rule: banyak OAuth redirect dari IP sama dalam 1 jam > 10
        if ip_events_hr > 10 and "OAuth Redirect" in event_type:
            anomaly_label = 1
            anomaly_reason = f"ip_burst_{ip_events_hr}_per_hour"

        rows.append({
            # ── Identitas log ────────────────────────────────────────
            "timestamp":          e["ts_str"],
            "log_level":          level,
            "event_type":         event_type,
            "event_category":     event_category,
            # ── User (anonim) ────────────────────────────────────────
            "user_email_hash":    email_hash,
            "user_domain":        domain,
            "user_domain_type":   domain_type,   # student/staff/external
            "role":               role,
            "status":             status,
            "session_id":         session_id,
            "user_id_hash":       user_id_hash,
            "nim_hash":           nim_hash,
            "is_dosen":           int(nuptk is not None and nuptk != ""),
            # ── Network ──────────────────────────────────────────────
            "ip_address":         ip_address if STORE_RAW_IP else sha256(ip_address),
            # ── Akademik ─────────────────────────────────────────────
            "id_fakultas":        id_fakultas,
            "semester_aktif":     semester,
            "period_source":      period_src,
            # ── URL ──────────────────────────────────────────────────
            "url_path":           url_path,
            "url_module":         url_module,
            # ── Temporal ─────────────────────────────────────────────
            "hour":               hour,
            "minute":             minute,
            "day_of_week":        dow,
            "day_name":           day_name,
            "is_weekend":         is_weekend,
            "is_off_hours":       is_off_hours,
            # ── Error ────────────────────────────────────────────────
            "is_error":           int(is_error),
            "error_class":        error_cls,
            "has_context":        int(bool(ctx)),
            # ── TOS (awal, akan diperkaya di Komponen B) ─────────────
            "sess_events_per_hour": sess_events_hr,
            "ip_events_per_hour":   ip_events_hr,
            # ── Label ────────────────────────────────────────────────
            "anomaly_label":      anomaly_label,
            "anomaly_reason":     anomaly_reason,
        })

    df = pd.DataFrame(rows)
    return df


# ─── RINGKASAN DATASET ────────────────────────────────────────────────

def write_summary(df: pd.DataFrame, out_path: str):
    lines = []
    lines.append("=" * 60)
    lines.append("RINGKASAN DATASET LOG SIUTER — ER-CyRIS Siklus 2")
    lines.append("=" * 60)
    lines.append(f"\nTotal records   : {len(df):,}")
    lines.append(f"Rentang waktu   : {df['timestamp'].min()} s.d. {df['timestamp'].max()}")
    lines.append(f"Kolom           : {len(df.columns)}")

    lines.append("\n── Distribusi Log Level ──")
    for lvl, cnt in df['log_level'].value_counts().items():
        lines.append(f"  {lvl:<15} {cnt:>8,}  ({100*cnt/len(df):.1f}%)")

    lines.append("\n── Distribusi Event Category ──")
    for cat, cnt in df['event_category'].value_counts().head(15).items():
        lines.append(f"  {cat:<30} {cnt:>8,}")

    lines.append("\n── Distribusi Role Pengguna ──")
    role_df = df[df['role'] != '']['role'].value_counts()
    for role, cnt in role_df.items():
        lines.append(f"  {role:<20} {cnt:>8,}")

    lines.append("\n── Distribusi Domain Email ──")
    for dt, cnt in df[df['user_domain_type']!='']['user_domain_type'].value_counts().items():
        lines.append(f"  {dt:<20} {cnt:>8,}")

    lines.append("\n── Distribusi Anomaly Label ──")
    for lbl, cnt in df['anomaly_label'].value_counts().items():
        pct = 100*cnt/len(df)
        lines.append(f"  label={lbl}  {cnt:>8,}  ({pct:.2f}%)")

    lines.append("\n── Top Anomaly Reasons ──")
    reasons = df[df['anomaly_label']==1]['anomaly_reason'].value_counts()
    for r, cnt in reasons.head(10).items():
        lines.append(f"  {r:<35} {cnt:>7,}")

    lines.append("\n── Top 10 Event Types (label=1) ──")
    top_anom = df[df['anomaly_label']==1]['event_type'].value_counts().head(10)
    for et, cnt in top_anom.items():
        lines.append(f"  {et[:55]:<55} {cnt:>7,}")

    lines.append("\n── Distribusi Akses per Jam (Off-hours 00-05) ──")
    hour_dist = df.groupby('hour')['anomaly_label'].agg(['sum','count'])
    hour_dist.columns = ['anomali', 'total']
    for h, row in hour_dist.iterrows():
        bar = "█" * min(int(row['total']/2000), 30)
        flag = " ← OFF HOURS" if int(h) in OFF_HOURS else ""
        lines.append(
            f"  Jam {h:02d}  total={row['total']:>7,}  "
            f"anomali={row['anomali']:>5,}  {bar}{flag}"
        )

    lines.append("\n── Unique Users & Sessions ──")
    n_users    = df[df['user_email_hash']!='']['user_email_hash'].nunique()
    n_sessions = df[df['session_id']!='']['session_id'].nunique()
    n_ips      = df[df['ip_address']!='']['ip_address'].nunique()
    lines.append(f"  Unique users (hash) : {n_users:,}")
    lines.append(f"  Unique sessions     : {n_sessions:,}")
    lines.append(f"  Unique IP addresses : {n_ips:,}")

    lines.append("\n── Catatan Privasi ──")
    lines.append("  ✓ Email       → SHA256 hash (16 char), domain dipertahankan")
    lines.append("  ✓ Nama        → DIHAPUS dari dataset")
    lines.append("  ✓ Token OAuth → DIHAPUS dari dataset")
    lines.append("  ✓ No. HP      → DIHAPUS dari dataset")
    lines.append("  ✓ NIM         → SHA256 hash")
    lines.append("  ✓ Google ID   → SHA256 hash")
    lines.append("  ✓ IP address  → dipertahankan (diperlukan deteksi anomali)")

    lines.append("\n── Kolom Dataset (untuk Komponen A & B ER-CyRIS) ──")
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        lines.append(f"  {col:<30} {dtype:<10} non-null={non_null:,}")

    lines.append("\n" + "=" * 60)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Summary saved → {out_path}")


# ─── ENTRY POINT ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ER-CyRIS Siklus 2 — SIUTER Log Converter")
    print("=" * 50)

    # 1. Parse log
    records = parse_log(LOG_PATH)

    # 2. Build dataset
    df = build_dataset(records)

    print(f"\n[INFO] Dataset shape: {df.shape}")
    print(f"[INFO] Kolom: {list(df.columns)}")

    # 3. Simpan CSV
    df.to_csv(OUT_DATASET, index=False, encoding="utf-8")
    print(f"[OK] Dataset saved → {OUT_DATASET}")
    print(f"     Ukuran: {df.shape[0]:,} baris × {df.shape[1]} kolom")

    # 4. Ringkasan
    write_summary(df, OUT_SUMMARY)

    # 5. Preview
    print("\n── Preview 5 baris pertama ──")
    preview_cols = [
        "timestamp","log_level","event_type",
        "user_domain_type","role","hour","is_off_hours",
        "is_error","anomaly_label","anomaly_reason"
    ]
    print(df[preview_cols].head().to_string())

    print("\n── Distribusi label ──")
    print(df['anomaly_label'].value_counts())

    print("\n[SELESAI] Konversi log SIUTER ke dataset berhasil.")
