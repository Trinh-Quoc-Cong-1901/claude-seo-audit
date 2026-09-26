# Hướng dẫn sử dụng Claude SEO (tiếng Việt)

Tài liệu này dành cho người dùng nội bộ. Phần 1 hướng dẫn viết báo cáo audit SEO.
Phần 2 là luồng làm việc khuyến nghị. Phần 3 là các cách chạy Claude SEO khác. Danh sách lệnh đầy đủ (tiếng Anh) nằm ở
[`docs/COMMANDS.md`](docs/COMMANDS.md).

---

## 0. Chuẩn bị (làm một lần)

**Cài Claude SEO**

Cách 1, cài dạng plugin (khuyên dùng). Gõ trong Claude Code:

```
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
/seo setup
```

Cách 2, cài thủ công từ thư mục repo này:

```bash
cd ~/Desktop/claude-seo
bash install.sh
```

**Kiểm tra cài đặt**

```
/seo doctor
```

Lệnh này chỉ đọc, không sửa gì. Nếu báo thiếu Python package hoặc Chromium, chạy lại `/seo setup`.

**Công cụ cần có trên máy**

- Python 3.10 trở lên
- Node.js (để chạy Lighthouse qua `npx`)
- Google Chrome (Lighthouse dùng Chrome headless)
- `curl`

---

## 1. Viết báo cáo audit SEO

Có hai loại báo cáo. Chọn theo mục đích:

| Loại | Dùng khi | Kết quả |
|---|---|---|
| **Báo cáo public (web)** | Gửi khách hàng, gửi link | Trang web trên claude.ai, tiếng Việt, có link chia sẻ |
| **Báo cáo PDF** | Cần file đính kèm, có dữ liệu Google (GSC, GA4, CrUX) | File PDF khổ A4 (và HTML/XLSX nếu cần) |

### 1.1. Báo cáo public (web, tiếng Việt)

Đây là mẫu báo cáo đã dùng cho Tolariz, Đại Hồng Phát, Toyota Thái Hòa.

**Cách chạy.** Gõ một trong các câu sau trong Claude Code:

```
/seo-audit-public tenmien.vn
```

hoặc nói tự nhiên:

```
site audit tenmien.vn
viết báo cáo audit public cho tenmien.vn
```

**Claude sẽ làm các bước sau:**

1. Kiểm tra trang chủ: status, TTFB, header, `robots.txt`, redirect http/www, `llms.txt`,
   title, meta, canonical, H1/H2, JSON-LD, số điện thoại.
2. Đọc sitemap, lập danh sách URL, đánh dấu URL rác (trang test, giỏ hàng, template…).
3. Crawl toàn bộ URL trong sitemap, rồi crawl thêm các link nội bộ không có trong sitemap.
4. Kiểm tra chuyên sâu theo loại site: schema sản phẩm, NAP/LocalBusiness, trang trùng lặp,
   nội dung YMYL, hreflang cho site đa ngôn ngữ.
5. Đo hiệu năng bằng Lighthouse trên 2–3 loại trang (trang chủ, sản phẩm/dịch vụ, bài viết).
6. Chấm điểm theo trọng số:

   | Hạng mục | Trọng số |
   |---|---|
   | Kỹ thuật | 22% |
   | Nội dung | 23% |
   | On-page | 20% |
   | Schema | 10% |
   | Hiệu năng | 10% |
   | AI Search | 10% |
   | Hình ảnh | 5% |

   Màu điểm: từ 70 trở lên là xanh, 50–69 là vàng, dưới 50 là đỏ.
7. Viết báo cáo và đăng lên claude.ai dưới dạng Artifact.

**Cấu trúc báo cáo:**

- Trang bìa: tên miền, doanh nghiệp, loại hình, nền tảng, ngày kiểm tra, điểm tổng.
- Tóm tắt: 4 chỉ số chính, biểu đồ điểm từng hạng mục, 5 vấn đề nghiêm trọng nhất,
  5 việc làm nhanh có hiệu quả cao.
- Một phần cho mỗi hạng mục: điểm làm tốt (✓), các lỗi theo mức độ
  (nghiêm trọng / cao / trung bình / thấp), kèm bằng chứng và "Cách sửa".
- Bảng Lighthouse.
- Kế hoạch hành động 4 giai đoạn: Tuần 1, Tuần 2–3, Tháng 2, Liên tục.
- Phương pháp và giới hạn của báo cáo.

**Sau khi có link:**

Artifact mới tạo ở chế độ riêng tư. Mở link, bấm **Share → Anyone with the link** để khách xem được.

**Quy tắc của báo cáo public:**

- Không nhắc tới "Claude" hay "Claude SEO" ở bất kỳ đâu trong báo cáo.
- Mọi con số phải lấy từ dữ liệu đo được. Điều gì không kiểm chứng được thì bỏ hoặc viết nhẹ lại.
- File tạm nằm trong thư mục scratchpad của phiên làm việc, không lưu vào repo.

**File của skill** (nằm ngoài repo, ở máy của bạn):

```
~/.claude/skills/seo-audit-public/
  SKILL.md             # Quy trình và quy tắc
  template-head.html   # CSS của báo cáo (không sửa khi viết báo cáo)
  example-body.html    # Mẫu nội dung
  crawl.py             # Script crawl danh sách URL
```

Muốn crawl thủ công một danh sách URL:

```bash
python3 ~/.claude/skills/seo-audit-public/crawl.py urls.txt crawl.json
```

**Mẹo:**

- API PageSpeed hay hết quota. Skill dùng Lighthouse chạy trên máy thay thế:

  ```bash
  npx -y lighthouse@12 https://tenmien.vn --quiet --chrome-flags="--headless=new" \
    --output=json --output-path=lh_home.json \
    --only-categories=performance,seo,accessibility,best-practices
  ```

- Muốn sửa báo cáo đã đăng, dán link artifact vào Claude và nói cần sửa gì. Link giữ nguyên.

### 1.2. Báo cáo PDF (dữ liệu Google)

Dùng khi đã kết nối Google API (Search Console, GA4, PageSpeed, CrUX).

**Bước 1. Cài đặt kết nối Google (một lần):**

```
/seo google setup
```

Cấp độ kết nối:

| Cấp | Cần gì | Mở khóa |
|---|---|---|
| Tier 0 | API key | PageSpeed, CrUX, CrUX History |
| Tier 1 | + OAuth hoặc Service Account | Search Console, URL Inspection |
| Tier 2 | + GA4 property | Lượt truy cập tự nhiên từ GA4 |
| Tier 3 | + Google Ads developer token | Keyword Planner |

File cấu hình nằm ở `~/.config/claude-seo/google-api.json`. Không commit file này lên git.

**Bước 2. Tạo báo cáo:**

```
/seo google report full               # Báo cáo đầy đủ
/seo google report cwv-audit          # Core Web Vitals
/seo google report gsc-performance    # Hiệu suất tìm kiếm (GSC)
/seo google report indexation         # Tình trạng index
```

**Chạy trực tiếp bằng script** (khi đã có file JSON dữ liệu):

```bash
python3 scripts/google_report.py --type full --data data.json \
  --domain tenmien.vn --format all --output-dir ./out/tenmien.vn
```

- `--type`: `cwv-audit`, `gsc-performance`, `indexation`, `full`
- `--format`: `pdf` (mặc định), `html`, `xlsx`, `both` (pdf+html), `all` (pdf+html+xlsx)

Script tự kiểm tra PDF sau khi tạo. Chỉ gửi PDF cho khách khi kết quả kiểm tra là `"status": "PASS"`.

Sau mỗi lệnh phân tích (`audit`, `page`, `technical`…), Claude sẽ hỏi có muốn tạo PDF không.

---

## 2. Luồng khuyến nghị cho một site mới

Chạy theo thứ tự sau:

1. `/seo audit https://tenmien.vn`: có cái nhìn tổng quan và danh sách vấn đề cần ưu tiên.
2. `/seo technical https://tenmien.vn`: sửa các lỗi chặn index trước tiên.
3. `/seo google pagespeed https://tenmien.vn`: lấy số liệu tốc độ thật.
4. `/seo google report full`: xuất PDF để gửi khách hàng hoặc team.
5. `/seo drift baseline https://tenmien.vn`: chốt mốc hiện tại để theo dõi về sau.

---

## 3. Các cách chạy Claude SEO khác

Tất cả lệnh gõ trong Claude Code, bắt đầu bằng `/seo`. Thay `https://tenmien.vn` bằng trang cần kiểm tra.

### 3.1. Audit và phân tích trang

| Lệnh | Làm gì |
|---|---|
| `/seo audit https://tenmien.vn` | Audit toàn site, chạy tối đa 15 agent song song, crawl tới 500 trang. Kết quả: `FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md` |
| `/seo page https://tenmien.vn/trang` | Phân tích sâu một trang |
| `/seo technical https://tenmien.vn` | SEO kỹ thuật: crawl, index, bảo mật, URL, mobile, Core Web Vitals, JS… |
| `/seo content https://tenmien.vn/bai-viet` | Chất lượng nội dung, E-E-A-T |
| `/seo schema https://tenmien.vn` | Kiểm tra và tạo schema JSON-LD |
| `/seo images https://tenmien.vn` | Tối ưu hình ảnh: alt, dung lượng, định dạng |
| `/seo sitemap https://tenmien.vn` | Kiểm tra sitemap |
| `/seo sitemap generate` | Tạo sitemap mới |
| `/seo geo https://tenmien.vn` | Tối ưu cho AI search (ChatGPT, Perplexity, AI Overviews) |
| `/seo sxo https://tenmien.vn` | Trải nghiệm tìm kiếm: trang có khớp ý định người tìm không |

### 3.2. Theo loại hình kinh doanh

| Lệnh | Làm gì |
|---|---|
| `/seo local https://tenmien.vn` | SEO địa phương: Google Business Profile, NAP, đánh giá |
| `/seo maps [lệnh]` | Geo-grid, audit GBP, đối thủ quanh khu vực |
| `/seo ecommerce https://tenmien.vn` | SEO thương mại điện tử, schema sản phẩm |
| `/seo hreflang https://tenmien.vn` | Site đa ngôn ngữ, hreflang |
| `/seo programmatic https://tenmien.vn` | SEO trang hàng loạt (programmatic) |

### 3.3. Lập kế hoạch và nội dung

| Lệnh | Làm gì |
|---|---|
| `/seo plan <loại>` | Chiến lược SEO theo ngành (saas, ecommerce, local, publisher, agency) |
| `/seo content-brief "chủ đề"` | Brief bài viết: từ khóa, dàn ý, link nội bộ |
| `/seo cluster "từ khóa gốc"` | Gom cụm chủ đề dựa trên SERP |
| `/seo competitor-pages generate` | Tạo trang so sánh với đối thủ |
| `/seo flow [giai đoạn] [url hoặc chủ đề]` | Bộ prompt theo framework FLOW |

### 3.4. Backlink và theo dõi thay đổi

| Lệnh | Làm gì |
|---|---|
| `/seo backlinks https://tenmien.vn` | Phân tích backlink (Moz, Bing, Common Crawl) |
| `/seo drift baseline https://tenmien.vn` | Chụp trạng thái SEO hiện tại |
| `/seo drift compare https://tenmien.vn` | So sánh với lần chụp trước, phát hiện thay đổi |
| `/seo drift history https://tenmien.vn` | Xem lịch sử thay đổi |

Nên chạy `drift baseline` trước khi khách sửa site, rồi `drift compare` sau khi sửa để kiểm tra.

### 3.5. Google API

```
/seo google pagespeed https://tenmien.vn     # PageSpeed + Core Web Vitals
/seo google crux https://tenmien.vn          # Dữ liệu người dùng thật (CrUX)
/seo google gsc sc-domain:tenmien.vn         # Click, hiển thị, CTR, vị trí
/seo google inspect https://tenmien.vn/trang # Trang đã được index chưa
/seo google ga4                              # Lượt truy cập tự nhiên
/seo google keywords "từ khóa"               # Gợi ý từ khóa (Tier 3)
```

### 3.6. Tiện ích mở rộng (cần cài thêm)

| Lệnh | Cần cài |
|---|---|
| `/seo dataforseo [lệnh]` | DataForSEO: SERP, từ khóa, backlink trực tiếp |
| `/seo firecrawl [lệnh] <url>` | Firecrawl: crawl toàn site, kể cả site dùng JavaScript |
| `/seo ahrefs [lệnh] <url>` | Ahrefs MCP |
| `/seo seranking [lệnh]` | SE Ranking: mức độ hiện diện trên AI search |
| `/seo profound [lệnh]` | Profound: theo dõi trích dẫn trên LLM |
| `/seo bing [lệnh] <url>` | Bing Webmaster Tools + IndexNow |
| `/seo unlighthouse https://tenmien.vn` | Chạy Lighthouse cho nhiều trang |
| `/seo image-gen [loại] <mô tả>` | Tạo ảnh cho SEO (OG image, ảnh bài viết) |

Script cài đặt nằm trong thư mục `extensions/<tên>/`. Xem [`docs/MCP-INTEGRATION.md`](docs/MCP-INTEGRATION.md).

### 3.7. Chạy script Python trực tiếp

Các script trong `scripts/` có giao diện dòng lệnh và trả kết quả JSON. Chạy qua launcher
để dùng đúng môi trường Python:

```bash
bin/claude-seo run fetch_page.py https://tenmien.vn
bin/claude-seo run pagespeed_check.py https://tenmien.vn
```

Xem tham số của một script bằng `--help`, ví dụ:

```bash
python3 scripts/pagespeed_check.py --help
```

---

## 4. Xử lý lỗi thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| `requires Python 3.10 or newer` | macOS mặc định có Python 3.9. Cài bản mới: `brew install python@3.12`, rồi chạy lại `/seo setup` |
| Thiếu thư viện Python, thiếu Chromium | Chạy `/seo setup`, rồi `/seo doctor` |
| PageSpeed API báo hết quota | Dùng Lighthouse qua `npx` như ở mục 1.1 |
| Lệnh `/seo google …` báo thiếu quyền | Chạy lại `/seo google setup`, kiểm tra tier |
| Site chặn crawl (403, Cloudflare) | Giảm tốc độ crawl, hoặc dùng extension Firecrawl |
| Báo cáo public người khác không xem được | Bấm **Share → Anyone with the link** |

Chi tiết hơn: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).
