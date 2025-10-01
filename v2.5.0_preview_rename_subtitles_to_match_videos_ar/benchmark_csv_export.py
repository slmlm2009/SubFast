#!/usr/bin/env python3
"""
Performance Benchmark: CSV Export Impact Analysis

Measures the performance impact of export_analysis_to_csv() on execution time.
Tests on Long_Anime scenario (1,145 files) to determine optimization strategy.
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

class CSVExportBenchmark:
    def __init__(self):
        self.base_dir = Path(os.getcwd())
        self.test_dir = self.base_dir / 'TESTS' / 'Long_Anime'
        self.script_path = self.base_dir / 'rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py'
        self.backup_dir = self.test_dir / 'Original_Testing_Files'
        
    def restore_test_data(self):
        """Restore Long_Anime test data from backup"""
        print("Restoring test data...")
        
        # Remove all files except Original_Testing_Files
        for item in self.test_dir.iterdir():
            if item.name != 'Original_Testing_Files':
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        
        # Restore from backup
        for item in self.backup_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, self.test_dir / item.name)
        
        print(f"Test data restored: {len(list(self.backup_dir.iterdir()))} files")
    
    def run_test_a_current(self):
        """Test A: Current implementation (both functions)"""
        print("\n" + "="*80)
        print("TEST A: Current Implementation (Export + Rename)")
        print("="*80)
        
        self.restore_test_data()
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            start = time.perf_counter()
            result = subprocess.run(
                [sys.executable, str(self.script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode == 0:
                print(f"[OK] Test A completed successfully")
                print(f"  Execution time: {elapsed:.4f} seconds")
                return elapsed
            else:
                print(f"[FAIL] Test A failed: {result.stderr}")
                return None
        finally:
            os.chdir(original_cwd)
    
    def run_test_b_export_only(self):
        """Test B: Export function only"""
        print("\n" + "="*80)
        print("TEST B: Export Function Only")
        print("="*80)
        
        self.restore_test_data()
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Create modified script that only runs export
            test_script = """
import sys
sys.path.insert(0, r'""" + str(self.base_dir) + """')
from rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking import export_analysis_to_csv
export_analysis_to_csv()
"""
            test_path = self.test_dir / 'test_export_only.py'
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_script)
            
            start = time.perf_counter()
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.perf_counter() - start
            
            test_path.unlink()  # Clean up
            
            if result.returncode == 0:
                print(f"[OK] Test B completed successfully")
                print(f"  Execution time: {elapsed:.4f} seconds")
                return elapsed
            else:
                print(f"[FAIL] Test B failed: {result.stderr}")
                return None
        finally:
            os.chdir(original_cwd)
    
    def run_test_c_rename_only(self):
        """Test C: Rename function only"""
        print("\n" + "="*80)
        print("TEST C: Rename Function Only")
        print("="*80)
        
        self.restore_test_data()
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Create modified script that only runs rename
            test_script = """
import sys
sys.path.insert(0, r'""" + str(self.base_dir) + """')
from rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking import rename_subtitles_to_match_videos
rename_subtitles_to_match_videos()
"""
            test_path = self.test_dir / 'test_rename_only.py'
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_script)
            
            start = time.perf_counter()
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.perf_counter() - start
            
            test_path.unlink()  # Clean up
            
            if result.returncode == 0:
                print(f"[OK] Test C completed successfully")
                print(f"  Execution time: {elapsed:.4f} seconds")
                return elapsed
            else:
                print(f"[FAIL] Test C failed: {result.stderr}")
                return None
        finally:
            os.chdir(original_cwd)
    
    def run_test_d_merged(self):
        """Test D: Merged function (optimized)"""
        print("\n" + "="*80)
        print("TEST D: Merged Function (Export + Rename in Single Pass)")
        print("="*80)
        
        self.restore_test_data()
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            merged_script = self.base_dir / 'rename_subtitles_to_match_videos_ar_optimized_merged.py'
            
            start = time.perf_counter()
            result = subprocess.run(
                [sys.executable, str(merged_script)],
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode == 0:
                print(f"[OK] Test D completed successfully")
                print(f"  Execution time: {elapsed:.4f} seconds")
                return elapsed
            else:
                print(f"[FAIL] Test D failed: {result.stderr}")
                return None
        finally:
            os.chdir(original_cwd)
    
    def run_phase_1_tests(self):
        """Run all Phase 1 baseline tests"""
        print("\n" + "#"*80)
        print("# PHASE 1: BASELINE PERFORMANCE TESTING")
        print("#"*80)
        
        results = {}
        
        # Run tests
        results['test_a'] = self.run_test_a_current()
        results['test_b'] = self.run_test_b_export_only()
        results['test_c'] = self.run_test_c_rename_only()
        
        return results
    
    def run_phase_2_test(self):
        """Run Phase 2 merged function test"""
        print("\n" + "#"*80)
        print("# PHASE 2: OPTIMIZED MERGED FUNCTION TEST")
        print("#"*80)
        
        return {'test_d': self.run_test_d_merged()}
    
    def generate_phase1_report(self, results):
        """Generate Phase 1 performance report"""
        print("\n" + "="*80)
        print("PHASE 1 RESULTS: BASELINE PERFORMANCE")
        print("="*80)
        
        if all(v is not None for v in results.values()):
            test_a = results['test_a']
            test_b = results['test_b']
            test_c = results['test_c']
            
            print(f"\nTest A (Current - Both):     {test_a:.4f} seconds")
            print(f"Test B (Export Only):        {test_b:.4f} seconds")
            print(f"Test C (Rename Only):        {test_c:.4f} seconds")
            
            # Calculate overhead
            if test_c > 0:
                csv_overhead = (test_b / test_c) * 100
                print(f"\nCSV Export Overhead:         {csv_overhead:.1f}% of rename time")
            
            sum_bc = test_b + test_c
            if test_a > 0:
                efficiency = (sum_bc / test_a) * 100
                print(f"Sum of B+C vs A:             {sum_bc:.4f}s vs {test_a:.4f}s ({efficiency:.1f}%)")
            
            # Analysis
            print("\n" + "-"*80)
            print("ANALYSIS:")
            print("-"*80)
            
            if csv_overhead < 20:
                print("[OK] CSV export overhead is MINIMAL (<20%)")
                print("  Recommendation: Keep current implementation")
            elif csv_overhead < 40:
                print("[WARNING] CSV export overhead is MODERATE (20-40%)")
                print("  Recommendation: Consider optimization if used frequently")
            else:
                print("[SIGNIFICANT] CSV export overhead is SIGNIFICANT (>40%)")
                print("  Recommendation: Optimize by merging functions")
            
            # Check for duplicate work
            if abs(test_a - sum_bc) < 0.050:  # Within 50ms
                print("\n[OK] Minimal overhead from running both functions")
                print("  (Test A approx Test B + Test C)")
            else:
                overhead_seconds = test_a - sum_bc
                print(f"\n[WARNING] Additional overhead detected: {overhead_seconds:.4f}s")
                print("  Possible causes: Script startup, imports, or I/O contention")
            
            return True
        else:
            print("\n[FAIL] Some tests failed. Cannot generate complete report.")
            return False

    def generate_phase2_report(self, phase1_results, phase2_results):
        """Generate Phase 2 performance report with full comparison"""
        print("\n" + "="*80)
        print("PHASE 2 RESULTS: MERGED FUNCTION COMPARISON")
        print("="*80)
        
        if phase2_results['test_d'] is not None:
            test_a = phase1_results['test_a']
            test_d = phase2_results['test_d']
            
            print(f"\nTest A (Current - Separate):  {test_a:.4f} seconds")
            print(f"Test D (Merged - Optimized):  {test_d:.4f} seconds")
            
            if test_a > 0:
                improvement = ((test_a - test_d) / test_a) * 100
                speedup = test_a / test_d
                
                print(f"\nPerformance Improvement:")
                if improvement > 0:
                    print(f"  {improvement:.1f}% faster ({speedup:.2f}x speedup)")
                    print(f"  Time saved: {(test_a - test_d)*1000:.1f}ms per run")
                else:
                    print(f"  {abs(improvement):.1f}% slower")
                    print(f"  Note: Merged version adds {(test_d - test_a)*1000:.1f}ms overhead")
                
                print("\n" + "-"*80)
                print("FINAL RECOMMENDATION:")
                print("-"*80)
                
                if improvement > 10:
                    print("[RECOMMENDED] Use MERGED version")
                    print(f"  - {improvement:.1f}% performance improvement")
                    print("  - Eliminates duplicate processing")
                    print("  - Single-pass design")
                elif improvement > 0:
                    print("[OPTIONAL] Merged version offers minor improvement")
                    print(f"  - {improvement:.1f}% faster (marginal)")
                    print("  - Current version is acceptable")
                else:
                    print("[KEEP CURRENT] Merged version shows no benefit")
                    print("  - Separate functions are clearer")
                    print("  - No performance penalty for separation")
            
            return True
        else:
            print("\n[FAIL] Test D failed. Cannot generate comparison.")
            return False

def main():
    print("="*80)
    print("CSV EXPORT PERFORMANCE BENCHMARK")
    print("Test Scenario: Long_Anime (1,145 files)")
    print("="*80)
    
    benchmark = CSVExportBenchmark()
    
    # Phase 1: Baseline tests
    phase1_results = benchmark.run_phase_1_tests()
    phase1_success = benchmark.generate_phase1_report(phase1_results)
    
    if not phase1_success:
        return 1
    
    print("\n" + "="*80)
    print("PHASE 1 COMPLETE")
    print("="*80)
    
    # Phase 2: Merged function test
    phase2_results = benchmark.run_phase_2_test()
    phase2_success = benchmark.generate_phase2_report(phase1_results, phase2_results)
    
    if phase2_success:
        print("\n" + "="*80)
        print("ALL TESTS COMPLETE")
        print("="*80)
    
    return 0 if (phase1_success and phase2_success) else 1

if __name__ == '__main__':
    sys.exit(main())
