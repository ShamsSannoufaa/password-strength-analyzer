import random
from pathlib import Path

import pandas as pd


COMMON_WEAK_PATTERNS = {
    "123456", "123456789", "12345678", "password", "qwerty", "abc123",
    "111111", "123123", "admin", "iloveyou", "000000", "1234"
}


def reservoir_sample_lines(file_path: str, k: int = 50000, encoding: str = "latin-1") -> list[str]:
    """
    Büyük dosyadan tümünü RAM'e almadan rastgele örnek seçer.
    Böylece ilk satırlara bağlı sampling bias azaltılır.
    """
    reservoir: list[str] = []
    path = Path(file_path)

    with path.open("r", encoding=encoding, errors="ignore") as f:
        for i, line in enumerate(f):
            item = line.strip()

            if not item:
                continue

            if len(reservoir) < k:
                reservoir.append(item)
            else:
                j = random.randint(0, i)
                if j < k:
                    reservoir[j] = item

    return reservoir


def load_txt_passwords(file_path: str, sample_size: int = 50000, encoding: str = "latin-1") -> pd.DataFrame:
    sampled = reservoir_sample_lines(file_path=file_path, k=sample_size, encoding=encoding)
    return pd.DataFrame({"password": sampled})


def clean_passwords(df: pd.DataFrame, max_len: int = 64) -> pd.DataFrame:
    """
    Basit veri temizleme:
    - boşları sil
    - çok uzun uç değerleri sil
    - tekrar eden parolaları sil
    """
    df = df.copy()

    df["password"] = df["password"].astype(str).str.strip()

    df = df[df["password"] != ""]
    df = df[df["password"].str.len() <= max_len]
    df = df.drop_duplicates(subset=["password"])

    return df.reset_index(drop=True)


def has_upper(pw: str) -> int:
    return int(any(c.isupper() for c in pw))


def has_lower(pw: str) -> int:
    return int(any(c.islower() for c in pw))


def has_digit(pw: str) -> int:
    return int(any(c.isdigit() for c in pw))


def has_special(pw: str) -> int:
    return int(any(not c.isalnum() for c in pw))


def char_variety(pw: str) -> int:
    """
    Kaç farklı karakter türü kullanıldığını hesaplar:
    - uppercase
    - lowercase
    - digit
    - special
    """
    variety = 0
    if any(c.islower() for c in pw):
        variety += 1
    if any(c.isupper() for c in pw):
        variety += 1
    if any(c.isdigit() for c in pw):
        variety += 1
    if any(not c.isalnum() for c in pw):
        variety += 1
    return variety


def label_password(pw: str) -> str:
    """
    Revize edilmiş rule-based etiketleme mantığı.

    Kural özeti:
    1. Çok kısa parolalar weak
    2. Bilinen yaygın zayıf parolalar weak
    3. Tek karakter türü kullanan parolalar weak
    4. 8 karakterden kısa parolalar weak
    5. 10+ karakter ve en az 3 karakter türü olan parolalar strong
    6. Geri kalanlar medium
    """
    length = len(pw)
    variety = char_variety(pw)
    lower_pw = pw.lower()

    # 1. Bilinen zayıf patternler
    if lower_pw in COMMON_WEAK_PATTERNS:
        return "weak"

    # 2. Çok kısa
    if length < 6:
        return "weak"

    # 3. Tek karakter türü
    if variety == 1:
        return "weak"

    # 4. Kısa parolalar
    if length < 8:
        return "weak"

    # 5. Güçlü sınıf
    if length >= 10 and variety >= 3:
        return "strong"

    # 6. Diğerleri
    return "medium"


def build_combined_dataset(
    rockyou_path: str,
    strong_path: str,
    rockyou_sample: int = 50000,
    strong_sample: int = 20000
) -> pd.DataFrame:
    """
    RockYou + strong dataset birleştirilir.

    RockYou:
        rule-based label uygulanır
    Strong dataset:
        doğrudan strong etiketi verilir
    """
    # RockYou
    rockyou_df = load_txt_passwords(
        rockyou_path,
        sample_size=rockyou_sample,
        encoding="latin-1"
    )
    rockyou_df = clean_passwords(rockyou_df)
    rockyou_df["label"] = rockyou_df["password"].apply(label_password)

    # Strong dataset
    strong_df = load_txt_passwords(
        strong_path,
        sample_size=strong_sample,
        encoding="utf-8"
    )
    strong_df = clean_passwords(strong_df)
    strong_df["label"] = "strong"

    # Birleştir
    df = pd.concat([rockyou_df, strong_df], ignore_index=True)

    # Aynı parola iki tarafta varsa son etiketi koru
    df = df.drop_duplicates(subset=["password"], keep="last").reset_index(drop=True)

    return df