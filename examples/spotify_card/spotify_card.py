import pygment
import pygame


WIN_WIDTH, WIN_HEIGHT = 500, 650
COL_BACKGROUND  = (12,12,12)
COL_CARD_NORMAL = (20,20,20)
COL_CARD_HOVER  = (34,34,34)
COL_BUTTON_PLAY = (30,215,96)
COL_BUTTON_PLAY_HOVER = (40,225,106)


def card_enter_event(obj):
    obj.style.color = COL_CARD_HOVER
    obj.card_frame.card_image.button_play.style.hidden = False
    
    
def card_leave_event(obj):
    obj.style.color = COL_CARD_NORMAL
    obj.card_frame.card_image.button_play.style.hidden = True
    
    
def button_play_enter_event(obj):
    obj.style.color = COL_BUTTON_PLAY_HOVER
    obj.width = 74
    obj.height = 74
    
    
def button_play_leave_event(obj):
    obj.style.color = COL_BUTTON_PLAY 
    obj.width = 70
    obj.height = 70
    
    
# pygame initialization
pygame.init()
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()


# pygment layout
header = pygment.component.Frame("header", (0, 0, "100sw", 100))
header.style.color = "black"

header_label = pygment.component.Label("header_label", (40, 40, "100pw", 40))
header_label.style.text = "Header Text..."
header_label.join(header)

card = pygment.component.Button("card", ("50sw", "55sh", 300, 400))
card.style = {
    "color": COL_CARD_NORMAL,
    "border_radius": 10,
    "centered": True
}
card.on_mouse_enter = card_enter_event
card.on_mouse_leave = card_leave_event

card_content = pygment.component.Frame("card_frame", ("50pw", "50ph", "85pw", "88ph"))
card_content.style.centered = True
card_content.join(card)

image = pygment.component.Image("card_image", (0, 0, "100pw", "100pw"))
image.style.source = "examples\\spotify_card\\playlist_image.png"
image.join(card_content)

button_play = pygment.component.Button("button_play", ("80pw", "80ph", 70, 70))
button_play.style = {
    "color": COL_BUTTON_PLAY,
    "border_radius": 70,
    "centered": True,
    "hidden": True, 
}
button_play.on_mouse_click = lambda: print("Play button pressed!")
button_play.on_mouse_enter = button_play_enter_event
button_play.on_mouse_leave = button_play_leave_event
button_play.join(image)

text_frame = pygment.component.Frame("text_frame", (0, "110pw", "100pw", 70))
text_frame.join(card_content)

label_name = pygment.component.Label("card_name", (0, 0, "100pw", 24))
label_name.style.text = "Liked Songs"
label_name.join(text_frame)

label_desc = pygment.component.Label("card_desc", (0, 38, "100pw", 32))
label_desc.style = {
    "text": "274 songs",
    "text_size": 18,
    "text_color": (120, 120, 120)
}
label_desc.join(text_frame)


# pygment initialization
layout = (header, card)
renderer = pygment.ViewRenderer((WIN_WIDTH, WIN_HEIGHT), layout)


# application body
finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
        if event.type == pygame.VIDEORESIZE:
            renderer.size = display.get_size()
    
    dt = clock.tick(60)
    renderer.update(dt)
    
    display.fill(COL_BACKGROUND)
    renderer.render(display, (0,0))
    pygame.display.flip()
    