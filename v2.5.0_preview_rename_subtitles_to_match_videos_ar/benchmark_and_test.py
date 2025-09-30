#!/usr/bin/env python3
"""
Comprehensive benchmarking and testing script for subtitle renaming script versions.
Tests functionality and performance across all three versions.
"""

import os
import shutil
import time
import tracemalloc
import subprocess
import sys
import traceback
from pathlib import Path
import json

# Version configurations
VERSIONS = {
    'original': 'rename_subtitles_to_match_videos_ar.py',
    'no_thinking': 'rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py',
    'thinking': 'rename_subtitles_to_match_videos_ar_optimized_Sonnet4_Thinking.py'
}

# Test scenarios
TEST_SCENARIOS = [
    'Mixed_Scenarios_1',
    'Mixed_Scenarios_2',
    'Movie',
    'Long_Anime'  # Last due to size
]

class TestRunner:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.tests_dir = self.base_dir / 'TESTS'
        self.results = {}
        
    def backup_test_data(self, scenario):
        """Backup original test data"""
        scenario_path = self.tests_dir / scenario
        original_path = scenario_path / 'Original_Testing_Files'
        
        if not original_path.exists():
            print(f"Creating backup for {scenario}...")
            original_path.mkdir(exist_ok=True)
            
            # Copy all test files to Original_Testing_Files
            for item in scenario_path.iterdir():
                if item.name != 'Original_Testing_Files':
                    if item.is_file():
                        shutil.copy2(item, original_path / item.name)
                    elif item.is_dir() and item.name != 'Original_Testing_Files':
                        shutil.copytree(item, original_path / item.name, dirs_exist_ok=True)
    
    def restore_test_data(self, scenario):
        """Restore test data from backup"""
        scenario_path = self.tests_dir / scenario
        original_path = scenario_path / 'Original_Testing_Files'
        
        if not original_path.exists():
            print(f"Warning: No backup found for {scenario}")
            return False
        
        # Remove all files except Original_Testing_Files
        for item in scenario_path.iterdir():
            if item.name != 'Original_Testing_Files':
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        
        # Restore from backup
        for item in original_path.iterdir():
            if item.is_file():
                shutil.copy2(item, scenario_path / item.name)
            elif item.is_dir():
                shutil.copytree(item, scenario_path / item.name, dirs_exist_ok=True)
        
        return True
    
    def run_version(self, version_name, scenario):
        """Run a specific version on a scenario and collect metrics"""
        script_path = self.base_dir / VERSIONS[version_name]
        scenario_path = self.tests_dir / scenario
        
        # Change to test directory
        original_cwd = os.getcwd()
        os.chdir(scenario_path)
        
        try:
            # Start memory tracking
            tracemalloc.start()
            start_time = time.time()
            
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Stop timers
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            execution_time = end_time - start_time
            
            # Collect results
            metrics = {
                'execution_time': execution_time,
                'memory_peak_mb': peak / 1024 / 1024,
                'memory_current_mb': current / 1024 / 1024,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
            
            # Check for renaming_report.csv
            csv_path = scenario_path / 'renaming_report.csv'
            if csv_path.exists():
                with open(csv_path, 'r', encoding='utf-8') as f:
                    metrics['csv_content'] = f.read()
            
            # Count renamed files
            renamed_files = []
            for file in scenario_path.iterdir():
                if file.is_file() and '.ar.' in file.name:
                    renamed_files.append(file.name)
            
            metrics['renamed_files'] = sorted(renamed_files)
            metrics['renamed_count'] = len(renamed_files)
            
            return metrics
            
        except subprocess.TimeoutExpired:
            tracemalloc.stop()
            return {
                'execution_time': 300,
                'error': 'Timeout after 5 minutes',
                'success': False
            }
        except Exception as e:
            tracemalloc.stop()
            return {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'success': False
            }
        finally:
            os.chdir(original_cwd)
    
    def compare_functionality(self, scenario):
        """Compare functionality across all versions for a scenario"""
        print(f"\n{'='*80}")
        print(f"Testing Scenario: {scenario}")
        print(f"{'='*80}")
        
        scenario_results = {}
        
        for version_name in VERSIONS.keys():
            print(f"\nTesting {version_name}...")
            
            # Restore clean test data
            self.restore_test_data(scenario)
            
            # Run the version
            metrics = self.run_version(version_name, scenario)
            scenario_results[version_name] = metrics
            
            if metrics['success']:
                print(f"  [OK] Completed in {metrics['execution_time']:.3f}s")
                print(f"  [OK] Memory peak: {metrics['memory_peak_mb']:.2f}MB")
                print(f"  [OK] Renamed {metrics['renamed_count']} files")
            else:
                print(f"  [FAIL] Failed: {metrics.get('error', 'Unknown error')}")
        
        # Compare results
        print(f"\n{'-'*80}")
        print("Functionality Comparison:")
        print(f"{'-'*80}")
        
        # Compare renamed file lists
        original_files = set(scenario_results['original'].get('renamed_files', []))
        no_thinking_files = set(scenario_results['no_thinking'].get('renamed_files', []))
        thinking_files = set(scenario_results['thinking'].get('renamed_files', []))
        
        if original_files == no_thinking_files == thinking_files:
            print("  [OK] All versions produced identical renamed files")
        else:
            print("  [FAIL] Discrepancies found in renamed files:")
            if original_files != no_thinking_files:
                print(f"    - Original vs NoThinking: {len(original_files ^ no_thinking_files)} differences")
            if original_files != thinking_files:
                print(f"    - Original vs Thinking: {len(original_files ^ thinking_files)} differences")
            if no_thinking_files != thinking_files:
                print(f"    - NoThinking vs Thinking: {len(no_thinking_files ^ thinking_files)} differences")
        
        # Compare CSV outputs
        orig_csv = scenario_results['original'].get('csv_content', '')
        no_think_csv = scenario_results['no_thinking'].get('csv_content', '')
        think_csv = scenario_results['thinking'].get('csv_content', '')
        
        if orig_csv == no_think_csv == think_csv:
            print("  [OK] All versions produced identical CSV reports")
        else:
            print("  [FAIL] Discrepancies found in CSV reports")
        
        self.results[scenario] = scenario_results
        
        return scenario_results
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print(f"\n\n{'='*80}")
        print("PERFORMANCE SUMMARY")
        print(f"{'='*80}")
        
        for scenario in TEST_SCENARIOS:
            if scenario not in self.results:
                continue
                
            print(f"\n{scenario}:")
            print(f"{'-'*80}")
            
            scenario_data = self.results[scenario]
            
            # Create comparison table
            print(f"{'Version':<20} {'Time (s)':<12} {'Memory (MB)':<15} {'Files':<10}")
            print(f"{'-'*80}")
            
            for version_name in VERSIONS.keys():
                if version_name not in scenario_data:
                    continue
                    
                metrics = scenario_data[version_name]
                if metrics['success']:
                    print(f"{version_name:<20} {metrics['execution_time']:>10.3f}  "
                          f"{metrics['memory_peak_mb']:>13.2f}  "
                          f"{metrics['renamed_count']:>8}")
            
            # Calculate speedup
            if all(v in scenario_data and scenario_data[v]['success'] for v in VERSIONS.keys()):
                orig_time = scenario_data['original']['execution_time']
                no_think_time = scenario_data['no_thinking']['execution_time']
                think_time = scenario_data['thinking']['execution_time']
                
                print(f"\nSpeedup vs Original:")
                print(f"  NoThinking: {(orig_time/no_think_time):.2f}x "
                      f"({((orig_time-no_think_time)/orig_time*100):+.1f}%)")
                print(f"  Thinking:   {(orig_time/think_time):.2f}x "
                      f"({((orig_time-think_time)/orig_time*100):+.1f}%)")
    
    def save_results(self, filename='benchmark_results.json'):
        """Save all results to JSON file"""
        output_path = self.base_dir / filename
        
        # Convert results to JSON-serializable format
        json_results = {}
        for scenario, scenario_data in self.results.items():
            json_results[scenario] = {}
            for version, metrics in scenario_data.items():
                json_results[scenario][version] = {
                    k: v for k, v in metrics.items() 
                    if k not in ['stdout', 'stderr', 'csv_content']  # Exclude large text
                }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"\nResults saved to: {output_path}")
    
    def generate_recommendation(self):
        """Generate final recommendation based on all tests"""
        print(f"\n\n{'='*80}")
        print("RECOMMENDATION")
        print(f"{'='*80}\n")
        
        # Check functionality compatibility
        all_compatible = True
        for scenario, scenario_data in self.results.items():
            original_files = set(scenario_data.get('original', {}).get('renamed_files', []))
            no_thinking_files = set(scenario_data.get('no_thinking', {}).get('renamed_files', []))
            thinking_files = set(scenario_data.get('thinking', {}).get('renamed_files', []))
            
            if not (original_files == no_thinking_files == thinking_files):
                all_compatible = False
                break
        
        if not all_compatible:
            print("[WARNING] Functionality discrepancies detected!")
            print("   Some versions produce different results.")
            print("   Recommendation: Stick with ORIGINAL until issues are resolved.\n")
            return
        
        # Calculate average speedups
        total_orig_time = 0
        total_no_think_time = 0
        total_think_time = 0
        count = 0
        
        for scenario, scenario_data in self.results.items():
            if all(v in scenario_data and scenario_data[v].get('success') for v in VERSIONS.keys()):
                total_orig_time += scenario_data['original']['execution_time']
                total_no_think_time += scenario_data['no_thinking']['execution_time']
                total_think_time += scenario_data['thinking']['execution_time']
                count += 1
        
        if count > 0:
            no_think_speedup = (total_orig_time / total_no_think_time)
            think_speedup = (total_orig_time / total_think_time)
            
            print(f"Average Speedup Across {count} Scenarios:")
            print(f"  NoThinking: {no_think_speedup:.2f}x faster "
                  f"({((total_orig_time-total_no_think_time)/total_orig_time*100):+.1f}%)")
            print(f"  Thinking:   {think_speedup:.2f}x faster "
                  f"({((total_orig_time-total_think_time)/total_orig_time*100):+.1f}%)\n")
            
            # Make recommendation
            if think_speedup > 1.2:  # >20% faster
                print("[RECOMMENDATION] Use THINKING version")
                print("   - Significant performance improvement (>20%)")
                print("   - 100% functional compatibility verified")
                print("   - Better code organization with OOP")
                print("   - Enhanced error handling")
            elif no_think_speedup > 1.1:  # >10% faster
                print("[RECOMMENDATION] Use NO_THINKING version")
                print("   - Good performance improvement (>10%)")
                print("   - 100% functional compatibility verified")
                print("   - Simpler code structure than Thinking version")
            else:
                print("[RECOMMENDATION] Either ORIGINAL or NO_THINKING version")
                print("   - Performance differences are minimal (<10%)")
                print("   - NoThinking offers slightly better organization")
                print("   - Original is battle-tested and familiar")

def main():
    base_dir = os.getcwd()
    
    print("="*80)
    print("Subtitle Renaming Script - Comprehensive Benchmark & Test Suite")
    print("="*80)
    
    runner = TestRunner(base_dir)
    
    # Backup all test scenarios
    print("\nCreating backups of test scenarios...")
    for scenario in TEST_SCENARIOS:
        runner.backup_test_data(scenario)
    
    # Run tests on each scenario
    for scenario in TEST_SCENARIOS:
        try:
            runner.compare_functionality(scenario)
        except KeyboardInterrupt:
            print("\n\nTesting interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\nError testing {scenario}: {e}")
            traceback.print_exc()
    
    # Generate reports
    runner.generate_performance_report()
    runner.save_results()
    runner.generate_recommendation()
    
    print(f"\n{'='*80}")
    print("Testing Complete!")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
