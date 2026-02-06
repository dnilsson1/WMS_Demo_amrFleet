# Kuka-interface 标准接口

## 目录

Kuka-interface 标准接口 ............................................................................................................................. 1


-- AMR 任务执行相关接口 ....................................................................................................................... 58


1 任务下发 Dispatch Mission （上游系统 -> Kuka 系统） ....................................................................... 58


公共请求参数说明 ................................................................................................................................ 58


1.1 货架移动任务 (missionType=RACK_MOVE) .................................................................................... 69


1.2 辊筒车搬运任务 (missionType=ROLLER_MOVE) ........................................................................... 811


1.3 料箱搬运 (missionType=PICKER_MOVE) ...................................................................................... 1013


1.4 叉车搬运任务 (missionType=FORKLIFT_MOVE) .......................................................................... 1114


1.5 机器人移动任务 (missionType=MOVE) ....................................................................................... 1316


1.6 复合机器人任务 (missionType=ROBOTICS_MOVE) ..................................................................... 1417


**1.7** 牵引类机器人任务 **(missionType=TUGGER_MOVE)** .................................................................. 1619


2 任务取消 Cancel Mission （上游系统 -> Kuka 系统） ...................................................................... 1821


3 任务放行 Resume Workflow （上游系统 -> Kuka 系统） ................................................................ 2023


4 任务重试 Retry Workflow （上游系统 -> Kuka 系统） ..................................................................... 2124


5 作业看板查询接口 Query Jobs （上游系统 -> Kuka 系统） ............................................................ 2124


6 暂停任务 Pause Mission （上游系统 -> Kuka 系统） ....................................................................... 2427


7 恢复任务 Recover Mission （上游系统 -> Kuka 系统） .................................................................... 2528


8 接口回调 Mission Status Callback （ Kuka 系统 -> 上游系统） ........................................................ 2629


-- AMR 容器相关接口 ........................................................................................................................... 2730


9 容器入场 Insert Container （上游系统 -> Kuka 系统） .................................................................... 2730


10 容器出场 Remove Container （上游系统 -> Kuka 系统） ............................................................. 2932


11 容器信息更新 Update Container （暂时支持：位置和空满状态的更新）（上游系统 -> Kuka 系
统） ........................................................................................................................................................ 3033


12 容器模型查询接口 Query Container Model Codes （上游系统 -> Kuka 系统） ........................... 3239


13 查询容器模型推荐的可存放区域 Query Area Codes By Conatiner Model （上游系统 -> Kuka 系
统） ........................................................................................................................................................ 3239


14-1 容器信息查询接口 ( 仅查询入场状态容器 ) Query Containers （上游系统 -> Kuka 系统） ...... 3340


V1.0    08.2025    KUKA AMR 1/63




---

14-2 容器信息查询接口 ( 同时查询入场和离场状态容器 ) Query Containers （上游系统 -> Kuka 系统）

................................................................................................................................................................ 3542


-- 机器人相关接口 ................................................................................................................................ 3744


15 根据点位 UUID 或外部编码查询机器人 Query robot by node UUID or node foreign code （上游系
统 -> Kuka 系统） .................................................................................................................................. 3744


16 机器人信息查询接口 Query Robots （上游系统 -> Kuka 系统） .................................................. 4048


17 下发机器人移动搬运任务 Dispatch Move Carry Task （上游系统 -> Kuka 系统） ...................... 4350


18 下发机器人举升任务 Dispatch lift up container task （上游系统 -> Kuka 系统） ........................ 4451


19 下发机器人降下任务 Dispatch drop down container task （上游系统 -> Kuka 系统） ................ 4552


20 下发机器人移动任务 Dispatch move task （上游系统 -> Kuka 系统） ......................................... 4653


21 机器人充电 Dispatch Charge Robot Task （上游系统 -> Kuka 系统） ........................................... 4755


22 解锁机器人 Unlock robot （上游系统 -> Kuka 系统） ................................................................... 4956


23 入场机器人 Insert The Robot Into The Map （上游系统 -> Kuka 系统） ....................................... 5057


24 离场机器人 Remove The Robot From The Map （上游系统 -> Kuka 系统） ................................. 5158


-- AMR 地图点位与区域相关接口 ....................................................................................................... 5259


25 查询所有 WCS 区域信息 Query All WCS Area Information （上游系统 -> Kuka 系统） ............... 5259


26 区域内点位信息查询 Query Nodes of the Area （上游系统 -> Kuka 系统） ................................ 5360


27 查询点位所属区域 Query Area by Map Node （上游系统 -> Kuka 系统） ................................... 5562


28 查询所有禁行区 Query All Forbidden Areas （上游系统 -> Kuka 系统） ...................................... 5663


29 查询指定禁行区 Query One Forbidden Area （上游系统 -> Kuka 系统） ..................................... 5865


30 更新指定禁行区的状态 Update Forbidden Area Status （上游系统 -> Kuka 系统） ................... 5966


31 查询功能点位 Query Function Node （上游系统 -> Kuka 系统） .................................................. 6168


-- 接口响应报文说明 ............................................................................................................................ 6370


V1.0    08.2025    KUKA AMR 2/63




---

|版本号|修改内容|日期|修改人|
|---|---|---|---|
|**1.2.3**|1.任务下发增加复合机器人类型 <br>2.接口回调，除了missionCode，和<br>missionStatus 都改成非必填|2023.11.22|陈文越|
|**2.0.0**|1.辊筒车任务，新增辊筒取放完成后是<br>否通知字段actionInform<br>2.料箱车任务，新增料箱取放完成后是<br>否通知字段 takeActionInform<br>putActionInform<br>取放交互一般用于与输送线对接时使用|20240708|李南|
|**2.11.1**|1.新增接口：/jobQuery。 <br>2.更新与禁区相关API 以及API<br>/missionCancel 的请求参数和请求体示<br>例。|20240125|赵禾川|
|**2.11.2**|1.新增接口：<br>/queryRobByNodeUuidOrForeignCode。 <br>2.更新API /updateForbiddenAreaStatus<br>的请求参数和请求示例。|20250214|张骞文|
|**2.11.3**|1.新增接口： <br>/queryContainerAll<br>(可以同时查询入场和离场状态的容器) <br>2.更新接口： <br>/containerIn<br>(新增时可以指定容器校验码)|20250310|李南|
|**2.11.4**|1.新增接口： <br>/robotMoveCarry<br>2.新增接口： <br>/queryFunctionNode<br>3.状态回调新增 WAITFEEDBACK 状态类<br>型（流程节点等待放行时回调该状态）|20250414|赵禾川，李南|
|**2.13.0**|1.新增接口： <br>/insertRobot<br>2.新增接口： <br>/removeRobot<br>3.新增接口： <br>/chargeRobot|20250414|赵禾川|
|**2.13.1**|1.任务下发(/submitMission)接口适配牵<br>引车|20250414|张骞文|
|**2.13.3**|1.适配叉车对接箱式货架槽位号|20250605|李南|
|**2.14.0**|1.新增机器人移动、举升、降下接口 <br>2.新增机器人解锁接口 <br>3.新增任务重试接口|20250711|赵禾川|



V1.0    08.2025    KUKA AMR 3/63




---

|2.14.1|更新部分接口的限制或描述<br>（operationFeedback 和<br>updateContainer）|20250731|张骞文|
|---|---|---|---|
|**2.14.2**|新增暂停恢复任务接口|20251021|赵禾川|
|**2.15.0**|1.叉车搬运任务，missionData 适配<br>actionConfirm,actionInform 字段 <br>2.货架移动任务，missionData 取消使用<br>putDown 字段，新增actionType 字段<br>（UP_CONTAINER/DOWN_CONTAINER）<br>实现指令设置|20250819|李南|
|**2.15.0**|插件支持accessToken 鉴权|20251107|赵禾川|


V1.0    08.2025    KUKA AMR 4/63




---

### -- AMR 任务执行相关接口 1 任务下发 Dispatch Mission （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|submitMission|
|---|---|
|**API** 描述|作业任务下发|
|**API URL**|http://[IP:Port]/interfaces/api/amr/submitMission|
|**HTTP Method**|POST|





|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|

#### 公共请求参数说明









|字段名称|参数类型|最大长度|是<br>否<br>必<br>填|默<br>认<br>值|字段描述|备注说明|
|---|---|---|---|---|---|---|
|**orgId**|String||T||库存组织ID(或工<br>厂代码，供应商代<br>码)||
|**requestId**|String|32|T||请求id|处理请求幂等|
|**missionCode**|String||T||任务编码||
|**missionType**|String||T||任务类型： <br>货<br>架(托<br>盘)移<br>动:RACK_MOVE<br>辊筒车搬运任务：<br>ROLLER_MOVE<br>料箱车搬运： <br>PICKER_MOVE<br>叉车搬运：<br>FORKLIFT_MOVE<br>机器人移动： <br>MOVE<br>复合机器人搬运： <br>ROBOTICS_MOVE||
|**viewBoardType**|String||F||任务看板展示任务<br>类型，用户自定义||


V1.0    08.2025    KUKA AMR 5/63




---

|robotType|String|Col3|F|Col5|机器人功能类型<br>顶升类：LIFT<br>辊筒类：ROLLER<br>料箱类：PICKER<br>叉车: FORKLIFT<br>HCS 箱 体 车 ：<br>HCSBOX<br>复 合 机 器 人 ：<br>COMPOSITE|原则上不允许为<br>空；如果为空，<br>就会通过通过机<br>器人具体型号或<br>容器类型编码进<br>行推断|
|---|---|---|---|---|---|---|
|**robotModels**|List<String>||F||机器人具体型号|支持指定多个，<br>会从多个中指定<br>一个合适的执行<br>任务|
|**robotIds**|List<String>||F||机器人编号|支持指定多个，<br>会从多个中指定<br>一个合适的执行<br>任务|
|**priority**|Integer||F|1|作业优先级,1-99,<br>数值越小，优先级<br>越高，默认是1|批量任务下发时<br>有效|
|**containerModelCode**|String||F||容器模型编码||
|**containerCode**|String||F||容器编号||
|**templateCode**|String||F||作业流程模板编号||
|**lockRobotAfterFinish**|Boolean||F|false|是否需要流程结束<br>后机器人保持任务<br>锁定状态|多用于流程结束<br>后，机器人放下<br>容器之后还需要<br>当前小车搬运的<br>场景|
|**unlockRobotId**|String||F||解锁当前小车的在<br>上个任务的锁定状<br>态|如果小车前一个<br>任务流程结束后<br>执行锁车，该字<br>段必填|
|**unlockMissionCode**|String||F||当前小车的上一个<br>任务|用于校验解锁是<br>否正确|
|**idleNode**|String||F||作业流程完成后，<br>指定机器人停放区<br>域/点||
|**missionData**|List<?>||T||当前任务包含的流<br>程节点信息列表具<br>体字段参考一下章<br>节 <br>如果是调用流程模<br>板，则次字段可以<br>不传||

#### 1.1 货架移动任务 ( missionType=RACK_MOVE )



⚫ 请求参数说明









|字段名称|参 数 类<br>型|最 大<br>长度|是 否<br>必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||序号 默认1 为起始货<br>架的起点，，后续需<br>要停留点的需要依次||


V1.0    08.2025    KUKA AMR 6/63




---

|Col1|Col2|Col3|Col4|Col5|递增，终点值最大|Col7|
|---|---|---|---|---|---|---|
|**position**|String||T||作业路径位置||
|**type**|String||T||作业位置类型： <br>点位：NODE_POINT<br>区域：NODE_AREA||
|**actionType**|String||F||动作类型： <br>UP_CONTAINER<br>DOWN_CONTAINER|指定到达对<br>应节点的动<br>作，为空表<br>示无动作|
|**putDown**|Boolean||F|false|作业点位是否需要放<br>下货架|Deprecated|
|**passStrategy**|String||F|AUTO|当前任务点结束后放<br>行策略： <br>自动：AUTO<br>手动：MANUAL||
|**waitingMillis**|Integer||F|0|自动触发离开当前任<br>务节点的时间，默认<br>单位:毫秒|若<br>passStrategy<br>是手动则可<br>不<br>填<br>，<br>passStrategy<br>是自动则必<br>填|


⚫ 请求报文示例

{

"orgId": "UNIVERSAL",

"requestId": "request202309250001",

"missionCode": "mission202309250001",

"missionType": "RACK_MOVE",

"viewBoardType": "",

"robotModels": [

"KMP600I"

],

"robotIds": [

"14"

],

"robotType": "LIFT",

"priority": 1,

"containerModelCode": "10001",

"containerCode": "1000002",

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"idleNode": "A000000013",

"missionData": [

{

"sequence": 1,

"position": "M001-A001-45",

"type": "NODE_POINT",
" actionType ": “UP_CONTAINER”,

"passStrategy": "AUTO",


V1.0    08.2025    KUKA AMR 7/63




---

"waitingMillis": 0

},

{

"sequence": 2,

"position": "M001-A001-40",

"type": "NODE_POINT",

"actionType": “DOWN_CONTAINER”,

"passStrategy": "AUTO",

"waitingMillis": 0

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.2 辊筒车搬运任务 ( missionType=ROLLER_MOVE )



⚫ 请求参数说明
















|字段名称|参 数 类<br>型|最 大<br>长度|是 否<br>必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||序号 默认1 为任务第<br>一个节点，后续需要<br>停留点的需要依次递<br>增，终点值最大||
|**position**|String||T||作业点位||
|**type**|String||T||作业位置类型： <br>点位：NODE_POINT<br>区域：NODE_AREA||
|**binCode**|String||T||辊筒车搬运的容器号||
|**rollerLevel**|Integer||F|1|指定容器放入辊筒车<br>的层数|多层辊筒车<br>需要指定|
|**deviceCode**|String||F||设备编号|当一个点位<br>对应多个设<br>备时需要传<br>入该值|
|**actionType**|String||F||在点位上需要执行的<br>动作 <br>ROLLER_RECEIVE：取 <br>ROLLER_SEND：放|当需要对接<br>输送线且需<br>要自动上下<br>料时，需要<br>传入对应的<br>执行指令；<br>如果是人工<br>上下料或者<br>是夹取料，<br>则可以不传|
|**actionConfirm**|Boolean||F|false|上下料前是否需要确<br>认|一般用于与<br>输送线对接|



V1.0    08.2025    KUKA AMR 8/63




---

|Col1|Col2|Col3|Col4|Col5|Col6|交互|
|---|---|---|---|---|---|---|
|**actionInform**|Boolean||F|false|上下料后是否需要通<br>知|一般用于与<br>输送线对接<br>交互|


⚫ 请求报文示例

{

"orgId": "UNIVERSAL",

"requestId": "request202309250002",

"missionCode": "mission202309250002",

"missionType": "ROLLER_MOVE",

"viewBoardType": "",

"robotModels": [

"KMP600I-1-T2"

],

"robotIds": [

"15"

],

"robotType": "ROLLER",

"priority": 1,

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"idleNode": "A000000013",

"missionData": [

{

"sequence": 1,

"position": "M001-A001-49",

"type": "NODE_POINT",

"actionType": "ROLLER_RECEIVE",

"binCode": "1000002",

"rollerLevel": 1,

"deviceCode": "bea8f740-5dcc-11ee-91ba-c7b4e0c01550",

"actionConfirm": false,

"actionInform": false

},

{

"sequence": 2,

"position": "M001-A001-40",

"type": "NODE_POINT",

"actionType": "ROLLER_SEND",

"binCode": "1000002",

"rollerLevel": 1,

"deviceCode": "bea8f740-5dcc-11ee-91ba-c7b4e0c01550",

"actionConfirm": false,


"actionInform": false

}

]

}


V1.0    08.2025    KUKA AMR 9/63




---

请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.3 料箱搬运 ( missionType=PICKER_MOVE )






















|字段名称|参数类<br>型|最<br>大<br>长<br>度|是<br>否<br>必<br>填|默 认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||搬运料箱序号，从1<br>开始，也可以认为是<br>执行的优先级||
|**startPosition**|String||T||料箱所在的起始点位||
|**startSlotCode**|String||T||料箱所在的起始槽位||
|**endPosition**|String||T||料箱所在的目标点位||
|**endSlotCode**|String||T||料箱所在的目标槽位||
|**binCode**|String||T||料箱号||
|**takeActionConfirm**|Boolean||F|false|取料箱时之前是否需<br>要确认|一般用于与输送线<br>对接时交互|
|**takeActionInform**|Boolean||F|false|取料箱后是否需要通<br>知|一般用于与输送线<br>对接时交互|
|**putActionConfirm**|Boolean||F|false|放料箱时之前是否需<br>要确认|一般用于与输送线<br>对接时交互|
|**putActionInform**|Boolean||F|false|放料箱后是否需要通<br>知|一般用于与输送线<br>对接时交互|



⚫ 请求报文示例

{

"orgId": "",

"requestId": "",

"missionCode": "",

"missionType": "",

"viewBoardType": "",

"robotModels": [],

"robotIds": [],

"robotType": "",

"priority": 0,

"containerModelCode": "",

"containerCode": "",

"templateCode": "",

"lockRobotAfterFinish": true,

"unlockRobotId": "",

"unlockMissionCode": "",

"idleNode": "",

"missionData": [


V1.0    08.2025    KUKA AMR 10/63




---

{

"sequence": 1,

"binCode": "box-001",

"startPosition": "",

"startSlotCode": "",

"takeActionConfirm": false,

"takeActionInform": false,

"endPosition": "",

"endSlotCode": "",

"putActionConfirm": false,

"putActionInform": false

},

{

"sequence": 2,

"binCode": "box-002",

"startPosition": "",

"startSlotCode": "",

"takeActionConfirm": false,


"takeActionInform": false,

"endPosition": "",

"endSlotCode": "",

"putActionConfirm": false,


"putActionInform": false

},

{

"sequence": 3,

"binCode": "box-003",

"startPosition": "",

"startSlotCode": "",

"takeActionConfirm": false,


"takeActionInform": false,

"endPosition": "",

"endSlotCode": "",

"putActionConfirm": false,


"putActionInform": false

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.4 叉车搬运任务 ( missionType=FORKLIFT_MOVE )


⚫ 请求参数说明


V1.0    08.2025    KUKA AMR 11/63




---

|字段名称|参 数 类<br>型|最 大<br>长度|是 否<br>必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||序号 默认1 为任务第<br>一个节点，后续需要<br>停留点的需要依次递<br>增，终点值最大||
|**position**|String||T||作业点位||
|**type**|String||T|NODE_POINT|点位类型： <br>普通货架点：<br>NODE_POINT<br>区域： <br>NODE_AREA<br>箱式货架槽位号： <br>NODE_SLOT|支持对接普<br>通点位，区<br>域和箱式货<br>架槽位号|
|**stackNumber**|Integer||F|0|叉取的层数/堆叠的层<br>数|预留：表示<br>库位已堆垛<br>层数|
|**actionConfirm**|Boolean||F|false|叉取或放下前是否需<br>要确认|预留：FLEET<br>2.15.0 版本<br>以及以后版<br>本支持|
|**actionInform**|Boolean||F|false|叉取或放下前是否需<br>要通知|预留：FLEET<br>2.15.0 版本<br>以及以后版<br>本支持|


⚫ 请求报文示例

{

"orgId": "9001",

"requestId": "request2023030800001",

"missionCode": "mission2023030800001",

"missionType": "FORKLIFT_MOVE",

"viewBoardType": "W01",

"robotType": "FORKLIFT",

"robotModels": [],

"robotIds": [],

"priority": 1,

"containerModelCode": "",

"containerCode": "forkContainer1",

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"idleNode": "",

"missionData": [

{

"sequence": 1,

"position": "A",

"type": "NODE_POINT",

"stackNumber": 0,

"actionConfirm": false,



"actionInform": false


V1.0    08.2025    KUKA AMR 12/63




---

},

{

"sequence": 2,

"position": "A-1-001-001",

"type": "NODE_SLOT",

"stackNumber": 0,

"actionConfirm": false,


"actionInform": false

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.5 机器人移动任务 ( missionType=MOVE )











|字段名称|参 数 类<br>型|最 大<br>长度|是 否<br>必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||序号 默认1 为经过的<br>第一个点，后续需要<br>停留点的需要依次递<br>增，终点值最大||
|**position**|String||T||作业路径位置||
|**type**|String||T||作业位置类型： <br>点位：NODE_POINT<br>区域：NODE_AREA||
|**passStrategy**|String||F|AUTO|当前任务点结束后放<br>行策略： <br>自动：AUTO<br>手动：MANUAL||
|**waitingMillis**|Integer||F|0|自动触发离开当前任<br>务节点的时间，默认<br>单位:毫秒|若<br>passStrategy<br>是手动则可<br>不<br>填<br>，<br>passStrategy<br>是自动则必<br>填|


⚫ 请求报文示例

{

"orgId": "UNIVERSAL",

"requestId": "request202309250005",

"missionCode": "mission202309250005",

"missionType": "MOVE",

"viewBoardType": "",





V1.0    08.2025    KUKA AMR 13/63




---

"robotModels": [

"KMP600I"

],

"robotIds": [

"14"

],

"robotType": "LIFT",

"priority": 1,

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"missionData": [

{

"sequence": 1,

"position": "M001-A001-26",

"type": "NODE_POINT",

"passStrategy": " MANUAL ",

"waitingMillis": 0

},

{

"sequence": 2,

"position": "M001-A001-31",

"type": "NODE_POINT",

"passStrategy": " MANUAL ",

"waitingMillis": 0

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.6 复合机器人任务 ( missionType=ROBOTICS_MOVE )



⚫ 请求参数说明







|字段名称|参数类型|最 大<br>长度|是 否<br>必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**sequence**|Integer||T||序号 默认1 为起始货<br>架的起点，后续需要<br>停留点的需要依次递<br>增，终点值最大||
|**position**|String||T||作业路径位置||
|**type**|String||T||作业位置类型： <br>点位：NODE_POINT<br>区域：NODE_AREA||


V1.0    08.2025    KUKA AMR 14/63




---

|applicationName|String|Col3|T|Col5|机械臂应用名|Col7|
|---|---|---|---|---|---|---|
|**params**|String||F||机械臂参数（JSON 字<br>符串）||
|**passStrategy**|String||F|AUTO|当前任务点结束后放<br>行策略： <br>自动：AUTO<br>手动：MANUAL||
|**waitingMillis**|Integer||F|0|自动触发离开当前任<br>务节点的时间，默认<br>单位:毫秒|若<br>passStrategy<br>是手动则可<br>不<br>填<br>，<br>passStrategy<br>是自动则必<br>填|


⚫ 请求报文示例

{

"orgId": "UNIVERSAL",

"requestId": "request202311220001",

"missionCode": "mission202311220001",

"missionType": "ROBOTICS_MOVE",

"viewBoardType": "",

"robotModels": [

"KMR-IISY"

],

"robotIds": [

"15"

],

"robotType": "COMPOSITE",

"priority": 1,

"containerModelCode": "10001",

"containerCode": "1000002",

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"idleNode": "A000000014",

"missionData": [

{

"sequence": 1,

"position": "M001-A001-45",

"type": "NODE_POINT",

"applicationName ": “app”,

"params": “{\"key1\": \"value1\",\"key2\": \"value2\"}”,

"passStrategy": "AUTO",

"waitingMillis": 0

},

{

"sequence": 2,

"position": "M001-A001-40",

"type": "NODE_POINT",


V1.0    08.2025    KUKA AMR 15/63




---

"applicationName ": “app”,
"params": “{\"key1\": \"value1\",\"key2\": \"value2\"}”,

"passStrategy": "AUTO",

"waitingMillis": 0

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

#### 1.7 牵引类机器人任务 (missionType=TUGGER_MOVE)










|字段名称|参数类<br>型|是否必填|默认值|字段描述|项目用途|
|---|---|---|---|---|---|
|**sequence**|Integer|T||序号 默认1 为经过的<br>第一个点，后续需要<br>停留点的需要依次递<br>增，终点值最大||
|**type**|String|T||作业位置类型： <br>点位：NODE_POINT<br>区域：NODE_AREA||
|**position**|String|T||作业路径位置||
|**actionType**|String|F||在点位上需要执行的<br>动作 <br>TUGGER_ATTACH：挂<br>钩指令 <br>TUGGER_DETACH：脱<br>钩指令|不传该值则视为移动。|
|**tugCount**|Integer|F||牵引车后方的拖挂车<br>数量|挂钩指令（TUGGER_ATTACH）<br>时该参数必填，其他指令不用<br>填该参数。 <br> <br>若执行挂钩指令的节点不传该<br>值，则本体保持单车的转弯半<br>径，Fleet 算法保持单车的包络<br>计算，会影响效率。|
|**passStrategy**|String|F|AUTO|当前任务点结束后放<br>行策略： <br>自动：AUTO<br>手动：MANUAL||
|**waitingMillis**|Integer|F|0|自动触发离开当前任<br>务节点的时间，默认<br>单位:毫秒|若passStrategy 是手动则可不<br>填，passStrategy 是自动则必填|



V1.0    08.2025    KUKA AMR 16/63




---

⚫ 请求报文示例 执行挂钩脱钩指令

{

"orgId": "KUKA",

"requestId": "request202504110001",

"missionCode": "mission202504110001",

"missionType": "TUGGER_MOVE",

"viewBoardType": "",

"robotModels": [

"KMT 1500i-4.5"

],

"robotIds": [

"14"

],

"robotType": "TUGGER",

"priority": 1,

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"missionData": [

{

"sequence": 1,

"type": "NODE_POINT",

"position": "Node34",

"actionType":"TUGGER_ATTACH",

"tugCount": 3,

"passStrategy": "MANUAL"

},

{

"sequence": 2,

"type": "NODE_AREA",

"position": "AREA0001",

"actionType":"TUGGER_DETACH",

"passStrategy": "AUTO",

"waitingMillis": 0

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

⚫ 请求报文示例 执行普通移动

{


V1.0    08.2025    KUKA AMR 17/63




---

"orgId": "KUKA",

"requestId": "request202504110001",

"missionCode": "mission202504110001",

"missionType": "TUGGER_MOVE",

"viewBoardType": "",

"robotModels": [

"KMT 1500i-4.5"

],

"robotIds": [

"14"

],

"robotType": "TUGGER",

"priority": 1,

"templateCode": "",

"lockRobotAfterFinish": false,

"unlockRobotId": "",

"unlockMissionCode": "",

"missionData": [

{

"sequence": 1,

"type": "NODE_POINT",

"position": "Node34"

},

{

"sequence": 2,

"type": "NODE_AREA",

"position": "AREA0001",

"passStrategy": "AUTO",

"waitingMillis": 0

}

]

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

### 2 任务取消 Cancel Mission （上游系统 -> Kuka 系统）


⚫ API 基本信息

|API 名称|missionCancel|
|---|---|
|**API** 描述|任务取消|
|**API URL**|http://[IP:Port]/interfaces/api/amr/missionCancel|



V1.0    08.2025    KUKA AMR 18/63




---

**HTTP Method** POST








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明















|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默 认<br>值|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|---|
|**requestId**|String|32|T||请求id，幂等uuid32 位||
|**missionCode**|String||F||任务编号|三选一必<br>填，优先<br>使用任务<br>号，点位<br>是在某些<br>特定场景<br>使用|
|**containerCode**|String||F||容器编号|容器编号|
|**position**|String||F||节点编号|节点编号|
|**cancelMode**|String||T|FORCE|取消模式： <br>FORCE强制取消，立即结<br>束当前指令 <br>NORMAL普通取消，不会<br>取消小车正在执行的任<br>务，等待小车把当前任务<br>执行完，再取消流程 <br>REDIRECT_END前往终点，<br>不会取消小车正在执行的<br>任务，等待小车把当前任<br>务执行完，如果目标点不<br>需要降下货架，则小车携<br>带货架前往终点，否则空<br>车移动至终点 <br>REDIRECT_START前往起<br>点，不会取消小车正在执<br>行的任务，等待小车把当<br>前任务执行完，如果目标<br>点不需要降下货架，则小<br>车携带货架回到起点，否<br>则空车移动回到起点|当前只有<br>LIFT 类型<br>机器人的<br>任务支持<br>所有策<br>略，其他<br>类型支持<br>FORCE,但<br>是具体还<br>需要看机<br>器人维度<br>是否支持<br>取消|
|**reason **|String||F||取消原因||


⚫ 请求报文示例

{

"requestId": "request202309250006",

"missionCode": "mission202309250004",

"containerCode": "",

"position": "",





V1.0    08.2025    KUKA AMR 19/63




---

"cancelMode": "FORCE",

"reason": ""

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

### 3 任务放行 Resume Workflow （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|operationFeedback|
|---|---|
|**API** 描述|节点passStrategy 为MANUAL 时，调用此接口以放行作业，使作业继续|
|**API URL**|http://[IP:Port]/interfaces/api/amr/operationFeedback|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明

|字段名称|参数类型|最大长度|是否必填|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|
|**requestId**|String|32|T|请求id,幂等uuid32 位||
|**missionCode**|String||F|当前执行作业id|三选一|
|**containerCode**|String||F|当前执行任务的容器号|当前执行任务的容器号|
|**position**|String||F|当前执行作业的节点|当前执行作业的节点|



⚫ 请求报文示例

{

"requestId": "request202309250007",

"containerCode": "",

"missionCode": "mission202309250005",

"position": ""

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,


V1.0    08.2025    KUKA AMR 20/63




---

"success": true

}

### 4 任务重试 Retry Workflow （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|retryMission|
|---|---|
|**API** 描述|对流程当前正在执行的机器人任务或者设备任务进行重试。|
|**API URL**|http://[IP:Port]/interfaces/api/amr/retryMission|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明

|字段名称|参数类型|最大长度|是否必填|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|
|**taskCode**|String||F|需要重试的作业的jobCode|三选一|
|**containerCode**|String||F|当前执行任务的容器号|当前执行任务的容器号|
|**robotId**|String||F|当前执行作业的机器人编<br>码|当前执行作业的机器人编<br>码|



⚫ 请求报文示例

{

"taskCode": "task202309250007"

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message":"Success",

"success": true

}

### 5 作业看板查询接口 Query Jobs （上游系统 -> Kuka 系统）


⚫ API 基本信息

|API 名称|jobQuery|
|---|---|
|**API** 描述|作业看板查询接口|



V1.0    08.2025    KUKA AMR 21/63




---

|API URL|http://[IP:Port]/interfaces/api/amr/jobQuery|
|---|---|
|**HTTP Method**|POST|






|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明










|字段名称|参数类型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**workflowId**|Long||F||流程实例id||
|**containerCode**|String||F||容器编码||
|**jobCode**|String||F||作业编号||
|**status**|String||F||作业状态 <br>10：待执行；20：执行<br>中；25：等待放行；<br>28：取消中；30：已完<br>成；31：已取消；35：<br>手动完成；50：告警；<br>60：流程启动异常||
|**robotId**|String||F||机器人编号||
|**targetCellCode**|String||F||目标点位||
|**workflowName**|String||F||流程配置名称||
|**workflowCode**|String||F||流程配置编码||
|**maps**|List<String>||F||地图编码集合||
|**createUsername**|String||F||操作员||
|**sourceValue**|Integer||F||来源 <br>2：接口平台任务；3：<br>PDA 任务；4：设备任<br>务；5：MLS 任务；6：<br>前端界面触发；7：流<br>程事件触发；||
|**limit**|Integer||F|10|返回作业条数，默认返<br>回10 条||



⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**jobCode**|String|作业编号||
|**workflowId**|Long|流程实例id||
|**containerCode**|String|容器编号||
|**robotId**|String|小车编号||
|**status**|Integer|作业状态 <br>10：待执行；20：执行||


V1.0    08.2025    KUKA AMR 22/63




---

|Col1|Col2|中；25：等待放行；<br>28：取消中；30：已完<br>成；31：已取消；35：<br>手动完成；50：告警；<br>60：流程启动异常|Col4|
|---|---|---|---|
|**workflowName**|String|流程名称||
|**workflowCode**|String|流程编码||
|**workflowPriority**|Integer|流程优先级||
|**mapCode**|String|地图编码||
|**targetCellCode**|String|目标点位||
|**beginCellCode**|String|起始点位||
|**targetCellCodeForeign**|String|目标点位外部编码||
|**beginCellCodeForeign**|String|起始点位外部编码||
|**finalNodeCode**|String|最终节点编码||
|**warnFlag**|Integer|告警标志 <br>0：正常；1：告警||
|**warnCode**|String|告警编码||
|**completeTime**|String|流程结束时间（yyyy-<br>MM-dd HH:mm:ss）||
|**spendTime**|Integer|流程花费时间（秒）||
|**createUsername**|String|操作员||
|**createTime**|String|流程创建时间（yyyy-<br>MM-dd HH:mm:ss）||
|**source**|String|作业来源 <br>INTERFACE：接口平台；<br>PDA：PDA<br>触<br>发<br>；<br>DEVICE：设备触发；<br>MLS：MLS 触发；SELF：<br>前端界面触发；EVENT：<br>流程事件触发；||
|**materialsInfo**|String|物料信息|现场需要<br>对容器进<br>行物料管<br>理时使用|


⚫ 请求报文示例（仅供参考，根据实际需要填写参数，所有字段非必填）

{

"containerCode": "C001",

"createUsername": "admin",

"jobCode": "T000096284",

"limit": 10,

"maps": ["TEST"],

"robotId": "1",

"sourceValue": 6,

"status": 20,

"targetCellCode": "TEST-1-90",

"workflowCode": " W000000587",

"workflowId": 100218,

"workflowName": "Carry01"

}
⚫ 请求返回报文示例

{


V1.0    08.2025    KUKA AMR 23/63




---

"data": [

{

"jobCode": "T000096284",

"workflowId": 100218,

"containerCode": "C001",

"robotId":"1",

"status": 20,

"workflowName": "Carry01",

"workflowCode": " W000000587",

"workflowPriority": 1,

"mapCode": "TEST",

"targetCellCode": "TEST-1-90",

"beginCellCode": "TEST-1-80",

"targetCellCodeForeign": "DROPPOINT",

"beginCellCodeForeign": "PICKPOINT",

"finalNodeCode": "TEST-1-90",

"warnFlag": 0,

"warnCode": null

"completeTime": null,

"spendTime": null,

"createUsername": "admin",

"createTime": "2025-01-10 16:01:42",

"source": "SELF",

"materialsInfo": "-"

} ],

"code": "0",

"message": null,

"success": true

}

### 6 暂停任务 Pause Mission （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|pauseMission|
|---|---|
|**API** 描述|通过作业编号或者机器人编号暂停任务|
|**API URL**|http://[IP:Port]/interfaces/api/amr/pauseMission|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



V1.0    08.2025    KUKA AMR 24/63




---

⚫ 请求参数说明

|字段名称|参数类型|最大长度|是否必填|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|
|**missionCode**|String||F|当前执行作业编号|二选一|
|**robotId**|String||F|机器人编号|机器人编号|



⚫ 请求报文示例
通过作业编号暂停：

{

"missionCode": "mission202309250005"

}
通过机器人编号暂停：

{

" robot Id": "2"

}
⚫ 请求返回报文示例

{

"data": "",

"code": "0",

"message": "lang.wcs.common.ok",

"success": true

}

### 7 恢复任务 Recover Mission （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|recoverMission|
|---|---|
|**API** 描述|通过作业编号或者机器人编号恢复任务|
|**API URL**|http://[IP:Port]/interfaces/api/amr/recoverMission|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明

|字段名称|参数类型|最大长度|是否必填|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|
|**missionCode**|String||F|当前执行作业编号|二选一|
|**robotId**|String||F|机器人编号|机器人编号|



⚫ 请求报文示例
通过作业编号恢复：


V1.0    08.2025    KUKA AMR 25/63




---

{

"missionCode": "mission202309250005"

}
通过机器人编号恢复：

{

" robot Id": "2"

}
⚫ 请求返回报文示例

{

"data": "",

"code": "0",

"message": "lang.wcs.common.ok",

"success": true

}

### 8 接口回调 Mission Status Callback （ Kuka 系统 -> 上游系统）


⚫ API 基本信息



|API 名称|missionStateCallback|
|---|---|
|**API** 描述|容器相关操作，出场|
|**API URL**|http://[IP:Port]/interfaces/api/amr/missionStateCallback|
|**HTTP Method**|POST|


⚫ 请求参数说明











|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|---|
|**missionCode**|String|32|T||作业id||
|**viewBoardType **|String||F||作业类型||
|**containerCode**|String||F||容器编号||
|**currentPosition**|String||F||容器当前位置||
|**slotCode**|String||F||当前所在槽位||
|**robotId**|String||F||执行当前任务的机器人id||
|**missionStatus**|String||T||作业当前状态 <br>开始移动：MOVE_BEGIN<br>到达任务节点：ARRIVED<br>顶<br>升<br>完<br>成<br>：<br>UP_CONTAINER<br>放<br>下<br>完<br>成<br>：<br>DOWN_CONTAINER<br>辊<br>筒<br>上<br>料<br>完<br>成: <br>ROLLER_RECEIVE<br>辊<br>筒<br>下<br>料<br>完<br>成: <br>ROLLER_SEND<br>料<br>箱<br>取<br>料<br>完<br>成: <br>PICKER_RECEIVE<br>料<br>箱<br>下<br>料<br>完<br>成: <br>PICKER_SEND<br>叉车叉取完成：||


V1.0    08.2025    KUKA AMR 26/63




---

|Col1|Col2|Col3|Col4|Col5|FORK_UP<br>叉车放下完成：<br>FORK_DOWN<br>等待放行：WAITFEEDBACK<br>任务完成：COMPLETED<br>任务取消完成：CANCELED|Col7|
|---|---|---|---|---|---|---|
|**message**|String||F||说明信息||
|**missionData**|||F||需要上报的定制信息对象||


⚫ 请求报文示例

{

"missionCode": "mission202309250005",

"viewBoardType": "",

"slotCode": "",

"robotId": "14",

"containerCode": "1000002",

"currentPosition": "M001-A001-31",

"missionStatus": "MOVE_BEGIN",

"message": "",

"missionData": {}

}

### -- AMR 容器相关接口 9 容器入场 Insert Container （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|containerIn|
|---|---|
|**API** 描述|容器相关操作，入场|
|**API URL**|http://[IP:Port]/interfaces/api/amr/containerIn|
|**HTTP Method**|POST|



|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|


⚫ 请求参数说明













V1.0    08.2025    KUKA AMR 27/63




---

|requestId|String|32|T|Col5|请 求 id， 幂 等<br>uuid32 位|Col7|
|---|---|---|---|---|---|---|
|**containerType**|String||F||容器类型 <br>货架：RACK<br>料箱：BIN(暂未实<br>现)||
|**containerModelCode**|String||F||容器模型编码|当<br>isNew=true<br>时必传|
|**containerCode**|String||T||容器编号||
|**enterOrientation**|String|32|F||容器入场角度|货架入场<br>时对角度<br>有特殊要<br>求|
|**position**|String||T||容器当前对应位置||
|**isNew**|Boolean||F|false|是否时新增容器||
|**containerValidationCode**|String||F||容器校验码|当<br>isNew=true<br>时可以指<br>定是否配<br>置校验码|
|**withDefaultValidationCode**|Boolean||F|false|配置容器默认校验<br>码|当<br>isNew=true<br>时配置容<br>器默认校<br>验码（同<br>容<br>器<br>编<br>号）|


⚫ 请求报文示例（当前货架入场）

{

"requestId": "request202309250008",

"containerType": "",

"containerCode": "10",

"position": "M001-A001-31",

"containerModelCode": "",

"enterOrientation": "",

"isNew": false

}
⚫ 请求报文示例（货架新增并入场, 不配置校验码）

{

"requestId": "request202309250009",

"containerType": "",

"containerCode": "10",

"position": "M001-A001-31",

"containerModelCode": "model1",

"enterOrientation": "",

"isNew": true,

"containerValidationCode": "",


"withDefaultValidationCode": false

}
⚫ 请求报文示例（货架新增并入场, 配置指定校验码）


V1.0    08.2025    KUKA AMR 28/63




---

{

"requestId": "request202309250010",

"containerType": "",

"containerCode": "10",

"position": "M001-A001-31",

"containerModelCode": "model1",

"enterOrientation": "",

"isNew": true,

"containerValidationCode": " ID: 10",


"withDefaultValidationCode": false

}
⚫ 请求报文示例（货架新增并入场, 配置默认校验码）

{

"requestId": "request202309250011",

"containerType": "",

"containerCode": "10",

"position": "M001-A001-31",

"containerModelCode": "model1",

"enterOrientation": "",

"isNew": true,

"containerValidationCode": "",


"withDefaultValidationCode": true

}

⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}

### 10 容器出场 Remove Container （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|containerOut|
|---|---|
|**API** 描述|容器相关操作，出场|
|**API URL**|http://[IP:Port]/interfaces/api/amr/containerOut|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



V1.0    08.2025    KUKA AMR 29/63




---

⚫ 请求参数说明











|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|---|
|**requestId**|String|32|T||请求id，幂等uuid32 位||
|**containerType**|String||F|RACK|容器类型 <br>货架：RACK<br>料箱：BIN(暂未实现)||
|**containerCode**|String||T||容器编号||
|**position**|String||F||容器出场位置||
|**isDelete**|Boolean||F|false|出场后是否删除||


⚫ 请求报文示例

{

"requestId": "request202309250009",

"containerType": "",


"containerCode": "10",

"position": "M001-A001-31",

"isDelete": false

}
⚫ 请求返回报文示例

{


"data": null,

"code": "0",

"message": null,

"success": true

}

### 11 容器信息更新 Update Container （暂时支持：位置和空满状态的更 新）（上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|updateContainer|
|---|---|
|**API** 描述|容器信息更新接口|
|**API URL**|http://[IP:Port]/interfaces/api/amr/updateContainer|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



V1.0    08.2025    KUKA AMR 30/63




---

⚫ 请求参数说明











|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用<br>途|
|---|---|---|---|---|---|---|
|**requestId**|String|32|T||请求id，幂等uuid32 位||
|**containerType**|String||F||容器类型 <br>货架：RACK<br>料箱：BIN(暂不支持)||
|**containerCode**|String||T||容器编号||
|**originPosition**|String||F||容器原始位置||
|**targetPosition**|String||F||容器目标位置|容器目标<br>位置和容<br>器空满状<br>态，至少<br>有一个字<br>段需要传<br>值|
|**emptyStatus**|String||F||容器的空满状态: <br>空：EMPTY<br>满：FULL|容器的空满状态: <br>空：EMPTY<br>满：FULL|
|**reason**|String||F||更新原因||


⚫ 请求报文示例

{

"requestId": "request202309250010",

"containerType": "BUCKET",

"containerCode": "10",

"originPosition": "M001-A001-31",

"targetPosition": "M001-A001-30",

"emptyStatus": "EMPTY",

"reason": ""

}
⚫ 请求返回报文示例

{

"data": null,

"code": "0",

"message": null,

"success": true

}



V1.0    08.2025    KUKA AMR 31/63




---

### 12 容器模型查询接口 Query Container Model Codes （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|queryAllContainerModelCode|
|---|---|
|**API** 描述|查询所有已配置容器模型|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryAllContainerModelCode|
|**HTTP Method**|GET|



|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|


⚫ 无请求参数
⚫ 请求返回报文示例

{

"code": "0",

"message": null,

"success": true,

"data": [

"10001"

]

}






### 13 查询容器模型推荐的可存放区域 Query Area Codes By Conatiner Model （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|queryAreaCodeForContainerModel|
|---|---|
|**API** 描述|查询容器模型推荐的可存放区域|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryAreaCodeForContainerModel|
|**HTTP Method**|GET|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



V1.0    08.2025    KUKA AMR 32/63




---

⚫ 请求参数说明










|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项 目 用<br>途|
|---|---|---|---|---|---|---|
|**containerModelCode**|String||T||容器模型编码||
|**noContainerFirst**|Boolean||F|false|是否区域内无容器优先： <br>ture是 <br>false否||



⚫ 请求 URL 示例

http://[IP:Port]/interfaces/api/amr/queryAreaCodeForContainerModel?containerModelCode=10001&

noContainerFirst=false
⚫ 请求返回报文示例

{

"code": "0",

"message": "",

"success": true,

"data": [

"areaCode1",

"areaCode2",

"areaCode3"

]

}

### 14-1 容器信息查询接口 ( 仅查询入场状态容器 ) Query Containers （上游 系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|containerQuery|
|---|---|
|**API** 描述|容器信息查询接口(仅查询入场状态的容器)|
|**API URL**|http://[IP:Port]/interfaces/api/amr/containerQuery|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**containerCode**|String||F||容器编码||


V1.0    08.2025    KUKA AMR 33/63




---

|nodeCode|String|Col3|F|Col5|点位编码|Col7|
|---|---|---|---|---|---|---|
|**areaCode**|String||F||区域编码||
|**containerModelCode**|String||F||容器模型编码||
|**emptyFullStatus**|Integer||F|2|容器的空满状态: <br>空 0<br>满 1<br>全部 2|空满只有<br>在区域编<br>码有值时<br>才会生效|


⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**containerCode**|String|容器编码||
|**nodeCode**|String|点位编码||
|**inMapStatus**|Integer|入场/离场状态 <br>0-离场，1-入场||
|**containerModelCode**|String|容器模型||
|**emptyFullStatus**|String|0-空1-满||
|**isCarry**|Integer|搬运状态 0-静止，1-搬<br>运中||
|**orientation**|String|容器朝向角度||
|**containerCheckCode**|String|容器校验码||
|**mapCode**|String|地图编码||
|**districtCode**|String|地图片区编码||


⚫ 请求报文示例（查询指定容器）

{

"nodeCode": "M001-A001-30",

"containerModelCode": "10001",

"containerCode": "10",

"areaCode": "A000000014",

"emptyFullStatus": 2

}
⚫ 请求返回报文示例

{

"data": [

{

"containerCode": "10",

"nodeCode": "",

"orientation": "0.0",

"containerModelCode": "10001",

"emptyFullStatus": 0,

"inMapStatus": 1,

"isCarry": 0,

"containerCheckCode": "10",

"mapCode": "ABC",


"districtCode": "1"

}

],

"code": "0",

"message": null,


V1.0    08.2025    KUKA AMR 34/63




---

"success": true

}

### 14-2 容器信息查询接口 ( 同时查询入场和离场状态容器 ) Query Containers （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|containerQueryAll|
|---|---|
|**API** 描述|容器信息查询接口(同时查询入场和离场状态的容器)|
|**API URL**|http://[IP:Port]/interfaces/api/amr/containerQueryAll|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明










|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**containerCode**|String||F||容器编码||
|**nodeCode**|String||F||点位编码||
|**areaCode**|String||F||区域编码||
|**mapCode**|String||F||地图编码||
|**districtCode**|String||F||地图片区编码||
|**containerModelCode**|String||F||容器模型编码||
|**emptyFullStatus**|Integer||F||容器的空满状态: <br>空 0<br>满 1||
|**inMapStatus**|Integer||F||容器入场离场状态 <br>离场 0<br>入场1||



⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**containerCode**|String|容器编码||
|**nodeCode**|String|点位编码||
|**inMapStatus**|Integer|入场/离场状态 <br>0-离场，1-入场||
|**containerModelCode**|String|容器模型||
|**emptyFullStatus**|String|0-空1-满||


V1.0    08.2025    KUKA AMR 35/63




---

|isCarry|Integer|搬运状态 0-静止，1-搬<br>运中|Col4|
|---|---|---|---|
|**orientation**|String|容器朝向角度||
|**containerCheckCode**|String|容器校验码||
|**mapCode**|String|地图编码||
|**districtCode**|String|地图片区编码||


⚫ 请求报文示例（查询指定地图所有容器）

{

" map Code": "ABC"

}
⚫ 请求返回报文示例

{

"data": [

{

"containerCode": "10",

"nodeCode": "1-1",

"orientation": "0.0",

"containerModelCode": "10001",

"emptyFullStatus": 0,

"inMapStatus": 1,

"isCarry": 0,

"containerCheckCode": "10",

"mapCode": "ABC",


"districtCode": "1"

},

{

"containerCode": "20",

"nodeCode": "1-1",

"orientation": "0.0",

"containerModelCode": "10001",

"emptyFullStatus": 0,

"inMapStatus": 0,

"isCarry": 0,

"containerCheckCode": "20",

"mapCode": "ABC",


"districtCode": "1"

}


],

"code": "0",

"message": null,

"success": true

}


V1.0    08.2025    KUKA AMR 36/63




---

### --  机器人相关接口 15 根据点位 UUID 或外部编码查询机器人 Query robot by node UUID or node foreign code （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|queryRobByNodeUuidOrForeignCode|
|---|---|
|**API 描述**|根据点位UUID 或点位外部编码查询机器人|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryRobByNodeUuidOrForeignCode|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明











|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**nodeCode**|String||T||点位UUID 或点位外部编<br>码|根据点位<br>UUID 或外<br>部编码查<br>询<br>机<br>器<br>人，查询<br>多个时用<br>英文逗号<br>分隔。|


⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**robotId**|String|机器人编码||
|**robotType**|String|机器人型号||
|**mapCode**|String|地图编码||
|**floorNumber**|String|片区编码||
|**buildingCode**|String|工厂或者仓库编码||
|**containerCode**|String|机器人持有容器的编码||
|**status**|Integer|1-离场；2-离线；3-空<br>闲；4-任务中；5-充电<br>中；6-更新中；7-异常||
|**occupyStatus**|Integer|是否占用：0-未占用；1-<br>占用||


V1.0    08.2025    KUKA AMR 37/63




---

|batteryLevel|Double|电量（单位：百分比）|Col4|
|---|---|---|---|
|**nodeCode**|String|当前点位||
|**X **|String|机器人当前所处坐标<br>x(单位：毫米)||
|**Y **|String|机器人当前所处坐标<br>y(单位：毫米)||
|**robotOrientation**|String|机器人当前角度||
|**missionCode**|String|当前任务号|上游下发<br>任务号|
|**liftStatus**|Integer|机器人顶升状态（1：顶<br>升；0：未顶升）||
|**reliability**|Integer|定位置信度: 0-不可信；<br>1-可信||
|**runTime**|String|运行时长||
|**karOsVersion**|String|软件版本||
|**mileage**|String|运行总里程||
|**leftMotorTemperature**|String|左电机温度||
|**rightMotorTemperature**|String|右电机温度||
|**liftMotorTemperature**|String|顶升电机温度||
|**rotateMotorTemperature**|String|旋转电机温度||
|**rotateTimes**|Integer|托盘旋转次数||
|**liftTimes**|Integer|托盘顶升次数||
|**nodeForeignCode**|String|机器人所在节点的外部<br>编码|当使用节<br>点的外部<br>编码查询<br>机器人<br>时，该字<br>段将有<br>值。|


⚫ 请求报文示例
1) 示例 1
{
"nodeCode": "startNode1, startNode2"
}

2) 示例 2

{

"nodeCode": "test01-5-91"

}

⚫ 返回报文示例
1) 示例 1
{
"data": [
{
"robotId": "925",
"robotType": "KMP600I",
"mapCode": "test01",
"floorNumber": "5",
"buildingCode": "test",
"containerCode": "",


V1.0    08.2025    KUKA AMR 38/63




---

"status": 3,
"occupyStatus": 0,
"batteryLevel": 1,
"nodeCode": "test01-5-64",
"x": "3000.0",
"y": "15000.0",
"robotOrientation": "90.0",
"missionCode": null,
"liftStatus": 0,
" reliability ": 1,
" runTime ": "6745",
" karOsVersion ": "",
" mileage ": "0.0",
" leftMotorTemperature ": "0.0",
" rightMotorTemperature ": "0.0",
" liftMotorTemperature ": "0.0",
" rotateMotorTemperature ": "0.0",
" rotateTimes ": 0,
" liftTimes ": 0,
"nodeForeignCode": " startNode1"
},
{
"robotId": "80211",
"robotType": "KMP600I",
"mapCode": "test01",
"floorNumber": "5",
"buildingCode": "test",
"containerCode": "",
"status": 3,
"occupyStatus": 0,
"batteryLevel": 1,
"nodeCode": "test01-5-74",
"x": "1200.0",
"y": "2400.0",
"robotOrientation": "0.0",
"missionCode": null,
"liftStatus": 0,
" reliability ": 1,
" runTime ": "null",
" karOsVersion ": "",
" mileage ": "0.0",
" leftMotorTemperature ": "0.0",
" rightMotorTemperature ": "0.0",
" liftMotorTemperature ": "0.0",
" rotateMotorTemperature ": "0.0",
" rotateTimes ": 0,
" liftTimes ": 0,
"nodeForeignCode": " startNode2"
}
],
"code": "0",


V1.0    08.2025    KUKA AMR 39/63




---

"message": null,

"success": true

}


2) 示例 2
{
"data": [
{
"robotId": "2041",
"robotType": "KMP600I",
"mapCode": "test01",
"floorNumber": "5",
"buildingCode": "test",
"containerCode": "",
"status": 3,
"occupyStatus": 0,
"batteryLevel": 1,
"nodeCode": "test01-5-91",
"x": "13000.0",
"y": "30000.0",
"robotOrientation": "-90.0",
"missionCode": null,
"liftStatus": 0,
" reliability ": 1,
" runTime ": "6745",
" karOsVersion ": "",
" mileage ": "0.0",
" leftMotorTemperature ": "0.0",
" rightMotorTemperature ": "0.0",
" liftMotorTemperature ": "0.0",
" rotateMotorTemperature ": "0.0",
" rotateTimes ": 0,
" liftTimes ": 0,
"nodeForeignCode": ""
}
],
"code": "0",
"message": null,

"success": true

}

### 16 机器人信息查询接口 Query Robots （上游系统 -> Kuka 系统）


⚫ API 基本信息

|API 名称|robotQuery|
|---|---|
|**API** 描述|机器人信息查询接口(默认查所有)|
|**API URL**|http://[IP:Port]/interfaces/api/amr/robotQuery|
|**HTTP Method**|POST|



V1.0    08.2025    KUKA AMR 40/63




---

|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明










|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||F||机器人编码|1）如果参<br>数值都为<br>空，则默认<br>查全部。 <br> <br>2）请求参<br>数 mapCode<br>和 <br>floorNumber<br>必须一起传<br>递。|
|**robotType**|String||F||机器人型号|机器人型号|
|**mapCode**|String||F||地图编码（禁用地图结<br>果为空）|地图编码（禁用地图结<br>果为空）|
|**floorNumber**|String||F||片区编码（禁用片区结<br>果为空）|片区编码（禁用片区结<br>果为空）|



⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**robotId**|String|机器人编码||
|**robotType**|String|机器人型号||
|**mapCode**|String|地图编码||
|**floorNumber**|String|片区编码||
|**buildingCode**|String|工厂或者仓库编码||
|**containerCode**|String|机器人持有容器的编码||
|**status**|Integer|1-离场；2-离线；3-空<br>闲；4-任务中；5-充电<br>中；6-更新中；7-异常||
|**occupyStatus**|Integer|是否占用：0-未占用；1-<br>占用||
|**batteryLevel**|Double|电量（单位：百分比）||
|**nodeCode**|String|当前点位||
|**X **|String|机器人当前所处坐标<br>x(单位：毫米)||
|**Y **|String|机器人当前所处坐标<br>y(单位：毫米)||
|**robotOrientation**|String|机器人当前角度||
|**missionCode**|String|当前任务号|上游下发<br>任务号|
|**liftStatus**|Integer|机器人顶升状态（1：顶<br>升；0：未顶升）||


V1.0    08.2025    KUKA AMR 41/63




---

|reliability|Integer|定位置信度: 0-不可信；<br>1-可信|Col4|
|---|---|---|---|
|**runTime**|String|运行时长||
|**karOsVersion**|String|软件版本||
|**mileage**|String|运行总里程||
|**leftMotorTemperature**|String|左电机温度||
|**rightMotorTemperature**|String|右电机温度||
|**liftMotorTemperature**|String|顶升电机温度||
|**rotateMotorTemperature**|String|旋转电机温度||
|**rotateTimes**|Integer|托盘旋转次数||
|**liftTimes**|Integer|托盘顶升次数||


⚫ 请求报文示例（当前货架入场）

{
"floorNumber": "A001",
"mapCode": "M001",
"robotId": "13",
"robotType": "KMP600I"
}
⚫ 请求返回报文示例

{
"data": [
{
"robotId": "13",
"robotType": "KMP600I",
"mapCode": "M001",
"floorNumber": "A001",
"buildingCode": "W001",
"containerCode": "",
"status": 3,
"occupyStatus": 0,
"batteryLevel": 1,
"nodeCode": "46",
"x": "3000.0",
"y": "15000.0",
"robotOrientation": "90.0",
"missionCode": null,
"liftStatus": 0,
" reliability ": 1,
" runTime ": "6745",
" karOsVersion ": "",
" mileage ": "0.0",
" leftMotorTemperature ": "0.0",
" rightMotorTemperature ": "0.0",
" liftMotorTemperature ": "0.0",
" rotateMotorTemperature ": "0.0",
" rotateTimes ": 0,

" liftTimes ": 0

}
],
"code": "0",


V1.0    08.2025    KUKA AMR 42/63




---

"message": null,

"success": true

}

### 17 下发机器人移动搬运任务 Dispatch Move Carry Task （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|robotMoveCarry|
|---|---|
|**API** 描述|下发机器人移动搬运任务，只在任务列表展示，作业看板不可见。<br>不会锁定机器人。<br>Dispatch a move carry task to the robot. The function is the same as<br>which in the Map Monitor, directly dispatched to the Mission Manager,<br>only displayed in the Mission List, and not visible on the Job Board.|
|**API URL**|http://[IP:Port]/interfaces/api/amr/robotMoveCarry|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**containerCode**|String||T||容器编号||
|**targetNodeCode**|String||T||目标点位编码（点位<br>UUID）||
|**missionCode**|String||F||任务号，下发给mission<br>manager的任务号。不传<br>会自动生成。||


⚫ 返回字段说明
下发成功时，返回任务号

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/robotMoveCarry](http://[IP:Port]/interfaces/api/amr/robotMoveCarry?forbiddenAreaId=2)

{

"robotId": "10001",

"containerCode": "C0002",

"targetNodeCode": "TEST-1-45"


V1.0    08.2025    KUKA AMR 43/63




---

}

⚫ 返回报文示例
示例 1

{

"data": "I-CARRY-1744609148201",

"code": "0",

"message": "OK",

"success": true

}

### 18 下发机器人举升任务 Dispatch lift up container task （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|robotLift|
|---|---|
|**API** 描述|下发机器人举升任务，只在任务列表展示，作业看板不可见。不会<br>锁定机器人。<br>Dispatch a lift container task to the robot. The function is the same as<br>which in the Map Monitor, directly dispatched to the Mission Manager,<br>only displayed in the Mission List, and not visible on the Job Board. The<br>robot won’t be locked after the task finish.|
|**API URL**|http://[IP:Port]/interfaces/api/amr/robotLift|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**containerCode**|String||F||容器编号|不传视为<br>盲顶|
|**moveLift**|Integer||F|1|0：普通举升 <br>1：移动举升||
|**missionCode**|String||F||任务号，下发给mission<br>manager的任务号。不传<br>会自动生成。||


V1.0    08.2025    KUKA AMR 44/63




---

⚫ 返回字段说明
下发成功时，返回任务号

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/robotLift](http://[IP:Port]/interfaces/api/amr/robotLift%20)

{

"robotId": "10001",

"containerCode": "C0002",

"moveLift": 0

}

⚫ 返回报文示例
示例 1

{

"data": "I-LIFT-1744609148201",

"code": "0",

"message": "OK",

"success": true

}

### 19 下发机器人降下任务 Dispatch drop down container task （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|robotDrop|
|---|---|
|**API** 描述|下发机器人降下任务，只在任务列表展示，作业看板不可见。不会<br>锁定机器人。<br>Dispatch a drop down container task to the robot. The function is the<br>same as which in the Map Monitor, directly dispatched to the Mission<br>Manager, only displayed in the Mission List, and not visible on the Job<br>Board. The robot won’t be locked after the task finish.|
|**API URL**|http://[IP:Port]/interfaces/api/amr/robotDrop|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明
字段名称 参 数类 最大 是 否 默认 字段描述 项目用途


V1.0    08.2025    KUKA AMR 45/63




---

|Col1|型|长度|必填|值|Col6|Col7|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**nodeCode**|String||F||点位编码或点位外部编<br>码|传值则为<br>移<br>动<br>降<br>下，不传<br>为原地降<br>下|
|**missionCode**|String||F||任务号，下发给mission<br>manager的任务号。不传<br>会自动生成。||


⚫ 返回字段说明
下发成功时，返回任务号

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/robotDrop](http://[IP:Port]/interfaces/api/amr/robotLift%20)

{

"robotId": "10001",

"nodeCode": "TEST-1-1001"

}

⚫ 返回报文示例
示例 1

{

"data": "I-DROP-1744609148201",

"code": "0",

"message": "OK",

"success": true

}

### 20 下发机器人移动任务 Dispatch move task （上游系统 -> Kuka 系统）


⚫ API 基本信息

|API 名称|robotMove|
|---|---|
|**API** 描述|下发机器人移动任务，只在任务列表展示，作业看板不可见。不会<br>锁定机器人。<br>Dispatch a drop down container task to the robot. The function is the<br>same as which in the Map Monitor, directly dispatched to the Mission<br>Manager, only displayed in the Mission List, and not visible on the Job<br>Board. The robot won’t be locked after the task finish.|
|**API URL**|http://[IP:Port]/interfaces/api/amr/robotMove|
|**HTTP Method**|POST|


|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||



V1.0    08.2025    KUKA AMR 46/63




---

|参数名称|参数值|是否必须|示<br>例|备注|
|---|---|---|---|---|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**nodeCode**|String||T||点位编码或点位外部编<br>码||
|**missionCode**|String||F||任务号，下发给mission<br>manager的任务号。不传<br>会自动生成。||


⚫ 返回字段说明
下发成功时，返回任务号

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/robotMove](http://[IP:Port]/interfaces/api/amr/robotLift%20)

{

"robotId": "10001",

"nodeCode": "TEST-1-1001"

}

⚫ 返回报文示例
示例 1

{

"data": "I-MOVE-1744609148201",

"code": "0",

"message": "OK",

"success": true

}

### 21 机器人充电 Dispatch Charge Robot Task （上游系统 -> Kuka 系统）


⚫ API 基本信息

|API 名称|chargeRobot|
|---|---|
|**API** 描述|机器人充电，只在任务列表展示，作业看板不可见。不会锁定机器<br>人。 <br>Dispatch charge task to the robot. The function is the same as which in<br>the Map Monitor, directly dispatched to the Mission Manager, only<br>displayed in the Mission List, and not visible on the Job Board. The<br>robot won’t be locked after the task finish.|



V1.0    08.2025    KUKA AMR 47/63




---

|API URL|http://[IP:Port]/interfaces/api/amr/chargeRobot|
|---|---|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**necessary**|Integer||T||是否强制生成充电任务 <br>1-一定生成任务并排<br>队；0-低于lowestLevel<br>则去充电，无资源的情<br>况下可直接完成||
|**targetLevel**|Integer||T||目标电量，单位百分比||
|**lowestLevel**|Integer||F||触发充电的电量，单位<br>百分比，necessary=0 时<br>必传||
|**missionCode**|String||F||任务编码，不指定时<br>WCS 自动生成||


⚫ 返回字段说明
无

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/chargeRobot](http://[IP:Port]/interfaces/api/amr/chargeRobot%20)

{

"lowestLevel": 5,

"necessary": 0,

"robotId": "2",

"targetLevel": 90

}
⚫ 返回报文示例

{
"data": null,
"code": "0",
"message": "OK",

"success": true

}


V1.0    08.2025    KUKA AMR 48/63




---

### 22 解锁机器人 Unlock robot （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|unlockRobot|
|---|---|
|**API** 描述|解锁机器人。仅用于异常恢复场景。使用前请确保作业看板中机器<br>人不存在对应执行中的作业。否则会导致流程执行异常。<br>Unlock the robot. Only for abnormal recovery scenarios. Before<br>request, please ensure that there is no corresponding executing jobs<br>for the robot on the job board. Otherwise, it may cause workflow<br>execution error.|
|**API URL**|http://[IP:Port]/interfaces/api/amr/unlockRobot|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||


⚫ 返回字段说明
下发成功时，返回任务号

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/unlockRobot](http://[IP:Port]/interfaces/api/amr/unlockRobot)

{

"robotId": "10001"

}

⚫ 返回报文示例
示例 1

{

"code": "0",

"message": "Success",

"success": true

}


V1.0    08.2025    KUKA AMR 49/63




---

### 23 入场机器人 Insert The Robot Into The Map （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|insertRobot|
|---|---|
|**API** 描述|入场机器人，该接口目前只支持真车。<br>Insert the robot into the map. Only support real AMR<br>currently (distinguished from simulated AMR).|
|**API URL**|http://[IP:Port]/interfaces/api/amr/insertRobot|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**cellCode**|String||T||机器人入场点位||
|**synchroContainer**|Integer||T||是否协同容器入场，0：<br>否；1：是||


⚫ 返回字段说明
无

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/insertRobot](http://[IP:Port]/interfaces/api/amr/insertRobot%20)

{

"cellCode": "TEST-1-69",

"robotId": "2",

"synchroContainer": 1

}
⚫ 返回报文示例

{
"data": null,
"code": "0",
"message": "OK",

"success": true

}


V1.0    08.2025    KUKA AMR 50/63




---

### 24 离场机器人 Remove The Robot From The Map （上游系统 -> Kuka 系 统）

⚫ API 基本信息


|API 名称|removeRobot|
|---|---|
|**API** 描述|离场机器人<br>Remove the robot from the map|
|**API URL**|http://[IP:Port]/interfaces/api/amr/removeRobot|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**robotId**|String||T||机器人编号||
|**withContainer**|Integer||F|1|是否携带容器离场，0:<br>否; 1:是||


⚫ 返回字段说明
无

⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/removeRobot](http://[IP:Port]/interfaces/api/amr/removeRobot%20)

{

"robotId": "2",

"withContainer": 1

}
⚫ 返回报文示例

{
"data": null,
"code": "0",
"message": "OK",

"success": true

}


V1.0    08.2025    KUKA AMR 51/63




---

### -- AMR 地图点位与区域相关接口 25 查询所有 WCS 区域信息 Query All WCS Area Information （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|areaQuery|
|---|---|
|**API** 描述|查询所有WCS 区域信息Query All WCS Area Information|
|**API URL**|http://[IP:Port]/interfaces/api/amr/areaQuery|
|**HTTP Method**|GET|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明
无

⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**areaName**|String|区域名称||
|**areaCode**|String|区域编码||
|**areaType**|Integer|区域类型,1:库区 3:暂存<br>区 4:缓存区 5:密集存储<br>区 6:监管区 7:叉车搬运<br>区||


⚫ 请求报文示例
⚫ 请求返回报文示例

{

"data": [

{

"areaName": "container storage area",

"areaType": 1,

"areaCode": "1-song-1732701220548"

},

{

"areaName": "temporary storage area",

"areaType": 3,

"areaCode": "1-song-1732701269477"

},


V1.0    08.2025    KUKA AMR 52/63




---

{

"areaName": "buffer area",

"areaType": 4,

"areaCode": "1-song-1732701316971"

},

{

"areaName": "dense storage area",

"areaType": 5,

"areaCode": "1-song-1732701347592"

},

{

"areaName": "exclusive area",

"areaType": 6,

"areaCode": "1-song-1732701422092"

},

{

"areaName": "fork area",

"areaType": 7,

"areaCode": "1-song-1732701459113"

}

],

"code": "0",

"message": null,

"success": true

}

### 26 区域内点位信息查询 Query Nodes of the Area （上游系统 -> Kuka 系 统）


⚫ API 基本信息


|API 名称|areaNodesQuery|
|---|---|
|**API** 描述|区域内点位（外部编码）信息查询Query Nodes of the Area|
|**API URL**|http://[IP:Port]/interfaces/api/amr/areaNodesQuery|
|**HTTP Method**|POST|



|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|


⚫ 请求参数说明







V1.0    08.2025    KUKA AMR 53/63




---

|字段名称|参数类型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**areaCodes**|List<String>||T||区域编码集合||


⚫ 返回字段说明

|字段名称|参数类型|字段描述|项目用途|
|---|---|---|---|
|**areaCode**|String|区域编码||
|**nodeList**|List<String>|点位外部编码的集合。<br>若该区域内所有点位均<br>无外部编码，则该字段<br>可能为空||



⚫ 请求报文示例
1 ） 示例 1

{

"areaCodes": ["A000000013","A000000014"]

}

2 ） 示例 2

{

"areaCodes": ["1-song-1732612877805"]

}


⚫ 返回报文示例
1 ）示例 1

{

"data": [

{

"areaCode": "A000000014",

"nodeList": [

"27"

]

},

{

"areaCode": "A000000013",

"nodeList": [

"46",

"50"

]

}

],

"code": "0",

"message": null,

"success": true

}

3 ） 示例 2 ，区域内点位均无外部编码

{

"data": [


V1.0    08.2025    KUKA AMR 54/63




---

{

"areaCode": "1-song-1732612877805",

"nodeList": [

""

]

}

],

"code": "0",

"message": null,

"success": true

}

### 27 查询点位所属区域 Query Area by Map Node （上游系统 -> Kuka 系 统）


⚫ API 基本信息


|API 名称|queryWCSAreaByMapNode|
|---|---|
|**API** 描述|查询点位所属区域 Query Area by Map Node|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryWCSAreaByMapNode|
|**HTTP Method**|GET|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**nodeUuid**|String||T||点位UUID||


⚫ 返回字段说明



|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**areaCode**|String|区域编码 <br>area code<br>||
|**containerModelCode**|String|区域可放置的容器的模<br>型编码|不一定有<br>值|


⚫ 请求 URL 示例

http://[IP:Port]/interfaces/api/amr/queryWCSAreaByMapNode?nodeUuid= 1-song-44


V1.0    08.2025    KUKA AMR 55/63




---

⚫ 返回报文示例
1) 查询到点位所属区域，区域未配置可放置的容器模型编码


{

"data": {

"areaCode": "1-song-1732612831825",

"containerModelCode": ""

},

"code": "0",

"message": null,

"success": true

}

2) 查询到点位所属区域，区域未配置可放置的容器模型编码


{

"data": {

"areaCode": "1-song-1732612877805",

"containerModelCode": "600i"

},

"code": "0",

"message": null,

"success": true

}

3 ） 未查询到点位所属区域


{

"data": null,

"code": "100001",

"message": "No such node in the graph.[7788]",

"success": false

}

### 28 查询所有禁行区 Query All Forbidden Areas （上游系统 -> Kuka 系统）


⚫ API 基本信息


|API 名称|queryAllForbiddenAreas|
|---|---|
|**API** 描述|查询所有禁行区 Query All Forbidden Areas|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryAllForbiddenAreas|
|**HTTP Method**|GET|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



V1.0    08.2025    KUKA AMR 56/63




---

⚫ 请求参数说明
无

⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**forbiddenAreaId**|Integer|禁行区id||
|**mapCode**|String|地图片区编码||
|**floorNumber**|String|楼层号||
|**description**|String|禁行区描述||
|**forbiddenAreaStrategy**|Integer|禁行策略:0-默认;1-允许<br>有车||
|**status**|Integer|状态:0-禁用;1-启用;2-生<br>效中;3-失效中||
|**enableType**|Integer|生效方式:0-立即生效;1-<br>按给定时间段生效||


⚫ 请求报文示例
无

⚫ 请求返回报文示例

{

"data": [

{

"forbiddenAreaId": 3,

"mapCode": "1",

"floorNumber": "song",

"description": "",

"forbiddenAreaStrategy": 0,

"status": 1,

"enableType": 0

},

{

"forbiddenAreaId": 4,

"mapCode": "1",

"floorNumber": "1",

"description": "",

"forbiddenAreaStrategy": 0,

"status": 1,

"enableType": 0

},

{

"forbiddenAreaId": 2,

"mapCode": "1",

"floorNumber": "song",

"description": "forbidden area1 of map song",

"forbiddenAreaStrategy": 0,

"status": 1,


V1.0    08.2025    KUKA AMR 57/63




---

"enableType": 0

}

],

"code": "0",

"message": null,

"success": true

} ],

"code": "0",

"message": null,

"success": true

}

### 29 查询指定禁行区 Query One Forbidden Area （上游系统 -> Kuka 系 统）


⚫ API 基本信息


|API 名称|queryOneForbiddenArea|
|---|---|
|**API** 描述|查询指定禁行区 Query One Forbidden Area|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryOneForbiddenArea|
|**HTTP Method**|GET|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明










|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**forbiddenAreaId**|Integer||T||禁行区id<br>forbidden area ID||



⚫ 返回字段说明





|字段名称|参数类<br>型|字段描述|项目用途|
|---|---|---|---|
|**forbiddenAreaId**|Integer|禁行区id||
|**mapCode**|String|地图片区编码||
|**floorNumber**|String|楼层号||
|**description**|String|禁行区描述|不一定有值|
|**forbiddenAreaStrategy**|Integer|禁行策略:0-默认;1-允许<br>有车||
|**status**|Integer|状态:0-禁用;1-启用;2-生||


V1.0    08.2025    KUKA AMR 58/63




---

|Col1|Col2|效中;3-失效中|Col4|
|---|---|---|---|
|**enableType**|Integer|生效方式:0-立即生效;1-<br>按给定时间段生效||


⚫ 请求 URL 示例

[http://[IP:Port]/interfaces/api/amr/queryOneForbiddenArea?forbiddenAreaId=2](http://[IP:Port]/interfaces/api/amr/queryOneForbiddenArea?forbiddenAreaId=2)

⚫ 返回报文示例
示例 1

{

"data": {

"forbiddenAreaId": 2,

"mapCode": "1",

"floorNumber": "song",

"description": "forbidden area1 of map song",

"forbiddenAreaStrategy": 0,

"status": 1,

"enableType": 0

},

"code": "0",

"message": null,

"success": true

}

### 30 更新指定禁行区的状态 Update Forbidden Area Status （上游系统 -> Kuka 系统）


⚫ PI 基本信息


|API 名称|updateForbiddenAreaStatus|
|---|---|
|**API** 描述|更新指定禁行区的状态 Update Forbidden Area Status|
|**API URL**|http://[IP:Port]/interfaces/api/amr/updateForbiddenAreaStatus|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









V1.0    08.2025    KUKA AMR 59/63




---

|forbiddenAreaId|Integer|Col3|T|0|禁行区id|在请求体中，<br>forbiddenAreaId 或<br>forbiddenAreaCode<br>只能选择其中一<br>个作为参数。|
|---|---|---|---|---|---|---|
|**forbiddenAreaCode**|String||T||禁行区code|禁行区code|
|**status**|String||T||禁行区状态: 0-禁用;1-启<br>用||


⚫ 返回字段说明
无

⚫ 请求报文示例 request body
1) 示例 1

{

"forbiddenAreaId": 2,

"status": "0"

}
2) 示例 2

{

"forbiddenAreaCode": "map1-01-1739427001143",

"status": "0"

}

⚫ 返回报文示例 response body
1) 状态修改成功后返回的报文

{

"data": null,

"code": "0",

"message": null,

"success": true

}

2) 状态修改失败后返回的报文
错误原因：该禁行区的状态已经为 0 （禁用），仍旧修改其状态为 0 ，则会收到如下错误。如果状态已
经为 1 （启用），再次修改其状态为 1 ，也会收到类似错误。

{

"data": null,

"code": "100001",

"message": "RCS returns error[[D]com.kuka.rcs.bd.common.grpc.util.CommonGrpcErrorCode.16[can not

update [ MAP_ZONE_STATUS_DISABLE ]]]",

"success": false


}
3) 传参错误
错误原因：每次只能选择 forbiddenAreaId 和 forbiddenAreaCode 中的一个作为请求参数。

{

"data": null,

"code": "100001",

"message": "only one of area ID or area code can be filled in",

"success": false

}


V1.0    08.2025    KUKA AMR 60/63




---

### 31 查询功能点位 Query Function Node （上游系统 -> Kuka 系统）

⚫ API 基本信息


|API 名称|queryFunctionNode|
|---|---|
|**API** 描述|查询功能点位 Query Function Node|
|**API URL**|http://[IP:Port]/interfaces/api/amr/queryFunctionNode|
|**HTTP Method**|POST|








|Headers|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|参数名称|参数值|是否必须|示<br>例|备注|
|Content-Type|application/json|是|||
|Authorization|${accrssToken}|当接口平台开启鉴<br>权时必填（接口平<br>台默认启用鉴权）||accessToken 获取方式见Fleet 文档 ->接口<br>平台 ->鉴权|



⚫ 请求参数说明









|字段名称|参数类<br>型|最 大<br>长度|是 否<br>必填|默认<br>值|字段描述|项目用途|
|---|---|---|---|---|---|---|
|**functionType**|Integer||T||功能点位类型|单点工作<br>站：1 <br>货架点：2 <br>休息点：3 <br>充电入口<br>点：4 <br>交互点：5 <br>避让点：6 <br>旋转点：7 <br>排队点：8 <br>校验点：9 <br>充电点：<br>10<br>电梯点：<br>11<br>箱式货架<br>点：12<br>输<br>送<br>线<br>点：13<br>语音播放<br>点：15<br>移动箱式<br>货架停留<br>点：16<br>输送线关<br>联点：17<br>无线充电<br>点：18<br>对接点：<br>19<br>料箱上下|


V1.0    08.2025    KUKA AMR 61/63




---

|Col1|Col2|Col3|Col4|Col5|Col6|料机点：<br>20|
|---|---|---|---|---|---|---|
|**mapCode**|String||T||地图编码||
|**floorNumber**|String||T||片区编码||
|**robotTypeClass**|String||F||机器人类型编码||
|**containerModel**|String||F||容器模型编码||


⚫ 返回字段说明

|字段名称|参数类型|字段描述|项目用途|
|---|---|---|---|
|**nodeCode**|String|点位编码（UUID）||
|**externalCode**|String|点位外部编码||
|**functionType**|Integer|功能点位类型||
|**containerModelCode**|List<String>|点位支持的容器模型编<br>码||
|**robotTypeCode**|List<String>|点位支持的机器人类型<br>编码||



⚫ 请求报文示例

{

"floorNumber": "1",

"functionType": 1,

"mapCode": "TEST"

}


⚫ 返回报文示例

{
"data": [
{
"nodeCode": "TEST-1-53",
"externalCode": "",
"functionType": 1,
"containerModelCode": [

"model1"

],
"robotTypeCode": [

"KMP600I"

]
},
{
"nodeCode": "TEST-1-1",

"externalCode": "",
"functionType": 1,
"containerModelCode": [],
"robotTypeCode": []
}
],
"code": "0",
"message": "lang.wcs.common.ok",

"success": true

}


V1.0    08.2025    KUKA AMR 62/63




---

### --  接口响应报文说明

⚫ 成功响应

{

"code": "0",

"message": "",

"success": true,

"data": ""

}
⚫ 异常响应

{
"code": "", // 异常代码
"message": "", // 异常信息

"success": false,

"data": null

}
异常信息说明：

|错误描述|异常code|message|
|---|---|---|
|未知异常|100001|UNKNOW ERROR|
|非法参数|100002|INVALID PARAMETER|
|参数缺失异常|100404|MISS PARAM|
|不存在枚举|100013|INVALID ENUM VALUE|
|位置信息不存在|100204|NO SUCH NODE|
|机器人**/**机器人类型不存在|100301|ROBOT NOT EXISTS|
|**requestId** 已经存在|100408|API REQUEST ID IS DUPLICATE|
|任务编码重复|100409|API MISSION CODE IS DUPLICATE|



V1.0    08.2025    KUKA AMR 63/63


