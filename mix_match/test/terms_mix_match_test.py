import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TERMS_FILE = ROOT / "terms_mix_match.html"


class TermsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.elements_by_id = {}
        self.links = []
        self.toc_links = []
        self.headings = []
        self.text_parts = []
        self._nav_depth = 0
        self._content_stack = []
        self._active_link = None
        self._active_heading = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
            self.elements_by_id[attributes["id"]] = attributes
        if tag == "main" and attributes.get("id") in {"content-en", "content-vi"}:
            self._content_stack.append(attributes["id"])
        if tag == "nav":
            self._nav_depth += 1
        if tag == "a":
            self._active_link = {
                "href": attributes.get("href"),
                "text": [],
                "content": self._content_stack[-1] if self._content_stack else None,
            }
            self.links.append(self._active_link)
            if self._nav_depth:
                self.toc_links.append(self._active_link)
        if tag in {"h1", "h2", "h3"}:
            self._active_heading = {
                "tag": tag,
                "id": attributes.get("id"),
                "text": [],
                "content": self._content_stack[-1] if self._content_stack else None,
            }
            self.headings.append(self._active_heading)

    def handle_endtag(self, tag):
        if tag == "nav":
            self._nav_depth -= 1
        if tag == "main" and self._content_stack:
            self._content_stack.pop()
        if tag == "a":
            self._active_link = None
        if tag in {"h1", "h2", "h3"}:
            self._active_heading = None

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._active_link is not None:
            self._active_link["text"].append(data)
        if self._active_heading is not None:
            self._active_heading["text"].append(data)

    @staticmethod
    def normalize(parts):
        return re.sub(r"\s+", " ", "".join(parts)).strip()

    @property
    def text(self):
        return self.normalize(self.text_parts)


class MixMatchTermsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = TERMS_FILE.read_text(encoding="utf-8") if TERMS_FILE.exists() else ""
        cls.parser = TermsParser()
        cls.parser.feed(cls.source)

    def test_terms_page_exists(self):
        self.assertTrue(TERMS_FILE.exists(), "terms_mix_match.html must be created")

    def test_table_of_contents_matches_all_31_screenshot_labels(self):
        expected = [
            "1. OUR SERVICES",
            "2. INTELLECTUAL PROPERTY RIGHTS",
            "3. USER REPRESENTATIONS",
            "4. USER REGISTRATION",
            "5. PRODUCTS",
            "6. PURCHASES AND PAYMENT",
            "7. SUBSCRIPTIONS",
            "8. REFUNDS POLICY",
            "9. SOFTWARE",
            "10. PROHIBITED ACTIVITIES",
            "11. USER GENERATED CONTRIBUTIONS",
            "12. CONTRIBUTION LICENSE",
            "13. MOBILE APPLICATION LICENSE",
            "14. SOCIAL MEDIA",
            "15. THIRD-PARTY WEBSITES AND CONTENT",
            "16. ADVERTISERS",
            "17. SERVICES MANAGEMENT",
            "18. PRIVACY POLICY",
            "19. TERM AND TERMINATION",
            "20. MODIFICATIONS AND INTERRUPTIONS",
            "21. GOVERNING LAW",
            "22. DISPUTE RESOLUTION",
            "23. CORRECTIONS",
            "24. DISCLAIMER",
            "25. LIMITATIONS OF LIABILITY",
            "26. INDEMNIFICATION",
            "27. USER DATA",
            "28. ELECTRONIC COMMUNICATIONS, TRANSACTIONS, AND SIGNATURES",
            "29. CALIFORNIA USERS AND RESIDENTS",
            "30. MISCELLANEOUS",
            "31. CONTACT US",
        ]
        actual = [
            self.parser.normalize(link["text"])
            for link in self.parser.toc_links
            if link["content"] in {None, "content-en"}
        ]
        self.assertEqual(expected, actual)
        self.assertTrue(all(link["href"].startswith("#") for link in self.parser.toc_links))

    def test_available_body_sections_are_in_screenshot_order(self):
        expected = [
            ("our-services", "1. OUR SERVICES"),
            ("intellectual-property-rights", "2. INTELLECTUAL PROPERTY RIGHTS"),
            ("user-representations", "3. USER REPRESENTATIONS"),
            ("user-registration", "4. USER REGISTRATION"),
            ("products", "5. PRODUCTS"),
            ("purchases-and-payment", "6. PURCHASES AND PAYMENT"),
            ("subscriptions", "7. SUBSCRIPTIONS"),
            ("refunds-policy", "8. REFUNDS POLICY"),
            ("software", "9. SOFTWARE"),
            ("prohibited-activities", "10. PROHIBITED ACTIVITIES"),
            ("user-generated-contributions", "11. USER GENERATED CONTRIBUTIONS"),
            ("contribution-license", "12. CONTRIBUTION LICENSE"),
            ("mobile-application-license", "13. MOBILE APPLICATION LICENSE"),
            ("social-media", "14. SOCIAL MEDIA"),
            ("third-party-websites-and-content", "15. THIRD-PARTY WEBSITES AND CONTENT"),
            ("advertisers", "16. ADVERTISERS"),
            ("services-management", "17. SERVICES MANAGEMENT"),
            ("privacy-policy", "18. PRIVACY POLICY"),
            ("term-and-termination", "19. TERM AND TERMINATION"),
            ("modifications-and-interruptions", "20. MODIFICATIONS AND INTERRUPTIONS"),
            ("governing-law", "21. GOVERNING LAW"),
            ("dispute-resolution", "22. DISPUTE RESOLUTION"),
            ("corrections", "23. CORRECTIONS"),
            ("disclaimer", "24. DISCLAIMER"),
            ("limitations-of-liability", "25. LIMITATIONS OF LIABILITY"),
            ("indemnification", "26. INDEMNIFICATION"),
            ("user-data", "27. USER DATA"),
            ("electronic-communications-transactions-and-signatures", "28. ELECTRONIC COMMUNICATIONS, TRANSACTIONS, AND SIGNATURES"),
            ("california-users-and-residents", "29. CALIFORNIA USERS AND RESIDENTS"),
            ("miscellaneous", "30. MISCELLANEOUS"),
            ("contact-us", "31. CONTACT US"),
        ]
        actual = [
            (heading["id"], self.parser.normalize(heading["text"]))
            for heading in self.parser.headings
            if heading["content"] in {None, "content-en"}
            and heading["id"] in {item[0] for item in expected}
        ]
        self.assertEqual(expected, actual)

    def test_agreement_and_every_supplied_screenshot_are_represented(self):
        required_text = [
            "MIX & MATCH TERMS AND CONDITIONS",
            "Last updated July 13, 2026",
            "AGREEMENT TO OUR LEGAL TERMS",
            "Mix & Match is a mobile fashion app that helps users organize clothing items, create outfits, and generate virtual try-on images using AI.",
            "We recommend that you print a copy of these Legal Terms for your records.",
            "The Services are not tailored to comply with industry-specific regulations",
            "Our intellectual property",
            "Your use of our Services",
            "Your submissions and contributions",
            "We may remove or edit your Content:",
            "By using the Services, you represent and warrant that:",
            "You may be required to register to use the Services.",
            "All products are subject to availability.",
            "We accept the following forms of payment:",
            "Apple App Store",
            "Google Play",
            "You agree to provide current, complete, and accurate purchase and account information for all purchases made via the Services.",
            "You agree to pay all charges at the prices then in effect for your purchases and any applicable shipping fees",
            "We reserve the right to refuse any order placed through the Services.",
            "Your subscription will continue and automatically renew unless canceled.",
            "All sales are final and no refund will be issued.",
            "We may include software for use in connection with our Services.",
            "As a user of the Services, you agree not to:",
            "Use a buying agent or purchasing agent to make purchases on the Services.",
            "Your Contributions do not otherwise violate, or link to material that violates, any provision of these Legal Terms, or any applicable law or regulation.",
            "Any use of the Services in violation of the foregoing violates these Legal Terms",
            "By posting your Contributions to any part of the Services or making Contributions accessible to the Services",
            "This license will apply to any form, media, or technology now known or hereafter developed",
            "We do not assert any ownership over your Contributions.",
            "We have the right, in our sole and absolute discretion",
            "If you access the Services via the App, then we grant you a revocable, non-exclusive, non-transferable, limited right",
            "Apple and Android Devices",
            "As part of the functionality of the Services, you may link your account with online accounts you have with third-party service providers",
            "The Services may contain (or you may be sent via the App) links to other websites",
            "We allow advertisers to display their advertisements and other information in certain areas of the Services",
            "We reserve the right, but not the obligation, to: (1) monitor the Services for violations of these Legal Terms",
            "We care about data privacy and security.",
            "These Legal Terms shall remain in full force and effect while you use the Services.",
            "If we terminate or suspend your account for any reason, you are prohibited from registering and creating a new account",
            "We reserve the right to change, modify, or remove the contents of the Services at any time or for any reason",
            "We cannot guarantee the Services will be available at all times.",
            "These Legal Terms shall be governed by and defined following the laws of Vietnam.",
            "You agree to irrevocably submit all disputes related to these Legal Terms",
            "There may be information on the Services that contains typographical errors, inaccuracies, or omissions",
            "THE SERVICES ARE PROVIDED ON AN AS-IS AND AS-AVAILABLE BASIS.",
            "IN NO EVENT WILL WE OR OUR DIRECTORS, EMPLOYEES, OR AGENTS BE LIABLE TO YOU OR ANY THIRD PARTY",
            "You agree to defend, indemnify, and hold us harmless",
            "We will maintain certain data that you transmit to the Services for the purpose of managing the performance of the Services",
            "Visiting the Services, sending us emails, and completing online forms constitute electronic communications.",
            "If any complaint with us is not satisfactorily resolved, you can contact the Complaint Assistance Unit",
            "These Legal Terms and any policies or operating rules posted by us on the Services",
            "In order to resolve a complaint regarding the Services or to receive further information regarding use of the Services",
            "Phạm Tiến Thắng Ha noi, Hà Nội 100000 Vietnam meocungptt@gmail.com",
        ]
        for text in required_text:
            with self.subTest(text=text):
                self.assertIn(text, self.parser.text)

    def test_email_and_prohibited_activity_links_are_wired(self):
        mail_links = [
            link
            for link in self.parser.links
            if link["href"] == "mailto:meocungptt@gmail.com"
            and link["content"] in {None, "content-en"}
        ]
        self.assertEqual(4, len(mail_links))
        self.assertTrue(
            all(self.parser.normalize(link["text"]) == "meocungptt@gmail.com" for link in mail_links)
        )

        prohibited_links = [
            link
            for link in self.parser.links
            if link["href"] == "#prohibited-activities"
            and link["content"] in {None, "content-en"}
            and self.parser.normalize(link["text"]) == "PROHIBITED ACTIVITIES"
        ]
        self.assertEqual(3, len(prohibited_links))
        self.assertIn("prohibited-activities", self.parser.ids)

    def test_privacy_policy_link_is_wired(self):
        url = "https://pham-tien-thang.github.io/policy/mix_match/policy_mix_match.html"
        privacy_links = [link for link in self.parser.links if link["href"] == url]
        self.assertEqual(2, len(privacy_links))
        self.assertTrue(
            all(url == self.parser.normalize(link["text"]) for link in privacy_links)
        )

    def test_missing_postal_address_placeholders_are_omitted(self):
        self.assertNotIn("__________", self.parser.text)
        self.assertNotIn("or by mail to", self.parser.text)
        self.assertNotIn("a company registered in Vietnam.", self.parser.text)
        self.assertIn(
            "Mix & Match is operated by Phạm Tiến Thắng, an individual developer "
            "based in Hanoi, Vietnam (“we,” “us,” or “our”).",
            self.parser.text,
        )
        self.assertIn(
            "You can contact us by email at meocungptt@gmail.com.",
            self.parser.text,
        )

    def test_language_switch_defaults_to_english(self):
        self.assertIn("languageToggle", self.parser.ids)
        self.assertIn("content-en", self.parser.ids)
        self.assertIn("content-vi", self.parser.ids)
        self.assertNotIn("hidden", self.parser.elements_by_id["content-en"])
        self.assertIn("hidden", self.parser.elements_by_id["content-vi"])
        self.assertEqual(
            "false",
            self.parser.elements_by_id["languageToggle"].get("aria-pressed"),
        )
        self.assertIn("Dịch sang tiếng Việt", self.parser.text)

    def test_vietnamese_document_has_all_sections_and_local_targets(self):
        expected_headings = [
            "1. DỊCH VỤ CỦA CHÚNG TÔI",
            "2. QUYỀN SỞ HỮU TRÍ TUỆ",
            "3. CAM KẾT CỦA NGƯỜI DÙNG",
            "4. ĐĂNG KÝ NGƯỜI DÙNG",
            "5. SẢN PHẨM",
            "6. MUA HÀNG VÀ THANH TOÁN",
            "7. ĐĂNG KÝ GÓI DỊCH VỤ",
            "8. CHÍNH SÁCH HOÀN TIỀN",
            "9. PHẦN MỀM",
            "10. HOẠT ĐỘNG BỊ CẤM",
            "11. NỘI DUNG DO NGƯỜI DÙNG ĐÓNG GÓP",
            "12. GIẤY PHÉP SỬ DỤNG NỘI DUNG ĐÓNG GÓP",
            "13. GIẤY PHÉP ỨNG DỤNG DI ĐỘNG",
            "14. MẠNG XÃ HỘI",
            "15. TRANG WEB VÀ NỘI DUNG CỦA BÊN THỨ BA",
            "16. NHÀ QUẢNG CÁO",
            "17. QUẢN LÝ DỊCH VỤ",
            "18. CHÍNH SÁCH QUYỀN RIÊNG TƯ",
            "19. THỜI HẠN VÀ CHẤM DỨT",
            "20. SỬA ĐỔI VÀ GIÁN ĐOẠN",
            "21. LUẬT ĐIỀU CHỈNH",
            "22. GIẢI QUYẾT TRANH CHẤP",
            "23. ĐÍNH CHÍNH",
            "24. TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM",
            "25. GIỚI HẠN TRÁCH NHIỆM",
            "26. BỒI THƯỜNG",
            "27. DỮ LIỆU NGƯỜI DÙNG",
            "28. GIAO TIẾP, GIAO DỊCH VÀ CHỮ KÝ ĐIỆN TỬ",
            "29. NGƯỜI DÙNG VÀ CƯ DÂN CALIFORNIA",
            "30. ĐIỀU KHOẢN KHÁC",
            "31. LIÊN HỆ VỚI CHÚNG TÔI",
        ]
        actual_headings = [
            self.parser.normalize(heading["text"])
            for heading in self.parser.headings
            if heading["content"] == "content-vi"
            and heading["tag"] == "h2"
            and heading["id"] != "vi-agreement-to-our-legal-terms"
            and heading["id"] != "vi-table-of-contents"
        ]
        self.assertEqual(expected_headings, actual_headings)

        vi_toc_links = [
            link for link in self.parser.toc_links if link["content"] == "content-vi"
        ]
        self.assertEqual(31, len(vi_toc_links))
        self.assertTrue(all(link["href"].startswith("#vi-") for link in vi_toc_links))
        self.assertTrue(all(link["href"][1:] in self.parser.ids for link in vi_toc_links))

    def test_vietnamese_translation_and_toggle_script_are_complete(self):
        required_vietnamese = [
            "ĐIỀU KHOẢN VÀ ĐIỀU KIỆN CỦA MIX & MATCH",
            "Mix & Match được vận hành bởi Phạm Tiến Thắng, một nhà phát triển cá nhân tại Hà Nội, Việt Nam",
            "Thông tin được cung cấp khi sử dụng Dịch vụ không nhằm mục đích phân phối",
            "Giấy phép sử dụng",
            "CÁC DỊCH VỤ ĐƯỢC CUNG CẤP TRÊN CƠ SỞ “NGUYÊN TRẠNG” VÀ “SẴN CÓ”",
            "Để giải quyết khiếu nại liên quan đến Dịch vụ",
        ]
        for text in required_vietnamese:
            with self.subTest(text=text):
                self.assertIn(text, self.parser.text)

        required_script = [
            "document.documentElement.lang",
            "enContent.hidden",
            "viContent.hidden",
            "aria-pressed",
            "Translate to English",
            "Dịch sang tiếng Việt",
        ]
        for code in required_script:
            with self.subTest(code=code):
                self.assertIn(code, self.source)


if __name__ == "__main__":
    unittest.main()
