"""Localize generated audit HTML to Vietnamese and fix methodology to reflect actual data sources."""
import re, json, os
src = "Google-SEO-Report-sharephong.us-full.html"
h = open(src, encoding="utf-8").read()
here = os.path.dirname(os.path.abspath(__file__))
h = h.replace('src="file://sharephong.us-audit/charts/', f'src="file://{here}/charts/')
h = h.replace('<html lang="en">', '<html lang="vi">')

# Lighthouse results for 3 page types
rows = []
for key, label in [("home", "Trang chủ /"), ("search", "Tìm kiếm /search/san-jose/"), ("prop", "Tin đăng /properties/fort-worth-tx-76179/")]:
    lh = json.load(open(f"raw/lh_{key}.json")); a = lh["audits"]; c = lh["categories"]
    v = lambda k: a[k]["displayValue"].replace("\xa0", " ")
    p = round(c["performance"]["score"] * 100)
    cls = "status-pass" if p >= 90 else ("status-warn" if p >= 50 else "status-fail")
    rows.append(f'<tr><td>{label}</td><td class="{cls}">{p}</td><td>{v("largest-contentful-paint")}</td><td>{v("total-blocking-time")}</td><td>{v("cumulative-layout-shift")}</td><td>{v("server-response-time").replace("Root document took ","")}</td></tr>')
table = ('\n  <hr class="divider">\n  <h3>3.3 So sánh 3 loại trang (Lighthouse di động)</h3>\n  <table>\n    <thead><tr><th>Trang</th><th>Hiệu suất</th><th>LCP</th><th>TBT</th><th>CLS</th><th>TTFB</th></tr></thead>\n    <tbody>\n      '
         + "\n      ".join(rows) + '\n    </tbody>\n  </table>\n  <p>Ghi chú: số liệu lab (mô phỏng Moto G Power, mạng 4G chậm) đo bằng Lighthouse 12 ngày 25/09/2026. Chưa có dữ liệu thực tế từ người dùng (CrUX) vì site chưa đủ lưu lượng hoặc chưa kết nối API Google.</p>\n')
h = h.replace("</table>\n</div>\n\n<!-- ======================================================= 4. ACTION PLAN", "</table>" + table + "</div>\n\n<!-- ======================================================= 4. ACTION PLAN", 1)
if "3.3 So sánh" not in h:
    h = re.sub(r'(3\.2 Lab Metrics.*?</table>)', lambda m: m.group(1) + table, h, count=1, flags=re.S)

# Intro paragraph
h = re.sub(r'<p>This report presents a comprehensive SEO audit of.*?</p>',
  '<p>Báo cáo này trình bày kết quả kiểm tra SEO toàn diện cho <strong>sharephong.us</strong>, một marketplace rao vặt cho thuê phòng và nhà dành cho cộng đồng người Việt tại Mỹ (song ngữ Việt/Anh, xây dựng bằng Next.js). Dữ liệu được thu thập ngày 25/09/2026 từ sitemap (1.198 URL), crawl 309 trang mẫu, render JavaScript bằng Chrome headless và đo hiệu suất bằng Lighthouse.</p>'
  '<p><strong>Kết luận chính:</strong> Nội dung tin đăng thật và trang thành phố là nền tảng tốt. Tuy nhiên, các lỗi kỹ thuật đang cản Google và AI search index đúng các trang này: sitemap sai, hreflang lỗi, tin đăng chỉ hiện sau khi chạy JavaScript, soft 404, và không có schema. Phần lớn lỗi nghiêm trọng có thể sửa trong 1–2 tuần.</p><p><em>Lưu ý: điểm Lighthouse SEO 100/100 chỉ kiểm tra các thẻ cơ bản trên một trang (title, meta, lang…). Nó không phát hiện lỗi sitemap, hreflang trỏ tới 404, soft 404 hay nội dung chỉ tải bằng JavaScript. Vì vậy điểm sức khoẻ SEO tổng thể (43/100) mới là con số phản ánh đúng tình trạng site.</em></p>', h, flags=re.S)

# Methodology
h = re.sub(r'<h3 style="text-align: left;">Data Sources &amp; Methodology</h3>.*?</div>\s*</body>',
 '''<h3 style="text-align: left;">5. Nguồn dữ liệu &amp; Phương pháp</h3>
  <table>
    <thead><tr><th>Nguồn</th><th>Nội dung</th><th>Phạm vi</th></tr></thead>
    <tbody>
      <tr><td>sitemap.xml &amp; robots.txt</td><td>Phân tích cấu trúc URL, mã trạng thái, lastmod</td><td>1.198 URL</td></tr>
      <tr><td>Crawl HTML (máy chủ)</td><td>Title, meta, canonical, hreflang, H1, schema, alt, số từ, mã HTTP</td><td>309 URL mẫu theo từng loại trang</td></tr>
      <tr><td>Chrome headless (render JS)</td><td>So sánh HTML gốc với nội dung sau render, đếm tin trên trang tìm kiếm/facet</td><td>17 trang</td></tr>
      <tr><td>Lighthouse 12 (di động)</td><td>Hiệu suất, trợ năng, best practices, SEO</td><td>3 loại trang</td></tr>
    </tbody>
  </table>
  <p style="text-align:left;">Điểm sức khoẻ SEO là trung bình có trọng số: Kỹ thuật 22%, Nội dung 23%, On-page 20%, Schema 10%, Hiệu suất 10%, AI Search 10%, Hình ảnh 5%. Báo cáo chưa bao gồm dữ liệu Google Search Console, GA4 và backlink vì chưa được cấp quyền truy cập. Khi có quyền, nên bổ sung để đo số trang đã index và lưu lượng thực tế.</p>
  <p style="color: #94a3b8; font-size: 9pt; margin-top: 5mm;">Báo cáo được tạo bởi Claude SEO &mdash; 25/09/2026</p>
</div>

</body>''', h, flags=re.S)

rep = [
 ("Full SEO Audit Report", "Báo cáo kiểm tra SEO toàn diện"), ("Prepared by Claude SEO", "Báo cáo phân tích SEO &amp; hướng dẫn khắc phục"),
 ("September 25, 2026", "25/09/2026"), (">Full Audit<", ">Audit toàn site<"), ("SEO Health Score", "Điểm sức khoẻ SEO"),
 ("Table of Contents", "Mục lục"), ("1. Executive Summary", "1. Tóm tắt tổng quan"), ("Executive Summary", "Tóm tắt tổng quan"),
 ("Key Metrics, Critical Issues &amp; Quick Wins", "Chỉ số chính, lỗi nghiêm trọng &amp; việc làm nhanh"),
 ("2. Audit Categories", "2. Kết quả theo hạng mục"), ("Audit Categories", "Kết quả theo hạng mục"),
 ("<span>Findings by Severity</span>", "<span>Vấn đề theo mức độ &amp; cách khắc phục</span>"), ("<span>What Works</span>", "<span>Điểm đang làm tốt</span>"),
 ("3. Core Web Vitals &amp; Performance", "3. Core Web Vitals &amp; Hiệu suất"), ("Core Web Vitals &amp; Performance", "Core Web Vitals &amp; Hiệu suất"),
 ("<span>Lighthouse Scores &amp; Lab Metrics</span>", "<span>Điểm Lighthouse &amp; chỉ số lab</span>"),
 ('<li class="toc-sub"><span>CrUX Field Data &amp; Trends</span></li>', '<li class="toc-sub"><span>So sánh 3 loại trang</span></li>'),
 ('<li class="toc-sub"><span>Failed Audits &amp; Opportunities</span></li>\n', ''),
 ("4. Action Plan", "4. Kế hoạch khắc phục"), ("Action Plan", "Kế hoạch khắc phục"), ("Phased Roadmap", "Lộ trình theo giai đoạn"),
 ("5. Data Sources &amp; Methodology", "5. Nguồn dữ liệu &amp; Phương pháp"),
 ("Critical Issues Found:", "Các lỗi nghiêm trọng nhất:"), ("Quick Wins:", "Việc làm nhanh, hiệu quả cao:"),
 ("<h4>What Works</h4>", "<h4>Điểm đang làm tốt</h4>"), ("<h4>Findings</h4>", "<h4>Vấn đề phát hiện</h4>"),
 ("<strong>Recommendation:</strong>", "<strong>Cách khắc phục:</strong>"), ("<strong>Score:</strong>", "<strong>Điểm:</strong>"),
 (">Critical<", ">Nghiêm trọng<"), (">High<", ">Cao<"), (">Medium<", ">Trung bình<"), (">Low<", ">Thấp<"),
 ("<strong>Critical:</strong>", "<strong>Nghiêm trọng:</strong>"), ("<strong>High:</strong>", "<strong>Cao:</strong>"),
 ("3.1 Lighthouse Scores", "3.1 Điểm Lighthouse (trang chủ, di động)"), ("3.2 Lab Metrics (Simulated)", "3.2 Chỉ số lab (mô phỏng, trang chủ)"),
 ("<th>Category</th><th>Score</th><th>Rating</th>", "<th>Hạng mục</th><th>Điểm</th><th>Đánh giá</th>"),
 ("<th>Metric</th><th>Value</th><th>Score</th><th>Threshold</th>", "<th>Chỉ số</th><th>Giá trị</th><th>Điểm</th><th>Ngưỡng tốt</th>"),
 ("<td>Needs Work</td>", "<td>Cần cải thiện</td>"), ("<td>Good</td>", "<td>Tốt</td>"), ("<td>Poor</td>", "<td>Kém</td>"),
 ("Figure 1: Lighthouse audit scores across Performance, Accessibility, Best Practices, and SEO.", "Hình 1: Điểm Lighthouse di động của trang chủ: Hiệu suất, Trợ năng, Best Practices và SEO."),
]
for a, b in rep: h = h.replace(a, b)
open("SharePhong-SEO-Audit-Report.html", "w", encoding="utf-8").write(h)
left = sorted(set(re.findall(r'>([A-Z][A-Za-z &;,:()/.-]{4,60})<', h)))
print("remaining english-ish labels:", left)
