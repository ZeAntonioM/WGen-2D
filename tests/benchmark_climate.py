import time
import numpy as np
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)


sys.path.append(project_root)


try:
    import settings
    from generation.climate_engine import ClimateEngine 
except ImportError as e:
    print("\nCRITICAL IMPORT ERROR")
    print(f"Could not find module: {e.name}")
    print(f"Python is looking in: {project_root}")
    sys.exit(1)


class MockTerrain:
    def get_terrain_at(self, x, y):
        # Return a simple generic height (0.5 = middle height)
        return 0.5

class MockWater:
    def get_water_level_at(self, x, y):
        # Constant sea level
        return 0.3

class MockWind:
    def get_wind_at(self, x, y):
        # Constant wind blowing North-East
        return (1.0, 1.0)

class MockRiver:
    def get_river_at(self, x, y):
        # No rivers for the benchmark
        return 0.0



def run_test(engine, label, step_size, iterations=50):
    print(f"Running: {label}...")
    
   
    original_step = settings.CLIMATE_STEP
    settings.CLIMATE_STEP = step_size
    
  
    engine.get_precipitation_map(0, 0)
    
    start_time = time.perf_counter()
    
    for i in range(iterations):
 
        engine.get_precipitation_map(i, i)
        
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    avg_ms = (total_time / iterations) * 1000.0
    
    print(f"  -> Total Time: {total_time:.4f}s")
    print(f"  -> Avg per Chunk: {avg_ms:.2f} ms")
    
  
    settings.CLIMATE_STEP = original_step
    return avg_ms


if __name__ == "__main__":
    print("=== CLIMATE ENGINE PERFORMANCE BENCHMARK ===")
    

    mock_terrain = MockTerrain()
    mock_water = MockWater()
    mock_wind = MockWind()
    mock_river = MockRiver()
    
   
    climate_engine = ClimateEngine(mock_terrain, mock_water, mock_wind, mock_river)
    
    print("\n[Test 1] Naive Tracing (High Quality)")
    print(f"Configuration: Step=1 (Tracing {settings.CHUNK_SIZE.x * settings.CHUNK_SIZE.y} pixels)")
    naive_time = run_test(climate_engine, "Naive Trace", 1, iterations=20)
    
    print("\n[Test 2] Optimized Tracing (Low Res + Upscale)")
    print(f"Configuration: Step=4 (Tracing reduced grid)")
    opt_time = run_test(climate_engine, "Optimized Trace", 4, iterations=100) # Run more iterations since it's faster
    
    print("\n" + "="*40)
    print("FINAL RESULTS")
    print("="*40)
    print(f"Naive Time:     {naive_time:.2f} ms")
    print(f"Optimized Time: {opt_time:.2f} ms")
    
    if opt_time > 0:
        speedup = naive_time / opt_time
        print(f"SPEEDUP FACTOR: {speedup:.2f}x")
    else:
        print("Speedup: Infinite (Optimized time was 0)")