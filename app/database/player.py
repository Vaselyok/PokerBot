from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from .common import order, get_all_and_total, apply_sorting
from app.models.player import Player


async def get_all_players(session, limit, offset, sorting_rules=None):
    stmt = select(Player).where(Player.is_archived.is_(False))

    if sorting_rules:
        stmt = apply_sorting(stmt=stmt, model=Player, sort="-elo", sorting_rules=sorting_rules)

    else:
        stmt = order(stmt=stmt, model=Player)

    result = await get_all_and_total(session, stmt, limit, offset)
    return result


async def get_player_by_id(session, player_id):
    result = await session.execute(
        select(Player)
        .options(selectinload(Player.games))
        .options(selectinload(Player.organized_games))
        .options(selectinload(Player.elo_history))
        .options(selectinload(Player.eliminations))
        .where(Player.id == player_id)
    )
    player = result.scalar_one_or_none()
    return player


async def get_player_by_tg_id(session, tg_id):
    result = await session.execute(
        select(Player)
        .options(selectinload(Player.games))
        .options(selectinload(Player.organized_games))
        .options(selectinload(Player.elo_history))
        .where(Player.telegram_id == tg_id)
    )
    player = result.scalar_one_or_none()
    return player


async def add_player(session, item, tg_id):
    player = Player(
        telegram_id=tg_id,
        name=item.name,
    )

    session.add(player)
    await session.flush()
    return player


async def reset_all_players_elo(session, elo: float = 1000):
    await session.execute(
        update(Player).values(
            elo=elo,
            elo_change_per_match=0,
        )
    )
    await session.flush()