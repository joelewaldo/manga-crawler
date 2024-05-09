
class Metadata:
  def __init__(self, data: dict[str, str]):
    self.manga = self._sanitize_filename(data["manga"].strip())
    self.chapter = self._sanitize_filename(data["chapter"].strip())
    self.chapter_minor = int(data["chapter_minor"]) if data["chapter_minor"] else None
    self.lang = data["lang"]
    self.language = data["language"]

  def _sanitize_filename(self, name):
    invalid_chars = ':*?"<>|\\/'
    for char in invalid_chars:
        name = name.replace(char, '-')
    return name