import chunk_management
from chunk_management import *


size = Vector2(100, 50)
chunk_management.CHUNK_SIZE = size
c = Chunk(Vector2(1, 0))
c.load()
assert c.get_corner_points() == [Vector2(size.x,0), size, Vector2(size.x*2, 0), Vector2(size.x*2, size.y)]
assert distance_to_chunk(Vector2(0, 0), c.position) == size.x
assert distance_to_chunk(Vector2(0, size.y*0.5), c.position) == size.x
assert distance_to_chunk(Vector2(0, size.y*3), c.position) == math.sqrt(size.x**2 + (size.y*2)**2)
c = Chunk(Vector2(1, 0))
if 0: # visual test for distance to chunk
    d = pygame.display.set_mode((400, 100))
    d.blit(c.surface, tile_to_world(c.position)+Vector2(0, 50))
    for x in range(d.get_width()):
        for y in range(-d.get_height(), d.get_height()):
            if 10 <= distance_to_chunk(Vector2(x, y), c.position) <= 12:
                d.set_at((x, y+50), (255, 255, 0))
    pygame.display.update()
    input("press enter to resume...")
print("all tests passed")
