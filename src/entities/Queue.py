from typing import List

class QueueItem:
  def __init__(self, origin: str, page: int):
    self.origin = origin
    self.page = page
    print(f"Item de fila criado: {self.origin}, ({self.page})")

class Queue:
  def __init__(self):
    self.items: List[QueueItem] = []

  def add_item(self, item: QueueItem):
    self.items.append(item)

  def remove_item(self, item: QueueItem):
    return self.items.remove(item)