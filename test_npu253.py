#!/usr/bin/env python3
"""
NPU-253 Test Suite

Comprehensive tests for the Pattern Coprocessor Driver.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from npu253 import (
    PatternCoprocessorDriver,
    NPUConfig,
    PatternMetadata,
    ArchetypalPattern,
    CMD_RESET,
    CMD_LOAD_PATTERNS,
    CMD_SELF_TEST,
    STATUS_IDLE,
    STATUS_PATTERNS_LOADED,
    STATUS_SELF_TEST_OK,
    ERR_NONE,
    ERR_PATTERN_NOT_FOUND,
    ERR_INVALID_DOMAIN,
    ERR_NOT_LOADED,
)


class TestNPU253Registers(unittest.TestCase):
    """Test MMIO register operations"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False)
        self.npu = PatternCoprocessorDriver(config)
    
    def test_write_read_reg32(self):
        """Test 32-bit register write/read"""
        test_val = 0x12345678
        self.npu.write_reg32(0x08, test_val)
        result = self.npu.read_reg32(0x08)
        self.assertEqual(result, test_val)
    
    def test_write_read_reg64(self):
        """Test 64-bit register write/read"""
        test_val = 0x123456789ABCDEF0
        self.npu.write_reg64(0x10, test_val)
        result = self.npu.read_reg64(0x10)
        self.assertEqual(result, test_val)
    
    def test_initial_status(self):
        """Test initial register state"""
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_IDLE)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_NONE)


class TestNPU253Loading(unittest.TestCase):
    """Test pattern loading"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False)
        self.npu = PatternCoprocessorDriver(config)
    
    def test_load_patterns(self):
        """Test pattern loading"""
        result = self.npu.load()
        self.assertTrue(result)
        
        # Check status
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_PATTERNS_LOADED)
        
        # Check pattern count
        count = self.npu.read_reg32(0x0C)
        self.assertEqual(count, len(self.npu.patterns))
    
    def test_probe_device(self):
        """Test device probe"""
        result = self.npu.probe()
        self.assertTrue(result)
    
    def test_initialize(self):
        """Test device initialization"""
        result = self.npu.initialize()
        self.assertTrue(result)
        
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_SELF_TEST_OK)


class TestNPU253Queries(unittest.TestCase):
    """Test pattern query operations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixture once for all tests"""
        config = NPUConfig(verbose=False)
        cls.npu = PatternCoprocessorDriver(config)
        cls.npu.load()
    
    def test_query_by_id_valid(self):
        """Test querying pattern by valid ID"""
        pattern = self.npu.query_by_id(1)
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.pattern_id, 1)
        self.assertIsInstance(pattern, PatternMetadata)
    
    def test_query_by_id_invalid(self):
        """Test querying pattern by invalid ID"""
        pattern = self.npu.query_by_id(9999)
        self.assertIsNone(pattern)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_PATTERN_NOT_FOUND)
    
    def test_query_by_name_valid(self):
        """Test querying pattern by valid name"""
        # First get a pattern to know a valid name
        ref_pattern = self.npu.query_by_id(1)
        if ref_pattern:
            pattern = self.npu.query_by_name(ref_pattern.name)
            self.assertIsNotNone(pattern)
            self.assertEqual(pattern.name, ref_pattern.name)
    
    def test_query_by_name_invalid(self):
        """Test querying pattern by invalid name"""
        pattern = self.npu.query_by_name("NonexistentPattern12345")
        self.assertIsNone(pattern)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_PATTERN_NOT_FOUND)
    
    def test_query_by_text(self):
        """Test full-text search"""
        results = self.npu.query_by_text("community")
        self.assertIsInstance(results, list)
        # Should find at least one pattern
        self.assertGreater(len(results), 0)
        
        # Check result count register
        count = self.npu.read_reg32(0x24)
        self.assertEqual(count, len(results))


class TestNPU253Navigation(unittest.TestCase):
    """Test pattern relationship navigation"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixture once for all tests"""
        config = NPUConfig(verbose=False)
        cls.npu = PatternCoprocessorDriver(config)
        cls.npu.load()
    
    def test_get_preceding_patterns(self):
        """Test getting preceding patterns"""
        # Pattern 1 might not have preceding patterns
        # Try with a higher number
        results = self.npu.get_preceding_patterns(10)
        self.assertIsInstance(results, list)
    
    def test_get_following_patterns(self):
        """Test getting following patterns"""
        results = self.npu.get_following_patterns(1)
        self.assertIsInstance(results, list)
        # First pattern should have following patterns
        self.assertGreater(len(results), 0)
    
    def test_navigation_invalid_id(self):
        """Test navigation with invalid pattern ID"""
        results = self.npu.get_preceding_patterns(9999)
        self.assertEqual(len(results), 0)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_PATTERN_NOT_FOUND)


class TestNPU253Categories(unittest.TestCase):
    """Test category queries"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixture once for all tests"""
        config = NPUConfig(verbose=False)
        cls.npu = PatternCoprocessorDriver(config)
        cls.npu.load()
    
    def test_get_category_towns(self):
        """Test getting towns category"""
        results = self.npu.get_category("towns")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # All patterns should be in range 1-94
        for p in results:
            self.assertGreaterEqual(p.pattern_id, 1)
            self.assertLessEqual(p.pattern_id, 94)
    
    def test_get_category_buildings(self):
        """Test getting buildings category"""
        results = self.npu.get_category("buildings")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # All patterns should be in range 95-204
        for p in results:
            self.assertGreaterEqual(p.pattern_id, 95)
            self.assertLessEqual(p.pattern_id, 204)
    
    def test_get_category_construction(self):
        """Test getting construction category"""
        results = self.npu.get_category("construction")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # All patterns should be in range 205-253
        for p in results:
            self.assertGreaterEqual(p.pattern_id, 205)
            self.assertLessEqual(p.pattern_id, 253)
    
    def test_get_category_invalid(self):
        """Test getting invalid category"""
        results = self.npu.get_category("invalid_category")
        self.assertEqual(len(results), 0)


class TestNPU253Sequences(unittest.TestCase):
    """Test pattern sequences"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixture once for all tests"""
        config = NPUConfig(verbose=False)
        cls.npu = PatternCoprocessorDriver(config)
        cls.npu.load()
    
    def test_get_sequence_valid(self):
        """Test getting valid sequence"""
        results = self.npu.get_sequence(1)
        self.assertIsInstance(results, list)
        # Sequences should have patterns
        self.assertGreater(len(results), 0)
    
    def test_get_sequence_invalid(self):
        """Test getting invalid sequence"""
        results = self.npu.get_sequence(9999)
        self.assertEqual(len(results), 0)


class TestNPU253Transformation(unittest.TestCase):
    """Test archetypal pattern domain transformation"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixture once for all tests"""
        config = NPUConfig(verbose=False)
        cls.npu = PatternCoprocessorDriver(config)
        cls.npu.load()
    
    def test_transform_valid_domains(self):
        """Test transformation to all valid domains"""
        if not self.npu.archetypal_patterns:
            self.skipTest("No archetypal patterns loaded")
        
        pattern_id = list(self.npu.archetypal_patterns.keys())[0]
        
        domains = ["physical", "social", "conceptual", "psychic"]
        for domain in domains:
            result = self.npu.transform_pattern(pattern_id, domain)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
    
    def test_transform_invalid_domain(self):
        """Test transformation to invalid domain"""
        if not self.npu.archetypal_patterns:
            self.skipTest("No archetypal patterns loaded")
        
        pattern_id = list(self.npu.archetypal_patterns.keys())[0]
        result = self.npu.transform_pattern(pattern_id, "invalid_domain")
        self.assertIsNone(result)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_INVALID_DOMAIN)
    
    def test_transform_invalid_pattern(self):
        """Test transformation with invalid pattern ID"""
        result = self.npu.transform_pattern("invalid_id_9999", "physical")
        self.assertIsNone(result)
        
        error = self.npu.read_reg32(0x34)
        self.assertEqual(error, ERR_PATTERN_NOT_FOUND)


class TestNPU253Cache(unittest.TestCase):
    """Test pattern caching"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False, enable_cache=True, cache_size=10)
        self.npu = PatternCoprocessorDriver(config)
        self.npu.load()
    
    def test_cache_hit(self):
        """Test cache hit"""
        # Query pattern twice
        pattern1 = self.npu.query_by_id(1)
        initial_hits = self.npu.telemetry.cache_hits
        
        pattern2 = self.npu.query_by_id(1)
        final_hits = self.npu.telemetry.cache_hits
        
        # Second query should hit cache
        self.assertEqual(pattern1.pattern_id, pattern2.pattern_id)
        self.assertGreater(final_hits, initial_hits)
    
    def test_cache_size_limit(self):
        """Test cache size limit"""
        # Query more patterns than cache size
        for i in range(1, 20):
            if i in self.npu.patterns:
                self.npu.query_by_id(i)
        
        # Cache should not exceed size limit
        self.assertLessEqual(len(self.npu.cache), self.npu.cache_size)


class TestNPU253Telemetry(unittest.TestCase):
    """Test telemetry and diagnostics"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False, enable_telemetry=True)
        self.npu = PatternCoprocessorDriver(config)
        self.npu.load()
    
    def test_query_telemetry(self):
        """Test query telemetry tracking"""
        initial_queries = self.npu.telemetry.total_queries
        
        self.npu.query_by_id(1)
        self.npu.query_by_id(2)
        
        final_queries = self.npu.telemetry.total_queries
        self.assertEqual(final_queries, initial_queries + 2)
    
    def test_transform_telemetry(self):
        """Test transformation telemetry tracking"""
        if not self.npu.archetypal_patterns:
            self.skipTest("No archetypal patterns loaded")
        
        initial_transforms = self.npu.telemetry.total_transformations
        
        pattern_id = list(self.npu.archetypal_patterns.keys())[0]
        self.npu.transform_pattern(pattern_id, "physical")
        
        final_transforms = self.npu.telemetry.total_transformations
        self.assertEqual(final_transforms, initial_transforms + 1)
    
    def test_get_telemetry(self):
        """Test getting telemetry data"""
        telemetry = self.npu.get_telemetry()
        
        self.assertIsNotNone(telemetry)
        self.assertGreaterEqual(telemetry.uptime_seconds, 0)
    
    def test_hardware_diagnostics(self):
        """Test hardware diagnostics"""
        diag = self.npu.get_hardware_diagnostics()
        
        self.assertIsInstance(diag, str)
        self.assertGreater(len(diag), 0)
        self.assertIn("NPU-253", diag)


class TestNPU253SelfTest(unittest.TestCase):
    """Test self-test functionality"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False)
        self.npu = PatternCoprocessorDriver(config)
        self.npu.load()
    
    def test_self_test_pass(self):
        """Test that self-test passes"""
        result = self.npu.run_self_test()
        self.assertTrue(result)
        
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_SELF_TEST_OK)
    
    def test_device_status_string(self):
        """Test device status string generation"""
        status_str = self.npu.get_device_status()
        
        self.assertIsInstance(status_str, str)
        self.assertGreater(len(status_str), 0)


class TestNPU253Commands(unittest.TestCase):
    """Test command interface"""
    
    def setUp(self):
        """Set up test fixture"""
        config = NPUConfig(verbose=False)
        self.npu = PatternCoprocessorDriver(config)
    
    def test_send_command_reset(self):
        """Test reset command"""
        self.npu.load()
        result = self.npu.send_command(CMD_RESET)
        self.assertTrue(result)
        
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_IDLE)
    
    def test_send_command_load(self):
        """Test load patterns command"""
        result = self.npu.send_command(CMD_LOAD_PATTERNS)
        self.assertTrue(result)
        
        status = self.npu.read_reg32(0x04)
        self.assertTrue(status & STATUS_PATTERNS_LOADED)
    
    def test_send_command_self_test(self):
        """Test self-test command"""
        self.npu.load()
        result = self.npu.send_command(CMD_SELF_TEST)
        self.assertTrue(result)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Registers))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Loading))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Queries))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Navigation))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Categories))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Sequences))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Transformation))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Cache))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Telemetry))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253SelfTest))
    suite.addTests(loader.loadTestsFromTestCase(TestNPU253Commands))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
