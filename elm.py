import numpy as np
from sklearn.datasets import load_iris  # 数据集
from sklearn.model_selection import train_test_split  # 数据集的分割函数
from sklearn.preprocessing import StandardScaler  # 数据预处理
from sklearn import metrics # 引入包含数据验证方法的包


class SingeHiddenLayer(object):

    def __init__(self, X, y, num_hidden):
        self.data_x = np.atleast_2d(X)  # 判断输入训练集是否大于等于二维; 把x_train()取下来
        self.data_y = np.array(y).flatten()  # a.flatten()把a放在一维数组中，不写参数默认是“C”，也就是先行后列的方式，也有“F”先列后行的方式； 把 y_train取下来
        self.num_data = len(self.data_x)  # 训练数据个数
        self.num_feature = self.data_x.shape[1];  # shape[] 读取矩阵的长度，比如shape[0]就是读取矩阵第一维度的长度 (120行，4列，所以shape[0]==120,shapep[1]==4)
        self.num_hidden = num_hidden;  # 隐藏层节点个数

        # 随机生产权重（从-1，到1，生成（num_feature行,num_hidden列））
        self.w1 = np.random.uniform(-1, 1, (self.num_feature, self.num_hidden))
        self.w2 = np.random.uniform(-1, 1, (self.num_feature, self.num_hidden))
        #self.w1 =
        # 随机生成偏置1，一个隐藏层节点对应一个偏置
        for i in range(self.num_hidden):
            b1 = np.random.uniform(-0.6, 0.6, (1, self.num_hidden))
            self.first_b1 = b1

        # 生成偏置矩阵1，以隐藏层节点个数4为行，样本数120为列
        for i in range(self.num_data - 1):
            b1 = np.row_stack((b1, self.first_b1))  # row_stack 以叠加行的方式填充数组
        self.b1 = b1
        #生成偏置矩阵2，以隐藏层节点个数4为行，样本数120为列
        for i in range(self.num_hidden):
            b2 = np.random.uniform(-0.6, -0.6, (1, self.num_hidden))
            self.first_b2 = b2

        # 生成偏置矩阵2，以隐藏层节点个数4为行，样本数120为列
        for i in range(self.num_data - 1):
            b2 = np.row_stack((b2, self.first_b2))  # row_stack 以叠加行的方式填充数组
        self.b2 = b2

    # 定义sigmoid函数
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))

    def train(self, x_train, y_train, classes):
        mul1 = np.dot(self.data_x, self.w1)  # 输入乘以权重
        add1 = mul1+ self.b1  # 加偏置
        H1 = self.sigmoid(add1)  # 激活函数

        H_1 = np.linalg.pinv(H1)  # 求广义逆矩阵
        # print(type(H_.shape))
        mul2 = np.dot(self.data_x, self.w2)
        add2 = mul1 + self.b2
        H2 = self.sigmoid(add2)
        H_2 = np.linalg.pinv(H2)
        # 将只有一列的Label矩阵转换，例如，iris的label中共有三个值，则转换为3列，以行为单位，label值对应位置标记为1，其它位置标记为0
        self.train_y = np.zeros((self.num_data, classes))  # 初始化一个120行，3列的全0矩阵
        for i in range(0, self.num_data):
            self.train_y[i, y_train[i]] = 1  # 对应位置标记为1

        self.out_w1 = np.dot(H_1, self.train_y)  # 求输出权重
        self.train_yt=np.dot(H1, self.out_w1)
        self.e1 =  self.train_y-self.train_yt
        self.out_w2 = np.dot(H_2, self.e1)

    def predict(self, x_test):
        self.t_data = np.atleast_2d(x_test)  # 测试数据集
        self.num_tdata = len(self.t_data)  # 测试集的样本数
        self.pred_Y = np.zeros((x_test.shape[0]))  # 初始化

        b1 = self.first_b1
        b2 = self.first_b2
        # 扩充偏置矩阵，以隐藏层节点个数4为行，样本数30为列
        for i in range(self.num_tdata - 1):
            b1 = np.row_stack((b1, self.first_b1))  # 以叠加行的方式填充数组
        for i in range(self.num_tdata - 1):
            b2 = np.row_stack((b2, self.first_b2))

        # 预测
        self.pred_yt =np.dot(self.sigmoid(np.dot(self.t_data, self.w1) + b1), self.out_w1)
        self.pred_e1t =np.dot(self.sigmoid(np.dot(self.t_data, self.w2) + b2), self.out_w2)
        self.pred_Y =self.pred_yt +  self.pred_e1t

        # 取输出节点中值最大的类别作为预测值
        self.predy = []
        for i in self.pred_Y:
            L = i.tolist()
            self.predy.append(L.index(max(L)))

    def score(self, y_test):
        print("准确率：")
        # 使用准确率方法验证
        print(metrics.accuracy_score(y_true=y_test, y_pred=self.predy))







stdsc = StandardScaler()  # StandardScaler类,利用接口在训练集上计算均值和标准差，以便于在后续的测试集上进行相同的缩放
iris = load_iris()
x, y = stdsc.fit_transform(iris.data), iris.target  # 数据归一化
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

ELM = SingeHiddenLayer(x_train, y_train, 4)  # 训练数据集，训练集的label，隐藏层节点个数
ELM.train(x_train, y_train, 4)
ELM.predict(x_test)
ELM.score(y_test)
