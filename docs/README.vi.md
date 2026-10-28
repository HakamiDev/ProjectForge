<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · **Tiếng Việt** · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Một hệ điều hành cho đội ngũ các tác tử AI.** Một lệnh biến một thư mục thông thường thành một văn phòng có kỷ luật: một bảng duy nhất để mọi tác tử làm việc theo, trên bất kỳ nền tảng nào; một cổng chất lượng độc lập; quản trị quyết định; nhật ký kiểm toán đầy đủ; các chỉ số hiệu suất có thể xuất sang Power BI; và một trang quản lý chạy từ một tệp HTML duy nhất.

Python 3.9 trở lên, không phụ thuộc thư viện ngoài, không cần máy chủ. Mã nguồn mở, giấy phép MIT.

Trang web: https://hakamidev.github.io/ProjectForge/

## Cài đặt

Một dòng lệnh, dán vào terminal. Lệnh này tải công cụ về, chạy nó, đặt bốn câu hỏi, rồi mở trang quản lý của bạn.

macOS và Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Trang web cũng cho phép bạn chọn trước nền tảng và ngôn ngữ ưa thích; cả hai được đưa vào lệnh cài đặt và được chọn sẵn trong trình hướng dẫn.

## Giải quyết vấn đề gì

- **Cuộc trò chuyện hay quên.** Quy tắc và bản mô tả vai trò nằm trong thư mục, không nằm trong bộ nhớ của cuộc trò chuyện, nên cuộc trò chuyện nào cũng có thể tiếp tục công việc.
- **Tác tử xung đột.** Một bảng được đánh số; trạng thái "đang thực hiện" khóa một dòng; cơ chế bảo vệ bằng checksum ngăn các thao tác ghi xung đột.
- **Kết quả không được kiểm tra.** Trưởng bộ phận đảm bảo chất lượng quyết định đạt hay không đạt trước khi bất cứ thứ gì đến tay chủ sở hữu.
- **Quyết định bị đình trệ.** Tối đa năm quyết định đang mở, và quy tắc 48 giờ: sau thời hạn đó, đề xuất sẽ được coi là quyết định.
- **Không có gì được đo lường.** `report` cung cấp tỷ lệ bàn giao, thời gian chu kỳ, tỷ lệ đạt QA và khối lượng công việc theo từng vai trò; `export` ghi các tệp CSV cho Power BI.
- **Thiếu trách nhiệm giải trình.** Mọi thao tác ghi lên bảng đều được ghi nhật ký: ai, khi nào và làm gì.
- **Dữ liệu nhạy cảm trong công cụ bên ngoài.** Một chính sách dữ liệu ràng buộc, có phân loại và danh sách công cụ được phê duyệt.

## Bạn nhận được gì

- **80 chuyên môn** (chiến lược, nhà hàng, bất động sản, phần mềm, nhân sự, giáo dục và nhiều hơn nữa) với hơn 330 vai trò dựng sẵn mà bạn thêm chỉ bằng một cú nhấp.
- **130 kỹ năng dựng sẵn trong 18 nhóm.** Một kỹ năng là một tệp ngắn mô tả khi nào nên dùng, các bước thực hiện, đầu ra và tiêu chí nghiệm thu, để nhân viên áp dụng thay vì làm theo ngẫu hứng.
- **Bốn nền tảng:** Claude, ChatGPT, Grok và Gemini. Mỗi nhân viên có thể làm việc trên một nền tảng khác nhau.
- **27 ngôn ngữ giao diện** trên trang web và trong trình hướng dẫn. Ngôn ngữ ưa thích là ngôn ngữ để quản lý toàn bộ hệ thống và là ngôn ngữ dùng khi làm việc với nhân viên.
- **Một trang quản lý** từ một tệp HTML: bảng công việc, đội ngũ, quyết định, chỉ số, thư viện lệnh dựng sẵn, và một công cụ cảnh báo đánh dấu những việc đã trễ hoặc đang chờ bạn.

## Lệnh

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Nền tảng

| Nền tảng | Cách thiết lập đội ngũ |
| --- | --- |
| Claude | Tạo một dự án đặt theo tên dự án của bạn và thêm thư mục đã tạo. |
| ChatGPT | Tạo một dự án và tải các tệp trong thư mục lên. |
| Grok | Tạo một dự án, dán lệnh Compass vào phần hướng dẫn của dự án, rồi thêm các tệp. |
| Gemini | Tạo một Gem cho mỗi nhân viên, dán lệnh của nhân viên đó vào phần hướng dẫn, rồi thêm các tệp trong mục Knowledge. |

Hãy tải các tệp lên từ thư mục dự án ở vị trí gốc và tải lại những tệp đã thay đổi. Theo hiểu biết của chúng tôi, Grok và Gemini không ghi trực tiếp vào thư mục, vì vậy bạn cần tự chuyển kết quả của chúng vào thư mục. Các bước này dựa trên tài liệu công khai tại thời điểm viết; giao diện và giới hạn do các nền tảng đó quy định và có thể thay đổi.

## Giới hạn hiện tại

- Trình hướng dẫn và trang web có 27 ngôn ngữ, nhưng các tệp dự án được tạo ra (quy tắc, bản mô tả vai trò, bảng) và trang quản lý hiện được viết bằng tiếng Ả Rập. Nhân viên được cho biết cần làm việc bằng ngôn ngữ nào và sẽ trả lời bạn bằng ngôn ngữ đó.
- Tên tệp, lệnh và các từ chỉ trạng thái của bảng vẫn giữ bằng tiếng Ả Rập vì công cụ đọc chúng theo đúng nghĩa đen.
- Việc cài đặt trên Windows chưa được kiểm thử trên máy thật.

## Dành cho nhà phát triển

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Mã nguồn nằm trong `forge/`; `tools/build-single.py` tạo ra công cụ một tệp trong `dist/`. Các mẫu nằm trong `forge/templates/`, trang web công khai nằm trong `site/`.

## Giấy phép

MIT.
