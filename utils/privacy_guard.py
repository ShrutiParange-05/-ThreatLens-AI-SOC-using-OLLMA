import re

class PrivacyGuard:
    def __init__(self):
        # Regex patterns to catch sensitive info
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "IP_ADDRESS": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "CREDIT_CARD": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "API_KEY": r'sk-[a-zA-Z0-9]{20,}'
        }

    def sanitize(self, text):
        """Replaces sensitive data with [REDACTED: TYPE] tags."""
        sanitized_text = text
        detected_items = []

        for p_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                # Avoid duplicates
                if match not in detected_items:
                    detected_items.append(match)
                    # Replace with a safe tag
                    sanitized_text = sanitized_text.replace(match, f"[{p_type}_REDACTED]")
        
        return sanitized_text, detected_items

    def check_for_leaks(self, llm_response, original_secrets):
        """Checks if the LLM hallucinated or leaked original secrets."""
        leaks = []
        if not original_secrets:
            return leaks
            
        for secret in original_secrets:
            if secret in llm_response:
                leaks.append(secret)
        return leaks
