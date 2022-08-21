from asyncpg import UniqueViolationError

from utils.db_api.schemes.registration import Registration


async def new_registration(user_id: int, client_fio: str, quest_fio: str, start_date: str, validity: str, status: str):
    try:
        registration = Registration(user_id=user_id, client_fio=client_fio, quest_fio=quest_fio, start_date=start_date,
                                    validity=validity, status=status)
        await registration.create()
    except UniqueViolationError:
        print('Регистрация не создана')


async def select_registration():
    registration = await Registration.query.where(Registration.status == 'created').gino.first()
    return registration


async def select_registration_by_user_id(user_id: int):
    registration = await Registration.query.where(Registration.user_id == user_id).gino.first()
    return registration


async def accept_registration(user_id: int):
    registration = await select_registration_by_user_id(user_id)
    await registration.update(status='accepted').apply()


async def reject_registration(user_id: int):
    registration = await select_registration_by_user_id(user_id)
    await registration.update(status='rejected').apply()