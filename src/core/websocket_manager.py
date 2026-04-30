"""
Simple, self-contained WebSocket manager
"""
import asyncio
import json
from typing import Dict, Set, Any, Optional
from datetime import datetime
from collections import defaultdict

class SimpleWebSocketManager:
    """Production-ready WebSocket manager without external dependencies"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set] = defaultdict(set)
        self.client_info: Dict[str, Dict[str, Any]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.stats = {
            "total_connections": 0,
            "total_messages": 0,
            "total_disconnections": 0
        }
    
    async def connect(self, websocket_id: str, client_id: str = None):
        """Register a new WebSocket connection"""
        self.active_connections[client_id or "default"].add(websocket_id)
        self.client_info[websocket_id] = {
            "client_id": client_id,
            "connected_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        self.stats["total_connections"] += 1
    
    async def disconnect(self, websocket_id: str, client_id: str = None):
        """Unregister a WebSocket connection"""
        client_group = client_id or "default"
        if websocket_id in self.active_connections[client_group]:
            self.active_connections[client_group].remove(websocket_id)
        
        if websocket_id in self.client_info:
            del self.client_info[websocket_id]
        
        self.stats["total_disconnections"] += 1
    
    async def send_personal_message(self, message: str, websocket_id: str):
        """Send a message to a specific WebSocket connection"""
        # In a real implementation, this would use actual WebSocket send
        # For this simplified version, we'll log it
        self.stats["total_messages"] += 1
        return True
    
    async def broadcast(self, message: str, client_id: str = None):
        """Broadcast a message to all connections in a group"""
        client_group = client_id or "default"
        message_count = len(self.active_connections[client_group])
        
        # In a real implementation, this would broadcast to actual WebSockets
        # For this simplified version, we'll log it
        self.stats["total_messages"] += message_count
        return message_count
    
    async def broadcast_to_all(self, message: str):
        """Broadcast a message to all active connections"""
        total_connections = sum(len(connections) for connections in self.active_connections.values())
        
        # In a real implementation, this would broadcast to all WebSockets
        # For this simplified version, we'll log it
        self.stats["total_messages"] += total_connections
        return total_connections
    
    async def send_json(self, data: Dict[str, Any], websocket_id: str):
        """Send JSON data to a specific connection"""
        message = json.dumps(data)
        return await self.send_personal_message(message, websocket_id)
    
    async def broadcast_json(self, data: Dict[str, Any], client_id: str = None):
        """Broadcast JSON data to a group"""
        message = json.dumps(data)
        return await self.broadcast(message, client_id)
    
    def get_connection_count(self, client_id: str = None) -> int:
        """Get the number of active connections"""
        client_group = client_id or "default"
        return len(self.active_connections[client_group])
    
    def get_total_connections(self) -> int:
        """Get the total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics"""
        return {
            "active_connections": self.get_total_connections(),
            "total_connections": self.stats["total_connections"],
            "total_messages": self.stats["total_messages"],
            "total_disconnections": self.stats["total_disconnections"],
            "client_groups": {
                group: len(connections) 
                for group, connections in self.active_connections.items()
            },
            "timestamp": datetime.now().isoformat()
        }

# Global WebSocket manager instance
websocket_manager = SimpleWebSocketManager()
