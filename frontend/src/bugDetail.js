import React, {Component} from 'react';
import {Tree, Input, Typography, Divider, Row, Col} from 'antd';
import {getBugDetail, getBugs} from "./api";

const {Title, Paragraph, Text} = Typography;
const {TreeNode} = Tree;
const {Search} = Input;
const name = '名称', disease = '疾病';
const generateList = (data, dataList) => {
    for (let i = 0; i < data.length; i++) {
        const node = data[i];
        const {title, parent} = node;
        dataList.push({title, parent});
        if (node.children) {
            generateList(node.children, dataList);
        }
    }
    return dataList;
};

class BugDetail extends Component {
    render() {
        const {data} = this.props;
        if (Object.keys(data).length === 0)
            return <div/>;
        return (
            <Typography>
                <Title>{data[name]}</Title>
                {Object.entries(data).map(([key, value]) => {
                    if (key === disease) {
                        return <Typography key={key}>
                            <Title level={3}>{key}</Title>
                            <ul>
                                {value.map((d, i) => <li key={i}>
                                    <ul>{Object.entries(d).map(([k, v]) => <li key={k}>
                                        <Title level={4}>{k}</Title>
                                        <Paragraph>{v}</Paragraph>
                                    </li>)}</ul>
                                </li>)}
                            </ul>
                        </Typography>;
                    } else {
                        if (value.trim() === '')
                            return {};
                        return <Typography key={key}>
                            <Title level={3}>{key}</Title>
                            <Paragraph ellipsis={{rows: 3, expandable: true}}>{value}</Paragraph>
                        </Typography>;
                    }
                })}
            </Typography>
        )
    }
}

export class BugMenu extends Component {
    state = {
        expandedKeys: [],
        searchValue: '',
        autoExpandParent: true,
        data: [],
        dataList: [],
        detail: {}
    };

    onExpand = expandedKeys => {
        this.setState({
            expandedKeys,
            autoExpandParent: false,
        });
    };
    onChange = e => {
        const {value} = e.target;
        const expandedKeys = this.state.dataList
            .map(item => {
                if (item.title.indexOf(value) > -1) {
                    return item.parent;
                }
                return null;
            })
            .filter((item, i, self) => item && self.indexOf(item) === i);
        this.setState({
            expandedKeys,
            searchValue: value,
            autoExpandParent: true,
        });
    };
    onSelect = selectedKeys => {
        if (selectedKeys.length === 1) {
            getBugDetail(selectedKeys[0], detail => {
                console.log(detail);
                this.setState({detail});
            });
        }
        console.log(selectedKeys);
    };

    componentWillMount() {
        getBugs((data) => {
            const dataList = generateList(data, []);
            this.setState({data, dataList})
        })
    }

    render() {
        const {searchValue, expandedKeys, autoExpandParent, data} = this.state;
        const loop = d =>
            d.map(item => {
                const index = item.title.indexOf(searchValue);
                const beforeStr = item.title.substr(0, index);
                const afterStr = item.title.substr(index + searchValue.length);
                const title = index > -1 ? (
                    <span>{beforeStr}<span style={{color: '#f50'}}>{searchValue}</span>{afterStr}</span>) : (
                    <span>{item.title}</span>);
                if (item.children) {
                    return (
                        <TreeNode key={item.key} title={title}>
                            {loop(item.children)}
                        </TreeNode>
                    );
                }
                return <TreeNode key={item.key} title={title}/>;
            });
        return (
            <Row type="flex" justify="space-around">
                <Col span={6}>
                    <Search style={{marginBottom: 8}} placeholder="Search" onChange={this.onChange}/>
                    <Tree
                        onExpand={this.onExpand}
                        expandedKeys={expandedKeys}
                        autoExpandParent={autoExpandParent}
                        onSelect={this.onSelect}
                    >
                        {loop(data)}
                    </Tree>
                </Col>
                <Col span={12}>
                    <BugDetail data={this.state.detail}/>
                </Col>
            </Row>
        );
    }
}


BugDetail.defaultProps = {
    data: {
        "名称": "沙门氏菌",
        "给消费者：简述": "沙门氏菌导致两种疾病：（1）肠胃病，能够导致反胃呕吐腹泻痉挛发烧，这些症状大概持续几天并且在一周内会逐渐停止。在其他的健康人当中，这些症状通常会自己逐渐消失，但是可能会导致长期关节炎。 （2）伤寒类疾病，可以是高烧腹泻或者便秘疼痛头痛和嗜睡症（嗜睡或者呆滞），有时是皮疹。这是非常严重的情况，超过10%的未治疗可能死亡。许多种类的食物可能会受到污染，从肉类、鸡蛋到水果和蔬菜，甚至干燥食物，如香料和生坚果。这种伤寒类疾病通常与被污染的饮用水和用污染的水灌溉庄稼有关。一些宠物，像海龟等爬行动物和鸡都能携带沙门氏菌，任何与这些宠物接触的东西都能被沙门氏菌。例如，一位未洗手的宠物主人，能污染食物甚至使他们的皮肤感染沙门氏菌。甚至用肥皂水都很难从食物上洗掉，因此防止食物沙门氏菌的重要措施包括：彻底的烹饪、洗手、生、熟食物分开烹饪，将食物储存在正确的温度中(在40ºF或者低于40ºF中冷冻食物)。免疫系统较弱的人，沙门氏菌能传播到其它器官，导致非常严重的疾病。",
        "微生物": "沙门氏菌肠杆菌科Salmonellae中一种能动的无芽孢的革兰氏阴性杆状细菌。非能动变体包括S. Gallinarum and S. Pullorum。沙门氏菌属均可引起人类疾病。分为：S. enterica S. bongori肠道沙门氏菌是最大的公共卫生问题，包含六个亚种：S. enterica subsp. enterica (I)S. enterica subsp. salamae (II)S. enterica subsp. arizonae (IIIa)S. enterica subsp. diarizonae (IIIb)S. enterica subsp. houtenae (IV)S. enterica subsp. indica (VI)沙门氏菌进一步细分为血清型，根据首次出版于1934年的Kaufmann White分类方案，通过表面和鞭毛抗原性质区分沙门氏菌株。沙门氏菌通常由血清型命名，例如，沙门氏菌亚种。肠道沙门氏菌可进一步分为多种血清型，包括在美国常见的肠炎沙门氏菌和鼠伤寒沙门氏菌，（注：物种名称是斜体，但血清型名字不是斜体）当Kaufmann第一次提出该方案时已发现44种血清型。截至2007年，已发现的血清型数量为2579种。",
        "疾病": [
            {
                "总述": "非伤寒沙门氏菌感染，由非血清型伤寒沙门氏菌和甲型副伤寒沙门氏菌血清型引起。",
                "死亡率": "通常少于1%。但S. Enteritidis在养老院和医院爆发时的死亡率为3.6%，且老年人特别容易被感染。",
                "发病": "暴露后的6-72小时。",
                "感染剂量": "最少可以是一个细胞，取决于宿主的年龄和健康状况以及菌株类型。",
                "症状": "恶心、呕吐、腹部痉挛、腹泻、高烧、头痛。",
                "病程": "症状通常持续4-7天，急性症状通常持续1-2天或者更长时间，这取决于宿主因素、摄入剂量和菌株特性。",
                "疾病和并发症": "（1）腹泻和呕吐可能导致脱水和电解质的失衡，若未及时治疗，这种情况会导致小孩、老人及免疫系统受损的人死亡。（2）在2%的培养病菌证明病例中，反应性关节炎（即免疫反应性关节炎的感染-自身免疫反应，而不是直接由感染本身导致）可能在急性症状发病期之后的3到4周发作。反应性关节炎的表现可能包括例如，关节炎、尿道炎、眼色素层炎和/或者结膜炎（3）非伤寒沙门氏菌感染有时能从肠道进入人体并能导致血液中毒（败血病）或者影响血液、内脏器官、关节（菌血症）。S. Dublin通常与这种并发症有关。",
                "进入途径": "口服（例如，摄入污染的食物、粪便颗粒或受污染的水）。",
                "感染路径": "沙门氏菌从肠壁渗入和传播到发生炎症的小肠上皮细胞中，有证据表明其可能在肠细胞内产生肠毒素。"
            },
            {
                "总述": "由血清型伤寒沙门氏菌和甲型副伤寒沙门氏菌引起，二者均仅在人类中发现。",
                "死亡率": "未经处理，高达10％。",
                "发病": "一般1-3周，但发病可能会长达2个月。",
                "感染剂量": "少于1000个细胞。",
                "症状": "高热，从103℉到104℉；昏睡；消化道症状，包括腹痛、腹泻或便秘；头痛；疼痛；食欲不振。有时会引发平坦的玫瑰色斑点。",
                "病程": "一般为2至4周。",
                "疾病和并发症": "败血症并感染其他组织和器官，例如可能导致心内膜炎。可能导致化脓性关节炎，感染直接影响关节且可能难以治疗。可能导致胆囊慢性感染，这可能导致感染者成为携带者。",
                "进入途径": "口服（例如，摄入污染的食物、粪便颗粒或受污染的水）。",
                "感染路径": "伤寒沙门氏菌从肠壁渗入和传播到小肠上皮细胞并进入血液（即败血症），这可能将病菌携带到体内发生炎症的其他部位。有证据表明可能在肠细胞内产生肠毒素。"
            }
        ],
        "致病频数": "美国每年：非伤寒沙门氏杆菌——最近的报告估计每年在美国国内的非伤寒沙门氏杆菌感染为1027561例，正在报告和诊断的也考虑在内。伤寒发热——同样的报告估计平均每年在美国国内感染伤寒沙门氏菌的为1821例。在美国，的病例与国外旅行有关。总的来说（即无论是不是在国内感染的），估计美国有433例伤寒发热能通过培养鉴定并证实的报告。美国最近的食源性非携带者的伤寒发热发生在1999年，这次病例与热带曼密苹果相关。",
        "来源": "沙门氏菌在自然当中广泛传播。它能移生于脊椎动物的肠道，包括家畜、野生动物家养宠物、人类且总是生活在类似池塘沉积物这样的环境中。它通过口服粪便或者被污染的水进行扩散。(某些原生动物可能扮演着该生物体蓄水池的角色)。例如，可能污染肉、灌溉农场的水（从而污染了田里的产物）、土壤及昆虫、工厂设备、手、厨房表面和器具。因为伤寒沙门氏菌和甲型副伤寒沙门氏菌仅仅在人类宿主中被发现，通常这些菌来源于饮用和/或灌溉未处理的污染水源。在这些微生物流行的地方，强烈建议使用饮用水和煮熟的蔬菜。各种沙门氏菌被在鸡蛋壳外，但是肠炎沙门氏菌可以在鸡蛋内。这强烈暗示菌垂直传播，即在壳形成前，该通过感染的母鸡在蛋白（鸡蛋白）的卵黄囊膜侧（卵黄膜）上沉积。也与某些动物有关，被饲养的宠物，海龟、青蛙和小鸡。食品来源虽然沙门氏菌传统上被认为与动物产品有关，但最近新鲜农产品也一直是主要爆发源。也能很好地生存在低水分的食物如香料，这对于大爆发来说也是重要的因素。一些与沙门氏菌有关的食物包括肉类、家禽、蛋类、奶类及乳制品、鱼、虾、香料、酵母、椰子、酱汁、用未处理的鸡蛋制作的新鲜沙拉酱、蛋糕粉、奶油填充的甜点其配料含有生鸡蛋、干明胶、花生酱、可可，农产品（水果和蔬菜，如西红柿、辣椒、哈密瓜）和巧克力。交叉感染当沙门氏菌从污染源（被污染的食物或被感染的食物处理者或动物）传播到环境中的其他食物或物体时，会发生交叉污染。发生这种情况的一个例子是，在准备或烹饪过程中潜在的受污染的生肉、家禽、海鲜、农产品或鸡蛋未能彼此分开，或在接触到这些产品后，食物处理者未能充分清洁用具、表面、设备和手。污染物可以扩散到工厂和设备表面，以及厨房表面和器具上。交叉污染可能发生在处理食物过程中的任何时刻。处理宠物或野生动物如海龟或青蛙（或其水、土壤或食物和碗），然后处理食物、食物制备器具或环境中的其他物体时也可能发生交叉污染（即使烹饪的青蛙腿引起沙门氏菌病的爆发）。",
        "诊断": "粪便培养物的血清学鉴定。现在可以从纯培养基中鉴定大约100种沙门氏菌血清型，但其余2400多种血清型只能通过传统血清分型来鉴定。",
        "易感人群": "任何年龄的人都可能感染沙门氏菌。免疫系统弱的人特别易感，如小孩和老人，艾滋病或慢性疾病患者和服用一些药物的人。例如：癌症化疗或用于治疗某些类型的关节炎的免疫抑制药物。感染HIV病毒的人感染沙门氏菌的概率至少是正常人的20倍，并且往往反复发作。",
        "食品分析": "许多针对有沙门氏菌污染史的食品的分离和检测方法已经建立。常规培养和鉴定方法可能需要4至6天才有准确结果。为了监测食物，有几种快速的方法，也需要1到2天；包括：基于抗体和分子（DNA或RNA）的检测；但在大多数情况下，出于监管目的仍然需要培养手段来确认沙门氏菌的存在。",
        "爆发实例": "有关最近爆发的信息，请参见疾病控制和预防中心（CDC）的每周发病率和死亡率报告。",
        "信息资源": "The CDC provides information about Salmonella including information about preventing Salmonella Enteritidis infection on avoiding salmonellosis from animal-handling and on typhoid fever.Loci index for genome Salmonella Enteritidis is available from GenBank.\n\n"
    }
};