from aiogram import Bot, Router
from aiogram.types import PollAnswer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import ApplicationException
from app.models.game import Game
import asyncio
from app.services.player import (
    check_player_tg_id,
    create_player,
)
from app.services.game import join_game, leave_game

from app.schemas.player import PlayerAddRequest
import datetime

router = Router(name="poll")

#дописать логику регистрации на турнир
#при шаффл мы проверяем тайминги когда кто пришел и на группы делим
@router.poll_answer()
async def poll_answer_handler(
    poll_answer: PollAnswer,
    bot: Bot,
    session: AsyncSession,
):
    
    # if not poll_answer:
    #     print("ПРоблемка в poll_answer_handler, пол не нашелся")
    #     return

    # Ищем poll_id
    poll_id = poll_answer.poll_id

    # Получаем игру
    game = await session.scalar(
        select(Game).where(
            Game.poll_id == poll_id
        )
    )
    

    if game is None:
        print("ПРоблемка в poll_answer_handler, игра не нашлась")
        return

    try:
        player = await check_player_tg_id(
            session=session,
            tg_id=poll_answer.user.id,
        )
    except ApplicationException as e:
        player = None

    # Если пользователь снял голос, удаляем из турнира
    if not poll_answer.option_ids:
        await leave_game(session, game.id, player.id)
        return
    
    # Если игрока нет — создаем
    if player is None:

        item = PlayerAddRequest(
            name=poll_answer.user.username if poll_answer.user.username else f"Неопознанный орангутанг {datetime.datetime.now().microsecond % 1000}"
        )

        player = await create_player(
            session=session,
            item=item,
            tg_id=poll_answer.user.id,
        )

    text = await join_game(
        session=session,
        game_id=game.id,
        player_id=player.id,
    )

    try:
        await bot.send_message(
            chat_id=poll_answer.user.id,
            text=text.result,
        )
        if text != "joined":
            msg = await bot.send_message(
            chat_id=game.telegram_chat.chat_id,
            text=f"@{poll_answer.user.username}, {text.result}"
        )

        await asyncio.sleep(15)
        await bot.delete_message(msg.chat.id, msg.message_id)
    except Exception:
        pass