from cvxopt import matrix, solvers
import numpy as np

class RecommendationSystem:
    def getFood(self):
        idList = []
        proteinList = []
        carbohydrateList=[]
        fatList = []
        '''
        # 调用数据库获得食物
        # 得到4个list：id1-id9，p1-p9，c1-p9，f1-f9
        '''
        print('a')
        return idList, proteinList, carbohydrateList, fatList

    def caculateEveryFoodNeeds(self, proteinList, carbohydrateList, fatList, proteinNeed, carbohydrateNeed, fatNeed, foodMinNeed):
        '''
        此函数为算法的核心！
        判断此组食物能否符合要求
        若可符合，返回true，并返回每类食物的质量
        否则，返回false
        :param proteinList:
        :param carbohydrateList:
        :param fatList:
        :return:
        '''
        flag = True
        XList = []

        proteinCon = proteinList + [-100.,100,0.,0.,0.,0.]
        carbohydrateCon = carbohydrateList + [0.,0.,-100.,100.,0.,0.]
        fatCon = fatList + [0.,0.,0.,0.,-100.,100.]
        constraint = [proteinNeed, proteinNeed, carbohydrateNeed, carbohydrateNeed, fatNeed, fatNeed]
        A = np.zeros((21,15))
        for i in range(A.shape[1]):
            A[0][i] = proteinCon[i]
            A[1][i] = -proteinCon[i]
        for i in range(A.shape[1]):
            A[2][i] = carbohydrateCon[i]
            A[3][i] = -carbohydrateCon[i]
        for i in range(A.shape[1]):
            A[4][i] = fatCon[i] 
            A[5][i] = -fatCon[i] 
        for i in range(A.shape[1]):
            A[6+i][i] = -1
        # 21个约束条件，21列：6+9+6
        # 15个变量，15行：9+6
        
        A = matrix(A)
        b = matrix([100.0*proteinNeed,-100.0*proteinNeed,100.0*carbohydrateNeed,-100.0*carbohydrateNeed,100.0*fatNeed,-100.*fatNeed]
                   +[-foodMinNeed for i in range(9)]
                   +[0.,0.,0.,0.,0.,0.]
                   )
        c = matrix([0. for i in range(9)]
                   +[100.0/c for c in constraint]
                   )

        sol = solvers.lp(c, A, b)
        print(sol['x'])
        



        #return flag, XList

    def formRecipe(self, idList, XList):
        '''
        封装菜名和各自的重量
        :param idList:
        :param XList:
        :return:
        '''
        recipe = []
        return recipe

    def recommend(self, user):

        # pN cN fN。caloeryNeed只需要向用户显示
        caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed = self.calNutrientNeeds(user)

        flag = False
        idList = []
        proteinList = []
        carbohydrateList = []
        fatList = []
        XList = []
        while not flag:
            idList,proteinList,carbohydrateList,fatList = self.getFood()
            flag,XList = self.caculateEveryFoodNeeds(proteinList,carbohydrateList,fatList)

        recipe = self.formRecipe(idList,XList)

        return recipe

    def calNutrientNeeds(self, user):
        proteinIndex = [0.165, 0.25, 0.2]
        carbohydrateIndex = [0.6, 0.55, 0.55]
        fatIndex = [0.235, 0.20, 0.25]

        index = [1.15, 0.8, 1]

        gender = user.getGender()
        age = user.getAge()
        height = user.getHeight()
        weight = user.getWeight()
        goal = user.getGoal()
        goalWeight = user.getGoalWeight()
        activityIndex = user.getActivityIndex()

        caloeryNeed = 0
        if gender == 0:
            caloeryNeed = 655 + 9.6 * weight + 1.8 * height - 4.7 * age
        elif gender == 1:
            caloeryNeed = 66 + 13.7 * weight + 5 * height - 6.8 * age

        caloeryNeed = caloeryNeed * activityIndex * index[goal]

        proteinNeed = caloeryNeed * proteinIndex[goal] / 4
        carbohydrateNeed = caloeryNeed * carbohydrateIndex[goal] / 4
        fatNeed = caloeryNeed * fatIndex[goal] / 9

        weeksNeed = 0
        if goal == 0 and goalWeight > weight:
            weeksNeed = (goalWeight - weight) * 1100 / 500 + 1
        elif goal == 1 and goalWeight < weight:
            weeksNeed = (weight - goalWeight) * 1100 / 500 + 1

        return caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed


class User:
    __gender = 0
    __age = 0
    __height = 0
    __weight = 0
    __goal = 0
    __goalWeight = 0
    __activityIndex = 0

    def __init__(self, gender, age, height, weight, goal, goalWeight, activityIndex):
        self.__gender = gender
        self.__age = age
        self.__height = height
        self.__weight = weight
        self.__goal = goal
        self.__goalWeight = goalWeight
        self.__activityIndex = activityIndex

    def getGender(self):
        return self.__gender

    def getAge(self):
        return self.__age

    def getHeight(self):
        return self.__height

    def getWeight(self):
        return self.__weight

    def getGoal(self):
        return self.__goal

    def getGoalWeight(self):
        return self.__goalWeight

    def getActivityIndex(self):
        return self.__activityIndex



user = User(0, 21, 160, 50, 1, 45, 2)
rs = RecommendationSystem()
pList = [2.5,15.0,0.9,2.6,12.10,0.8,8.3,1.5,1.4]
cList = [9.3,66.90,4.00,25.9,0.1,2.90,61.90,2.7,2.2]
fList = [2.70,6.70,0.2,0.3,10.5,0.2,0.7,0.3,0.2]

pn = 113
cn = 248
fn = 40
rs.caculateEveryFoodNeeds(pList,cList,fList,pn,cn,fn,50)

'''   
# 以下为 cvxopt 的一个demo
A = matrix([
    [1.0, -1.0, 2.0, -2.0, 3.0, -3.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x1
    [0.0, 0.0, 1.0, -1.0, 2.0, -2.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x2
    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # x3
    [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0], # x4
    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], # x5
    [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0], # x6
    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0], # x7
    [0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] # x8
])
print(A)


b = matrix([10.0, -10.0, 40.0, -40.0, 100.0, -100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
c = matrix([0.0, 0.0, 2.0, 0.0, 0.0, 2.0, 1.0, 0.0])
print(A)
print(b)
print(c)
sol = solvers.lp(c, A, b)
print(sol['x'])


a=np.array([
    [1.0, -1.0, 2.0, -2.0, 3.0, -3.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x1
    [0.0, 0.0, 1.0, -1.0, 2.0, -2.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x2
    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # x3
    [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0], # x4
    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], # x5
    [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0], # x6
    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0], # x7
    [0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] # x8
    ])

print(matrix(a))
print(matrix(a.T))
'''