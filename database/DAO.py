from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """SELECT distinct Chromosome 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getNodi(v1, v2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
from genes g where Chromosome between %s and %s"""
            cursor.execute(query, [v1, v2])

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(v1, v2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
with nodi as (select *
from genes g where Chromosome between %s  and %s),
localiz as (
select n.GeneId, n.Function, n.Chromosome, Localization
from classification c, nodi n
where c.GeneId = n.GeneId
group by n.GeneId, n.Function, n.Chromosome, Localization),
coppie as (select l1.GeneId primo, l1.function primof, l2.GeneId secondo, l2.function secondof 
from localiz l1, localiz l2
where l1.Chromosome<l2.Chromosome and l1.Localization = l2.Localization
group by l1.GeneId, l1.Function, l2.GeneId, l2.function
union 
select l1.GeneId, l1.Function, l2.GeneId, l2.function
from localiz l1, localiz l2
where l1.Chromosome=l2.Chromosome and l1.Localization = l2.Localization and l1.GeneId!=l2.Geneid
)

select primo, primof, secondo, secondof, Expression_Corr
from coppie c, interactions i
where (c.primo = i.GeneID1 and c.secondo = i.GeneID2) or (c.primo = i.GeneID2 and c.secondo = i.GeneID1)
group by primo, primof, secondo, secondof, Expression_Corr"""
            cursor.execute(query, [v1, v2])

            for row in cursor:
                result.append(row)

            cursor.close()
            cnx.close()
        return result