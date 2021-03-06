
class QuestionPaser:

  

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    def parser_main(self, res_classify):
        args = res_classify['entities']
        entity_dict = self.build_entitydict(args)
        question_type = res_classify['question_types']
        sql_ = {}

        sql_['question_type'] = question_type
        sql = []
        if question_type == 'disease_symptom':
            entities = entity_dict.get('disease')

        elif question_type == 'symptom_disease':
            entities = entity_dict.get('symptom')

        elif question_type == 'result_from':
            entities = entity_dict.get('disease')

        elif question_type == 'disease_easyget':
            entities = entity_dict.get('disease')

        sql = self.sql_transfer(question_type, entities)
        if sql:
            sql_['sql'] = sql
            sql_['entities'] = entities
        return sql_

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 查询症状会导致哪些疾病
        if question_type == 'symptom_disease':
            sql = [
                "MATCH (m:Bug)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        if question_type == 'disease_symptom':
            sql = [
                "MATCH (m:Bug)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        if question_type == 'belongs_to':
            sql = [
                "MATCH (m:Bug)-[r:belongs_to]->(n:People) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        if question_type == 'has_time':
            sql = [
                "MATCH (m:Bug)-[r:has_time]->(n:DiseaseTime) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        if question_type == 'result_from':
            sql = [
                "MATCH (m:Bug)-[r:result_from]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        if question_type == 'disease_easyget':

            sql = [
                "MATCH (m:Bug)-[r:belongs_to]->(n:People) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
