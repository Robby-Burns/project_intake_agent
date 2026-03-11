# 🏭 Agnostic Database Factory - Creates database adapters.
# This factory implements the "Agnostic Factory" pattern, a core tenet of the framework,
# allowing the system to be decoupled from a specific database technology.
# Reference: agent.md - The System Kernel for AI behavior and rules.
# Reference: workflow/08_AGNOSTIC_FACTORIES.md

from app.config import config
from app.interfaces.database_adapter import DatabaseAdapter

class DatabaseFactory:
    """
    Factory to create a database adapter based on scale.yaml configuration.
    """
    
    _instance = None

    @staticmethod
    def get_adapter() -> DatabaseAdapter:
        """
        Returns a singleton instance of the configured database adapter.
        """
        if DatabaseFactory._instance is None:
            db_type = config.database.type.lower()
            
            if db_type == "postgresql":
                # Lazy import
                from app.adapters.database_adapter import PostgresAdapter
                DatabaseFactory._instance = PostgresAdapter()
            
            elif db_type == "sqlite":
                # Lazy import
                from app.adapters.database_adapter import PostgresAdapter # Re-use for sqlite connection string
                DatabaseFactory._instance = PostgresAdapter(connection_string="sqlite:///local_state.db")
                
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
                
        return DatabaseFactory._instance
