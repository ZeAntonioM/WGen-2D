
import math
import pygame
from pygame.math import Vector2


class Chunk():
    
    def __init__(self, tile_pos: Vector2, size: Vector2):
        """
        params:
         - tile_pos: Vector2 - the index of the chunk (tile_coordinate)
         - size: Vector2 - size of this chunk
        """
        self.tile_pos = tile_pos
        self.size = size
        
        self.surface = pygame.Surface(size)
        self.surface.fill((255, 0, 0))

    def get_corner_points(self) -> list[Vector2]:
        """ returns the four corner points of this chunk, given in world coordinates """
        return [Vector2((self.tile_pos.x + i) * self.size.x, (self.tile_pos.y+j) * self.size.y) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        self.surface.fill((0, 255, 0))
    
    def unload(self):
        self.surface.fill((255, 0, 0))
    
    @property
    def position(self):
        return self.tile_pos
            

class ChunkManager():
    CHUNK_SIZE = Vector2(16, 16)
    DISTANCE_FOR_LOADING_CHUNKS = 60
    DISTANCE_FOR_UNLOADING_CHUNKS = 90

    def __init__(self):
        self._chunks = dict() # mapping (x, y) in tile_coordinates to Chunk objects
        self._active_chunks = set() # subset of self._chunks
        
        assert(self.DISTANCE_FOR_LOADING_CHUNKS < self.DISTANCE_FOR_UNLOADING_CHUNKS)

    def update(self, camera_pos: Vector2):
        p = self.world_to_chunk(camera_pos)
        # chunk unloading
        self._unload_chunks_away_from_camera(camera_pos)
        # chunk loading
        self._load_chunks_near_camera(camera_pos)
            

    """ world_position gets rounded to get the position of the chunk it is inside of """
    def world_to_chunk(self, world_pos: Vector2) -> Vector2:
        return Vector2(world_pos.x // self.CHUNK_SIZE.x, world_pos.y // self.CHUNK_SIZE.y)
    
    def tile_to_world(self, tile_pos: Vector2) -> Vector2:
        return Vector2(tile_pos.x * self.CHUNK_SIZE.x, tile_pos.y * self.CHUNK_SIZE.y)

    def distance_to_chunk(self, pos: Vector2, tile_pos: Vector2) -> float:
        """ returns the distance of pos (world coordinates) to the tile specified by tile_pos.
        0 means inside or exactly on the border. """
        ### get corner points
        corner_points = Chunk(tile_pos, self.CHUNK_SIZE).get_corner_points()
        ### characterize the position
        x, y = 0, 0
        if all(p.x < pos.x for p in corner_points):
            x = 1
        if all(p.x > pos.x for p in corner_points):
            x = -1
        if all(p.y < pos.y for p in corner_points):
            y = 1
        if all(p.y > pos.y for p in corner_points):
            y = -1
        ### calculate the right distance
        if x == 0 and y == 0: return 0
        if x != 0 and y != 0: return min(pos.distance_to(p) for p in corner_points)
        if x == 0 and y != 0: return min(abs(pos.y - p.y) for p in corner_points)
        if x != 0 and y == 0: return min(abs(pos.x - p.x) for p in corner_points)

    @property
    def active_chunks(self) -> set[Chunk]:
        return self._active_chunks

    def _unload_chunks_away_from_camera(self, camera_pos):
        for c in self._active_chunks.copy():
            if self.distance_to_chunk(camera_pos, c.position) >= self.DISTANCE_FOR_UNLOADING_CHUNKS:
                c.unload()
                self._active_chunks.remove(c)

    def _load_chunks_near_camera(self, camera_pos: Vector2):
        camera_tile = self.world_to_chunk(camera_pos)
        # get the tile positions for all chunks in radius of DISTANCE_FOR_LOADING_CHUNKS
        tile_positions = []
        num_chunks_x_dir = math.ceil(self.DISTANCE_FOR_LOADING_CHUNKS / self.CHUNK_SIZE.x)+2 # +2 for safety, if they are too far away, they'll be removed in next step
        num_chunks_y_dir = math.ceil(self.DISTANCE_FOR_LOADING_CHUNKS / self.CHUNK_SIZE.y)+2
        for x in range(-num_chunks_x_dir, num_chunks_x_dir):
            for y in range(-num_chunks_y_dir, num_chunks_y_dir):
                chunk_pos = Vector2(x, y) + camera_tile
                if self.distance_to_chunk(camera_pos, chunk_pos) <= self.DISTANCE_FOR_LOADING_CHUNKS:
                    tile_positions.append(chunk_pos)
        # do the chunk loading
        for p in tile_positions:
            if tuple(p) in self._chunks:
                c = self._chunks[tuple(p)]
            else:
                self._chunks[tuple(p)] = c = Chunk(p, self.CHUNK_SIZE)
            if not c in self._active_chunks:
                c.load()
                self._active_chunks.add(c)
        
def tests():
    size = Vector2(100, 50)
    m = ChunkManager()
    prev_chunk_size = m.CHUNK_SIZE.copy()
    m.CHUNK_SIZE = size
    c = Chunk(Vector2(1, 0), m.CHUNK_SIZE)
    c.load()
    c.unload()
    c.load()
    assert c.get_corner_points() == [Vector2(size.x,0), size, Vector2(size.x*2, 0), Vector2(size.x*2, size.y)]
    assert m.distance_to_chunk(Vector2(0, 0), c.position) == size.x
    assert m.distance_to_chunk(Vector2(0, size.y*0.5), c.position) == size.x
    assert m.distance_to_chunk(Vector2(0, size.y*3), c.position) == math.sqrt(size.x**2 + (size.y*2)**2)
    m.CHUNK_SIZE = prev_chunk_size
    c = Chunk(Vector2(1, 0), m.CHUNK_SIZE)
    if 0: # visual test for distance to chunk
        d = pygame.display.set_mode((400, 100))
        d.blit(c.surface, m.tile_to_world(c.position)+Vector2(0, 50))
        for x in range(d.get_width()):
            for y in range(-d.get_height(), d.get_height()):
                if 10 <= m.distance_to_chunk(Vector2(x, y), c.position) <= 12:
                    d.set_at((x, y+50), (255, 255, 0))
        pygame.display.update()
        input("press enter to resume...")
    print("all tests passed")

def open_visuals():
    d = pygame.display.set_mode((1000, 500))
    camera_pos = Vector2(500, 250)
    m = ChunkManager()
    m.CHUNK_SIZE = Vector2(60, 40)
    running = True
    grid = pygame.Surface(d.get_size())
    for x in range(int(grid.get_width()//m.CHUNK_SIZE.x)+1):
        pygame.draw.line(grid, (100, 100, 100), (x*m.CHUNK_SIZE.x, 0), (x*m.CHUNK_SIZE.x, grid.get_height()), 3)
    for y in range(int(grid.get_height()//m.CHUNK_SIZE.y)+1):
        pygame.draw.line(grid, (100, 100, 100), (0, y*m.CHUNK_SIZE.y), (grid.get_width(), y*m.CHUNK_SIZE.y), 3)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(m._chunks)
                print(m._active_chunks)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: camera_pos.x -= 10
                if event.key == pygame.K_RIGHT: camera_pos.x += 10
                if event.key == pygame.K_UP: camera_pos.y -= 10
                if event.key == pygame.K_DOWN: camera_pos.y += 10
        #update
        m.update(camera_pos)
        # draw
        d.blit(grid, (0,0))
        for c in m._chunks.values():
            d.blit(c.surface, m.tile_to_world
                   (c.position))
        pygame.draw.circle(d,(0, 0, 255), camera_pos, 4)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    tests()
    open_visuals()
