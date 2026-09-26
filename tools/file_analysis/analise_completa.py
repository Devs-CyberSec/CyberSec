import os
import re
import json
import math
import hashlib
import mimetypes
import zipfile
import stat
import datetime
import tkinter as tk
from tkinter import filedialog

import pandas as pd

jan = tk.Tk()
jan.withdraw()

arq = filedialog.askopenfilename(title="Selecione um arquivo")

if not arq:
    print("Nenhum arquivo selecionado.")
    raise SystemExit

nm = os.path.basename(arq)
tam = os.path.getsize(arq)
ext = os.path.splitext(arq)[1].lower()
mime = mimetypes.guess_type(arq)[0]

with open(arq, "rb") as f:
    dados = f.read()

b = dados[:32]

tipos = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"GIF87a": "GIF",
    b"GIF89a": "GIF",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP/Container",
    b"MZ": "PE/EXE",
    b"\x7fELF": "ELF",
    b"\x1f\x8b": "GZIP",
    b"BM": "BMP",
    b"RIFF": "RIFF"
}

tipo = "Desconhecido"

for ass, nome in tipos.items():
    if b.startswith(ass):
        tipo = nome
        break

if tipo == "ZIP/Container":
    try:
        with zipfile.ZipFile(arq) as z:
            nomes = z.namelist()

            if "[Content_Types].xml" in nomes:
                if any(x.startswith("xl/") for x in nomes):
                    tipo = "XLSX"
                elif any(x.startswith("word/") for x in nomes):
                    tipo = "DOCX"
                elif any(x.startswith("ppt/") for x in nomes):
                    tipo = "PPTX"
    except zipfile.BadZipFile:
        tipo = "ZIP"

if tipo == "Desconhecido":
    try:
        txt = dados[:65536].decode("utf-8", errors="ignore").lower()

        if "<!doctype html" in txt or "<html" in txt:
            tipo = "HTML"
        elif ext == ".json":
            json.loads(dados.decode("utf-8"))
            tipo = "JSON"
        elif ext == ".csv":
            tipo = "CSV"
        elif ext in [".txt", ".log"]:
            tipo = "TXT"
    except Exception:
        pass

hashes = {
    "MD5": hashlib.md5(dados).hexdigest(),
    "SHA-1": hashlib.sha1(dados).hexdigest(),
    "SHA-256": hashlib.sha256(dados).hexdigest(),
    "SHA-512": hashlib.sha512(dados).hexdigest(),
    "SHA-3-256": hashlib.sha3_256(dados).hexdigest(),
    "BLAKE2b": hashlib.blake2b(dados).hexdigest()
}

freq = [0] * 256

for byte in dados:
    freq[byte] += 1

ent = 0

if tam:
    for qtd in freq:
        if qtd:
            p = qtd / tam
            ent -= p * math.log2(p)

ascii_str = re.findall(rb"[\x20-\x7e]{4,}", dados)
ascii_str = [x.decode("ascii", errors="ignore") for x in ascii_str]

urls = sorted(set(
    re.findall(
        rb"https?://[^\s\"'<>]+",
        dados
    )
))

urls = [x.decode("utf-8", errors="ignore") for x in urls]

ips = sorted(set(
    re.findall(
        rb"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        dados
    )
))

ips = [x.decode() for x in ips]

doms = sorted(set(
    re.findall(
        rb"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
        dados
    )
))

doms = [x.decode("utf-8", errors="ignore") for x in doms]

emails = sorted(set(
    re.findall(
        rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        dados
    )
))

emails = [x.decode("utf-8", errors="ignore") for x in emails]

perms = os.stat(arq)

perm_txt = stat.filemode(perms.st_mode)

criacao = datetime.datetime.fromtimestamp(
    os.path.getctime(arq)
).isoformat()

modificacao = datetime.datetime.fromtimestamp(
    os.path.getmtime(arq)
).isoformat()

acesso = datetime.datetime.fromtimestamp(
    os.path.getatime(arq)
).isoformat()

disfarce = ext not in ["", ".bin"] and mime is not None

ext_map = {
    ".exe": ["PE/EXE"],
    ".dll": ["PE/EXE"],
    ".png": ["PNG"],
    ".jpg": ["JPEG"],
    ".jpeg": ["JPEG"],
    ".gif": ["GIF"],
    ".pdf": ["PDF"],
    ".zip": ["ZIP/Container", "ZIP"],
    ".gz": ["GZIP"],
    ".xlsx": ["XLSX"],
    ".docx": ["DOCX"],
    ".pptx": ["PPTX"],
    ".html": ["HTML"],
    ".htm": ["HTML"],
    ".csv": ["CSV"],
    ".json": ["JSON"],
    ".txt": ["TXT"]
}

suspeito = False

if ext in ext_map:
    if tipo not in ext_map[ext]:
        suspeito = True

if tipo == "PE/EXE" and ext not in [".exe", ".dll", ".sys", ".scr", ".com"]:
    suspeito = True

if tipo == "PDF" and ext != ".pdf":
    suspeito = True

if tipo == "PNG" and ext not in [".png"]:
    suspeito = True

if tipo == "JPEG" and ext not in [".jpg", ".jpeg"]:
    suspeito = True

if tipo == "HTML" and ext not in [".html", ".htm"]:
    suspeito = True

csv_info = None

if tipo == "CSV":
    try:
        df = pd.read_csv(arq)

        csv_info = {
            "linhas": int(df.shape[0]),
            "colunas": int(df.shape[1]),
            "nomes_colunas": list(df.columns),
            "valores_nulos": int(df.isnull().sum().sum()),
            "duplicados": int(df.duplicated().sum()),
            "tipos": {
                str(k): str(v)
                for k, v in df.dtypes.items()
            },
            "estatisticas": df.describe(
                include="all"
            ).to_dict()
        }
    except Exception as e:
        csv_info = {
            "erro": str(e)
        }

excel_info = None

if tipo in ["XLSX", "XLS"]:
    try:
        df = pd.read_excel(arq)

        excel_info = {
            "linhas": int(df.shape[0]),
            "colunas": int(df.shape[1]),
            "nomes_colunas": list(df.columns),
            "valores_nulos": int(df.isnull().sum().sum()),
            "duplicados": int(df.duplicated().sum()),
            "tipos": {
                str(k): str(v)
                for k, v in df.dtypes.items()
            },
            "estatisticas": df.describe(
                include="all"
            ).to_dict()
        }
    except Exception as e:
        excel_info = {
            "erro": str(e)
        }

rel = {
    "arquivo": {
        "nome": nm,
        "caminho": arq,
        "tamanho_bytes": tam,
        "extensao": ext,
        "mime": mime,
        "tipo_real": tipo,
        "magic_bytes": b.hex(" ")
    },
    "hashes": hashes,
    "entropia": round(ent, 6),
    "strings": {
        "quantidade": len(ascii_str),
        "amostras": ascii_str[:200]
    },
    "rede": {
        "urls": urls,
        "ips": ips,
        "dominios": doms,
        "emails": emails
    },
    "permissoes": {
        "modo": perm_txt,
        "uid": perms.st_uid,
        "gid": perms.st_gid
    },
    "timestamps": {
        "criacao": criacao,
        "modificacao": modificacao,
        "ultimo_acesso": acesso
    },
    "deteccao": {
        "extensao_compativel": not suspeito,
        "possivel_arquivo_disfarçado": suspeito
    },
    "analise_dados": {
        "csv": csv_info,
        "excel": excel_info
    }
}

nome_rel = os.path.splitext(nm)[0] + "_relatorio.json"

with open(nome_rel, "w", encoding="utf-8") as f:
    json.dump(
        rel,
        f,
        indent=4,
        ensure_ascii=False,
        default=str
    )

print("\n=== SYBERSEC — ANÁLISE ===")
print("Nome:", nm)
print("Tamanho:", tam, "bytes")
print("Extensão:", ext)
print("MIME:", mime)
print("Tipo real:", tipo)
print("Magic Bytes:", b.hex(" "))

print("\n=== HASHES ===")

for nome, valor in hashes.items():
    print(nome + ":", valor)

print("\n=== ENTROPIA ===")
print(ent)

print("\n=== STRINGS ===")
print("Encontradas:", len(ascii_str))

print("\n=== REDE ===")
print("URLs:", len(urls))
print("IPs:", len(ips))
print("Domínios:", len(doms))
print("E-mails:", len(emails))

print("\n=== PERMISSÕES ===")
print(perm_txt)

print("\n=== TIMESTAMPS ===")
print("Criação:", criacao)
print("Modificação:", modificacao)
print("Acesso:", acesso)

print("\n=== DETECÇÃO ===")
print("Possível arquivo disfarçado:", suspeito)

if csv_info:
    print("\n=== ANÁLISE CSV ===")
    print("Linhas:", csv_info.get("linhas"))
    print("Colunas:", csv_info.get("colunas"))
    print("Nulos:", csv_info.get("valores_nulos"))
    print("Duplicados:", csv_info.get("duplicados"))

if excel_info:
    print("\n=== ANÁLISE EXCEL ===")
    print("Linhas:", excel_info.get("linhas"))
    print("Colunas:", excel_info.get("colunas"))
    print("Nulos:", excel_info.get("valores_nulos"))
    print("Duplicados:", excel_info.get("duplicados"))

print("\nRelatório salvo em:", nome_rel)
