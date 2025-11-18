"""
WebSocket connection manager for real-time chat
"""

from typing import Dict, List
from fastapi import WebSocket
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections for real-time communication"""

    def __init__(self):
        # Dictionary mapping user_id to list of WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # Dictionary mapping conversation_id to list of connected user_ids
        self.conversation_participants: Dict[int, List[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, conversation_id: int):
        """Connect a user to a conversation"""
        await websocket.accept()

        # Add connection to active connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

        # Add user to conversation participants
        if conversation_id not in self.conversation_participants:
            self.conversation_participants[conversation_id] = []
        if user_id not in self.conversation_participants[conversation_id]:
            self.conversation_participants[conversation_id].append(user_id)

        logger.info(f"User {user_id} connected to conversation {conversation_id}")

    def disconnect(self, websocket: WebSocket, user_id: int, conversation_id: int):
        """Disconnect a user from a conversation"""
        # Remove connection
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        # Remove user from conversation participants
        if conversation_id in self.conversation_participants:
            if user_id in self.conversation_participants[conversation_id]:
                self.conversation_participants[conversation_id].remove(user_id)
            if not self.conversation_participants[conversation_id]:
                del self.conversation_participants[conversation_id]

        logger.info(f"User {user_id} disconnected from conversation {conversation_id}")

    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to a specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send message to user {user_id}: {e}")

    async def broadcast_to_conversation(
        self,
        message: dict,
        conversation_id: int,
        sender_id: int = None
    ):
        """Broadcast message to all participants in a conversation"""
        if conversation_id not in self.conversation_participants:
            return

        participants = self.conversation_participants[conversation_id]
        for user_id in participants:
            # Optionally skip sender
            if sender_id and user_id == sender_id:
                continue

            await self.send_personal_message(message, user_id)

    async def send_typing_indicator(
        self,
        conversation_id: int,
        user_id: int,
        is_typing: bool
    ):
        """Send typing indicator to other participants"""
        message = {
            "type": "typing",
            "user_id": user_id,
            "is_typing": is_typing,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.broadcast_to_conversation(
            message,
            conversation_id,
            sender_id=user_id  # Don't send to the typer
        )

    def get_active_users_in_conversation(self, conversation_id: int) -> List[int]:
        """Get list of active users in a conversation"""
        return self.conversation_participants.get(conversation_id, [])

    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is currently online"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0


# Singleton instance
manager = ConnectionManager()
