import tkinter, tkinter.font as tkfont
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
FONT_SIZE = 12

FONTS = {} # for font cache

def get_font(size, weight, style):
  key = (size, weight, style)

  if key not in FONTS:
    font = tkfont.Font(size=size, weight=weight, slant=style)
    label = tkinter.Label(font=font)
    FONTS[key] = (font, label)

  return FONTS[key][0]

def lex(body):
  out = []
  buffer = ""
  in_tag = False

  for c in body:
    if c == "<":
      in_tag = True
      if buffer:
        out.append(Text(buffer))
      buffer = ""
    elif c == ">":
      in_tag = False
      out.append(Tag(buffer))
      buffer = ""
    else:
      buffer += c

  if not in_tag and buffer:
    out.append(Text(buffer))

  return out


class Tag:
  def __init__(self, tag):
    self.tag = tag

class Text:
  def __init__(self, text):
    self.text = text

class Layout:
  def __init__(self, tokens):
    self.display_list = []
    self.size = FONT_SIZE
    self.cursor_x, self.cursor_y = HSTEP, VSTEP
    self.weight, self.style = "normal", "roman"

    self.line = []
    for tok in tokens:
      self.token(tok)
    self.flush()

  def token(self, tok: Tag):
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.word(word)
    elif tok.tag == "small":
        self.size -= 2
    elif tok.tag == "/small":
        self.size += 2
    elif tok.tag == "big":
        self.size += 4
    elif tok.tag == "/big":
        self.size -= 4
    elif tok.tag == "i":
      self.style = "italic"
    elif tok.tag == "/i":
      self.style = "roman"
    elif tok.tag == "b":
      self.weight = "bold"
    elif tok.tag == "/b":
      self.weight = "normal"
    elif tok.tag == 'br':
      self.flush()
    elif tok.tag == '/p':
      self.flush()
      self.cursor_y += VSTEP

  def word(self, word):
    font = get_font(self.size, self.weight, self.style)
    w = font.measure(word)

    if self.cursor_x + w >= WIDTH - HSTEP:
      self.flush()
    self.line.append((self.cursor_x, word, font))
    self.cursor_x += w + font.measure(" ")

  def flush(self):
    if not self.line:
      return
    metrics = [font.metrics() for x, word, font in self.line]
    max_ascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.25 * max_ascent

    for x, word, font in self.line:
      y = baseline - font.metrics("ascent")
      self.display_list.append((x, y, word, font))

    max_descent = max([metric["descent"] for metric in metrics])
    self.cursor_y = baseline + 1.25 * max_descent
    self.cursor_x = HSTEP
    self.line = []





class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
    self.canvas.pack()

    self.scroll = 0
    self.window.bind("<Down>", self.scroll_down)
    self.window.bind("<Up>", self.scroll_up)

  def scroll_down(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  def scroll_up(self, e):
    self.scroll -= SCROLL_STEP
    self.draw()

  def draw(self):
    self.canvas.delete("all")
    for x, y, c, f in self.display_list:
      # 跳过屏幕外的字符绘制
      if y > self.scroll + HEIGHT: continue
      if y + f.metrics("linespace") < self.scroll: continue

      self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor="nw")

  def load(self, url: URL):
    body = url.request()
    tokens = lex(body)
    self.display_list = Layout(tokens).display_list
    self.draw()


if __name__ == "__main__":
  import sys

  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()
