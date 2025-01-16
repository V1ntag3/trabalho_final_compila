from antlr4.error.ErrorListener import ErrorListener


class LPMSErrorListener(ErrorListener):
    def __init__(self):
        super(LPMSErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Erro sintático na linha {line}:{column} - {msg}")

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
