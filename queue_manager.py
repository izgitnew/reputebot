#!/usr/bin/env python3
"""
Queue Manager for handling Bluesky API rate limits and request queuing.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

class RequestType(Enum):
    """Types of API requests."""
    POST_REPLY = "post_reply"
    GET_NOTIFICATIONS = "get_notifications"
    GET_AUTHOR_POSTS = "get_author_posts"
    GET_POST_THREAD = "get_post_thread"
    MARK_NOTIFICATION_READ = "mark_notification_read"

@dataclass
class QueuedRequest:
    """Represents a queued API request."""
    request_type: RequestType
    func: Callable
    args: tuple
    kwargs: dict
    priority: int = 1  # 1 = normal, 2 = high, 0 = low
    created_at: float = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class RateLimiter:
    """Handles rate limiting for different API endpoints."""
    
    def __init__(self):
        # Bluesky rate limits (approximate)
        self.limits = {
            RequestType.POST_REPLY: {"requests": 10, "window": 60},  # 10 posts per minute
            RequestType.GET_NOTIFICATIONS: {"requests": 30, "window": 60},  # 30 requests per minute
            RequestType.GET_AUTHOR_POSTS: {"requests": 20, "window": 60},  # 20 requests per minute
            RequestType.GET_POST_THREAD: {"requests": 30, "window": 60},  # 30 requests per minute
            RequestType.MARK_NOTIFICATION_READ: {"requests": 50, "window": 60},  # 50 requests per minute
        }
        
        # Track request timestamps
        self.request_history: Dict[RequestType, List[float]] = {
            request_type: [] for request_type in RequestType
        }
    
    def can_make_request(self, request_type: RequestType) -> bool:
        """Check if we can make a request without hitting rate limits."""
        if request_type not in self.limits:
            return True  # No limit specified
        
        limit = self.limits[request_type]
        current_time = time.time()
        
        # Clean old requests outside the window
        self.request_history[request_type] = [
            timestamp for timestamp in self.request_history[request_type]
            if current_time - timestamp < limit["window"]
        ]
        
        # Check if we're under the limit
        return len(self.request_history[request_type]) < limit["requests"]
    
    def record_request(self, request_type: RequestType):
        """Record that a request was made."""
        if request_type not in self.request_history:
            self.request_history[request_type] = []
        
        self.request_history[request_type].append(time.time())
    
    def get_wait_time(self, request_type: RequestType) -> float:
        """Get how long to wait before making the next request."""
        if request_type not in self.limits:
            return 0
        
        limit = self.limits[request_type]
        current_time = time.time()
        
        # Clean old requests
        self.request_history[request_type] = [
            timestamp for timestamp in self.request_history[request_type]
            if current_time - timestamp < limit["window"]
        ]
        
        if len(self.request_history[request_type]) < limit["requests"]:
            return 0
        
        # Find the oldest request in the window
        oldest_request = min(self.request_history[request_type])
        return (oldest_request + limit["window"]) - current_time

class QueueManager:
    """Manages queued requests with rate limiting."""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.request_queue: List[QueuedRequest] = []
        self.processing = False
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited_requests": 0,
        }
    
    async def add_request(
        self,
        request_type: RequestType,
        func: Callable,
        *args,
        priority: int = 1,
        **kwargs
    ) -> Any:
        """Add a request to the queue and wait for it to complete."""
        request = QueuedRequest(
            request_type=request_type,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority
        )
        
        # Add to queue (sorted by priority, then by creation time)
        self.request_queue.append(request)
        self.request_queue.sort(key=lambda x: (-x.priority, x.created_at))
        
        self.logger.info(f"Queued {request_type.value} request (priority: {priority})")
        
        # Start processing if not already running
        if not self.processing:
            asyncio.create_task(self._process_queue())
        
        # Wait for this specific request to complete
        return await self._wait_for_request(request)
    
    async def _wait_for_request(self, request: QueuedRequest) -> Any:
        """Wait for a specific request to complete."""
        while request in self.request_queue:
            await asyncio.sleep(0.1)
        
        # The request has been processed, return the result
        if hasattr(request, 'result'):
            return request.result
        elif hasattr(request, 'error'):
            raise request.error
        else:
            return None
    
    async def _process_queue(self):
        """Process the request queue with rate limiting."""
        self.processing = True
        
        while self.request_queue:
            request = self.request_queue[0]
            
            # Check rate limits
            if not self.rate_limiter.can_make_request(request.request_type):
                wait_time = self.rate_limiter.get_wait_time(request.request_type)
                self.logger.info(f"Rate limited, waiting {wait_time:.2f}s for {request.request_type.value}")
                await asyncio.sleep(wait_time)
                continue
            
            # Remove from queue
            self.request_queue.pop(0)
            
            # Execute the request
            try:
                self.stats["total_requests"] += 1
                self.rate_limiter.record_request(request.request_type)
                
                # Execute the function
                if asyncio.iscoroutinefunction(request.func):
                    result = await request.func(*request.args, **request.kwargs)
                else:
                    result = request.func(*request.args, **request.kwargs)
                
                request.result = result
                self.stats["successful_requests"] += 1
                self.logger.info(f"Successfully executed {request.request_type.value}")
                
            except Exception as e:
                self.stats["failed_requests"] += 1
                request.error = e
                self.logger.error(f"Failed to execute {request.request_type.value}: {e}")
                
                # Retry logic
                if request.retry_count < request.max_retries:
                    request.retry_count += 1
                    request.created_at = time.time()  # Reset creation time
                    self.request_queue.append(request)
                    self.request_queue.sort(key=lambda x: (-x.priority, x.created_at))
                    self.logger.info(f"Retrying {request.request_type.value} (attempt {request.retry_count})")
                    await asyncio.sleep(2 ** request.retry_count)  # Exponential backoff
                else:
                    self.logger.error(f"Max retries exceeded for {request.request_type.value}")
        
        self.processing = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            **self.stats,
            "queue_length": len(self.request_queue),
            "processing": self.processing,
        }
    
    def clear_queue(self):
        """Clear all pending requests."""
        self.request_queue.clear()
        self.logger.info("Queue cleared")

# Global queue manager instance
queue_manager = QueueManager() 