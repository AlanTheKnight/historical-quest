from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.utils.markdown import hbold, hitalic
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .. import api, models, quests_storage

router = Router()

qs = quests_storage.QuestsStorage()
rs = quests_storage.ResultStorage()


def get_list_quests_markup(quests: list[models.Quest]) -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=q.title)] for q in quests]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)


def get_quest_inline_keyboard(quest: models.Quest) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❤️", callback_data=f"like:{quest.id}"))
    builder.add(InlineKeyboardButton(text="Начать", callback_data=f"start:{quest.id}"))
    return builder.as_markup()


def get_step_keyboard(step: models.Step):
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(step.options):
        builder.add(
            InlineKeyboardButton(text=str(i + 1), callback_data=f"option_after:{step.quest}:{step.id}:{opt.id}")
        )
    return builder.as_markup()


def get_aftertext_keyboard(data: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Следующий шаг", callback_data=f"next_step:{data}"))
    return builder.as_markup()


@router.message(Command("quests"))
async def command_start_handler(message: Message) -> None:
    quests = await qs.data()

    if quests:
        await message.answer(
            "👇 Нажми на квест, чтобы узнать о нём больше",
            reply_markup=get_list_quests_markup(quests),
        )
        return

    await message.answer("🤷‍♂️ Не нашёл доступных квестов. Попробуй позже")


@router.message(F.text)
async def text_handler(message: Message) -> None:
    quest = qs.get_quest_by_title(message.text)

    if quest is None:
        await message.answer("🤷‍♂️ Не нашёл такого квеста. Попробуй ещё раз")
        return

    if quest.cover:
        await message.answer_photo(
            quest.cover,
            quest.get_quest_info(),
            reply_markup=get_quest_inline_keyboard(quest),
        )
        return

    await message.answer(quest.get_quest_info(), reply_markup=get_quest_inline_keyboard(quest))


@router.callback_query(F.data.startswith("like:"))
async def like_handler(query: CallbackQuery) -> None:
    quest_id = int(query.data.split(":")[1])
    quest = await qs.toggle_like(quest_id, query.from_user.id)

    if query.message.content_type == "photo":
        await query.message.edit_caption(
            caption=quest.get_quest_info(),
            reply_markup=get_quest_inline_keyboard(quest),
        )
    else:
        await query.message.edit_text(text=quest.get_quest_info(), reply_markup=get_quest_inline_keyboard(quest))


async def send_step(msg: Message, step: models.Step):
    text = hbold(step.title) + "\n\n" + step.text + "\n\nВыберите ваше действие:\n"
    for i, opt in enumerate(step.options):
        text += f"{hbold(str(i + 1) + ')')} {opt.text}\n"
    markup = get_step_keyboard(step)

    if step.cover:
        await msg.answer_photo(step.cover, caption=text, reply_markup=markup)
    else:
        await msg.answer(text, reply_markup=markup)


@router.callback_query(F.data.startswith("start:"))
async def start_handler(query: CallbackQuery) -> None:
    quest_id = int(query.data.split(":")[1])
    quest = qs.get_quest_by_id(quest_id)
    rs.start(query.message.from_user.id, quest_id)
    await send_step(query.message, quest.steps.get(quest.initial_step))


@router.callback_query(F.data.startswith("option_after:"))
async def option_after(query: CallbackQuery) -> None:
    quest_id, step_id, opt_id = map(int, query.data.split(":")[1:])

    if rs.step_done(query.message.from_user.id, quest_id, step_id):
        await query.message.answer("☝️ Вы уже выбрали ответ на этот шаг")
        return

    q = qs.get_quest_by_id(quest_id)
    options = q.steps.get(step_id).options
    option = list(filter(lambda x: x.id == opt_id, options))[0]

    rs.add_points(query.message.from_user.id, quest_id, option.points)
    rs.complete_step(query.message.from_user.id, quest_id, step_id)

    markup = get_aftertext_keyboard(f"{quest_id}:{step_id}:{opt_id}")

    if option.after_cover:
        await query.message.answer_photo(option.after_cover, caption=option.after_text, reply_markup=markup)
    else:
        await query.message.answer(option.after_text, reply_markup=markup)


async def quest_results(msg: Message, quest: models.Quest) -> None:
    if (msg.from_user.id, quest.id) not in rs._data:
        return
    points = rs.pop(msg.from_user.id, quest.id)[0]

    for ending in quest.endings:
        ev = eval(ending.condition, {"x": points})
        if not ev:
            continue
        text = f'{hbold("🏆 Квест пройден!")}\n\n' + ending.text
        if ending.cover:
            await msg.reply_photo(ending.cover, caption=text)
        else:
            await msg.reply(text)
        break


@router.callback_query(F.data.startswith("next_step:"))
async def quest_next_step(query: CallbackQuery) -> None:
    quest_id, step_id, opt_id = map(int, query.data.split(":")[1:])

    q = qs.get_quest_by_id(quest_id)
    options = q.steps.get(step_id).options
    option = list(filter(lambda x: x.id == opt_id, options))[0]
    next_step = q.steps.get(option.next_step)
    if next_step:
        await send_step(query.message, next_step)
    else:
        await quest_results(query.message, q)
