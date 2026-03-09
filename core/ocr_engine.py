"""
core/ocr_engine.py
==================
OCR AI Engine — يُستدعى من documents/views.py

الدالة: extract_and_validate(document_path)
  - تاخد path الملف (صورة / PDF / DOCX)
  - ترجع (specs_dict, report_dict)
"""

import os
import sys

# Add core dir to path so internal imports work
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

from core.ocr_src.core_ocr import OCREngine
from core.ocr_src.extraction import SpecificationExtractor, SpecCorrector
from core.ocr_src.validation import CableValidator
from core.keyword_gen.keyword_tool import CableClassifier, KeywordExtractor


def extract_and_validate(document_path: str):
    """
    Extract cable specs from a document/image and validate them.

    Args:
        document_path (str): Absolute path to the document (image, PDF, DOCX).

    Returns:
        tuple: (specs: dict, report: dict)
               specs  — extracted cable specifications
               report — validation result with keys: status, errors, warnings, keyword_details
    """
    if not os.path.exists(document_path):
        return {}, {
            "status": "ERROR",
            "valid": False,
            "errors": [f"File not found: {document_path}"],
            "warnings": []
        }

    try:
        # 1. Initialize OCR Engine (CPU mode to avoid GPU dependency issues)
        ocr = OCREngine(languages=['en'], gpu=False)

        # 2. Read Text from document
        results = ocr.read_image(document_path, detail=0)
        full_text = " ".join(results) if isinstance(results, list) else str(results)

        # 3. Extract Specifications
        extractor = SpecificationExtractor()
        raw_specs = extractor.extract_specs(full_text)

        # 4. Apply Post-OCR Corrections
        corrector = SpecCorrector()
        corrected_specs, correction_logs = corrector.correct_all(raw_specs)

        # 5. Validate against Engineering Rules
        validator = CableValidator()
        validation_report = validator.validate_cable(corrected_specs)
        validation_report['correction_logs'] = correction_logs

        # 6. Keyword Generation
        try:
            classifier = CableClassifier()
            kw_extractor = KeywordExtractor()

            category = classifier.classify(full_text)
            keywords = kw_extractor.extract_keywords(full_text)

            # Merge keyword data into specs
            corrected_specs['cable_category'] = category
            if keywords.get('Top Terms'):
                corrected_specs['top_terms'] = keywords['Top Terms']
            if keywords.get('Conductor Type'):
                corrected_specs['conductor_type_keyword'] = ", ".join(keywords['Conductor Type'])

            # Store full keyword details in report
            validation_report['keyword_details'] = {
                "category": category,
                "extracted_data": keywords,
            }

        except Exception as kw_error:
            validation_report.setdefault('warnings', []).append(
                f"Keyword generation failed: {str(kw_error)}"
            )
            validation_report['keyword_details'] = {
                "category": "Unknown",
                "extracted_data": {},
            }

        return corrected_specs, validation_report

    except Exception as e:
        return {}, {
            "status": "ERROR",
            "valid": False,
            "errors": [str(e)],
            "warnings": []
        }
