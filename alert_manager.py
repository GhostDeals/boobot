class AlertManager:
    def __init__(self):
        self.keywords = set()
        self.alert_log = []

    def add_keyword(self, keyword):
        keyword = keyword.strip().lower()
        if keyword and keyword not in self.keywords:
            self.keywords.add(keyword)
            return True
        return False

    def list_keywords(self):
        return sorted(self.keywords)

    def keyword_match(self, message):
        message = message.lower()
        matches = [kw for kw in self.keywords if kw in message]
        return matches

    def log_alert(self, keyword, message):
        self.alert_log.append((keyword, message))
        print(f"[ALERT] Keyword matched: '{keyword}' in message: '{message}'")
