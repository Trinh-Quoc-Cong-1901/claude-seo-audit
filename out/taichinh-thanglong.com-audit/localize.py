"""Localize generated audit HTML to Vietnamese and fix methodology to reflect actual data sources."""
import re, json, os
src = "Google-SEO-Report-taichinh-thanglong.com-full.html"
h = open(src, encoding="utf-8").read()
here = os.path.dirname(os.path.abspath(__file__))
h = h.replace('src="file://out/taichinh-thanglong.com-audit/charts/', f'src="file://{here}/charts/')
h = h.replace('<html lang="en">', '<html lang="vi">')

# Lighthouse results for 3 page types
rows = []
for key, label in [("home", "Trang chủ /"), ("svc", "Dịch vụ /dich-vu-chung-minh-tai-chinh-du-hoc/"), ("prod", "Sản phẩm demo /product/luxury-hotel/")]:
    lh = json.load(open(f"raw/lh_{key}.json")); a = lh["audits"]; c = lh["categories"]
    v = lambda k: a[k]["displayValue"].replace("\xa0", " ")
    p = round(c["performance"]["score"] * 100)
    cls = "status-pass" if p >= 90 else ("status-warn" if p >= 50 else "status-fail")
    rows.append(f'<tr><td>{label}</td><td class="{cls}">{p}</td><td>{v("largest-contentful-paint")}</td><td>{v("total-blocking-time")}</td><td>{v("cumulative-layout-shift")}</td><td>{v("server-response-time").replace("Root document took ","")}</td></tr>')
table = ('\n  <hr class="divider">\n  <h3>3.3 So sánh 3 loại trang (Lighthouse di động)</h3>\n  <table>\n    <thead><tr><th>Trang</th><th>Hiệu suất</th><th>LCP</th><th>TBT</th><th>CLS</th><th>TTFB</th></tr></thead>\n    <tbody>\n      '
         + "\n      ".join(rows) + '\n    </tbody>\n  </table>\n  <p>Ghi chú: số liệu lab (mô phỏng Moto G Power, mạng 4G chậm) đo bằng Lighthouse 12 ngày 26/09/2026. Chưa có dữ liệu thực tế từ người dùng (CrUX) vì chưa kết nối API Google.</p>\n')
h = h.replace("</table>\n</div>\n\n<!-- ======================================================= 4. ACTION PLAN", "</table>" + table + "</div>\n\n<!-- ======================================================= 4. ACTION PLAN", 1)
if "3.3 So sánh" not in h:
    h = re.sub(r'(3\.2 Lab Metrics.*?</table>)', lambda m: m.group(1) + table, h, count=1, flags=re.S)

# Intro paragraph
h = re.sub(r'<p>This report presents a comprehensive SEO audit of.*?</p>',
  '<p>Báo cáo này trình bày kết quả kiểm tra SEO toàn diện cho <strong>taichinh-thanglong.com</strong>, website dịch vụ chứng minh tài chính du học, du lịch và doanh nghiệp của Công ty Dịch vụ Tài chính Thăng Long (Hà Nội), xây dựng trên WordPress + theme Flatsome. Dữ liệu được thu thập ngày 26/09/2026: crawl toàn bộ 150 URL trong sitemap, phân tích robots.txt, canonical, schema, nội dung và đo hiệu suất bằng Lighthouse trên 3 loại trang.</p>'
  '<p><strong>Kết luận chính:</strong> Các trang dịch vụ có nội dung dài và đúng nhu cầu tìm kiếm – đây là tài sản tốt. Nhưng site đang bị kéo xuống bởi 3 vấn đề nền tảng: (1) toàn site vẫn khai báo http:// làm bản chính thức, (2) 71% URL trong sitemap là sản phẩm demo của theme, (3) trang Giới thiệu và chuyên mục tin tức thuộc về doanh nghiệp khác. Với lĩnh vực tài chính, Google yêu cầu mức độ tin cậy cao nên cần ưu tiên xử lý các lỗi này trong 1–2 tuần đầu.</p><p><em>Lưu ý: điểm Lighthouse SEO 92/100 chỉ kiểm tra thẻ cơ bản trên một trang. Nó không phát hiện canonical http, nội dung demo hay nội dung sao chép. Điểm sức khoẻ SEO tổng thể (40/100) mới phản ánh đúng tình trạng site.</em></p>', h, flags=re.S)

# Methodology
h = re.sub(r'<h3 style="text-align: left;">Data Sources &amp; Methodology</h3>.*?</div>\s*</body>',
 '''<h3 style="text-align: left;">5. Nguồn dữ liệu &amp; Phương pháp</h3>
  <table>
    <thead><tr><th>Nguồn</th><th>Nội dung</th><th>Phạm vi</th></tr></thead>
    <tbody>
      <tr><td>sitemap_index.xml &amp; robots.txt</td><td>Cấu trúc sitemap (8 sitemap con), giao thức URL, lastmod</td><td>150 URL</td></tr>
      <tr><td>Crawl HTML</td><td>Mã HTTP, thời gian phản hồi, title, meta description, canonical, robots, H1, schema, alt ảnh, số từ</td><td>Toàn bộ 150 URL + 2 URL kiểm thử</td></tr>
      <tr><td>Kiểm tra chuyển hướng</td><td>http/https, www/non-www</td><td>4 biến thể tên miền</td></tr>
      <tr><td>Lighthouse 12 (di động)</td><td>Hiệu suất, trợ năng, best practices, SEO</td><td>3 loại trang</td></tr>
    </tbody>
  </table>
  <p style="text-align:left;">Điểm sức khoẻ SEO là trung bình có trọng số: Kỹ thuật 22%, Nội dung 23%, On-page 20%, Schema 10%, Hiệu suất 10%, AI Search 10%, Hình ảnh 5%. Báo cáo chưa bao gồm dữ liệu Google Search Console, GA4 và backlink vì chưa được cấp quyền truy cập. Khi có quyền, nên bổ sung để đo số trang đã index và lưu lượng thực tế.</p>
  <p style="color: #94a3b8; font-size: 9pt; margin-top: 5mm;">Ngày lập báo cáo: 26/09/2026</p>
</div>

</body>''', h, flags=re.S)

rep = [
 ("Full SEO Audit Report", "Báo cáo kiểm tra SEO toàn diện"), ("Prepared by Claude SEO", "Báo cáo phân tích SEO &amp; hướng dẫn khắc phục"),
 ("September 26, 2026", "26/09/2026"), (">Full Audit<", ">Audit toàn site<"), ("SEO Health Score", "Điểm sức khoẻ SEO"),
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
open("ThangLong-SEO-Audit-Report.html", "w", encoding="utf-8").write(h)
left = sorted(set(re.findall(r'>([A-Z][A-Za-z &;,:()/.-]{4,60})<', h)))
print("remaining english-ish labels:", left)
