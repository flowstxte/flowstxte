import os
import re
import sys
import traceback
import urllib.request

KOMAREV_URL = "https://komarev.com/ghpvc/?username=flowstxte"
FALLBACK_FILE = os.path.join(os.path.dirname(__file__), "last_views.txt")
DEFAULT_COUNT = "1,942"

def fetch_count():
    try:
        req = urllib.request.Request(
            KOMAREV_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            matches = re.findall(r"<text[^>]*>([\d,]+)</text>", content)
            if matches:
                # The count is typically the last text tag in komarev's SVG
                count = matches[-1].strip()
                if count:
                    try:
                        with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
                            f.write(count)
                    except Exception:
                        pass
                    return count
    except Exception as e:
        print(f"[Warning] Failed to fetch latest views from komarev: {e}")

    # Fallback to cached file
    if os.path.exists(FALLBACK_FILE):
        try:
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                cached = f.read().strip()
                if cached:
                    return cached
        except Exception:
            pass

    return DEFAULT_COUNT

def generate_svg(count_str):
    label = "PROFILE VIEWS"
    # Dynamic calculation of widths
    count_chars = len(count_str)
    count_width = max(52, count_chars * 9 + 18)
    label_width = 114
    total_width = label_width + count_width
    height = 24
    split_pct = round((label_width / total_width) * 100, 1)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}" viewBox="0 0 {total_width} {height}" role="img" aria-label="{label}: {count_str}">
  <title>{label}: {count_str}</title>
  <defs>
    <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2a2a2a"/>
      <stop offset="{split_pct}%" stop-color="#2a2a2a"/>
      <stop offset="{split_pct}%" stop-color="#F25623"/>
      <stop offset="100%" stop-color="#F25623"/>
    </linearGradient>
  </defs>

  <!-- Profile Views (Left) Background -->
  <rect width="{label_width}" height="{height}" fill="#121212"/>

  <!-- Count (Right) Background -->
  <rect x="{label_width}" width="{count_width}" height="{height}" fill="#F25623"/>

  <!-- Gloss Overlay -->
  <rect width="{total_width}" height="{height}" fill="url(#gloss)"/>

  <!-- Outer Border -->
  <rect x="0.5" y="0.5" width="{total_width - 1}" height="{height - 1}" fill="none" stroke="url(#border-grad)" stroke-width="1"/>

  <!-- Minimal Eye / Radar Icon -->
  <g transform="translate(9, 5)" fill="#F25623">
    <path d="M7 1.5C3.8 1.5 1 3.8 0 7c1 3.2 3.8 5.5 7 5.5s6-2.3 7-5.5c-1-3.2-3.8-5.5-7-5.5zm0 9.2A3.7 3.7 0 1 1 7 3.3a3.7 3.7 0 0 1 0 7.4zm0-5.8A2.1 2.1 0 1 0 7 9.1 2.1 2.1 0 0 0 7 4.9z"/>
  </g>

  <!-- Text Labels -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="10" font-weight="600" letter-spacing="0.8">
    <text x="31" y="15.5" fill="#ffffff">{label}</text>
    <text x="{label_width + count_width / 2}" y="15.5" fill="#ffffff" font-weight="700" text-anchor="middle">{count_str}</text>
  </g>
</svg>"""

def main():
    try:
        out_dir = sys.argv[1] if len(sys.argv) > 1 else "./dist"
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "profile-views.svg")

        count = fetch_count()
        svg = generate_svg(count)

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[Success] Generated profile-views.svg with count '{count}' -> {out_file}")
    except Exception as e:
        print(f"[Error] Failed to generate SVG badge: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
