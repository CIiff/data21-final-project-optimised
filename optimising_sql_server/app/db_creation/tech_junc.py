from optimising_sql_server.app.db_creation.tech import *
from optimising_sql_server.app.db_creation.candidate import candidate_sql_tbl





# creation of course staff junction table
class techCandidateJunc(CreateDB):

    def __init__(self):
        super().__init__()        # SubClass initialization code
        
        tech_sql_tbl.create_tech_table()
        
    @staticmethod
    def pysqldf(q):
        return sqldf(q,globals())
 

    def create_table(self):
        with self.db:
            self.c.execute("""
                    DROP TABLE IF EXISTS tech_junction;
                    CREATE TABLE tech_junction
                            (
                            tech_id INT,
                            candidate_id INT,
                            score INT,
                            FOREIGN KEY(tech_id) REFERENCES tech(tech_id),
                            FOREIGN KEY(candidate_id) REFERENCES candidate(candidate_id)
                            )
                            """)

    def data_entry(self):
        
        sql_insert = """
                INSERT INTO tech_junction(
                    candidate_id,
                    tech_id,
                    score
                )
                VALUES
                (
                    ?,?,?
                )"""
        self.c.executemany(sql_insert,tech_junc_df.values.tolist()) 
        # ).to_sql('tech_junction',con=self.db,index=False,if_exists='append')
    
    
    def update_tech_df(self):

        df = json_df_dict['tech_df']
        # logger.info(df.head(5))
        
        for row in self.c.execute("SELECT tech,tech_id FROM tech "):
            df['tech_name'].replace({row[0]:row[1]},inplace=True)
        # logger.info(df.head(5))
        for row in self.c.execute("SELECT candidate_name,candidate_id FROM candidate ORDER BY candidate_name "):
            # logger.info(f'replacements {row}')
            df['candidate_name'].replace({(row[0]):str(row[1])},inplace=True)
        # logger.info(df.head(5))
        df = df.rename(columns=({'candidate_name':'candidate_id','tech_name':'tech_id','tech_score':'score'}))
        return df


    def sample_query(self):
        logger.info('TECH_JUNCTION_TABLE \n')
        data = self.c.execute("SELECT * FROM tech_junction LIMIT 10")
        for row in data:
            logger.info(row)
        return data

    def create_tech_junc_table(self):

        # self.update_weakness_df()
        self.create_table()
        self.db.commit()
        self.data_entry()
        logger.info('\nLOADING TO TECH_JUNCTION SQL TABLE\n')
        self.db.commit()
        # self.sample_query()


tech_junc_sql_tbl = techCandidateJunc()
tech_junc_df = tech_junc_sql_tbl.update_tech_df()



