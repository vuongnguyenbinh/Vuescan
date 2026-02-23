"""Bilingual translation system - English and Vietnamese."""

TRANSLATIONS = {
    "en": {
        # App
        "app_title": "FiScanPro - Document Scanner",
        "app_about": "FiScanPro v1.0.0\nProfessional Document Scanner\nfor Fujitsu Fi-6125",

        # Menu
        "menu_file": "&File",
        "menu_edit": "&Edit",
        "menu_scan": "&Scan",
        "menu_tools": "&Tools",
        "menu_settings": "&Settings",
        "menu_help": "&Help",

        # File menu
        "action_new": "New Session",
        "action_open": "Open Image...",
        "action_save": "Save",
        "action_save_as": "Save As...",
        "action_export_pdf": "Export to PDF...",
        "action_export_tiff": "Export to TIFF...",
        "action_export_jpeg": "Export to JPEG...",
        "action_export_png": "Export to PNG...",
        "action_print": "Print...",
        "action_exit": "Exit",

        # Scan menu
        "action_scan": "Scan",
        "action_scan_batch": "Batch Scan...",
        "action_scan_preview": "Preview Scan",
        "action_scan_stop": "Stop Scan",
        "action_select_scanner": "Select Scanner...",
        "action_scanner_settings": "Scanner Settings...",

        # Edit menu
        "action_undo": "Undo",
        "action_redo": "Redo",
        "action_rotate_left": "Rotate Left 90°",
        "action_rotate_right": "Rotate Right 90°",
        "action_rotate_180": "Rotate 180°",
        "action_flip_h": "Flip Horizontal",
        "action_flip_v": "Flip Vertical",
        "action_crop": "Crop",
        "action_deskew": "Auto Deskew",
        "action_delete_page": "Delete Page",

        # Tools menu
        "action_ocr": "OCR Text Recognition",
        "action_auto_enhance": "Auto Enhance",
        "action_color_correction": "Color Correction...",

        # Settings
        "settings_language": "Language",
        "settings_general": "General Settings",
        "settings_scanner": "Scanner Settings",
        "settings_output": "Output Settings",
        "settings_default_folder": "Default Save Folder",
        "settings_browse": "Browse...",

        # Help
        "help_about": "About FiScanPro",
        "help_manual": "User Manual",
        "help_check_update": "Check for Updates",

        # Scanner Panel
        "panel_scanner": "Scanner",
        "scanner_device": "Device:",
        "scanner_no_device": "No scanner detected",
        "scanner_source": "Source:",
        "scanner_source_flatbed": "Flatbed",
        "scanner_source_adf_front": "ADF (Front)",
        "scanner_source_adf_back": "ADF (Back)",
        "scanner_source_adf_duplex": "ADF (Duplex)",
        "scanner_mode": "Color Mode:",
        "scanner_mode_color": "Color",
        "scanner_mode_gray": "Grayscale",
        "scanner_mode_bw": "Black & White",
        "scanner_resolution": "Resolution (DPI):",
        "scanner_paper_size": "Paper Size:",
        "scanner_brightness": "Brightness:",
        "scanner_contrast": "Contrast:",
        "scanner_threshold": "Threshold:",
        "scanner_refresh": "Refresh Devices",

        # Paper sizes
        "paper_auto": "Auto Detect",
        "paper_a3": "A3 (297 × 420 mm)",
        "paper_a4": "A4 (210 × 297 mm)",
        "paper_a5": "A5 (148 × 210 mm)",
        "paper_a6": "A6 (105 × 148 mm)",
        "paper_letter": "Letter (8.5 × 11 in)",
        "paper_legal": "Legal (8.5 × 14 in)",
        "paper_custom": "Custom...",

        # Output Panel
        "panel_output": "Output",
        "output_format": "Format:",
        "output_folder": "Save To:",
        "output_filename": "File Name:",
        "output_multi_page": "Multi-page PDF",
        "output_compression": "Compression:",
        "output_quality": "Quality:",
        "output_browse": "Browse...",
        "output_compression_none": "None",
        "output_compression_jpeg": "JPEG",
        "output_compression_lzw": "LZW",
        "output_compression_zip": "ZIP/Deflate",

        # Preview Panel
        "panel_preview": "Preview",
        "preview_zoom_in": "Zoom In",
        "preview_zoom_out": "Zoom Out",
        "preview_fit_page": "Fit Page",
        "preview_fit_width": "Fit Width",
        "preview_actual_size": "Actual Size (100%)",
        "preview_no_image": "No image to display.\nClick 'Scan' or 'Preview Scan' to start.",

        # Pages Panel
        "panel_pages": "Pages",
        "pages_count": "{count} page(s)",
        "pages_select_all": "Select All",
        "pages_deselect_all": "Deselect All",
        "pages_delete_selected": "Delete Selected",
        "pages_move_up": "Move Up",
        "pages_move_down": "Move Down",

        # Toolbar
        "toolbar_scan": "Scan",
        "toolbar_preview": "Preview",
        "toolbar_stop": "Stop",
        "toolbar_save_pdf": "Save PDF",
        "toolbar_rotate_l": "Rotate L",
        "toolbar_rotate_r": "Rotate R",
        "toolbar_crop": "Crop",
        "toolbar_deskew": "Deskew",
        "toolbar_settings": "Settings",

        # Status bar
        "status_ready": "Ready",
        "status_scanning": "Scanning...",
        "status_processing": "Processing...",
        "status_saving": "Saving...",
        "status_scan_complete": "Scan complete - {count} page(s) scanned",
        "status_saved": "Saved to: {path}",
        "status_error": "Error: {message}",
        "status_scanner_connected": "Scanner connected: {name}",
        "status_no_scanner": "No scanner connected",

        # Dialogs
        "dialog_save_title": "Save File",
        "dialog_open_title": "Open Image File",
        "dialog_folder_title": "Select Folder",
        "dialog_confirm_exit": "Are you sure you want to exit?\nUnsaved pages will be lost.",
        "dialog_confirm_delete": "Delete {count} selected page(s)?",
        "dialog_confirm_title": "Confirm",
        "dialog_error_title": "Error",
        "dialog_info_title": "Information",
        "dialog_warning_title": "Warning",
        "dialog_yes": "Yes",
        "dialog_no": "No",
        "dialog_ok": "OK",
        "dialog_cancel": "Cancel",

        # Scanner selection dialog
        "select_scanner_title": "Select Scanner",
        "select_scanner_label": "Available scanners:",
        "select_scanner_none": "No scanners found.\nPlease check that your scanner is connected\nand the TWAIN driver is installed.",
        "select_scanner_refresh": "Refresh",
        "select_scanner_select": "Select",

        # Batch scan dialog
        "batch_title": "Batch Scan Settings",
        "batch_count": "Number of pages to scan:",
        "batch_unlimited": "Scan until empty",
        "batch_delay": "Delay between scans (sec):",
        "batch_start": "Start Batch",

        # Export PDF dialog
        "pdf_title": "Export to PDF",
        "pdf_pages": "Pages:",
        "pdf_all_pages": "All Pages",
        "pdf_selected_pages": "Selected Pages",
        "pdf_page_range": "Page Range:",
        "pdf_author": "Author:",
        "pdf_subject": "Subject:",
        "pdf_compress": "Compress Images",
        "pdf_quality_label": "JPEG Quality:",
        "pdf_export": "Export",

        # Image processing
        "enhance_title": "Image Enhancement",
        "enhance_brightness": "Brightness",
        "enhance_contrast": "Contrast",
        "enhance_sharpness": "Sharpness",
        "enhance_saturation": "Saturation",
        "enhance_auto_level": "Auto Levels",
        "enhance_reset": "Reset",
        "enhance_apply": "Apply",
        "enhance_preview": "Preview",

        # Errors
        "error_no_scanner": "No scanner selected. Please select a scanner first.",
        "error_scan_failed": "Scan failed: {message}",
        "error_save_failed": "Failed to save file: {message}",
        "error_open_failed": "Failed to open file: {message}",
        "error_no_pages": "No pages to export.",
        "error_driver_not_found": "Scanner driver not found.\nPlease install the Fujitsu TWAIN driver.",
        "error_scanner_busy": "Scanner is busy. Please wait.",
        "error_paper_jam": "Paper jam detected. Please clear the jam and try again.",
        "error_adf_empty": "Document feeder is empty.",
    },

    "vi": {
        # App
        "app_title": "FiScanPro - Máy Quét Tài Liệu",
        "app_about": "FiScanPro v1.0.0\nCông cụ Quét Tài Liệu Chuyên Nghiệp\ncho Fujitsu Fi-6125",

        # Menu
        "menu_file": "&Tệp",
        "menu_edit": "&Chỉnh sửa",
        "menu_scan": "&Quét",
        "menu_tools": "&Công cụ",
        "menu_settings": "&Cài đặt",
        "menu_help": "&Trợ giúp",

        # File menu
        "action_new": "Phiên mới",
        "action_open": "Mở ảnh...",
        "action_save": "Lưu",
        "action_save_as": "Lưu thành...",
        "action_export_pdf": "Xuất ra PDF...",
        "action_export_tiff": "Xuất ra TIFF...",
        "action_export_jpeg": "Xuất ra JPEG...",
        "action_export_png": "Xuất ra PNG...",
        "action_print": "In...",
        "action_exit": "Thoát",

        # Scan menu
        "action_scan": "Quét",
        "action_scan_batch": "Quét hàng loạt...",
        "action_scan_preview": "Xem trước",
        "action_scan_stop": "Dừng quét",
        "action_select_scanner": "Chọn máy quét...",
        "action_scanner_settings": "Cài đặt máy quét...",

        # Edit menu
        "action_undo": "Hoàn tác",
        "action_redo": "Làm lại",
        "action_rotate_left": "Xoay trái 90°",
        "action_rotate_right": "Xoay phải 90°",
        "action_rotate_180": "Xoay 180°",
        "action_flip_h": "Lật ngang",
        "action_flip_v": "Lật dọc",
        "action_crop": "Cắt xén",
        "action_deskew": "Tự động căn thẳng",
        "action_delete_page": "Xóa trang",

        # Tools menu
        "action_ocr": "Nhận dạng chữ OCR",
        "action_auto_enhance": "Tự động cải thiện",
        "action_color_correction": "Chỉnh màu...",

        # Settings
        "settings_language": "Ngôn ngữ",
        "settings_general": "Cài đặt chung",
        "settings_scanner": "Cài đặt máy quét",
        "settings_output": "Cài đặt xuất",
        "settings_default_folder": "Thư mục lưu mặc định",
        "settings_browse": "Duyệt...",

        # Help
        "help_about": "Giới thiệu FiScanPro",
        "help_manual": "Hướng dẫn sử dụng",
        "help_check_update": "Kiểm tra cập nhật",

        # Scanner Panel
        "panel_scanner": "Máy quét",
        "scanner_device": "Thiết bị:",
        "scanner_no_device": "Không phát hiện máy quét",
        "scanner_source": "Nguồn:",
        "scanner_source_flatbed": "Mặt phẳng",
        "scanner_source_adf_front": "ADF (Mặt trước)",
        "scanner_source_adf_back": "ADF (Mặt sau)",
        "scanner_source_adf_duplex": "ADF (Hai mặt)",
        "scanner_mode": "Chế độ màu:",
        "scanner_mode_color": "Màu",
        "scanner_mode_gray": "Xám",
        "scanner_mode_bw": "Đen trắng",
        "scanner_resolution": "Độ phân giải (DPI):",
        "scanner_paper_size": "Khổ giấy:",
        "scanner_brightness": "Độ sáng:",
        "scanner_contrast": "Độ tương phản:",
        "scanner_threshold": "Ngưỡng:",
        "scanner_refresh": "Làm mới thiết bị",

        # Paper sizes
        "paper_auto": "Tự động nhận diện",
        "paper_a3": "A3 (297 × 420 mm)",
        "paper_a4": "A4 (210 × 297 mm)",
        "paper_a5": "A5 (148 × 210 mm)",
        "paper_a6": "A6 (105 × 148 mm)",
        "paper_letter": "Letter (8.5 × 11 in)",
        "paper_legal": "Legal (8.5 × 14 in)",
        "paper_custom": "Tùy chỉnh...",

        # Output Panel
        "panel_output": "Đầu ra",
        "output_format": "Định dạng:",
        "output_folder": "Lưu vào:",
        "output_filename": "Tên tệp:",
        "output_multi_page": "PDF nhiều trang",
        "output_compression": "Nén:",
        "output_quality": "Chất lượng:",
        "output_browse": "Duyệt...",
        "output_compression_none": "Không nén",
        "output_compression_jpeg": "JPEG",
        "output_compression_lzw": "LZW",
        "output_compression_zip": "ZIP/Deflate",

        # Preview Panel
        "panel_preview": "Xem trước",
        "preview_zoom_in": "Phóng to",
        "preview_zoom_out": "Thu nhỏ",
        "preview_fit_page": "Vừa trang",
        "preview_fit_width": "Vừa chiều rộng",
        "preview_actual_size": "Kích thước thật (100%)",
        "preview_no_image": "Không có ảnh để hiển thị.\nNhấn 'Quét' hoặc 'Xem trước' để bắt đầu.",

        # Pages Panel
        "panel_pages": "Trang",
        "pages_count": "{count} trang",
        "pages_select_all": "Chọn tất cả",
        "pages_deselect_all": "Bỏ chọn tất cả",
        "pages_delete_selected": "Xóa đã chọn",
        "pages_move_up": "Di chuyển lên",
        "pages_move_down": "Di chuyển xuống",

        # Toolbar
        "toolbar_scan": "Quét",
        "toolbar_preview": "Xem trước",
        "toolbar_stop": "Dừng",
        "toolbar_save_pdf": "Lưu PDF",
        "toolbar_rotate_l": "Xoay T",
        "toolbar_rotate_r": "Xoay P",
        "toolbar_crop": "Cắt",
        "toolbar_deskew": "Căn thẳng",
        "toolbar_settings": "Cài đặt",

        # Status bar
        "status_ready": "Sẵn sàng",
        "status_scanning": "Đang quét...",
        "status_processing": "Đang xử lý...",
        "status_saving": "Đang lưu...",
        "status_scan_complete": "Quét xong - {count} trang đã quét",
        "status_saved": "Đã lưu tại: {path}",
        "status_error": "Lỗi: {message}",
        "status_scanner_connected": "Máy quét đã kết nối: {name}",
        "status_no_scanner": "Chưa kết nối máy quét",

        # Dialogs
        "dialog_save_title": "Lưu tệp",
        "dialog_open_title": "Mở tệp ảnh",
        "dialog_folder_title": "Chọn thư mục",
        "dialog_confirm_exit": "Bạn có chắc muốn thoát?\nCác trang chưa lưu sẽ bị mất.",
        "dialog_confirm_delete": "Xóa {count} trang đã chọn?",
        "dialog_confirm_title": "Xác nhận",
        "dialog_error_title": "Lỗi",
        "dialog_info_title": "Thông tin",
        "dialog_warning_title": "Cảnh báo",
        "dialog_yes": "Có",
        "dialog_no": "Không",
        "dialog_ok": "Đồng ý",
        "dialog_cancel": "Hủy",

        # Scanner selection dialog
        "select_scanner_title": "Chọn máy quét",
        "select_scanner_label": "Các máy quét khả dụng:",
        "select_scanner_none": "Không tìm thấy máy quét.\nVui lòng kiểm tra kết nối máy quét\nvà cài đặt driver TWAIN.",
        "select_scanner_refresh": "Làm mới",
        "select_scanner_select": "Chọn",

        # Batch scan dialog
        "batch_title": "Cài đặt quét hàng loạt",
        "batch_count": "Số trang cần quét:",
        "batch_unlimited": "Quét đến khi hết giấy",
        "batch_delay": "Độ trễ giữa các lần quét (giây):",
        "batch_start": "Bắt đầu quét",

        # Export PDF dialog
        "pdf_title": "Xuất ra PDF",
        "pdf_pages": "Trang:",
        "pdf_all_pages": "Tất cả các trang",
        "pdf_selected_pages": "Các trang đã chọn",
        "pdf_page_range": "Phạm vi trang:",
        "pdf_author": "Tác giả:",
        "pdf_subject": "Chủ đề:",
        "pdf_compress": "Nén ảnh",
        "pdf_quality_label": "Chất lượng JPEG:",
        "pdf_export": "Xuất",

        # Image processing
        "enhance_title": "Cải thiện hình ảnh",
        "enhance_brightness": "Độ sáng",
        "enhance_contrast": "Độ tương phản",
        "enhance_sharpness": "Độ sắc nét",
        "enhance_saturation": "Độ bão hòa",
        "enhance_auto_level": "Tự động cân bằng",
        "enhance_reset": "Đặt lại",
        "enhance_apply": "Áp dụng",
        "enhance_preview": "Xem trước",

        # Errors
        "error_no_scanner": "Chưa chọn máy quét. Vui lòng chọn máy quét trước.",
        "error_scan_failed": "Quét thất bại: {message}",
        "error_save_failed": "Lưu tệp thất bại: {message}",
        "error_open_failed": "Mở tệp thất bại: {message}",
        "error_no_pages": "Không có trang nào để xuất.",
        "error_driver_not_found": "Không tìm thấy driver máy quét.\nVui lòng cài đặt driver TWAIN của Fujitsu.",
        "error_scanner_busy": "Máy quét đang bận. Vui lòng đợi.",
        "error_paper_jam": "Phát hiện kẹt giấy. Vui lòng xử lý kẹt giấy và thử lại.",
        "error_adf_empty": "Khay nạp giấy trống.",
    },
}


class Translator:
    """Handles translation between English and Vietnamese."""

    def __init__(self, language: str = "en"):
        self._language = language

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, lang: str):
        if lang in TRANSLATIONS:
            self._language = lang

    def t(self, key: str, **kwargs) -> str:
        """Get translated string by key with optional format arguments."""
        text = TRANSLATIONS.get(self._language, {}).get(key, "")
        if not text:
            text = TRANSLATIONS.get("en", {}).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text

    def available_languages(self) -> dict:
        return {"en": "English", "vi": "Tiếng Việt"}


# Global translator instance
tr = Translator("en")
