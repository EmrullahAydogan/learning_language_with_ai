"""
WebSocket endpoints for real-time chat
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.websocket_manager import manager
from app.models.chat import ChatConversation, ChatMessage
from app.models.user import User
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/chat/{conversation_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    conversation_id: int,
    token: str = Query(...),  # JWT token passed as query parameter
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time chat

    Usage:
    ws://localhost:8000/api/v1/ws/chat/{conversation_id}?token=YOUR_JWT_TOKEN

    Messages format:
    {
        "type": "message" | "typing" | "read",
        "content": "message content",  // for type: message
        "is_typing": true | false,     // for type: typing
        "message_id": 123              // for type: read
    }
    """

    # TODO: Verify JWT token and get user
    # For now, we'll use a placeholder user_id
    # In production, you should decode the JWT token here
    try:
        # Placeholder: Extract user from token
        # from app.core.security import verify_token
        # user_id = verify_token(token)
        user_id = 1  # Placeholder

        # Verify conversation exists and user has access
        conversation = db.query(ChatConversation).filter(
            ChatConversation.id == conversation_id,
            ChatConversation.user_id == user_id
        ).first()

        if not conversation:
            await websocket.close(code=1008, reason="Conversation not found or access denied")
            return

        # Connect user
        await manager.connect(websocket, user_id, conversation_id)

        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Notify other participants
        await manager.broadcast_to_conversation(
            {
                "type": "user_joined",
                "user_id": user_id,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat()
            },
            conversation_id,
            sender_id=user_id
        )

        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)

                message_type = message_data.get("type", "message")

                if message_type == "message":
                    # Save message to database
                    content = message_data.get("content", "")
                    if content.strip():
                        new_message = ChatMessage(
                            conversation_id=conversation_id,
                            role="user",
                            content=content
                        )
                        db.add(new_message)
                        db.commit()
                        db.refresh(new_message)

                        # Broadcast message to all participants
                        await manager.broadcast_to_conversation(
                            {
                                "type": "message",
                                "message_id": new_message.id,
                                "conversation_id": conversation_id,
                                "user_id": user_id,
                                "role": "user",
                                "content": content,
                                "timestamp": new_message.created_at.isoformat() if new_message.created_at else datetime.utcnow().isoformat()
                            },
                            conversation_id
                        )

                elif message_type == "typing":
                    # Send typing indicator
                    is_typing = message_data.get("is_typing", False)
                    await manager.send_typing_indicator(
                        conversation_id,
                        user_id,
                        is_typing
                    )

                elif message_type == "read":
                    # Mark message as read
                    message_id = message_data.get("message_id")
                    if message_id:
                        await manager.broadcast_to_conversation(
                            {
                                "type": "read",
                                "message_id": message_id,
                                "user_id": user_id,
                                "conversation_id": conversation_id,
                                "timestamp": datetime.utcnow().isoformat()
                            },
                            conversation_id
                        )

        except WebSocketDisconnect:
            # User disconnected
            manager.disconnect(websocket, user_id, conversation_id)

            # Notify other participants
            await manager.broadcast_to_conversation(
                {
                    "type": "user_left",
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "timestamp": datetime.utcnow().isoformat()
                },
                conversation_id
            )
            logger.info(f"User {user_id} disconnected from conversation {conversation_id}")

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            manager.disconnect(websocket, user_id, conversation_id)
            await websocket.close(code=1011, reason="Internal server error")

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await websocket.close(code=1008, reason="Authentication failed")


@router.get("/active-users/{conversation_id}")
def get_active_users(conversation_id: int):
    """Get list of currently active users in a conversation"""
    active_users = manager.get_active_users_in_conversation(conversation_id)
    return {
        "conversation_id": conversation_id,
        "active_users": active_users,
        "count": len(active_users)
    }


@router.get("/user-status/{user_id}")
def check_user_online_status(user_id: int):
    """Check if a user is currently online"""
    is_online = manager.is_user_online(user_id)
    return {
        "user_id": user_id,
        "is_online": is_online
    }
