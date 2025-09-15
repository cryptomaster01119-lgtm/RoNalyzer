import requests
import re
import sys
import json
from datetime import datetime

HEADERS = {
    "User-Agent": "roblox-analyzer/1.0 (termux/replit/colab)",
    "Accept": "application/json"
}

def extrair_place_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    m = re.search(r"/games/(\d+)", s)
    if m:
        return m.group(1)
    if re.match(r"^\d+$", s):
        return s
    raise ValueError("Link inválido. Cole o link do jogo (ex: https://www.roblox.com/games/123456789/Name) ou só o PlaceID.")

def get_universe_id_from_place(place_id: str) -> str:
    url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    uni = data.get("universeId") or data.get("UniverseId") or data.get("UniverseID")
    if not uni:
        raise RuntimeError("Resposta sem universeId.")
    return str(uni)

def get_game_stats(universe_id: str) -> dict:
    url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json().get("data", [])
    if not data:
        raise RuntimeError("Resposta vazia do endpoint games.")
    g = data[0]
    return {
        "name": g.get("name"),
        "description": g.get("description"),
        "visits": int(g.get("visits") or 0),
        "playing": int(g.get("playing")) if g.get("playing") is not None else None,
        "maxPlayers": int(g.get("maxPlayers") or 0),
        "creator": g.get("creator", {}).get("name") or g.get("creator", {}).get("displayName"),
        "creator_type": g.get("creator", {}).get("type"),
        "creator_id": g.get("creator", {}).get("id") or g.get("creator", {}).get("targetId"),
        "favoritedCount": int(g.get("favoritedCount") or 0),
        "universeId": str(g.get("universeId") or universe_id),
        "rootPlaceId": g.get("rootPlaceId") or g.get("placeId") or None,
        "access": g.get("access"),
        "price": g.get("price"),
        "created": g.get("created") or g.get("createdAt") or None,
        "updated": g.get("updated") or g.get("updatedAt") or None,
        "id": g.get("id") or g.get("placeId") or None,
    }

def get_votes(universe_id: str) -> dict:
    url = f"https://games.roblox.com/v1/games/votes?universeIds={universe_id}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    payload = r.json()
    arr = payload.get("data") or payload.get("Data") or []
    if arr:
        rec = arr[0]
        return {
            "upVotes": int(rec.get("upVotes") or rec.get("upvoteCount") or 0),
            "downVotes": int(rec.get("downVotes") or rec.get("downvoteCount") or 0),
        }
    return {"upVotes": 0, "downVotes": 0}

def get_thumbnail(universe_id: str, size="150x150") -> str:
    url = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size={size}&format=png"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json().get("data", [])
    if data and isinstance(data, list) and data[0].get("imageUrl"):
        return data[0]["imageUrl"]
    return None

def safe_str(x):
    return str(x) if x is not None else "N/A"

def human_readable_date(s):
    if not s:
        return "N/A"
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            continue
    return s

def imprimir_detalhado(stats: dict, votes: dict, thumbnail_url: str, place_input: str, save_json=False, show_full_desc=False):
    name = stats.get("name") or "N/A"
    desc = stats.get("description") or "N/A"
    visits = stats.get("visits", 0) or 0
    playing = stats.get("playing")
    maxp = stats.get("maxPlayers", 0) or 0
    favs = stats.get("favoritedCount", 0) or 0
    up = votes.get("upVotes", 0)
    down = votes.get("downVotes", 0)
    created = human_readable_date(stats.get("created"))
    updated = human_readable_date(stats.get("updated"))
    uni = stats.get("universeId") or "N/A"
    root_place = stats.get("rootPlaceId") or "N/A"
    creator = stats.get("creator") or "N/A"
    creator_id = stats.get("creator_id") or "N/A"

    eng_rate_favs = (favs / visits * 100) if visits > 0 else 0.0
    eng_rate_likes = (up / visits * 100) if visits > 0 else 0.0
    likes_per_1k = (up / visits * 1000) if visits > 0 else 0.0
    up_ratio = (up / (up + down) * 100) if (up + down) > 0 else None
    occupancy = (playing / maxp * 100) if (playing is not None and maxp > 0) else None

    sep = "=" * 60
    print("\n" + sep)
    print("ROBLOX GAME ANALYZER — DETAILED REPORT")
    print(sep + "\n")

    print(f"Input PlaceID/URL: {place_input}")
    print(f"Name: {name}")
    if show_full_desc:
        print(f"Description: {desc}")
    else:
        print(f"Description: {desc[:400] + ('...' if len(desc) > 400 else '')}")
    print()
    print(f"Universe ID: {uni}")
    print(f"Root/Representative Place ID: {root_place}")
    print(f"Place/ID (from API): {safe_str(stats.get('id'))}")
    print(f"Creator: {creator} (id: {creator_id}, type: {safe_str(stats.get('creator_type'))})")
    print()
    print("— Dates —")
    print(f"Created: {created}")
    print(f"Last updated: {updated}")
    print()
    print("— Activity & Capacity —")
    print(f"Total visits: {visits:,}")
    print(f"Currently playing (CCU reported): {safe_str(playing)}")
    print(f"Max players (server cap): {maxp}")
    if occupancy is not None:
        print(f"Occupancy: {occupancy:.2f}% of max players")
    print()
    print("— Social / Feedback —")
    print(f"Favorites: {favs:,}")
    print(f"Likes (upVotes): {up:,}  Downvotes: {down:,}")
    if up_ratio is not None:
        print(f"Upvote ratio: {up_ratio:.2f}%")
    print(f"Engagement (favorites/visits): {eng_rate_favs:.4f}%")
    print(f"Engagement (likes/visits): {eng_rate_likes:.6f}%")
    print(f"Likes per 1k visits: {likes_per_1k:.6f}")
    print()
    print("— Misc —")
    print(f"Price (if any): {safe_str(stats.get('price'))}")
    print(f"Access type: {safe_str(stats.get('access'))}")
    if thumbnail_url:
        print(f"Thumbnail / Icon URL: {thumbnail_url}")
    else:
        print("Thumbnail: N/A")
    print("\n" + sep + "\n")

    if save_json:
        out = {
            "input": place_input,
            "universeId": uni,
            "rootPlaceId": root_place,
            "game": stats,
            "votes": votes,
            "thumbnail": thumbnail_url,
            "metrics": {
                "engagement_favorites_percent": eng_rate_favs,
                "engagement_likes_percent": eng_rate_likes,
                "likes_per_1000_visits": likes_per_1k,
                "occupancy_percent": occupancy,
            },
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
        fname = f"roblox_report_{uni}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"Relatório salvo como: {fname}")

def main():
    print("=== Roblox Game Analyzer (DETAILED) ===")
    inp = input("Cole o link do jogo Roblox (ou PlaceID): ").strip()
    try:
        place = extrair_place_id(inp)
    except ValueError as e:
        print("Erro:", e)
        sys.exit(1)

    try:
        universe = get_universe_id_from_place(place)
    except Exception as e:
        print("Falha ao obter universeId: ", e)
        print("Dica: verifique se 'apis.roblox.com' resolve na sua rede ou tente Replit/Colab/Wi-Fi.")
        sys.exit(1)

    try:
        stats = get_game_stats(universe)
    except Exception as e:
        print("Falha ao obter dados do jogo:", e)
        sys.exit(1)

    try:
        votes = get_votes(universe)
    except Exception:
        votes = {"upVotes": 0, "downVotes": 0}

    try:
        thumb = get_thumbnail(universe)
    except Exception:
        thumb = None

    try:
        show_full = input("Mostrar descrição completa? (y/N): ").strip().lower() in ("y", "yes")
        imprimir_detalhado(stats, votes, thumb, inp, save_json=False, show_full_desc=show_full)
        s = input("Deseja salvar um relatório JSON local? (s/N): ").strip().lower()
        if s in ("s", "y"):
            imprimir_detalhado(stats, votes, thumb, inp, save_json=True, show_full_desc=show_full)
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()
