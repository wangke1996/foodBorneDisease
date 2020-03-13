import _locale
import os
import json
from py2neo import Graph, Node
from tqdm import tqdm
from bert_serving.client import BertClient
import json
bc = BertClient()
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/ExtractedBug.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        # 共5类节点
        self.Bugs = []  # 病原体
        self.Symptoms = []  # 症状
        self.DiseaseTime = []  # 　发病时间
        self.People = []  # 易感人群
        self.Food = []  # 食物来源

        # 实体关系

        self.rels_disease_symptom = []  # 疾病症状关系
        self.rels_disease_time = []  # 疾病时间关系
        self.rels_disease_people = []  # 疾病人群关系
        self.rels_disease_food = []  # 疾病来源关系

    def node_update(self, bug):
        bug_name = bug['名称']
        self.Bugs.append(bug_name)
        for d in bug['疾病']:
            for s in d['症状']:
                self.Symptoms.append(s)
                self.rels_disease_symptom.append([bug_name, s])
            if '发病' in d:
                for t in d['发病']:
                    self.DiseaseTime.append(t)
                    self.rels_disease_time.append([bug_name, t])
        if '易感人群' in bug:
            for p in bug['易感人群']:
                self.People.append(p)
                self.rels_disease_people.append([bug_name, p])
        if '来源' in bug:
            for f in bug['来源']:
                self.Food.append(f)
                self.rels_disease_food.append([bug_name, f])

    def read_nodes(self):

        with open(self.data_path, encoding='utf-8') as f:
            jsonobj = json.load(f)

        for bug in jsonobj['病原菌']['革兰氏阴性菌']:
            self.node_update(bug)
        for bug in jsonobj['病原菌']['革兰氏阳性菌']:
            self.node_update(bug)
        for bug in jsonobj["寄生原虫和寄生虫"]:
            self.node_update(bug)
        for bug in jsonobj["病毒"]:
            self.node_update(bug)
        for bug in jsonobj["其他病原体"]:
            self.node_update(bug)
        for bug in jsonobj["天然毒素"]:
            self.node_update(bug)

    def create_node(self, label, nodes):
        for node_name in tqdm(nodes):
            node = Node(label, name=node_name)
            self.g.create(node)
        return

    def create_graphnodes(self):

        self.create_node('Bug', set(self.Bugs))
        self.create_node('Symptom', set(self.Symptoms))
        self.create_node('DiseaseTime', set(self.DiseaseTime))
        self.create_node('People', set(self.People))
        self.create_node('Food', set(self.Food))

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    def create_graphrels(self):

        self.create_relationship(
            'Bug', 'Symptom', self.rels_disease_symptom, 'has_symptom', '症状')
        self.create_relationship('Bug', 'DiseaseTime',
                                 self.rels_disease_time, 'has_time', '发病')
        self.create_relationship(
            'Bug', 'People', self.rels_disease_people, 'belongs_to', '易感人群')
        self.create_relationship(
            'Bug', 'Food', self.rels_disease_food, 'result_from', '来源')
        print(self.rels_disease_food)

    def export_data(self):
        f_food = open('dict/food.json', 'w')
        f_symptom = open('dict/symptom.json', 'w')
        f_bug = open('dict/disease.json', 'w')
        f_people = open('dict/people.json', 'w')

        d_food = {}
        d_symptom ={}
        d_bug = {}
        d_people = {}

        for wd in list(set(self.Food)):
            d_food[wd]= bc.encode([wd]).tolist()
        f_food.write(json.dumps(d_food,ensure_ascii=False))

        for wd in list(set(self.Symptoms)):
            d_symptom[wd]= bc.encode([wd]).tolist()
        f_symptom.write(json.dumps(d_symptom,ensure_ascii=False))

        for wd in list(set(self.Bugs)):
            d_bug[wd]= bc.encode([wd]).tolist()
        f_bug.write(json.dumps(d_bug,ensure_ascii=False))

        for wd in list(set(self.People)):
            d_people[wd]= bc.encode([wd]).tolist()
        f_people.write(json.dumps(d_people,ensure_ascii=False))


        f_food.close()
        f_symptom.close()
        f_bug.close()
        f_people.close()


if __name__ == '__main__':
    handler = MedicalGraph()
    handler.read_nodes()
    # print(len(handler.Bugs))
    # handler.create_graphnodes()
    # handler.create_graphrels()
    handler.export_data()
