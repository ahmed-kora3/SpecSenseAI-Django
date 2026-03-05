"""
core/ocr_engine.py
==================
OCR AI Engine — عضو 5 مسؤول عن ملء هذا الملف

المطلوب:
    - نقل منطق ocr_module/interface.py من المشروع القديم إلى هنا
    - الدالة extract_and_validate تاخد path المستند وترجع (specs_dict, report_dict)
"""


def extract_and_validate(document_path: str):
    """
    Extract specs from a document and validate them.

    Args:
        document_path (str): Absolute path to the document file.

    Returns:
        tuple: (specs: dict, report: dict)
               specs — extracted cable specifications
               report — validation result with keys: status, errors, keyword_details
    """
    # TODO (عضو 5): انقل الكود من:
    # C:/Users/HP/Desktop/SpecSenseAI/ocr_module/interface.py
    # واستدعي extract_and_validate من هناك

    raise NotImplementedError("OCR engine not implemented yet. See TODO above.")
