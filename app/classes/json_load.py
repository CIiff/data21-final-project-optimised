import datetime

from app.classes.json_transform import JsonTransform
# import orm
from app.classes.logger import Logger
from sqlalchemy.orm import sessionmaker


class JsonLoad(Logger):
    def __init__(self, engine, logging_level):
        # Initialise logging
        Logger.__init__(self, logging_level)
        # Setting up connection to sql server.
        self.engine = engine
        factory = sessionmaker(bind=self.engine)
        self.session = factory()
        self.session.expire_on_commit = False

    def check_candidate_exists(self, name):
        self.log_print("Checking if candidate exists", "INFO")
        isempty = self.engine.execute(f"SELECT * FROM candidate WHERE "
                                f"candidate_name = '{name}'").fetchall()
        self.log_print(isempty, "INFO")
        if isempty == []:
            return False
        else:
            #self.log_print(f'{name} already exists', "FLAG")
            candidate_id = self.engine.execute(f"SELECT candidate_id FROM candidate WHERE "
                                f"candidate_name = '{name}'").fetchall()
            return candidate_id[0][0]

    def insert_candidate(self, name):
        return self.engine.execute(f"INSERT INTO candidate (candidate_name) VALUES ('{name}')")

    def insert_sparta_day(self, name, bool_lst, date, course_interest):
        if self.check_candidate_exists(name):
            candidate_id = self.check_candidate_exists(name)
            return self.engine.execute(f"INSERT INTO sparta_day "
                                       f"(candidate_id, "
                                       f"location_id, "
                                       f"date, "
                                       f"self_development, "
                                       f"geo_flex, "
                                       f"financial_support, "
                                       f"result,"
                                       f"course_interest) "
                                       f"VALUES ('{candidate_id}', "
                                       f"'1', "
                                       f"CAST('{date}' as datetime),"
                                       f"'{bool_lst[0]}', "
                                       f"'{bool_lst[1]}', "
                                       f"'{bool_lst[2]}', "
                                       f"'{bool_lst[3]}',"
                                       f"'{course_interest}')")
        else:
            self.insert_candidate(name)
            self.insert_sparta_day(name, bool_lst, date, course_interest)

