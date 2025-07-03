# ============================================================================
# CONFIGURATION SETTINGS FOR MARKDOWN TO PDF CONVERTER
# ============================================================================
# This module defines the default configuration settings for PDF generation,
# including page size, margins, and encoding, used by the MarkdownConverter class.
# ============================================================================

# DEFAULT PDF CONFIGURATION
# Defines the default settings for PDF output, such as page size and margins.
# These settings are used by pdfkit to format the generated PDF files.
DEFAULT_CONFIG = {
    'page_size': 'A4',         # Standard A4 page size for PDF output
    'margin_top': '25mm',      # Top margin of 25mm for the PDF
    'margin_right': '25mm',    # Right margin of 25mm for the PDF
    'margin_bottom': '25mm',   # Bottom margin of 25mm for the PDF
    'margin_left': '25mm',     # Left margin of 25mm for the PDF
    'encoding': 'UTF-8'        # UTF-8 encoding for proper character support
}
