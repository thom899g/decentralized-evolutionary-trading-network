"""
Firebase Manager for Decentralized Evolutionary Trading Network
Handles all Firestore operations for agent state and insight sharing
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    from google.cloud import firestore_v1
    from google.cloud.firestore_v1.base_query import FieldFilter
except ImportError as e:
    logging.error(f"Missing required dependency: {e}")
    raise

logger = logging.getLogger(__name__)


class InsightType(Enum):
    """Types of insights agents can share"""
    MARKET_SIGNAL = "market_signal"
    STRATEGY_PARAM = "strategy_param"
    RISK_ALERT = "risk_alert"
    PERFORMANCE_METRIC = "performance_metric"
    EVOLUTIONARY_ADAPTATION = "evolutionary_adaptation"


@dataclass
class TradingInsight:
    """Data structure for trading insights"""
    insight_id: str
    agent_id: str
    insight_type: InsightType
    content: Dict[str, Any]
    timestamp: datetime
    confidence_score: float
    validation_count: int = 0
    consensus_score: float = 0.0
    is_validated: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary"""
        data = asdict(self)
        data['insight_type'] = self.insight_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TradingInsight':
        """Create from Firestore document"""
        data['insight_type'] = InsightType(data['insight_type'])
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)