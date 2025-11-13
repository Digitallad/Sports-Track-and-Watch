"""
Rugby Atlas - Rights Resolution Rules
Business rules for evaluating broadcast rights
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

from ..core.logging import get_logger

logger = get_logger(__name__)


class RulePriority(int, Enum):
    """Priority levels for rights rules"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class RightsRule:
    """
    Base class for broadcast rights rules.
    Rules are evaluated to determine the appropriate broadcast option.
    """
    
    def __init__(self, name: str, priority: RulePriority = RulePriority.MEDIUM):
        self.name = name
        self.priority = priority
        self.logger = logger
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate the rule against a context.
        
        Args:
            context: Dictionary containing fixture, territory, rights, and user data
        
        Returns:
            True if the rule applies, False otherwise
        """
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def apply(self, rights_options: List[Any]) -> List[Any]:
        """
        Apply the rule to filter or modify rights options.
        
        Args:
            rights_options: List of available rights options
        
        Returns:
            Filtered or modified list of rights options
        """
        raise NotImplementedError("Subclasses must implement apply()")


class ExclusivityRule(RightsRule):
    """Rule for handling exclusive broadcast rights"""
    
    def __init__(self):
        super().__init__("ExclusivityRule", RulePriority.HIGH)
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if any rights in the context are exclusive"""
        rights = context.get("rights", [])
        return any(getattr(r, "is_exclusive", False) for r in rights)
    
    def apply(self, rights_options: List[Any]) -> List[Any]:
        """Filter to only exclusive rights if any exist"""
        exclusive = [r for r in rights_options if getattr(r, "is_exclusive", False)]
        return exclusive if exclusive else rights_options


class GeographicRestrictionRule(RightsRule):
    """Rule for geographic broadcast restrictions"""
    
    def __init__(self):
        super().__init__("GeographicRestrictionRule", RulePriority.CRITICAL)
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if geographic restrictions apply"""
        territory = context.get("territory")
        return territory is not None
    
    def apply(self, rights_options: List[Any]) -> List[Any]:
        """Filter rights based on geographic availability"""
        # Placeholder - in production, this would check territory coverage
        return rights_options


class TimeBasedAvailabilityRule(RightsRule):
    """Rule for time-based availability (live vs on-demand)"""
    
    def __init__(self):
        super().__init__("TimeBasedAvailabilityRule", RulePriority.MEDIUM)
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if time-based filtering should apply"""
        fixture = context.get("fixture")
        return fixture is not None
    
    def apply(self, rights_options: List[Any]) -> List[Any]:
        """Filter based on current time relative to match time"""
        # Placeholder - would check if match is live, upcoming, or past
        return rights_options


class SubscriptionRequiredRule(RightsRule):
    """Rule for subscription-based filtering"""
    
    def __init__(self):
        super().__init__("SubscriptionRequiredRule", RulePriority.MEDIUM)
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if user subscription status should be considered"""
        user = context.get("user")
        return user is not None
    
    def apply(self, rights_options: List[Any]) -> List[Any]:
        """
        Prioritize free options or options matching user's subscriptions.
        Placeholder implementation.
        """
        # In production, check user subscriptions and prioritize accordingly
        free_options = [r for r in rights_options if getattr(r, "is_free", False)]
        return free_options if free_options else rights_options


class RuleEvaluator:
    """
    Evaluates and applies broadcast rights rules.
    Manages the rule evaluation pipeline.
    """
    
    def __init__(self):
        self.rules: List[RightsRule] = []
        self.logger = logger
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize with default rules"""
        self.add_rule(ExclusivityRule())
        self.add_rule(GeographicRestrictionRule())
        self.add_rule(TimeBasedAvailabilityRule())
        self.add_rule(SubscriptionRequiredRule())
        
        self.logger.info(f"Initialized rule evaluator with {len(self.rules)} rules")
    
    def add_rule(self, rule: RightsRule):
        """Add a rule to the evaluator"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority.value, reverse=True)
    
    def evaluate_all(self, context: Dict[str, Any]) -> List[RightsRule]:
        """
        Evaluate all rules against a context.
        
        Args:
            context: Evaluation context
        
        Returns:
            List of rules that apply to the context
        """
        applicable_rules = []
        for rule in self.rules:
            if rule.evaluate(context):
                applicable_rules.append(rule)
                self.logger.debug(f"Rule {rule.name} applies")
        
        return applicable_rules
    
    def apply_rules(
        self,
        rights_options: List[Any],
        context: Dict[str, Any]
    ) -> List[Any]:
        """
        Apply all applicable rules to filter rights options.
        
        Args:
            rights_options: Available rights options
            context: Evaluation context
        
        Returns:
            Filtered rights options
        """
        applicable_rules = self.evaluate_all(context)
        
        result = rights_options
        for rule in applicable_rules:
            result = rule.apply(result)
            self.logger.debug(f"Applied rule {rule.name}, {len(result)} options remain")
        
        return result
