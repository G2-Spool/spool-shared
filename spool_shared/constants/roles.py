"""Role and permission constants."""

from enum import Enum


class UserRole(str, Enum):
    """User roles."""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    SYSTEM = "system"


class Permission(str, Enum):
    """System permissions."""
    # Progress permissions
    VIEW_OWN_PROGRESS = "progress:view:own"
    VIEW_ALL_PROGRESS = "progress:view:all"
    UPDATE_PROGRESS = "progress:update"
    
    # Content permissions
    VIEW_CONTENT = "content:view"
    CREATE_CONTENT = "content:create"
    UPDATE_CONTENT = "content:update"
    DELETE_CONTENT = "content:delete"
    
    # Exercise permissions
    SUBMIT_EXERCISE = "exercise:submit"
    EVALUATE_EXERCISE = "exercise:evaluate"
    VIEW_ALL_SUBMISSIONS = "exercise:view:all"
    
    # Gamification permissions
    VIEW_LEADERBOARD = "gamification:leaderboard:view"
    AWARD_POINTS = "gamification:points:award"
    MANAGE_BADGES = "gamification:badges:manage"
    
    # Analytics permissions
    VIEW_OWN_ANALYTICS = "analytics:view:own"
    VIEW_ALL_ANALYTICS = "analytics:view:all"
    EXPORT_ANALYTICS = "analytics:export"
    
    # Admin permissions
    MANAGE_USERS = "admin:users:manage"
    MANAGE_SYSTEM = "admin:system:manage"
    VIEW_LOGS = "admin:logs:view"


# Role to permissions mapping
ROLE_PERMISSIONS = {
    UserRole.STUDENT: [
        Permission.VIEW_OWN_PROGRESS,
        Permission.VIEW_CONTENT,
        Permission.SUBMIT_EXERCISE,
        Permission.VIEW_LEADERBOARD,
        Permission.VIEW_OWN_ANALYTICS,
    ],
    UserRole.INSTRUCTOR: [
        Permission.VIEW_OWN_PROGRESS,
        Permission.VIEW_ALL_PROGRESS,
        Permission.UPDATE_PROGRESS,
        Permission.VIEW_CONTENT,
        Permission.CREATE_CONTENT,
        Permission.UPDATE_CONTENT,
        Permission.SUBMIT_EXERCISE,
        Permission.EVALUATE_EXERCISE,
        Permission.VIEW_ALL_SUBMISSIONS,
        Permission.VIEW_LEADERBOARD,
        Permission.AWARD_POINTS,
        Permission.VIEW_OWN_ANALYTICS,
        Permission.VIEW_ALL_ANALYTICS,
        Permission.EXPORT_ANALYTICS,
    ],
    UserRole.ADMIN: [
        # Admins have all permissions
        permission for permission in Permission
    ],
    UserRole.SYSTEM: [
        # System has all permissions
        permission for permission in Permission
    ],
}