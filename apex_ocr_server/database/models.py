import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Legends(enum.Enum):
    BLOODHOUND = enum.auto()
    GIBRALTAR = enum.auto()
    LIFELINE = enum.auto()
    PATHFINDER = enum.auto()
    WRAITH = enum.auto()
    BANGALORE = enum.auto()
    CAUSTIC = enum.auto()
    MIRAGE = enum.auto()
    OCTANE = enum.auto()
    WATTSON = enum.auto()
    CRYPTO = enum.auto()
    REVENANT = enum.auto()
    LOBA = enum.auto()
    RAMPART = enum.auto()
    HORIZON = enum.auto()
    FUSE = enum.auto()
    VALKYRIE = enum.auto()
    SEER = enum.auto()
    ASH = enum.auto()
    MAD_MAGGIE = enum.auto()
    NEWCASTLE = enum.auto()
    VANTAGE = enum.auto()
    CATALYST = enum.auto()
    BALLISTIC = enum.auto()


class MatchType(enum.Enum):
    ARENAS = enum.auto()
    BATTLE_ROYALE = enum.auto()


class WinLoss(enum.Enum):
    WIN = enum.auto()
    LOSS = enum.auto()


class BaseMixin:
    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{c.name}={repr(getattr(self, str(c.name)))}"
                for c in self.__table__.columns
            ),
        )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Clan(Base, BaseMixin):
    __tablename__ = "clan"

    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    name = Column(String)

    players = relationship(
        "Player",
        back_populates="clan",
    )


class Player(Base, BaseMixin):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    clan_id = Column(Integer, ForeignKey("clan.id", ondelete="SET NULL"))
    name = Column(String, nullable=False, unique=True)

    match_results = relationship(
        "PlayerMatchResult",
        back_populates="player",
        cascade="all, delete",
        passive_deletes=True,
    )
    clan = relationship("Clan", back_populates="players")

    def __str__(self):
        if self.clan:
            return f"[{self.clan.tag}] {self.name}"
        else:
            return f"{self.name}"


class PlayerMatchResult(Base, BaseMixin):
    __tablename__ = "player_match_result"

    id = Column(Integer, primary_key=True)
    match_id = Column(
        Integer, ForeignKey("match_result.id", ondelete="CASCADE"), nullable=False
    )
    player_id = Column(
        Integer, ForeignKey("player.id", ondelete="CASCADE"), nullable=False
    )
    legend = Column(Enum(Legends))
    kills = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    knockdowns = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    survival_time = Column(Integer, nullable=False)
    revives = Column(Integer, nullable=False)
    respawns = Column(Integer, nullable=False)

    player = relationship("Player", back_populates="match_results")
    match_result = relationship("MatchResult", back_populates="player_match_results")

    def __repr__(self):
        return (
            f"PlayerMatchResult(id={self.id}, match_result=MatchResult(id={self.match_result.id}, "
            f"datetime={self.match_result.datetime}, match_type={self.match_result.match_type}, "
            f"place={self.match_result.place}, result={self.match_result.result}, hash={self.match_result.hash}), "
            f"player=Player(id={self.player_id}, clan_id={self.player.clan_id}, name={self.player.name}), "
            f"legend={self.legend}, kills={self.kills}, assists={self.assists}, "
            f"knockdowns={self.knockdowns}, damage={self.damage}, survival_time={self.survival_time}, "
            f"revives={self.revives}, respawns={self.respawns})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "match_id": self.match_result.id,
            "datetime": self.match_result.datetime,
            "match_type": self.match_result.match_type,
            "place": self.match_result.place,
            "result": self.match_result.result,
            "hash": self.match_result.hash,
            "player_id": self.player_id,
            "clan_id": self.player.clan_id,
            "player_name": self.player.name,
            "legend": self.legend,
            "kills": self.kills,
            "assists": self.assists,
            "knockdowns": self.knockdowns,
            "damage": self.damage,
            "survival_time": self.survival_time,
            "revives": self.revives,
            "respawns": self.respawns,
        }


class Season(Base, BaseMixin):
    __tablename__ = "season"
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    name = Column(String, unique=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    match_results = relationship(
        "MatchResult",
        cascade="all, delete",
        passive_deletes=True,
    )


class MatchResult(Base, BaseMixin):
    __tablename__ = "match_result"

    id = Column(Integer, primary_key=True)
    season = Column(ForeignKey("season.id", ondelete="SET NULL"))
    datetime = Column(DateTime(timezone=True), nullable=False)
    match_type = Column(Enum(MatchType), nullable=False)
    place = Column(Integer)
    result = Column(Enum(WinLoss))
    hash = Column(String, unique=True, nullable=False)

    player_match_results = relationship(
        "PlayerMatchResult",
        cascade="all, delete",
        passive_deletes=True,
    )
