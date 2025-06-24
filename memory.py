from typing import Optional, Dict, Any, List


class ConversationStore:
    def get(self, conversation_id: str) -> Optional[List[Dict[str, Any]]]:
        pass

    def save(self, conversation_id: str, state: List[Dict[str, Any]]):
        pass


class InMemoryConversationStore(ConversationStore):
    _conversations: Dict[str, List[Dict[str, Any]]] = {}

    def get(self, conversation_id: str) -> Optional[List[Dict[str, Any]]]:
        return self._conversations.get(conversation_id)

    def save(self, conversation_id: str, state: List[Dict[str, Any]]):
        self._conversations[conversation_id] = state


# TODO: when deploying this app in scale, switch to your own production-ready implementation
conversation_store = InMemoryConversationStore()
