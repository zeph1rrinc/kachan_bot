from sys import argv

from .bot import bot
from .database import engine, Session
from .tables import Base, Participant
from .exceptions import NotAdminError, NonExistentParticipantError

if __name__ == "__main__":
    if len(argv) > 1:
        match argv[1]:
            case "init_db":
                Base.metadata.create_all(engine)
                exit(0)
            case "init_test_users":
                session = Session()
                players = [
                    Participant(username='@zeph1rr', name='Антон Григорьев'),
                    Participant(name='Олег Ясенев', rating=12, username='')
                ]
                for player in players:
                    session.add(player)
                session.commit()
                session.close()
                exit(0)
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except NotAdminError as _ex:
            bot.send_message(_ex.chat_id, _ex)
        except NonExistentParticipantError as _ex:
            bot.send_message(_ex.chat_id, _ex)
