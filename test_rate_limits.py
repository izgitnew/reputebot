#!/usr/bin/env python3
"""
Test script to demonstrate rate limiting and queuing functionality.
"""

import asyncio
import time
from queue_manager import queue_manager, RequestType

async def test_rate_limiting():
    """Test the rate limiting functionality."""
    
    print("🧪 TESTING RATE LIMITING AND QUEUING\n")
    print("=" * 60)
    
    # Test 1: Basic queue functionality
    print("\n📋 Test 1: Basic Queue Functionality")
    print("-" * 40)
    
    async def dummy_function(name: str, delay: float = 0.1):
        """Dummy function that simulates API calls."""
        await asyncio.sleep(delay)
        print(f"✅ Executed: {name}")
        return f"Result from {name}"
    
    # Add multiple requests to the queue
    tasks = []
    for i in range(5):
        task = queue_manager.add_request(
            RequestType.GET_NOTIFICATIONS,
            dummy_function,
            f"Request {i+1}",
            0.2
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    print(f"📊 Results: {results}")
    
    # Test 2: Rate limiting simulation
    print("\n⏱️ Test 2: Rate Limiting Simulation")
    print("-" * 40)
    
    # Simulate rapid requests that should be rate limited
    print("Adding 15 rapid requests (limit is 10 per minute)...")
    
    start_time = time.time()
    tasks = []
    for i in range(15):
        task = queue_manager.add_request(
            RequestType.POST_REPLY,
            dummy_function,
            f"Post {i+1}",
            0.1
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    print(f"⏱️ Total time: {end_time - start_time:.2f} seconds")
    print(f"📊 Results: {len(results)} completed")
    
    # Test 3: Priority queuing
    print("\n🎯 Test 3: Priority Queuing")
    print("-" * 40)
    
    # Add requests with different priorities
    tasks = []
    
    # Low priority requests
    for i in range(3):
        task = queue_manager.add_request(
            RequestType.GET_AUTHOR_POSTS,
            dummy_function,
            f"Low Priority {i+1}",
            0.1,
            priority=0
        )
        tasks.append(task)
    
    # High priority requests
    for i in range(2):
        task = queue_manager.add_request(
            RequestType.POST_REPLY,
            dummy_function,
            f"High Priority {i+1}",
            0.1,
            priority=2
        )
        tasks.append(task)
    
    # Normal priority requests
    for i in range(2):
        task = queue_manager.add_request(
            RequestType.GET_NOTIFICATIONS,
            dummy_function,
            f"Normal Priority {i+1}",
            0.1,
            priority=1
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    print(f"📊 Results: {results}")
    
    # Test 4: Error handling and retries
    print("\n🔄 Test 4: Error Handling and Retries")
    print("-" * 40)
    
    async def failing_function(name: str, fail_count: int = 2):
        """Function that fails a few times before succeeding."""
        if not hasattr(failing_function, 'call_count'):
            failing_function.call_count = 0
        
        failing_function.call_count += 1
        print(f"🔄 Attempt {failing_function.call_count} for {name}")
        
        if failing_function.call_count <= fail_count:
            raise Exception(f"Simulated failure for {name}")
        
        print(f"✅ Success after {failing_function.call_count} attempts: {name}")
        return f"Success: {name}"
    
    try:
        result = await queue_manager.add_request(
            RequestType.GET_POST_THREAD,
            failing_function,
            "Failing Test",
            0.1
        )
        print(f"📊 Final result: {result}")
    except Exception as e:
        print(f"❌ Final failure: {e}")
    
    # Test 5: Queue statistics
    print("\n📊 Test 5: Queue Statistics")
    print("-" * 40)
    
    stats = queue_manager.get_stats()
    print("Queue Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

async def test_concurrent_requests():
    """Test concurrent requests to see how the queue handles them."""
    
    print("\n🚀 Test 6: Concurrent Requests")
    print("-" * 40)
    
    async def concurrent_function(name: str, delay: float = 0.5):
        """Function that simulates concurrent API calls."""
        print(f"🚀 Starting: {name}")
        await asyncio.sleep(delay)
        print(f"✅ Completed: {name}")
        return f"Completed: {name}"
    
    # Create many concurrent requests
    print("Creating 20 concurrent requests...")
    start_time = time.time()
    
    tasks = []
    for i in range(20):
        task = queue_manager.add_request(
            RequestType.GET_NOTIFICATIONS,
            concurrent_function,
            f"Concurrent {i+1}",
            0.3
        )
        tasks.append(task)
    
    # Wait for all to complete
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    print(f"⏱️ Total time: {end_time - start_time:.2f} seconds")
    print(f"📊 Completed: {len(results)} requests")
    
    # Show final statistics
    stats = queue_manager.get_stats()
    print(f"📈 Final stats: {stats['total_requests']} total, {stats['successful_requests']} success, {stats['failed_requests']} failed")

async def main():
    """Run all tests."""
    await test_rate_limiting()
    await test_concurrent_requests()
    
    print("\n🎉 All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 