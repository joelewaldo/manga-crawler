
class Metadata:
  def __init__(self, data: dict[str, str]):
    self.manga = data["manga"]
    self.chapter: int = int(data["chapter"])
    self.chapter_minor = data["chapter_minor"]
    self.lang = data["lang"]
    self.language = data["language"]