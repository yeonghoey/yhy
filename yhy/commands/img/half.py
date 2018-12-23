from yhy.core.img import clipboard_img, copy


def command():
    img, _ = clipboard_img(half=True)
    copy(img)
