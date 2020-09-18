"""48 IX RSAgent Configuration & Validation."""

# Third Party
from pydantic import BaseModel, SecretBytes


class Agent(BaseModel):
    """Configuration Parameters for 48ix/rsagent."""

    key: SecretBytes
    port: int = 4848
